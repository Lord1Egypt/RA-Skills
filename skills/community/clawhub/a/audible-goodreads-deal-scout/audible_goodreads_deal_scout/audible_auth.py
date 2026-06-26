from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .shared import normalize_space, redact_sensitive_payload, redact_sensitive_text, write_json_atomic


AUDIBLE_AUTH_SCHEMA_VERSION = 1
AUDIBLE_AUTH_PURPOSE = "audible_member_price_lookup"
AUDIBLE_IOS_DEVICE_TYPE = "A2CZJZGLK2JJVM"
AUDIBLE_IOS_APP_VERSION = "3.56.2"
AUDIBLE_IOS_SOFTWARE_VERSION = "35602678"
AUDIBLE_PRODUCT_RESPONSE_GROUPS = (
    "price,product_attrs,product_desc,contributors,customer_rights,product_plan_details,product_plans"
)
AUDIBLE_PRODUCT_ID_RE = re.compile(r"^[A-Z0-9]{10}$")
SUPPORTED_AUTH_MARKETPLACES = {
    "us": {
        "countryCode": "us",
        "domain": "com",
        "marketPlaceId": "AF2M0KC94RCEA",
        "locale": "en-US",
    }
}


class AudibleAuthError(RuntimeError):
    pass


def _auth_marketplace_spec(marketplace: Any) -> dict[str, str]:
    normalized = normalize_space(str(marketplace or "")).lower() or "us"
    spec = SUPPORTED_AUTH_MARKETPLACES.get(normalized)
    if not spec:
        supported = ", ".join(sorted(SUPPORTED_AUTH_MARKETPLACES))
        raise AudibleAuthError(f"Authenticated Audible price lookup supports: {supported}.")
    return spec


def _validate_auth_domain(domain: Any, *, marketplace: Any = None) -> str:
    normalized = normalize_space(str(domain or "")).lower()
    if not normalized:
        raise AudibleAuthError("Audible auth file is missing marketplace domain.")
    if marketplace is not None:
        spec = _auth_marketplace_spec(marketplace)
        if normalized != spec["domain"]:
            raise AudibleAuthError("Audible auth file marketplace/domain mismatch.")
        return normalized
    supported_domains = {str(spec["domain"]) for spec in SUPPORTED_AUTH_MARKETPLACES.values()}
    if normalized not in supported_domains:
        supported = ", ".join(sorted(supported_domains))
        raise AudibleAuthError(f"Authenticated Audible price lookup supports domains: {supported}.")
    return normalized


def _normalize_product_id(product_id: str) -> str:
    normalized = normalize_space(product_id).upper()
    if not normalized:
        raise AudibleAuthError("Missing Audible ASIN/product id for authenticated price lookup.")
    if not AUDIBLE_PRODUCT_ID_RE.fullmatch(normalized):
        raise AudibleAuthError("Audible ASIN/product id must be exactly 10 uppercase letters or digits.")
    return normalized


def auth_credential_metadata() -> dict[str, Any]:
    return {
        "purpose": AUDIBLE_AUTH_PURPOSE,
        "allowedUse": "audible_product_price_lookup_only",
        "allowedHosts": sorted(
            {
                f"api.amazon.{spec['domain']}"
                for spec in SUPPORTED_AUTH_MARKETPLACES.values()
            }
            | {f"api.audible.{spec['domain']}" for spec in SUPPORTED_AUTH_MARKETPLACES.values()}
        ),
        "allowedEndpoints": ["/auth/token", "/1.0/catalog/products/<asin>"],
        "storesRefreshToken": True,
        "requestsCookieStyleCredentials": True,
        "persistsCookieStyleCredentials": False,
        "tokenContentsExposedByStatus": False,
    }


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _secure_write_json(path: Path, payload: dict[str, Any]) -> None:
    write_json_atomic(path, payload)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AudibleAuthError(f"Audible auth file not found at {path}.") from exc
    except Exception as exc:
        raise AudibleAuthError(f"Could not read Audible auth file at {path}: {redact_sensitive_text(exc)}") from exc
    if not isinstance(payload, dict):
        raise AudibleAuthError(f"Audible auth file at {path} must contain a JSON object.")
    return payload


def _urlopen_json(request: urllib.request.Request, *, timeout: int = 30) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        raise AudibleAuthError(f"Audible API HTTP {exc.code}: {redact_sensitive_text(body or exc.reason)}") from exc
    except urllib.error.URLError as exc:
        raise AudibleAuthError(f"Audible API request failed: {redact_sensitive_text(exc)}") from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AudibleAuthError(f"Audible API returned non-JSON response: {redact_sensitive_text(raw[:200])}") from exc
    if not isinstance(payload, dict):
        raise AudibleAuthError("Audible API returned an unexpected JSON payload.")
    return payload


def _post_json(url: str, body: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    return _urlopen_json(request)


def _post_form(url: str, body: dict[str, str]) -> dict[str, Any]:
    data = urllib.parse.urlencode(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    return _urlopen_json(request)


def _get_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers, method="GET")
    return _urlopen_json(request)


def create_code_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii").rstrip("=")


def create_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def build_client_id(serial: str) -> str:
    return (serial.upper().encode("ascii") + b"#" + AUDIBLE_IOS_DEVICE_TYPE.encode("ascii")).hex()


def build_external_login_url(*, marketplace: str, serial: str, code_verifier: str) -> str:
    spec = _auth_marketplace_spec(marketplace)
    domain = spec["domain"]
    country_code = spec["countryCode"]
    client_id = build_client_id(serial)
    params = {
        "openid.oa2.response_type": "code",
        "openid.oa2.code_challenge_method": "S256",
        "openid.oa2.code_challenge": create_code_challenge(code_verifier),
        "openid.return_to": f"https://www.amazon.{domain}/ap/maplanding",
        "openid.assoc_handle": f"amzn_audible_ios_{country_code}",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "pageId": "amzn_audible_ios",
        "accountStatusPolicy": "P1",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.mode": "checkid_setup",
        "openid.ns.oa2": "http://www.amazon.com/ap/ext/oauth/2",
        "openid.oa2.client_id": f"device:{client_id}",
        "openid.ns.pape": "http://specs.openid.net/extensions/pape/1.0",
        "marketPlaceId": spec["marketPlaceId"],
        "openid.oa2.scope": "device_auth_access",
        "forceMobileLayout": "true",
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.pape.max_auth_age": "0",
    }
    return f"https://www.amazon.{domain}/ap/signin?{urllib.parse.urlencode(params)}"


def start_external_auth(auth_path: Path, *, marketplace: str = "us") -> dict[str, Any]:
    marketplace = normalize_space(marketplace).lower() or "us"
    spec = _auth_marketplace_spec(marketplace)
    serial = uuid.uuid4().hex.upper()
    code_verifier = create_code_verifier()
    login_url = build_external_login_url(marketplace=marketplace, serial=serial, code_verifier=code_verifier)
    payload = {
        "schemaVersion": AUDIBLE_AUTH_SCHEMA_VERSION,
        "status": "pending_external_login",
        "purpose": AUDIBLE_AUTH_PURPOSE,
        "credentialMetadata": auth_credential_metadata(),
        "createdAt": _now_iso(),
        "updatedAt": _now_iso(),
        "marketplace": marketplace,
        "domain": spec["domain"],
        "marketPlaceId": spec["marketPlaceId"],
        "serial": serial,
        "codeVerifier": code_verifier,
        "loginUrl": login_url,
    }
    _secure_write_json(auth_path.expanduser(), payload)
    return {
        "ok": True,
        "authPath": str(auth_path.expanduser()),
        "marketplace": marketplace,
        "loginUrl": login_url,
        "instructions": (
            "Open loginUrl in a browser and complete Amazon login. "
            "After login, copy the final URL from the browser address bar, even if it is an error/not-found page. "
            "Then run audible-auth-finish with that final redirect URL."
        ),
    }


def authorization_code_from_redirect(redirect_url: str) -> str:
    parsed = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(parsed.query)
    values = query.get("openid.oa2.authorization_code")
    if not values:
        raise AudibleAuthError("Redirect URL does not contain openid.oa2.authorization_code.")
    return values[0]


def register_device(*, authorization_code: str, code_verifier: str, domain: str, serial: str) -> dict[str, Any]:
    domain = _validate_auth_domain(domain)
    body = {
        "requested_token_type": [
            "bearer",
            "mac_dms",
            "website_cookies",
            "store_authentication_cookie",
        ],
        "cookies": {"website_cookies": [], "domain": f".amazon.{domain}"},
        "registration_data": {
            "domain": "Device",
            "app_version": AUDIBLE_IOS_APP_VERSION,
            "device_serial": serial,
            "device_type": AUDIBLE_IOS_DEVICE_TYPE,
            "device_name": "Audible for iPhone",
            "os_version": "15.0.0",
            "software_version": AUDIBLE_IOS_SOFTWARE_VERSION,
            "device_model": "iPhone",
            "app_name": "Audible",
        },
        "auth_data": {
            "client_id": build_client_id(serial),
            "authorization_code": authorization_code,
            "code_verifier": code_verifier,
            "code_algorithm": "SHA-256",
            "client_domain": "DeviceLegacy",
        },
        "requested_extensions": ["device_info", "customer_info"],
    }
    payload = _post_json(f"https://api.amazon.{domain}/auth/register", body)
    try:
        success = payload["response"]["success"]
        tokens = success["tokens"]
        bearer = tokens["bearer"]
    except Exception as exc:
        raise AudibleAuthError(f"Audible registration returned an unexpected payload: {redact_sensitive_payload(payload)}") from exc
    expires = datetime.now(UTC) + timedelta(seconds=int(bearer["expires_in"]))
    return {
        "accessToken": bearer["access_token"],
        "refreshToken": bearer["refresh_token"],
        "expires": expires.timestamp(),
        "deviceInfo": success.get("extensions", {}).get("device_info"),
        "customerInfo": success.get("extensions", {}).get("customer_info"),
    }


def finish_external_auth(auth_path: Path, *, redirect_url: str) -> dict[str, Any]:
    path = auth_path.expanduser()
    pending = _load_json(path)
    if pending.get("status") != "pending_external_login":
        raise AudibleAuthError(f"Audible auth file at {path} is not waiting for external login.")
    authorization_code = authorization_code_from_redirect(redirect_url)
    domain = _validate_auth_domain(pending.get("domain"), marketplace=pending.get("marketplace") or "us")
    registered = register_device(
        authorization_code=authorization_code,
        code_verifier=str(pending["codeVerifier"]),
        domain=domain,
        serial=str(pending["serial"]),
    )
    payload = {
        "schemaVersion": AUDIBLE_AUTH_SCHEMA_VERSION,
        "status": "ready",
        "purpose": AUDIBLE_AUTH_PURPOSE,
        "credentialMetadata": auth_credential_metadata(),
        "createdAt": pending.get("createdAt") or _now_iso(),
        "updatedAt": _now_iso(),
        "marketplace": pending.get("marketplace") or "us",
        "domain": domain,
        "marketPlaceId": pending["marketPlaceId"],
        "serial": pending["serial"],
        **registered,
    }
    _secure_write_json(path, payload)
    return {
        "ok": True,
        "authPath": str(path),
        "marketplace": payload["marketplace"],
        "expires": payload["expires"],
        "message": "Audible authentication is ready for headless price lookup.",
    }


def auth_file_status(auth_path: Path, *, fix_permissions: bool = False) -> dict[str, Any]:
    path = auth_path.expanduser()
    warnings: list[str] = []
    errors: list[str] = []
    exists = path.exists()
    permission_mode: str | None = None
    permission_secure: bool | None = None
    if exists:
        try:
            mode = path.stat().st_mode & 0o777
            permission_mode = oct(mode)
            permission_secure = (mode & 0o077) == 0
            if not permission_secure:
                if fix_permissions:
                    os.chmod(path, 0o600)
                    permission_mode = "0o600"
                    permission_secure = True
                    warnings.append("Auth file permissions were tightened to 0600.")
                else:
                    warnings.append("Auth file is readable by group or others; run audible-auth-status --fix-permissions.")
        except OSError as exc:
            warnings.append(f"Could not inspect auth file permissions: {redact_sensitive_text(exc)}")
    if not exists:
        return {
            "ok": False,
            "schemaVersion": AUDIBLE_AUTH_SCHEMA_VERSION,
            "status": "missing",
            "authPath": str(path),
            "exists": False,
            "ready": False,
            "expired": None,
            "secondsRemaining": None,
            "permissionMode": None,
            "permissionSecure": None,
            "credentialMetadata": auth_credential_metadata(),
            "warnings": warnings,
            "errors": [f"Audible auth file not found at {path}."],
        }
    try:
        payload = _load_json(path)
    except AudibleAuthError as exc:
        return {
            "ok": False,
            "schemaVersion": AUDIBLE_AUTH_SCHEMA_VERSION,
            "status": "unreadable",
            "authPath": str(path),
            "exists": True,
            "ready": False,
            "expired": None,
            "secondsRemaining": None,
            "permissionMode": permission_mode,
            "permissionSecure": permission_secure,
            "credentialMetadata": auth_credential_metadata(),
            "warnings": warnings,
            "errors": [str(exc)],
        }
    status = normalize_space(str(payload.get("status") or "unknown")) or "unknown"
    expires_raw = payload.get("expires")
    expires: float | None = None
    seconds_remaining: int | None = None
    expired: bool | None = None
    if expires_raw not in (None, ""):
        try:
            expires = float(expires_raw)
            seconds_remaining = int(expires - time.time())
            expired = seconds_remaining <= 0
            if expired:
                warnings.append("Audible access token is expired; refresh will be attempted on the next authenticated request.")
        except Exception:
            warnings.append("Auth file contains an unreadable expires value.")
    ready = status == "ready" and bool(payload.get("refreshToken"))
    if status == "pending_external_login":
        warnings.append("Auth flow is pending; finish with audible-auth-finish.")
    elif status != "ready":
        errors.append(f"Auth file status is {status!r}, not 'ready'.")
    if status == "ready" and not payload.get("refreshToken"):
        errors.append("Auth file is missing refreshToken.")
    if status == "ready":
        try:
            _validate_auth_domain(payload.get("domain"), marketplace=payload.get("marketplace") or "us")
        except AudibleAuthError as exc:
            errors.append(str(exc))
    if permission_secure is False:
        errors.append("Auth file permissions are too broad.")
    return {
        "ok": not errors,
        "schemaVersion": AUDIBLE_AUTH_SCHEMA_VERSION,
        "status": status,
        "authPath": str(path),
        "exists": True,
        "ready": ready,
        "marketplace": payload.get("marketplace"),
        "domain": payload.get("domain"),
        "createdAt": payload.get("createdAt"),
        "updatedAt": payload.get("updatedAt"),
        "expires": expires,
        "expired": expired,
        "secondsRemaining": seconds_remaining,
        "permissionMode": permission_mode,
        "permissionSecure": permission_secure,
        "credentialMetadata": auth_credential_metadata(),
        "warnings": warnings,
        "errors": errors,
    }


def load_ready_auth(auth_path: Path) -> dict[str, Any]:
    payload = _load_json(auth_path.expanduser())
    if payload.get("status") != "ready":
        raise AudibleAuthError(f"Audible auth file at {auth_path} is not ready. Run audible-auth-start/finish first.")
    if not payload.get("refreshToken"):
        raise AudibleAuthError(f"Audible auth file at {auth_path} is missing refreshToken.")
    _validate_auth_domain(payload.get("domain"), marketplace=payload.get("marketplace") or "us")
    return payload


def refresh_access_token(auth_path: Path, *, force: bool = False) -> dict[str, Any]:
    path = auth_path.expanduser()
    payload = load_ready_auth(path)
    expires = float(payload.get("expires") or 0)
    if not force and expires - time.time() > 120:
        return payload
    domain = _validate_auth_domain(payload.get("domain"), marketplace=payload.get("marketplace") or "us")
    response = _post_form(
        f"https://api.amazon.{domain}/auth/token",
        {
            "app_name": "Audible",
            "app_version": AUDIBLE_IOS_APP_VERSION,
            "source_token": str(payload["refreshToken"]),
            "requested_token_type": "access_token",
            "source_token_type": "refresh_token",
        },
    )
    try:
        payload["accessToken"] = response["access_token"]
        payload["expires"] = (datetime.now(UTC) + timedelta(seconds=int(response["expires_in"]))).timestamp()
        payload["updatedAt"] = _now_iso()
    except Exception as exc:
        raise AudibleAuthError(f"Audible token refresh returned an unexpected payload: {redact_sensitive_payload(response)}") from exc
    _secure_write_json(path, payload)
    return payload


def _price_to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip().replace("$", "").replace("US", "").replace(",", "")
        try:
            return float(cleaned)
        except ValueError:
            return None
    if isinstance(value, dict):
        for key in ("amount", "base", "value", "price", "display_amount"):
            parsed = _price_to_float(value.get(key))
            if parsed is not None:
                return parsed
    return None


def _round_price(value: float | None) -> float | None:
    return round(value, 2) if value is not None else None


def _collect_price_fields(payload: Any, *, path: str = "") -> list[tuple[str, Any]]:
    fields: list[tuple[str, Any]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_path = f"{path}.{key}" if path else str(key)
            if "price" in str(key).casefold() or str(key).casefold() in {"amount", "value", "currency", "currency_code"}:
                fields.append((key_path, value))
            fields.extend(_collect_price_fields(value, path=key_path))
    elif isinstance(payload, list):
        for index, item in enumerate(payload):
            fields.extend(_collect_price_fields(item, path=f"{path}[{index}]"))
    return fields


def parse_authenticated_pricing(product_payload: dict[str, Any], *, threshold: int = 10) -> dict[str, Any]:
    product = product_payload.get("product") if isinstance(product_payload.get("product"), dict) else product_payload
    fields = _collect_price_fields(product)
    currency_code = "USD"
    for key, value in fields:
        lowered = key.casefold()
        if "currency" in lowered and isinstance(value, str) and value:
            currency_code = value.upper()
            break
    current_price: float | None = None
    list_price: float | None = None
    for key, value in fields:
        lowered = key.casefold()
        if "credit" in lowered:
            continue
        parsed = _price_to_float(value)
        if parsed is None:
            continue
        if any(marker in lowered for marker in ("list", "regular", "base", "was", "strikethrough")):
            list_price = list_price if list_price is not None else parsed
        elif any(marker in lowered for marker in ("sale", "member", "current", "purchase", "lowest", "price")):
            current_price = current_price if current_price is not None else parsed
    discount_percent = None
    if current_price is not None and list_price is not None and list_price > 0 and current_price < list_price:
        discount_percent = max(0, round((1 - current_price / list_price) * 100))
    current_price = _round_price(current_price)
    list_price = _round_price(list_price)
    plan_text = json.dumps(product, sort_keys=True, ensure_ascii=False).casefold()
    included = any(marker in plan_text for marker in ("included", "plus catalog", "all you can eat", "rodizio"))
    price_basis = "unknown"
    deal_type = "unknown"
    if current_price is not None or list_price is not None:
        price_basis = "audible_member_cash"
        deal_type = "member_cash_below_list" if discount_percent is not None else "none"
    if included:
        price_basis = "audible_membership"
        deal_type = "included_with_membership"
    if discount_percent is not None and discount_percent >= threshold:
        status = "discounted"
    elif current_price is not None and list_price is not None:
        status = "available_no_discount"
    elif included:
        status = "included_with_membership"
    elif current_price is not None:
        status = "price_unknown"
    else:
        status = "price_unknown"
    return {
        "currencyCode": currency_code,
        "currentPrice": current_price,
        "listPrice": list_price,
        "discountPercent": discount_percent,
        "priceBasis": price_basis,
        "dealType": deal_type,
        "pricingStatus": status,
        "source": "audible_api_authenticated",
    }


def authenticated_product_pricing(auth_path: Path, asin: str, *, threshold: int = 10) -> dict[str, Any]:
    asin = _normalize_product_id(asin)
    auth = refresh_access_token(auth_path)
    domain = _validate_auth_domain(auth.get("domain"), marketplace=auth.get("marketplace") or "us")
    query = urllib.parse.urlencode(
        {
            "response_groups": AUDIBLE_PRODUCT_RESPONSE_GROUPS,
        }
    )
    url = f"https://api.audible.{domain}/1.0/catalog/products/{urllib.parse.quote(asin)}?{query}"
    payload = _get_json(
        url,
        {
            "Authorization": "Bearer " + str(auth["accessToken"]),
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    return parse_authenticated_pricing(payload, threshold=threshold)


def test_authenticated_price(auth_path: Path, asin: str) -> dict[str, Any]:
    pricing = authenticated_product_pricing(auth_path, asin)
    return {"ok": True, "asin": asin, "pricing": pricing}
