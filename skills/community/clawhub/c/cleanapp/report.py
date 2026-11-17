#!/usr/bin/env python3
"""Preview approved CleanApp reports, explicit handling and recorded outcomes."""
import argparse
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import json
import math
import os
import re
from pathlib import Path
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid

FRONT_DOOR = "https://www.cleanapp.io/agents"
VERSION = "0.3.0"
ALLOWED_HOSTS = {"www.cleanapp.io", "cleanapp.io", "live.cleanapp.io"}
FIELDS = {"description", "title", "source_id", "agent_name", "url", "latitude", "longitude", "handling"}


class ClientError(Exception):
    pass


class HTTPFailure(ClientError):
    def __init__(self, status, retry_after=None, response=None):
        self.status, self.retry_after, self.response = status, retry_after, response
        super().__init__(f"HTTP {status}" + (f"; Retry-After: {retry_after}" if retry_after else ""))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def checked_url(url, allow_local_http=False):
    p = urllib.parse.urlsplit(url)
    local = p.hostname in {"localhost", "127.0.0.1", "::1"}
    if p.username or p.password or p.fragment or not p.hostname:
        raise ClientError("Endpoint must not contain credentials or a fragment")
    if local and allow_local_http and p.scheme in {"http", "https"}:
        return url
    if p.scheme != "https" or p.hostname not in ALLOWED_HOSTS or p.port not in {None, 443}:
        raise ClientError("Use a CleanApp HTTPS endpoint; loopback fixtures require --allow-local-http")
    return url


def origin(url):
    p = urllib.parse.urlsplit(url)
    return p.scheme, p.hostname, p.port or (443 if p.scheme == "https" else 80)


def request(url, *, method="GET", payload=None, token=None, allow_local_http=False, timeout=20):
    checked_url(url, allow_local_http)
    headers = {"Accept": "application/json, text/plain, text/html", "User-Agent": f"cleanapp-public-client/{VERSION}"}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=timeout) as r:
            body = r.read(524289)
            if len(body) > 524288:
                raise ClientError("Response exceeded 512 KiB")
            return r.status, body.decode("utf-8")
    except urllib.error.HTTPError as e:
        # Server bodies can include private receipt data; never print them.
        try:
            response = json.loads(e.read(524288))
        except (ValueError, UnicodeError):
            response = None
        raise HTTPFailure(e.code, e.headers.get("Retry-After"), response) from None
    except (urllib.error.URLError, TimeoutError):
        raise ClientError("Network request failed; delivery may be unknown. Reuse the saved source_id when retrying.") from None


def json_request(url, **kwargs):
    status, body = request(url, **kwargs)
    try:
        obj = json.loads(body)
    except ValueError:
        raise ClientError("Expected a JSON response") from None
    if not isinstance(obj, dict):
        raise ClientError("Expected a JSON object")
    return status, obj


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(v for k, v in attrs if k == "href" and v)


def discover(front_door=FRONT_DOOR, *, allow_local_http=False, timeout=20):
    _, html = request(front_door, allow_local_http=allow_local_http, timeout=timeout)
    links = Links()
    links.feed(html)
    candidates = [urllib.parse.urljoin(front_door, x) for x in links.hrefs
                  if urllib.parse.urlsplit(x).path.endswith("/agents.txt")]
    if not candidates:
        raise ClientError("Agent front door does not link to agents.txt")
    descriptor = candidates[0]
    if origin(descriptor) != origin(front_door):
        raise ClientError("Agent instructions must share the front-door origin")
    _, text = request(descriptor, allow_local_http=allow_local_http, timeout=timeout)
    labels = {}
    for line in text.splitlines():
        label, sep, value = line.partition(": ")
        if sep:
            labels[label.strip().lstrip("- ")] = value.strip().strip("`")
    endpoint, mcp = labels.get("Public report endpoint"), labels.get("MCP endpoint")
    if not endpoint or not mcp:
        raise ClientError("Agent instructions must name Public report endpoint and MCP endpoint")
    if labels.get("MCP authentication", "").lower() != "none" or labels.get("Public report authentication", "").lower() != "none":
        raise ClientError("Agent instructions no longer declare the no-auth public paths; inspect them before sending")
    checked_url(endpoint, allow_local_http)
    checked_url(mcp, allow_local_http)
    return {"front_door": front_door, "instructions_url": descriptor, "public_report_endpoint": endpoint, "mcp_endpoint": mcp}


def validate_payload(obj):
    if not isinstance(obj, dict) or set(obj) - FIELDS:
        raise ClientError("Input must be one public report object; authenticated batches use CleanApp Wire")
    if not isinstance(obj.get("description"), str) or not obj["description"].strip():
        raise ClientError("description is required")
    if len(obj["description"].encode("utf-8")) > 8192:
        raise ClientError("description exceeds 8192 UTF-8 bytes")
    obj = dict(obj)
    if "handling" in obj:
        handling = obj["handling"]
        if (not isinstance(handling, dict) or set(handling) != {"publication", "notices"}
                or handling["publication"] not in ("private", "automatic")
                or handling["notices"] not in ("none", "automatic")):
            raise ClientError("handling must explicitly set publication private|automatic and notices none|automatic")
        obj["handling"] = dict(handling)
    for name, limit in (("title", 255), ("source_id", 128), ("agent_name", 80), ("url", 2048)):
        if name in obj:
            if not isinstance(obj[name], str):
                raise ClientError(f"{name} must be text")
            length = len(obj[name]) if name in {"agent_name", "source_id"} else len(obj[name].encode("utf-8"))
            if length > limit:
                raise ClientError(f"{name} exceeds its documented length limit")
    if "source_id" in obj:
        try:
            value = uuid.UUID(obj["source_id"])
            if value.version != 4 or str(value) != obj["source_id"].lower():
                raise ValueError()
            obj["source_id"] = str(value)
        except ValueError:
            raise ClientError("source_id must be a private random UUIDv4 generated once for this report") from None
    if "url" in obj:
        p = urllib.parse.urlsplit(obj["url"])
        if p.scheme not in {"https", "http"} or not p.hostname or p.username or p.password:
            raise ClientError("url must be an HTTP(S) source URL without credentials")
    if ("latitude" in obj) != ("longitude" in obj):
        raise ClientError("Supply latitude and longitude together")
    for key, limit in (("latitude", 90), ("longitude", 180)):
        if key in obj and (isinstance(obj[key], bool) or not isinstance(obj[key], (int, float))
                           or not math.isfinite(obj[key]) or not -limit <= obj[key] <= limit):
            raise ClientError(f"Invalid {key}")
    return dict(obj)


def save_private(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".cleanapp-receipt-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def validate_receipt(receipt, endpoint, *, allow_local_http=False):
    if not isinstance(receipt, dict):
        raise ClientError("Expected a private receipt object")
    if not all(isinstance(receipt.get(x), str) and receipt[x] for x in ("receipt_id", "tracking_token", "status_url")):
        raise ClientError("Response did not contain a complete private receipt")
    if receipt.get("status") != "quarantined" or receipt.get("publication_status") not in ("private", "pending", "public", "held"):
        raise ClientError("Expected a quarantine intake receipt with a recorded publication state; inspect the saved response")
    result = dict(receipt)
    result["status_url"] = urllib.parse.urljoin(endpoint, receipt["status_url"])
    checked_url(result["status_url"], allow_local_http)
    if origin(result["status_url"]) != origin(endpoint) or urllib.parse.urlsplit(result["status_url"]).query:
        raise ClientError("Receipt status URL must share the intake origin and exclude token queries")
    if (not re.fullmatch(r"rcpt_[A-Za-z0-9_-]{1,128}", result["receipt_id"])
            or urllib.parse.urlsplit(result["status_url"]).path != "/api/v1/public/agent-reports/receipts/" + result["receipt_id"]):
        raise ClientError("Receipt status URL must identify exactly this private receipt")
    return result


def bounded_text(value, limit):
    return value if isinstance(value, str) and len(value) <= limit else None


def recorded_time(value):
    if not isinstance(value, str) or len(value) > 40:
        return None
    try:
        return value if datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo else None
    except ValueError:
        return None


def canonical_path(value):
    return value if isinstance(value, str) and re.fullmatch(r"/(physical|digital)/report/rpt_[A-Za-z0-9_-]+", value) else None


def project_outcome(value):
    """Expose recorded decisions/actions; never raw reports or provider bodies."""
    if not isinstance(value, dict):
        return None
    processing, publication, action = (value.get(k) for k in ("processing", "publication", "next_action"))
    deliveries = value.get("delivery")
    if (not all(isinstance(x, dict) for x in (processing, publication, action))
            or processing.get("status") not in ("pending_analysis", "analyzed", "failed", "not_required")
            or publication.get("status") not in ("private", "pending", "public", "held")
            or action.get("type") not in ("none", "provide_information", "wait", "retry", "review_privacy")
            or not isinstance(value.get("final"), bool) or not isinstance(deliveries, list) or len(deliveries) > 20):
        return None
    result = {"processing": {"status": processing["status"]}, "publication": {"status": publication["status"]},
              "delivery": [], "next_action": {"type": action["type"]}, "final": value["final"]}
    if recorded_time(processing.get("completed_at")):
        result["processing"]["completed_at"] = processing["completed_at"]
    if publication["status"] == "public":
        path = canonical_path(publication.get("canonical_path"))
        if not path:
            return None
        result["publication"]["canonical_path"] = path
    if bounded_text(publication.get("reason_code"), 128):
        result["publication"]["reason_code"] = publication["reason_code"]
    if value.get("decision") is not None:
        decision = value["decision"]
        if (not isinstance(decision, dict) or decision.get("state") not in ("pending", "accepted", "cluster_candidate", "needs_information", "rejected", "held")
                or not bounded_text(decision.get("reason_code"), 128) or not bounded_text(decision.get("message"), 2000)
                or type(decision.get("policy_version")) is not int or decision["policy_version"] < 1):
            return None
        result["decision"] = {k: decision[k] for k in ("state", "reason_code", "message", "policy_version")}
        if recorded_time(decision.get("decided_at")):
            result["decision"]["decided_at"] = decision["decided_at"]
    for delivery in deliveries:
        if (not isinstance(delivery, dict) or delivery.get("channel") not in ("email", "blockscan")
                or delivery.get("status") not in ("not_requested", "pending", "sent", "held", "failed", "uncertain")
                or type(delivery.get("evidence_count")) is not int or delivery["evidence_count"] < 0):
            return None
        if delivery["status"] == "sent" and (not delivery["evidence_count"] or not recorded_time(delivery.get("last_sent_at"))):
            return None
        item = {k: delivery[k] for k in ("channel", "status", "evidence_count")}
        if recorded_time(delivery.get("last_sent_at")):
            item["last_sent_at"] = delivery["last_sent_at"]
        if bounded_text(delivery.get("reason_code"), 128):
            item["reason_code"] = delivery["reason_code"]
        result["delivery"].append(item)
    if isinstance(action.get("fields"), list):
        result["next_action"]["fields"] = [x for x in action["fields"][:20] if isinstance(x, str) and re.fullmatch(r"[a-z_]{1,80}", x)]
    relationship = value.get("relationship")
    if isinstance(relationship, dict) and relationship.get("type") == "cluster_candidate" and isinstance(relationship.get("candidates"), list):
        candidates = []
        for candidate in relationship["candidates"][:10]:
            if not isinstance(candidate, dict):
                continue
            path = canonical_path(candidate.get("canonical_path"))
            if (path and candidate.get("type") == "report" and candidate.get("reference") == path.rsplit("/", 1)[1]
                    and bounded_text(candidate.get("reason_code"), 128)):
                candidates.append({k: candidate[k] for k in ("type", "reference", "canonical_path", "reason_code")})
        result["relationship"] = {"type": "cluster_candidate", "candidates": candidates}
    return result


def receipt_summary(receipt):
    result = {k: receipt[k] for k in ("receipt_id", "status", "publication_status", "processing_status", "received_at")
              if bounded_text(receipt.get(k), 191)}
    if isinstance(receipt.get("idempotency_replay"), bool):
        result["idempotency_replay"] = receipt["idempotency_replay"]
    outcome = project_outcome(receipt.get("outcome"))
    if outcome is not None:
        result["outcome"] = outcome
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", help="One report JSON file; omit to read JSON from stdin")
    p.add_argument("--description", help="Observed problem text; use --input for optional fields")
    p.add_argument("--front-door", default=FRONT_DOOR)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--discover", action="store_true", help="Read-only front-door discovery")
    mode.add_argument("--submit", action="store_true", help="Send the approved report; default is offline preview")
    mode.add_argument("--dry-run", action="store_true", help="Offline preview; no credential or network")
    p.add_argument("--receipt-file", help="Private receipt/checkpoint file (required with --submit)")
    p.add_argument("--retry", action="store_true", help="Reuse the saved source_id; require unchanged input")
    mode.add_argument("--status", action="store_true", help="Check --receipt-file privately")
    p.add_argument("--allow-local-http", action="store_true", help="Allow only loopback HTTP fixture endpoints")
    p.add_argument("--timeout", type=int, default=20)
    args = p.parse_args(argv)
    net = {"allow_local_http": args.allow_local_http, "timeout": args.timeout}
    try:
        if args.retry and not args.submit:
            raise ClientError("--retry requires --submit and the saved receipt file")
        if args.status:
            if not args.receipt_file:
                raise ClientError("--status requires --receipt-file")
            saved = json.loads(Path(args.receipt_file).read_text())
            receipt = validate_receipt(saved["receipt"], saved["endpoint"], allow_local_http=args.allow_local_http)
            _, result = json_request(receipt["status_url"], token=receipt["tracking_token"], **net)
            if result.get("receipt_id") != receipt["receipt_id"]:
                raise ClientError("Status did not identify the same private receipt")
            print(json.dumps(receipt_summary(result)))
            return 0
        if args.discover:
            print(json.dumps(discover(args.front_door, **net), indent=2))
            return 0
        if args.description is not None and args.input:
            raise ClientError("Use --description or --input, not both")
        raw = {"description": args.description} if args.description is not None else json.loads(
            Path(args.input).read_text() if args.input else sys.stdin.read())
        payload = validate_payload(raw)
        if not args.submit:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        if not args.receipt_file:
            raise ClientError("--submit requires --receipt-file for safe retries after unknown delivery")
        if args.retry:
            previous = json.loads(Path(args.receipt_file).read_text())
            payload.setdefault("source_id", previous["source_id"])
        payload.setdefault("source_id", str(uuid.uuid4()))
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if args.retry and digest != previous["payload_sha256"]:
            raise ClientError("Retry payload changed; reuse the original approved report")
        if Path(args.receipt_file).exists() and not args.retry:
            raise ClientError("Receipt file exists; use --retry for the same report or choose a new file")
        endpoints = discover(args.front_door, **net)
        endpoint = endpoints["public_report_endpoint"]
        if args.retry and endpoint != previous["endpoint"]:
            raise ClientError("Intake endpoint changed since the first attempt; inspect the saved receipt before retrying")
        checkpoint = {"endpoint": endpoint, "source_id": payload["source_id"], "payload_sha256": digest, "delivery": "unknown"}
        save_private(args.receipt_file, checkpoint)
        try:
            _, receipt = json_request(endpoint, method="POST", payload=payload, **net)
        except HTTPFailure as e:
            if isinstance(e.response, dict) and e.response.get("receipt_id"):
                checkpoint["receipt"] = e.response
                save_private(args.receipt_file, checkpoint)
            raise
        checkpoint["receipt"] = receipt
        save_private(args.receipt_file, checkpoint)
        validate_receipt(receipt, endpoint, allow_local_http=args.allow_local_http)
        if receipt.get("source_id") != payload["source_id"]:
            raise ClientError("Receipt source_id differs from the request; inspect saved response")
        checkpoint["delivery"] = "acknowledged"
        save_private(args.receipt_file, checkpoint)
        print(json.dumps({**receipt_summary(receipt), "private_receipt_file": args.receipt_file}))
        return 0
    except (ClientError, ValueError, OSError, KeyError) as e:
        print(f"CleanApp: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
