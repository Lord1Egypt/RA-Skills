from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = SKILL_ROOT / "references" / "rpc_catalog.json"
STATE_DIR = SKILL_ROOT / "state"
ENDPOINTS_PATH = STATE_DIR / "endpoints.json"
ENDPOINTS_KEY_PATH = STATE_DIR / ".endpoints.key"
ENDPOINTS_ENCRYPTION_VERSION = 2
ENDPOINTS_ENCRYPTION_ALGO = "hmac-sha256-stream-v1"


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}. Run build_blockpi_catalog.py first.")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _is_encrypted_state(payload: object) -> bool:
    return isinstance(payload, dict) and payload.get("encrypted") is True


def _derive_key(master_key: bytes, label: bytes) -> bytes:
    return hmac.new(master_key, label, hashlib.sha256).digest()


def _stream_xor(data: bytes, key: bytes, nonce: bytes) -> bytes:
    chunks = bytearray()
    counter = 0
    while len(chunks) < len(data):
        counter_block = counter.to_bytes(8, "big")
        chunks.extend(hmac.new(key, nonce + counter_block, hashlib.sha256).digest())
        counter += 1
    keystream = chunks[: len(data)]
    return bytes(a ^ b for a, b in zip(data, keystream))


def _read_or_create_master_key() -> bytes:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if ENDPOINTS_KEY_PATH.exists():
        encoded = ENDPOINTS_KEY_PATH.read_text(encoding="utf-8").strip()
        try:
            key = base64.urlsafe_b64decode(encoded.encode("utf-8"))
        except Exception as exc:
            raise SystemExit(f"Invalid key file at {ENDPOINTS_KEY_PATH}: {exc}") from exc
        if len(key) < 32:
            raise SystemExit(f"Invalid key length in {ENDPOINTS_KEY_PATH}; expected at least 32 bytes.")
        return key[:32]

    key = os.urandom(32)
    encoded_key = base64.urlsafe_b64encode(key).decode("utf-8")
    try:
        fd = os.open(ENDPOINTS_KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        return _read_or_create_master_key()
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(encoded_key)
    return key


def _encrypt_endpoints(data: dict) -> dict:
    master = _read_or_create_master_key()
    enc_key = _derive_key(master, b"blockpi-endpoints-enc-v1")
    mac_key = _derive_key(master, b"blockpi-endpoints-mac-v1")
    nonce = os.urandom(16)
    plaintext = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ciphertext = _stream_xor(plaintext, enc_key, nonce)
    tag = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    return {
        "version": ENDPOINTS_ENCRYPTION_VERSION,
        "encrypted": True,
        "algorithm": ENDPOINTS_ENCRYPTION_ALGO,
        "nonce": base64.urlsafe_b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.urlsafe_b64encode(ciphertext).decode("utf-8"),
        "tag": base64.urlsafe_b64encode(tag).decode("utf-8"),
    }


def _decrypt_endpoints(payload: dict) -> dict:
    if payload.get("version") != ENDPOINTS_ENCRYPTION_VERSION:
        raise SystemExit(
            f"Unsupported encrypted endpoint version in {ENDPOINTS_PATH}: {payload.get('version')!r}. "
            f"Expected {ENDPOINTS_ENCRYPTION_VERSION}."
        )
    if payload.get("algorithm") != ENDPOINTS_ENCRYPTION_ALGO:
        raise SystemExit(
            f"Unsupported endpoint encryption algorithm in {ENDPOINTS_PATH}: {payload.get('algorithm')!r}. "
            f"Expected {ENDPOINTS_ENCRYPTION_ALGO!r}."
        )
    try:
        nonce = base64.urlsafe_b64decode(payload["nonce"])
        ciphertext = base64.urlsafe_b64decode(payload["ciphertext"])
        received_tag = base64.urlsafe_b64decode(payload["tag"])
    except Exception as exc:
        raise SystemExit(f"Malformed encrypted endpoint payload in {ENDPOINTS_PATH}: {exc}") from exc

    if not ENDPOINTS_KEY_PATH.exists():
        raise SystemExit(
            f"Encrypted endpoint state found at {ENDPOINTS_PATH}, but key file {ENDPOINTS_KEY_PATH} is missing. "
            "Re-provide endpoints with --endpoint to rebuild local state."
        )

    master = _read_or_create_master_key()
    enc_key = _derive_key(master, b"blockpi-endpoints-enc-v1")
    mac_key = _derive_key(master, b"blockpi-endpoints-mac-v1")
    expected_tag = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(received_tag, expected_tag):
        raise SystemExit(
            f"Encrypted endpoint integrity check failed for {ENDPOINTS_PATH}. "
            "The file may be corrupted or paired with a different key."
        )

    plaintext = _stream_xor(ciphertext, enc_key, nonce)
    try:
        decoded = json.loads(plaintext.decode("utf-8"))
    except Exception as exc:
        raise SystemExit(f"Failed to decode decrypted endpoints from {ENDPOINTS_PATH}: {exc}") from exc
    if not isinstance(decoded, dict):
        raise SystemExit(f"Decrypted endpoint state in {ENDPOINTS_PATH} must be a JSON object.")
    return decoded


def _persist_encrypted_endpoints(data: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = _encrypt_endpoints(data)
    ENDPOINTS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_saved_endpoints() -> dict:
    if not ENDPOINTS_PATH.exists():
        return {}
    payload = json.loads(ENDPOINTS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"Invalid endpoint state format at {ENDPOINTS_PATH}. Expected JSON object.")
    if _is_encrypted_state(payload):
        return _decrypt_endpoints(payload)

    # Backward compatibility for legacy plaintext endpoint state.
    _persist_encrypted_endpoints(payload)
    return payload


def save_endpoint(chain: str, protocol: str, endpoint: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    data = load_saved_endpoints()
    chain_entry = data.setdefault(chain, {})
    if isinstance(chain_entry, str):
        chain_entry = {"jsonrpc": chain_entry}
        data[chain] = chain_entry
    chain_entry[protocol] = endpoint
    _persist_encrypted_endpoints(data)


def resolve_endpoint(chain: str, protocol: str, explicit_endpoint: str | None) -> str:
    saved = load_saved_endpoints()
    chain_entry = saved.get(chain, {})
    if isinstance(chain_entry, str):
        chain_entry = {"jsonrpc": chain_entry}
    if explicit_endpoint:
        save_endpoint(chain, protocol, explicit_endpoint)
        return explicit_endpoint
    endpoint = chain_entry.get(protocol)
    if endpoint:
        return endpoint
    raise SystemExit(
        f"No endpoint provided for chain={chain!r}, protocol={protocol!r}. Pass --endpoint once and it will be saved for future calls."
    )


def list_methods_for_protocol(catalog: dict, chain: str, protocol: str) -> list[dict]:
    info = catalog["chains"].get(chain)
    if not info:
        return []
    return [item for item in info["methods"] if item.get("protocol") == protocol]


def find_method(catalog: dict, chain: str, method: str, protocol: str | None = None) -> dict | None:
    info = catalog["chains"].get(chain)
    if not info:
        return None
    candidates = info["methods"]
    if protocol:
        candidates = [item for item in candidates if item.get("protocol") == protocol]
    for item in candidates:
        if item["method"].lower() == method.lower() or item.get("title", "").lower() == method.lower():
            return item
    return None


def infer_protocol(catalog: dict, chain: str, method: str, explicit: str | None) -> str:
    if explicit and explicit != "auto":
        return explicit
    info = catalog["chains"].get(chain)
    if not info:
        return "jsonrpc"
    match = find_method(catalog, chain, method)
    if match:
        return match.get("protocol", "jsonrpc")
    protocols = info.get("protocols", {})
    ranked = sorted(
        protocols.items(),
        key=lambda item: item[1].get("default_preference", 0),
        reverse=True,
    )
    return ranked[0][0] if ranked else "jsonrpc"


def parse_headers(header_args: list[str] | None, use_postman_defaults: bool = True) -> dict:
    headers = {"Content-Type": "application/json"}
    if use_postman_defaults:
        headers.update(
            {
                "User-Agent": "blockpi-rpc-skill/1.0.0",
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "Postman-Token": "openclaw-blockpi-default",
            }
        )
    for item in header_args or []:
        if ":" not in item:
            raise SystemExit(f"Invalid --header value: {item!r}. Expected NAME: VALUE")
        name, value = item.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def http_request(url: str, method: str, body: bytes | None, headers: dict, timeout: int = 60) -> tuple[dict | str, dict]:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body_text = resp.read().decode("utf-8", errors="ignore")
            meta = {
                "status": getattr(resp, "status", resp.getcode()),
                "headers": dict(resp.headers.items()),
                "url": resp.geturl(),
            }
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="ignore")
        meta = {
            "status": exc.code,
            "reason": exc.reason,
            "headers": dict(exc.headers.items()) if exc.headers else {},
            "url": url,
            "error_body": body_text,
        }
        raise SystemExit(json.dumps({"http_error": meta}, ensure_ascii=False, indent=2)) from exc

    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError:
        parsed = body_text
    return parsed, meta


def parse_json_value(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def load_json_from_arg(raw: str | None, path: str | None, default):
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    if raw is None:
        return default
    return parse_json_value(raw)


def build_rest_url(endpoint: str, path_or_method: str) -> str:
    if path_or_method.startswith("http://") or path_or_method.startswith("https://"):
        return path_or_method
    return urllib.parse.urljoin(endpoint.rstrip("/") + "/", path_or_method.lstrip("/"))


def run_grpcurl(args: argparse.Namespace, endpoint: str, meta: dict | None) -> dict:
    grpcurl = shutil.which(args.grpcurl_bin or "grpcurl")
    if not grpcurl:
        raise SystemExit(
            "gRPC call requested, but grpcurl is not installed or not on PATH. Install grpcurl or use protocol metadata only."
        )
    service = args.grpc_service or (meta.get("service") if meta else None)
    if not service and "/" in args.method:
        service = args.method.split("/", 1)[0]
    if not service:
        raise SystemExit("gRPC calls need --grpc-service or a catalog entry with a service folder.")

    rpc_name = args.grpc_method or args.method
    if "/" not in rpc_name:
        rpc_name = f"{service}/{rpc_name}"

    data = load_json_from_arg(args.body, args.body_file, {})
    command = [grpcurl]
    if args.grpc_proto:
        command.extend(["-proto", args.grpc_proto])
    for header in args.header or []:
        command.extend(["-H", header])
    if args.grpc_token:
        command.extend(["-H", f"x-token: {args.grpc_token}"])
    elif args.grpc_metadata:
        for item in args.grpc_metadata:
            command.extend(["-H", item])
    command.extend(["-d", json.dumps(data), endpoint, rpc_name])

    proc = subprocess.run(command, capture_output=True, text=True)
    result = {
        "grpcurl": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }
    if proc.returncode != 0:
        raise SystemExit(json.dumps({"grpc_error": result}, ensure_ascii=False, indent=2))
    try:
        result["parsed"] = json.loads(proc.stdout)
    except json.JSONDecodeError:
        pass
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Call a BlockPI endpoint with protocol-aware routing.")
    parser.add_argument("--chain", required=True, help="Chain key, e.g. ethereum, sui, solana, cosmos-hub")
    parser.add_argument("--method", required=True, help="RPC method, REST path, GraphQL label, or gRPC RPC name")
    parser.add_argument("--protocol", default="auto", choices=["auto", "jsonrpc", "http", "grpc", "graphql"], help="Transport protocol")
    parser.add_argument("--endpoint", help="Full endpoint URL or host:port. Saved per chain and protocol once provided.")
    parser.add_argument("--params", default="[]", help="JSON array for JSON-RPC params")
    parser.add_argument("--params-file", help="Path to a JSON file for JSON-RPC params")
    parser.add_argument("--id", default="1", help="JSON-RPC id value, default 1")
    parser.add_argument("--http-method", default="GET", help="HTTP verb for protocol=http, default GET")
    parser.add_argument("--body", help="JSON body for protocol=http, grpc, or graphql variables")
    parser.add_argument("--body-file", help="JSON file for protocol=http or grpc request body")
    parser.add_argument("--query", help="GraphQL query string")
    parser.add_argument("--query-file", help="GraphQL query file")
    parser.add_argument("--variables", help="GraphQL variables JSON object")
    parser.add_argument("--variables-file", help="GraphQL variables JSON file")
    parser.add_argument("--grpc-service", help="gRPC service name, for example geyser.Geyser or sui.rpc.v2.TransactionExecutionService")
    parser.add_argument("--grpc-method", help="Full gRPC method path if different from --method")
    parser.add_argument("--grpc-proto", help="Local .proto file path for grpcurl")
    parser.add_argument("--grpc-token", help="Convenience token, sent as x-token metadata header")
    parser.add_argument("--grpc-metadata", action="append", help="Extra grpcurl metadata header, repeatable")
    parser.add_argument("--grpcurl-bin", help="grpcurl executable name or path")
    parser.add_argument("--header", action="append", help="Extra HTTP header in the form NAME: VALUE. Repeat as needed.")
    parser.add_argument("--no-postman", action="store_true", help="Disable the default Postman-like HTTP header set")
    parser.add_argument("--skip-validate", action="store_true", help="Skip checking the local catalog before calling")
    parser.add_argument("--show-meta", action="store_true", help="Print catalog metadata before the response")
    parser.add_argument("--debug-http", action="store_true", help="Print the final HTTP request and response metadata")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("BLOCKPI_RPC_TIMEOUT", "60")), help="Network timeout in seconds")
    args = parser.parse_args()

    catalog = load_catalog()
    protocol = infer_protocol(catalog, args.chain, args.method, args.protocol)
    meta = None
    if not args.skip_validate:
        meta = find_method(catalog, args.chain, args.method, None if args.protocol == "auto" else protocol)
        if not meta:
            available = sorted(catalog["chains"].keys())
            hint = list_methods_for_protocol(catalog, args.chain, protocol)[:10]
            hint_names = [item["method"] for item in hint]
            raise SystemExit(
                f"Method not found in catalog for chain={args.chain!r}, method={args.method!r}, protocol={protocol!r}. "
                f"Known chains: {available}. Sample methods for this protocol: {hint_names}"
            )

    endpoint = resolve_endpoint(args.chain, protocol, args.endpoint)
    headers = parse_headers(args.header, use_postman_defaults=not args.no_postman)

    if args.show_meta:
        print(json.dumps({"catalog": meta, "protocol": protocol, "endpoint": endpoint}, ensure_ascii=False, indent=2))

    if protocol == "jsonrpc":
        params = load_json_from_arg(args.params, args.params_file, [])
        if not isinstance(params, list):
            raise SystemExit("JSON-RPC params must decode to a JSON array. Use --params-file if shell quoting is awkward.")
        payload = {
            "jsonrpc": "2.0",
            "method": args.method,
            "params": params,
            "id": parse_json_value(args.id),
        }
        result, response_meta = http_request(
            endpoint,
            method="POST",
            body=json.dumps(payload).encode("utf-8"),
            headers=headers,
            timeout=args.timeout,
        )
        if args.debug_http:
            print(json.dumps({"http": {"request": {"url": endpoint, "headers": headers, "payload": payload}, "response": response_meta}}, ensure_ascii=False, indent=2))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if protocol == "graphql":
        query = Path(args.query_file).read_text(encoding="utf-8") if args.query_file else args.query
        if not query:
            raise SystemExit("GraphQL calls require --query or --query-file.")
        variables = load_json_from_arg(args.variables, args.variables_file, {})
        payload = {"query": query, "variables": variables}
        result, response_meta = http_request(
            endpoint,
            method="POST",
            body=json.dumps(payload).encode("utf-8"),
            headers=headers,
            timeout=args.timeout,
        )
        if args.debug_http:
            print(json.dumps({"http": {"request": {"url": endpoint, "headers": headers, "payload": payload}, "response": response_meta}}, ensure_ascii=False, indent=2))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if protocol == "http":
        body_obj = load_json_from_arg(args.body, args.body_file, None)
        body_bytes = None if body_obj is None else json.dumps(body_obj).encode("utf-8")
        url = build_rest_url(endpoint, args.method)
        result, response_meta = http_request(
            url,
            method=args.http_method.upper(),
            body=body_bytes,
            headers=headers,
            timeout=args.timeout,
        )
        if args.debug_http:
            print(json.dumps({"http": {"request": {"url": url, "headers": headers, "method": args.http_method.upper(), "body": body_obj}, "response": response_meta}}, ensure_ascii=False, indent=2))
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if protocol == "grpc":
        result = run_grpcurl(args, endpoint, meta)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    raise SystemExit(f"Unsupported protocol: {protocol}")


if __name__ == "__main__":
    sys.exit(main())
