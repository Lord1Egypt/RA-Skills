#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request


BASE_URL = "https://openapi.duoplus.net"
REDACTED = "***REDACTED***"


class DuoPlusError(Exception):
    pass


class ValidationError(DuoPlusError):
    pass


class ConfirmationError(DuoPlusError):
    pass


class ApiError(DuoPlusError):
    pass


def _default_transport(url, headers, payload, timeout):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ApiError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"Transport error: {exc.reason}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError(f"Invalid JSON response: {raw[:500]}") from exc


def _canonical_hash(operation, facts):
    body = {"operation": operation, "facts": facts}
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _unique_sorted(values):
    return sorted(set(values))


def resolve_api_key(argument_value, environment=None):
    environment = os.environ if environment is None else environment
    return argument_value or environment.get("DUOPLUS_API_KEY")


def resolve_api_base(environment=None):
    environment = os.environ if environment is None else environment
    return environment.get("DUOPLUS_API_BASE", BASE_URL).rstrip("/")


class DuoPlusClient:
    def __init__(self, api_key, base_url=BASE_URL, timeout=30, transport=None, clock=None, sleep=None):
        if not api_key:
            raise ValidationError("API key is required; pass --api-key or set DUOPLUS_API_KEY")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transport = transport or _default_transport
        self.clock = clock or time.monotonic
        self.sleep = sleep or time.sleep
        self._last_request = {}

    def _redact(self, value):
        return str(value).replace(self.api_key, REDACTED)

    def _request(self, path, payload):
        now = self.clock()
        previous = self._last_request.get(path)
        if previous is not None:
            remaining = 1.0 - (now - previous)
            if remaining > 0:
                self.sleep(remaining)
                now = self.clock()
        self._last_request[path] = now
        headers = {
            "DuoPlus-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Lang": "en",
        }
        try:
            response = self.transport(self.base_url + path, headers, payload, self.timeout)
        except DuoPlusError as exc:
            raise type(exc)(self._redact(exc)) from exc
        except Exception as exc:
            raise ApiError(self._redact(exc)) from exc
        if not isinstance(response, dict):
            raise ApiError("Invalid JSON response object")
        if response.get("code") != 200:
            raise ApiError(self._redact(response.get("message", f"API error {response.get('code')}")))
        return response

    @staticmethod
    def _validate_pagination(payload):
        pagesize = payload.get("pagesize")
        if pagesize is not None and (not isinstance(pagesize, int) or not 1 <= pagesize <= 100):
            raise ValidationError("pagesize must be an integer from 1 to 100")

    def number_list(self, filters):
        payload = dict(filters)
        self._validate_pagination(payload)
        return self._request("/api/v1/cloudNumber/numberList", payload)

    def sms_list(self, number_id, page=1, pagesize=10):
        if not number_id:
            raise ValidationError("number_id is required")
        payload = {"number_id": number_id, "page": page, "pagesize": pagesize}
        self._validate_pagination(payload)
        return self._request("/api/v1/cloudNumber/smsList", payload)

    def purchase_packages(self):
        return self._request("/api/v1/cloudNumber/purchasePackage", {})

    def package_durations(self, region, number_type=1):
        if not region:
            raise ValidationError("region is required")
        return self._request("/api/v1/cloudNumber/package", {"region": region, "type": number_type})

    def renewal_packages(self, number_ids):
        ids = _unique_sorted(number_ids)
        if not ids:
            raise ValidationError("number_ids must not be empty")
        return self._request("/api/v1/cloudNumber/renewalPackage", {"number_ids": ids})

    def _purchase_preflight(self, request):
        operation = dict(request)
        operation.setdefault("type", 1)
        operation.setdefault("quantity", 1)
        operation.setdefault("renewal_status", 1)
        region = operation.get("region")
        if not isinstance(region, str) or len(region) != 2 or not region.isalpha() or region != region.upper():
            raise ValidationError("region must be an ISO 3166-1 alpha-2 uppercase code")
        if not isinstance(operation.get("duration"), int) or operation["duration"] <= 0:
            raise ValidationError("duration must be a positive integer")
        if operation.get("type") not in (0, 1):
            raise ValidationError("type must be 0 or 1")
        if not isinstance(operation.get("quantity"), int) or operation["quantity"] <= 0:
            raise ValidationError("quantity must be a positive integer")
        if operation.get("renewal_status") not in (0, 1):
            raise ValidationError("renewal_status must be 0 or 1")
        response = self.purchase_packages()
        match = None
        for number_type in response.get("data", []):
            if number_type.get("type") != operation["type"]:
                continue
            for country in number_type.get("country", []):
                if country.get("region") != operation["region"]:
                    continue
                for duration in country.get("durations", []):
                    if duration.get("days") == operation["duration"]:
                        match = {key: duration.get(key) for key in ("days", "price", "card_price", "total_price", "is_special_offer", "gif_days", "random_gif_days")}
        if match is None:
            raise ValidationError("The requested purchase package is not currently available")
        return operation, match

    def purchase(self, request, confirm=False, expected_preflight_sha256=None):
        operation, facts = self._purchase_preflight(request)
        digest = _canonical_hash(operation, facts)
        preview = {"confirmation_required": True, "operation": operation, "package": facts, "preflight_sha256": digest}
        if not confirm:
            return preview
        if not expected_preflight_sha256 or expected_preflight_sha256 != digest:
            raise ConfirmationError("Preflight changed or confirmation fingerprint is missing; review and confirm again")
        return self._request("/api/v1/cloudNumber/purchase", operation)

    @staticmethod
    def _normalize_renewal_list(items):
        normalized = []
        for item in items:
            ids = _unique_sorted(item.get("number_ids", []))
            duration = item.get("duration")
            if not ids or not isinstance(duration, int):
                raise ValidationError("Each renewal item requires number_ids and integer duration")
            normalized.append({"number_ids": ids, "duration": duration})
        if not normalized:
            raise ValidationError("Renewal list must not be empty")
        return normalized

    def _renewal_preflight(self, items):
        operation = self._normalize_renewal_list(items)
        all_ids = _unique_sorted(number_id for item in operation for number_id in item["number_ids"])
        response = self.renewal_packages(all_ids)
        supported = {entry.get("id"): sorted(entry.get("duration", [])) for entry in response.get("data", {}).get("numbers", [])}
        for item in operation:
            for number_id in item["number_ids"]:
                if item["duration"] not in supported.get(number_id, []):
                    raise ValidationError(f"Duration {item['duration']} is not available for number {number_id}")
        facts = {number_id: supported[number_id] for number_id in all_ids}
        return operation, facts

    def renew(self, items, confirm=False, expected_preflight_sha256=None):
        operation, facts = self._renewal_preflight(items)
        digest = _canonical_hash(operation, facts)
        preview = {"confirmation_required": True, "operation": operation, "supported_durations": facts, "preflight_sha256": digest}
        if not confirm:
            return preview
        if not expected_preflight_sha256 or expected_preflight_sha256 != digest:
            raise ConfirmationError("Preflight changed or confirmation fingerprint is missing; review and confirm again")
        return self._request("/api/v1/cloudNumber/renewal", {"list": operation})

    def set_auto_renewal(self, number_ids, enabled, confirm=False):
        ids = _unique_sorted(number_ids)
        if not ids:
            raise ValidationError("number_ids must not be empty")
        if enabled and not confirm:
            raise ConfirmationError("Enabling auto-renewal requires explicit confirmation")
        return self._request("/api/v1/proxy/autoRenewal", {"number_ids": ids, "type": 1 if enabled else 0})


def build_parser():
    parser = argparse.ArgumentParser(description="Manage DuoPlus cloud numbers")
    parser.add_argument("--api-key", help="DuoPlus API key; DUOPLUS_API_KEY is the optional fallback")
    sub = parser.add_subparsers(dest="command", required=True)
    list_parser = sub.add_parser("list")
    list_parser.add_argument("--page", type=int, default=1)
    list_parser.add_argument("--pagesize", type=int, default=10)
    sms = sub.add_parser("sms")
    sms.add_argument("number_id")
    sms.add_argument("--page", type=int, default=1)
    sms.add_argument("--pagesize", type=int, default=10)
    sub.add_parser("purchase-packages")
    package = sub.add_parser("package")
    package.add_argument("region")
    package.add_argument("--type", type=int, choices=(0, 1), default=1)
    purchase = sub.add_parser("purchase")
    purchase.add_argument("region")
    purchase.add_argument("duration", type=int)
    purchase.add_argument("--type", type=int, choices=(0, 1), default=1)
    purchase.add_argument("--quantity", type=int, default=1)
    purchase.add_argument("--coupon-code")
    purchase.add_argument("--renewal-status", type=int, choices=(0, 1), default=1)
    purchase.add_argument("--confirm", action="store_true")
    purchase.add_argument("--expected-preflight-sha256")
    renewal_package = sub.add_parser("renewal-package")
    renewal_package.add_argument("number_ids", nargs="+")
    renew = sub.add_parser("renew")
    renew.add_argument("--items-json", required=True)
    renew.add_argument("--confirm", action="store_true")
    renew.add_argument("--expected-preflight-sha256")
    auto = sub.add_parser("auto-renewal")
    auto.add_argument("mode", choices=("enable", "disable"))
    auto.add_argument("number_ids", nargs="+")
    auto.add_argument("--confirm", action="store_true")
    return parser


def _run(args, client):
    if args.command == "list":
        return client.number_list({"page": args.page, "pagesize": args.pagesize})
    if args.command == "sms":
        return client.sms_list(args.number_id, args.page, args.pagesize)
    if args.command == "purchase-packages":
        return client.purchase_packages()
    if args.command == "package":
        return client.package_durations(args.region, args.type)
    if args.command == "purchase":
        payload = {"region": args.region, "duration": args.duration, "type": args.type, "quantity": args.quantity, "renewal_status": args.renewal_status}
        if args.coupon_code:
            payload["coupon_code"] = args.coupon_code
        return client.purchase(payload, args.confirm, args.expected_preflight_sha256)
    if args.command == "renewal-package":
        return client.renewal_packages(args.number_ids)
    if args.command == "renew":
        return client.renew(json.loads(args.items_json), args.confirm, args.expected_preflight_sha256)
    return client.set_auto_renewal(args.number_ids, args.mode == "enable", args.confirm)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        client = DuoPlusClient(resolve_api_key(args.api_key), base_url=resolve_api_base())
        result = _run(args, client)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValidationError, ConfirmationError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except DuoPlusError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
