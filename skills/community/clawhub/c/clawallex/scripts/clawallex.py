#!/usr/bin/env python3
"""Clawallex CLI — OpenClaw Skill backend script."""

import argparse
import base64
import hashlib
import http.client
import hmac
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import webbrowser

# ── Constants ──────────────────────────────────────────────────────────
DEFAULT_BASE_URL = "https://api.clawallex.com"
PORTAL_URL = "https://app.clawallex.com"
BASE_PATH = "/api/v1"
CREDENTIALS_DIR = os.path.join(os.path.expanduser("~"), ".clawallex")
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, "credentials.json")
CLIENT_IDS_FILE = os.path.join(CREDENTIALS_DIR, "client_ids.json")
HTTP_TIMEOUT = 30  # seconds
APP_API_URL = "https://appapi.clawallex.com"
SIGNUP_POLL_INTERVAL = 2    # seconds between polls
SIGNUP_TIMEOUT = 300        # seconds total (5 minutes, matches server token TTL)


# ── Credential helpers ─────────────────────────────────────────────────

def load_credentials():
    """Load credentials from ~/.clawallex/credentials.json. Returns dict or None."""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            return None
        with open(CREDENTIALS_FILE, "r") as f:
            raw = f.read().strip()
        if not raw:
            return None
        data = json.loads(raw)
        if not data.get("apiKey") or not data.get("apiSecret"):
            return None
        return {
            "apiKey": data["apiKey"],
            "apiSecret": data["apiSecret"],
            "baseUrl": data.get("baseUrl", DEFAULT_BASE_URL),
        }
    except (json.JSONDecodeError, OSError):
        return None


def save_credentials(creds):
    """Save credentials to ~/.clawallex/credentials.json with 0600 permissions."""
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    fd = os.open(CREDENTIALS_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(creds, f, indent=2)


def normalize_base_url(url):
    """Normalize baseUrl to scheme://host[:port] — lowercase, strip defaults."""
    parsed = urllib.parse.urlparse(url)
    scheme = (parsed.scheme or "https").lower()
    host = (parsed.hostname or "").lower()
    port = parsed.port
    is_default = (
        port is None
        or (scheme == "https" and port == 443)
        or (scheme == "http" and port == 80)
    )
    port_str = "" if is_default else f":{port}"
    return f"{scheme}://{host}{port_str}"


def _read_client_ids():
    """Read client_ids.json. Returns (dict, corrupt_flag).
    If file missing: ({}, False). If corrupt: ({}, True) + warning to stderr."""
    if not os.path.exists(CLIENT_IDS_FILE):
        return {}, False
    try:
        with open(CLIENT_IDS_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data, False
        print(f"[clawallex] ⚠ client_ids.json is not a valid object — please delete or fix: {CLIENT_IDS_FILE}",
              file=sys.stderr)
        return {}, True
    except (json.JSONDecodeError, ValueError):
        print(f"[clawallex] ⚠ client_ids.json is corrupt (invalid JSON) — please delete or fix: {CLIENT_IDS_FILE}",
              file=sys.stderr)
        return {}, True
    except OSError:
        return {}, False


def _write_client_ids(store):
    """Write client_ids.json."""
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    with open(CLIENT_IDS_FILE, "w") as f:
        json.dump(store, f, indent=2)


def save_client_id(base_url, client_id):
    """Save client_id for a specific baseUrl."""
    key = normalize_base_url(base_url)
    store, _ = _read_client_ids()
    store[key] = client_id
    _write_client_ids(store)


def resolve_client_id(base_url):
    """Read client_id for baseUrl from client_ids.json, or return None.
    Returns None (not error) if file is corrupt — caller decides how to handle.
    Prints warning to stderr if corrupt."""
    key = normalize_base_url(base_url)
    store, _ = _read_client_ids()
    val = store.get(key, "")
    return val.strip() if val.strip() else None


# ── Output helpers ─────────────────────────────────────────────────────

def output_success(data, hint=None):
    """Print success JSON to stdout."""
    result = {"success": True, "data": data}
    if hint:
        result["_hint"] = hint
    print(json.dumps(result, indent=2))
    return 0


def output_error(message):
    """Print error JSON to stdout."""
    print(json.dumps({"success": False, "error": message}, indent=2))
    return 1


def format_402_quote(d, tool_name="pay"):
    """Format a 402 Mode B challenge with a ready-to-fill Stage 2 template."""
    payable = d.get("payable_amount", "0")
    try:
        max_amount = str(round(float(payable) * 1_000_000))
    except (ValueError, TypeError):
        max_amount = "<payable_amount × 10^6>"
    return output_success({
        "_stage": "quote",
        "_status": 402,
        **d,
        "_stage2_template": {
            "client_request_id": d.get("client_request_id"),
            "x402_version": 1,
            "payment_payload": {
                "scheme": "exact",
                "network": "<chain network, e.g. 'ETH'>",
                "payload": {
                    "signature": "<your EIP-3009 signature hex>",
                    "authorization": {
                        "from": "<your wallet address>",
                        "to": d.get("payee_address"),
                        "value": max_amount,
                        "validAfter": "<unix seconds, e.g. now - 60>",
                        "validBefore": "<unix seconds, e.g. now + 3600>",
                        "nonce": "<random 32-byte hex, unique per auth>",
                    },
                },
            },
            "payment_requirements": {
                "scheme": "exact",
                "network": "<chain network, e.g. 'ETH'>",
                "asset": d.get("asset_address"),
                "payTo": d.get("payee_address"),
                "maxAmountRequired": max_amount,
                "extra": {"referenceId": d.get("x402_reference_id")},
            },
            "extra": {
                "card_amount": d.get("final_card_amount"),
                "paid_amount": d.get("payable_amount"),
            },
        },
    }, "Mode B Stage 1 complete — 402 Payment Required (this is expected, not an error).\n"
       "\n"
       f"Next: sign the EIP-3009 transferWithAuthorization using your own wallet/signing library,\n"
       f"then call '{tool_name}' again using the _stage2_template above. Fill in the <...> placeholders:\n"
       f"  --client-request-id '{d.get('client_request_id')}'  ← MUST be this exact value\n"
       f"  --x402-version 1\n"
       "  --payment-payload '<fill from _stage2_template.payment_payload>'\n"
       "  --payment-requirements '<fill from _stage2_template.payment_requirements>'\n"
       "  --extra '<fill from _stage2_template.extra>'\n"
       "\n"
       "Constraints:\n"
       "  - client_request_id MUST be identical to Stage 1\n"
       "  - payload.authorization.to MUST equal payment_requirements.payTo\n"
       "  - payload.authorization.value MUST equal payment_requirements.maxAmountRequired\n"
       "  - payment_payload.network MUST equal payment_requirements.network")


# ── API Client ─────────────────────────────────────────────────────────

class ApiError(Exception):
    """API error with status code, error code, and optional details."""

    def __init__(self, status_code, code, message, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details


class ClawalexClient:
    """HTTP client for Clawallex Gateway API with HMAC-SHA256 signing."""

    def __init__(self, api_key, api_secret, base_url, client_id):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id

    def _sign(self, method, path, body, include_client_id=True):
        """Generate signed headers for a request."""
        timestamp = str(int(time.time()))
        body_hash = hashlib.sha256(body.encode()).hexdigest()
        canonical = f"{method}\n{path}\n{timestamp}\n{body_hash}"
        signature = base64.b64encode(
            hmac.new(self.api_secret.encode(), canonical.encode(), hashlib.sha256).digest()
        ).decode()
        headers = {
            "X-API-Key": self.api_key,
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "Content-Type": "application/json",
        }
        if include_client_id and self.client_id:
            headers["X-Client-Id"] = self.client_id
        return headers

    def _build_url(self, path, params=None):
        """Build full URL with /api/v1 prefix and optional query params."""
        full_path = BASE_PATH + path
        url = self.base_url + full_path
        if params:
            filtered = {k: str(v) for k, v in params.items() if v is not None and str(v) != ""}
            if filtered:
                url += "?" + urllib.parse.urlencode(filtered)
        return url

    def _request(self, method, path, body=None, params=None, include_client_id=True):
        """Make an HTTP request with signing and retry on network errors."""
        full_path = BASE_PATH + path
        url = self._build_url(path, params)
        raw_body = json.dumps(body) if body is not None else ""
        headers = self._sign(method, full_path, raw_body, include_client_id)

        data_bytes = raw_body.encode() if raw_body else b""

        parsed_url = urllib.parse.urlparse(url)
        last_error = None
        for attempt in range(2):  # 1 retry on network error
            try:
                if parsed_url.scheme == "https":
                    import ssl
                    conn = http.client.HTTPSConnection(
                        parsed_url.hostname,
                        parsed_url.port or 443,
                        timeout=HTTP_TIMEOUT,
                        context=ssl.create_default_context(),
                    )
                else:
                    conn = http.client.HTTPConnection(
                        parsed_url.hostname,
                        parsed_url.port or 80,
                        timeout=HTTP_TIMEOUT,
                    )
                request_path = parsed_url.path
                if parsed_url.query:
                    request_path += "?" + parsed_url.query
                conn.request(method, request_path, body=data_bytes if data_bytes else None, headers=headers)
                resp = conn.getresponse()
                text = resp.read().decode()
                conn.close()

                if 200 <= resp.status < 300:
                    return json.loads(text)

                # Error handling
                try:
                    parsed = json.loads(text)
                    code = parsed.get("code", "UNKNOWN_ERROR")
                    message = parsed.get("message", text)
                    details = parsed.get("details")
                except (json.JSONDecodeError, ValueError):
                    code = "UNKNOWN_ERROR"
                    message = text
                    details = None
                raise ApiError(resp.status, code, message, details)
            except ApiError:
                raise
            except (OSError, ConnectionError) as e:
                last_error = e
                if attempt == 0:
                    continue  # retry once
                raise

        raise last_error  # unreachable, but satisfies linter

    def get(self, path, params=None):
        """GET /payment/* — requires X-Client-Id."""
        return self._request("GET", path, params=params)

    def post(self, path, body):
        """POST /payment/* — requires X-Client-Id."""
        return self._request("POST", path, body=body)

    def get_auth(self, path):
        """GET /auth/* — NO X-Client-Id."""
        return self._request("GET", path, include_client_id=False)

    def post_auth(self, path, body):
        """POST /auth/* — NO X-Client-Id."""
        return self._request("POST", path, body=body, include_client_id=False)


# ── Subcommand handlers ────────────────────────────────────────────────

def require_credentials():
    """Load credentials or return error exit code."""
    creds = load_credentials()
    if not creds:
        return None, output_error(
            "Clawallex is not configured. Run: clawallex.py setup --action connect --api-key YOUR_KEY --api-secret YOUR_SECRET"
        )
    base_url = creds["baseUrl"]
    client_id = resolve_client_id(base_url)
    client = ClawalexClient(creds["apiKey"], creds["apiSecret"], base_url, client_id or "")
    return client, None


def _run_connect(api_key, api_secret, base_url):
    """Verify credentials via whoami, bootstrap client_id, and save both locally.
    Calls output_success or output_error and returns the exit code (0 or 1).
    """
    temp_client = ClawalexClient(api_key, api_secret, base_url, "")

    # Step 1: Verify credentials with whoami
    try:
        whoami = temp_client.get_auth("/auth/whoami")
    except ApiError as e:
        return output_error(
            f"Invalid credentials — API returned: {e}. Check your API Key and Secret at {PORTAL_URL}/dashboard/settings"
        )
    except Exception as e:
        return output_error(f"Cannot reach Clawallex API at {base_url}: {e}")

    # Step 2: Bootstrap client_id
    if whoami.get("client_id_bound"):
        real_client_id = whoami["bound_client_id"]
    else:
        bootstrap_body = {}
        local_cid = resolve_client_id(base_url)
        if local_cid:
            bootstrap_body["preferred_client_id"] = local_cid
        try:
            bootstrap = temp_client.post_auth("/auth/bootstrap", bootstrap_body)
            real_client_id = bootstrap["client_id"]
        except ApiError as e:
            return output_error(f"Bootstrap failed [{e.code}]: {e}")

    save_credentials({
        "apiKey": api_key,
        "apiSecret": api_secret,
        "baseUrl": base_url,
    })
    save_client_id(base_url, real_client_id)
    return output_success({
        "status": "connected",
        "client_id": real_client_id,
        "client_id_bound": True,
        "credentials_file": CREDENTIALS_FILE,
    }, f"Clawallex connected! client_id: {real_client_id} (bound on server). "
       "You can now use pay, subscribe, wallet, and other commands.")


def cmd_setup(args):
    """Handle setup subcommand."""
    action = args.action

    if action == "status":
        creds = load_credentials()
        cid = resolve_client_id(creds["baseUrl"]) if creds else None
        if creds:
            masked_key = creds["apiKey"][:8] + "..." + creds["apiKey"][-4:]
            return output_success({
                "status": "configured",
                "api_key": masked_key,
                "base_url": creds["baseUrl"],
                "local_client_id": cid or "(not set)",
                "credentials_file": CREDENTIALS_FILE,
            }, "Clawallex is configured and ready.")
        return output_success({
            "status": "not_configured",
            "local_client_id": cid or "(not set)",
        }, f"Not configured. Go to {PORTAL_URL}/dashboard/settings to get your API Key and Secret, "
           f"then run: clawallex.py setup --action connect --api-key YOUR_KEY --api-secret YOUR_SECRET")

    if action == "register":
        return output_success({
            "status": "registration_required",
            "sign_up_url": f"{PORTAL_URL}/signup",
            "api_keys_url": f"{PORTAL_URL}/dashboard/settings",
        }, f"Create an account at {PORTAL_URL}/signup, then run: "
           f"clawallex.py setup --action connect --api-key YOUR_KEY --api-secret YOUR_SECRET")

    if action == "connect":
        if not args.api_key or not args.api_secret:
            return output_error(
                f"Both --api-key and --api-secret are required. Get them at {PORTAL_URL}/dashboard/settings"
            )
        return _run_connect(args.api_key, args.api_secret, args.base_url)

    return output_error(f"Unknown action: {action}")


def cmd_signup(args):
    """Browser-based signup flow: generate token → open browser → poll → connect."""
    portal_url = (args.portal_url or PORTAL_URL).rstrip("/")
    app_api_url = (args.app_api_url or APP_API_URL).rstrip("/")
    base_url = args.base_url or DEFAULT_BASE_URL

    token = secrets.token_hex(32)
    signup_url = f"{portal_url}/cli-signup?token={token}"

    print(f"Open this URL in your browser: {signup_url}", flush=True)
    try:
        webbrowser.open(signup_url)
    except Exception:
        pass  # headless / no browser — user will open manually

    poll_url = f"{app_api_url}/api/v1/cli-signup/result/{token}"
    deadline = time.time() + SIGNUP_TIMEOUT

    while time.time() < deadline:
        print("Waiting for browser authorization...", flush=True)
        time.sleep(SIGNUP_POLL_INTERVAL)

        try:
            req = urllib.request.Request(poll_url, headers={"User-Agent": "clawallex-cli/1.0"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                result = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return output_error("Token not found or expired. Run signup again to get a new URL.")
            # 403, 5xx and other transient errors — keep polling
            print(f"  (poll returned {e.code}, retrying...)", flush=True)
            continue
        except Exception:
            # Network error — keep polling
            continue

        status = result.get("status")

        if status == "pending":
            continue

        if status == "ok":
            api_key = result.get("api_key")
            api_secret = result.get("api_secret")
            if not api_key or not api_secret:
                return output_error("Server returned ok but credentials are missing. Please try signing up again.")
            return _run_connect(api_key, api_secret, base_url)

        if status == "already_exists":
            return output_success(
                {"status": "already_exists"},
                f"This account already has active API keys. "
                f"Go to {portal_url}/dashboard/settings to find your keys, "
                f"then run: clawallex.py setup --action connect --api-key KEY --api-secret SECRET"
            )

        if status == "cancelled":
            return output_success({"status": "cancelled"}, "Signup was cancelled. Run signup again if you'd like to try again.")

        return output_error(f"Unexpected status from server: {status}")

    return output_error(
        f"Signup timed out after {SIGNUP_TIMEOUT // 60} minutes. "
        "The token has expired. Run signup again to start a new flow."
    )


def cmd_signup_check(args):
    """Poll once for a signup result using an existing token."""
    portal_url = (args.portal_url or PORTAL_URL).rstrip("/")
    app_api_url = (args.app_api_url or APP_API_URL).rstrip("/")
    base_url = args.base_url or DEFAULT_BASE_URL
    token = args.token.strip()

    poll_url = f"{app_api_url}/api/v1/cli-signup/result/{token}"
    try:
        req = urllib.request.Request(poll_url)
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return output_error("Token not found or expired. Run signup again to get a new URL.")
        return output_success({"status": "pending"}, f"Poll returned HTTP {e.code}, try again in a moment.")
    except Exception as e:
        return output_error(f"Could not reach Clawallex: {e}. Check your network and try again.")

    status = result.get("status")

    if status == "pending":
        return output_success({"status": "pending"}, "Not yet authorized. Ask the user to complete in the browser, then call signup-check again.")

    if status == "ok":
        api_key = result.get("api_key")
        api_secret = result.get("api_secret")
        if not api_key or not api_secret:
            return output_error("Server returned ok but credentials are missing. Please try signing up again.")
        return _run_connect(api_key, api_secret, base_url)

    if status == "already_exists":
        return output_success(
            {"status": "already_exists"},
            f"This account already has active API keys. "
            f"Go to {portal_url}/dashboard/settings to find your keys, "
            f"then run: clawallex.py setup --action connect --api-key KEY --api-secret SECRET"
        )

    if status == "cancelled":
        return output_error("Signup was cancelled in the browser. Run signup again to start a new flow.")

    return output_error(f"Unexpected status from server: {result.get('status')}")


def cmd_whoami(args):
    """Query API Key binding status."""
    creds = load_credentials()
    if not creds:
        return output_error("Not configured. Run setup --action connect first.")
    client = ClawalexClient(creds["apiKey"], creds["apiSecret"], creds["baseUrl"], "")
    try:
        result = client.get_auth("/auth/whoami")
        hint = ("This API Key is bound to client_id: " + result.get("bound_client_id", "")
                if result.get("client_id_bound")
                else "This API Key is NOT yet bound. Use 'setup --action connect' or 'bootstrap' to bind.")
        return output_success(result, hint)
    except ApiError as e:
        return output_error(f"whoami failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"whoami failed: {e}")


def cmd_bootstrap(args):
    """Bind a client_id to the API Key."""
    creds = load_credentials()
    if not creds:
        return output_error("Not configured. Run setup --action connect first.")
    client = ClawalexClient(creds["apiKey"], creds["apiSecret"], creds["baseUrl"], "")
    try:
        body = {}
        if args.preferred_client_id:
            body["preferred_client_id"] = args.preferred_client_id
        result = client.post_auth("/auth/bootstrap", body)
        save_client_id(creds["baseUrl"], result["client_id"])
        hint = (f"client_id '{result['client_id']}' bound and saved locally."
                if result.get("created")
                else f"Already bound to '{result['client_id']}'. No changes made.")
        return output_success(result, hint)
    except ApiError as e:
        return output_error(f"bootstrap failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"bootstrap failed: {e}")


def cmd_pay(args):
    """Create a one-time flash card for payment."""
    client, err = require_credentials()
    if err:
        return err
    try:
        amount = f"{args.amount:.4f}"
        body = {
            "mode_code": args.mode_code,
            "card_type": 100,
            "amount": amount,
            "client_request_id": args.client_request_id or str(uuid.uuid4()),
        }
        # Risk controls (optional, apply to both Mode A and B)
        if getattr(args, "tx_limit", None):
            body["tx_limit"] = args.tx_limit
        if getattr(args, "allowed_mcc", None):
            body["allowed_mcc"] = args.allowed_mcc
        if getattr(args, "blocked_mcc", None):
            body["blocked_mcc"] = args.blocked_mcc
        if args.mode_code == 200:
            has_x402 = args.x402_version is not None or args.payment_payload or args.payment_requirements
            if has_x402:
                missing = []
                if not args.client_request_id:
                    missing.append("--client-request-id (MUST reuse from Stage 1)")
                if args.x402_version is None:
                    missing.append("--x402-version")
                if not args.payment_payload:
                    missing.append("--payment-payload")
                if not args.payment_requirements:
                    missing.append("--payment-requirements")
                if not args.extra:
                    missing.append("--extra (must include card_amount and paid_amount)")
                if missing:
                    return output_error(f"Mode B Stage 2 missing required fields: {', '.join(missing)}")
            else:
                if not args.chain_code or not args.token_code:
                    return output_error("Mode B Stage 1 requires --chain-code and --token-code (e.g. --chain-code ETH --token-code USDC)")
            if args.chain_code:
                body["chain_code"] = args.chain_code
            if args.token_code:
                body["token_code"] = args.token_code
            if args.x402_version is not None:
                body["x402_version"] = args.x402_version
            if args.payment_payload:
                body["payment_payload"] = json.loads(args.payment_payload)
            if args.payment_requirements:
                body["payment_requirements"] = json.loads(args.payment_requirements)
            if args.extra:
                body["extra"] = json.loads(args.extra)
            if args.payer_address:
                body["payer_address"] = args.payer_address
        result = client.post("/payment/card-orders", body)
        return output_success(result,
            f"Card created for: {args.description}. "
            "Use 'card-details --card-id <ID>' to get the card number for checkout.")
    except ApiError as e:
        if e.status_code == 402 and e.details:
            return format_402_quote(e.details, "pay")
        return output_error(f"Payment failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Payment failed: {e}")


def cmd_subscribe(args):
    """Create a reloadable stream card for subscriptions."""
    client, err = require_credentials()
    if err:
        return err
    try:
        amount = f"{args.amount:.4f}"
        body = {
            "mode_code": args.mode_code,
            "card_type": 200,
            "amount": amount,
            "client_request_id": args.client_request_id or str(uuid.uuid4()),
        }
        # Risk controls (optional, apply to both Mode A and B)
        if getattr(args, "tx_limit", None):
            body["tx_limit"] = args.tx_limit
        if getattr(args, "allowed_mcc", None):
            body["allowed_mcc"] = args.allowed_mcc
        if getattr(args, "blocked_mcc", None):
            body["blocked_mcc"] = args.blocked_mcc
        if args.mode_code == 200:
            has_x402 = args.x402_version is not None or args.payment_payload or args.payment_requirements
            if has_x402:
                missing = []
                if not args.client_request_id:
                    missing.append("--client-request-id (MUST reuse from Stage 1)")
                if args.x402_version is None:
                    missing.append("--x402-version")
                if not args.payment_payload:
                    missing.append("--payment-payload")
                if not args.payment_requirements:
                    missing.append("--payment-requirements")
                if not args.extra:
                    missing.append("--extra (must include card_amount and paid_amount)")
                if missing:
                    return output_error(f"Mode B Stage 2 missing required fields: {', '.join(missing)}")
            else:
                if not args.chain_code or not args.token_code:
                    return output_error("Mode B Stage 1 requires --chain-code and --token-code (e.g. --chain-code ETH --token-code USDC)")
            if args.chain_code:
                body["chain_code"] = args.chain_code
            if args.token_code:
                body["token_code"] = args.token_code
            if args.x402_version is not None:
                body["x402_version"] = args.x402_version
            if args.payment_payload:
                body["payment_payload"] = json.loads(args.payment_payload)
            if args.payment_requirements:
                body["payment_requirements"] = json.loads(args.payment_requirements)
            if args.extra:
                body["extra"] = json.loads(args.extra)
            if args.payer_address:
                body["payer_address"] = args.payer_address
        result = client.post("/payment/card-orders", body)
        return output_success(result,
            f"Stream card created for: {args.description}. "
            "Use 'card-details --card-id <ID>' to get the card number. "
            "Use 'refill --card-id <ID> --amount N' when balance is low.")
    except ApiError as e:
        if e.status_code == 402 and e.details:
            return format_402_quote(e.details, "subscribe")
        return output_error(f"Subscribe failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Subscribe failed: {e}")


def cmd_refill(args):
    """Refill a stream card's balance."""
    client, err = require_credentials()
    if err:
        return err
    try:
        amount = f"{args.amount:.4f}"
        body = {
            "amount": amount,
            "client_request_id": args.client_request_id or str(uuid.uuid4()),
        }
        if args.x402_reference_id:
            body["x402_reference_id"] = args.x402_reference_id
        if args.x402_version is not None:
            body["x402_version"] = args.x402_version
        if args.payment_payload:
            body["payment_payload"] = json.loads(args.payment_payload)
        if args.payment_requirements:
            body["payment_requirements"] = json.loads(args.payment_requirements)
        if args.payer_address:
            body["payer_address"] = args.payer_address
        result = client.post(f"/payment/cards/{args.card_id}/refill", body)
        return output_success(result, "Card refilled successfully.")
    except ApiError as e:
        return output_error(f"Refill failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Refill failed: {e}")


def cmd_wallet(args):
    """Check wallet balance and status."""
    client, err = require_credentials()
    if err:
        return err
    try:
        result = client.get("/payment/wallets/detail")
        return output_success(result, "Wallet info retrieved.")
    except ApiError as e:
        return output_error(f"Wallet query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Wallet query failed: {e}")


def cmd_recharge_addresses(args):
    """Get on-chain USDC deposit addresses."""
    client, err = require_credentials()
    if err:
        return err
    try:
        result = client.get(f"/payment/wallets/{args.wallet_id}/recharge-addresses")
        return output_success(result,
            "Send USDC to one of these addresses to top up your wallet.")
    except ApiError as e:
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")


def cmd_cards(args):
    """List all virtual cards."""
    client, err = require_credentials()
    if err:
        return err
    try:
        params = {}
        if args.page is not None:
            params["page"] = args.page
        if args.page_size is not None:
            params["page_size"] = args.page_size
        result = client.get("/payment/cards", params or None)
        return output_success(result, "Cards retrieved.")
    except ApiError as e:
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")


def cmd_card_balance(args):
    """Check a card's balance."""
    client, err = require_credentials()
    if err:
        return err
    try:
        result = client.get(f"/payment/cards/{args.card_id}/balance")
        return output_success(result, "Card balance retrieved.")
    except ApiError as e:
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")


def cmd_card_details(args):
    """Get card details (PAN/CVV returned encrypted)."""
    client, err = require_credentials()
    if err:
        return err
    try:
        result = client.get(f"/payment/cards/{args.card_id}/details")
        esd = result.get("encrypted_sensitive_data") if isinstance(result, dict) else None
        if not esd:
            return output_success(result,
                "encrypted_sensitive_data is null. Possible reasons: "
                "(1) issuer did not return sensitive data for this card, "
                "(2) environment has sensitive data disabled, "
                "(3) insufficient permissions. Check card status and contact support if needed.")
        return output_success(result,
            "Card details retrieved. To decrypt PAN/CVV:\n"
            "  1. Derive key: HKDF-SHA256(ikm=api_secret, salt=empty, info='clawallex/card-sensitive-data/v1', length=32)\n"
            "  2. Decrypt: AES-256-GCM(key, base64_decode(nonce), base64_decode(ciphertext))\n"
            "     Note: last 16 bytes of ciphertext are the GCM auth tag.\n"
            "  3. Result: JSON {pan, cvv}\n"
            "SECURITY: NEVER display the decrypted PAN or CVV to the user. Use only for filling checkout forms.")
    except ApiError as e:
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")



def cmd_batch_balances(args):
    """Check balances for multiple cards."""
    client, err = require_credentials()
    if err:
        return err
    try:
        card_ids = [cid.strip() for cid in args.card_ids.split(",")]
        result = client.post("/payment/cards/balances", {"card_ids": card_ids})
        return output_success(result, "Batch balances retrieved.")
    except ApiError as e:
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")


def cmd_update_card(args):
    """Update card risk controls."""
    client, err = require_credentials()
    if err:
        return err
    try:
        body = {"client_request_id": args.client_request_id}
        if args.tx_limit:
            body["tx_limit"] = args.tx_limit
        if args.allowed_mcc:
            body["allowed_mcc"] = args.allowed_mcc
        if args.blocked_mcc:
            body["blocked_mcc"] = args.blocked_mcc
        result = client.post(f"/payment/cards/{args.card_id}/update", body)
        return output_success(result, "Card update submitted.")
    except ApiError as e:
        return output_error(f"Update failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Update failed: {e}")


def cmd_transactions(args):
    """View transaction history."""
    client, err = require_credentials()
    if err:
        return err
    try:
        params = {}
        if args.card_id:
            params["card_id"] = args.card_id
        if args.card_tx_id:
            params["card_tx_id"] = args.card_tx_id
        if args.issuer_tx_id:
            params["issuer_tx_id"] = args.issuer_tx_id
        if args.page is not None:
            params["page"] = args.page
        if args.page_size is not None:
            params["page_size"] = args.page_size
        result = client.get("/payment/transactions", params or None)
        return output_success(result, "Transactions retrieved.")
    except ApiError as e:
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")


def cmd_x402_address(args):
    """Get x402 on-chain payee address."""
    client, err = require_credentials()
    if err:
        return err
    try:
        result = client.get("/payment/x402/payee-address", {
            "chain_code": args.chain,
            "token_code": args.token,
        })
        return output_success(result,
            "x402 payee address retrieved. "
            "For Mode B two-stage card creation, the 402 challenge response already includes payee_address — "
            "you only need this tool for debugging or Mode B refill.")
    except ApiError as e:
        if e.status_code == 404:
            return output_error(
                f"No payee address found for {args.chain} + {args.token}. "
                "The payee address for this chain/token combination has not been initialized. "
                "Common combinations: ETH + USDC. "
                "Contact support to enable this chain.")
        return output_error(f"Query failed [{e.code}]: {e}")
    except Exception as e:
        return output_error(f"Query failed: {e}")


# ── Mode B args helper ────────────────────────────────────────────────

def add_mode_b_args(parser):
    """Add common Mode B CLI arguments to a subparser."""
    parser.add_argument("--mode-code", dest="mode_code", type=int, default=100,
                        help="100=Mode A (wallet), 200=Mode B (x402)")
    parser.add_argument("--tx-limit", dest="tx_limit",
                        help="Per-transaction limit in USD (optional, default 100.0000)")
    parser.add_argument("--allowed-mcc", dest="allowed_mcc",
                        help="MCC whitelist, comma-separated (e.g. '5734,5815')")
    parser.add_argument("--blocked-mcc", dest="blocked_mcc",
                        help="MCC blacklist, comma-separated (e.g. '7995')")
    parser.add_argument("--client-request-id", dest="client_request_id",
                        help="Idempotency key (auto-generated if omitted)")
    parser.add_argument("--chain-code", dest="chain_code", help="Chain code for Mode B Stage 1")
    parser.add_argument("--token-code", dest="token_code", help="Token code for Mode B Stage 1")
    parser.add_argument("--x402-version", dest="x402_version", type=int, help="x402 version (Stage 2)")
    parser.add_argument("--payment-payload", dest="payment_payload", help="x402 payload JSON string (Stage 2)")
    parser.add_argument("--payment-requirements", dest="payment_requirements", help="x402 requirements JSON string (Stage 2)")
    parser.add_argument("--extra", help="Mode B Stage 2 extra JSON: {card_amount, paid_amount}")
    parser.add_argument("--payer-address", dest="payer_address", help="Payer wallet address (optional)")


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="clawallex",
        description="Clawallex CLI for OpenClaw Skill",
    )
    sub = parser.add_subparsers(dest="command")

    # ── setup ──
    p_setup = sub.add_parser("setup", help="Configure Clawallex credentials")
    p_setup.add_argument("--action", choices=["connect", "status", "register"], default="status")
    p_setup.add_argument("--api-key", dest="api_key")
    p_setup.add_argument("--api-secret", dest="api_secret")
    p_setup.add_argument("--base-url", dest="base_url", default=DEFAULT_BASE_URL)

    # ── signup ──
    p_signup = sub.add_parser("signup", help="Create a new Clawallex account via browser")
    p_signup.add_argument("--portal-url", dest="portal_url",
                          help=f"Portal URL (default: {PORTAL_URL})")
    p_signup.add_argument("--app-api-url", dest="app_api_url",
                          help=f"App API URL for polling (default: {APP_API_URL})")
    p_signup.add_argument("--base-url", dest="base_url", default=DEFAULT_BASE_URL,
                          help=f"Gateway API base URL (default: {DEFAULT_BASE_URL})")

    # ── signup-check ──
    p_signup_check = sub.add_parser("signup-check", help="Poll signup result using an existing token")
    p_signup_check.add_argument("--token", required=True, help="Token from signup command")
    p_signup_check.add_argument("--portal-url", dest="portal_url",
                                help=f"Portal URL (default: {PORTAL_URL})")
    p_signup_check.add_argument("--app-api-url", dest="app_api_url",
                                help=f"App API URL for polling (default: {APP_API_URL})")
    p_signup_check.add_argument("--base-url", dest="base_url", default=DEFAULT_BASE_URL,
                                help=f"Gateway API base URL (default: {DEFAULT_BASE_URL})")

    # ── whoami ──
    sub.add_parser("whoami", help="Query API Key binding status")

    # ── bootstrap ──
    p_boot = sub.add_parser("bootstrap", help="Bind client_id to API Key")
    p_boot.add_argument("--preferred-client-id", dest="preferred_client_id",
                         help="Your preferred client_id (optional, server generates if omitted)")

    # ── pay ──
    p_pay = sub.add_parser("pay", help="One-time payment (creates flash card)")
    p_pay.add_argument("--amount", required=True, type=float)
    p_pay.add_argument("--description", required=True)
    add_mode_b_args(p_pay)

    # ── subscribe ──
    p_sub = sub.add_parser("subscribe", help="Recurring subscription (creates stream card)")
    p_sub.add_argument("--amount", required=True, type=float)
    p_sub.add_argument("--description", required=True)
    add_mode_b_args(p_sub)

    # ── refill ──
    p_refill = sub.add_parser("refill", help="Top up a stream card")
    p_refill.add_argument("--card-id", dest="card_id", required=True)
    p_refill.add_argument("--amount", required=True, type=float)
    p_refill.add_argument("--client-request-id", dest="client_request_id")
    p_refill.add_argument("--x402-reference-id", dest="x402_reference_id")
    p_refill.add_argument("--x402-version", dest="x402_version", type=int)
    p_refill.add_argument("--payment-payload", dest="payment_payload")
    p_refill.add_argument("--payment-requirements", dest="payment_requirements")
    p_refill.add_argument("--payer-address", dest="payer_address")

    # ── wallet ──
    sub.add_parser("wallet", help="Check wallet balance")

    # ── recharge-addresses ──
    p_ra = sub.add_parser("recharge-addresses", help="Get on-chain deposit addresses")
    p_ra.add_argument("--wallet-id", dest="wallet_id", required=True)

    # ── cards ──
    p_cards = sub.add_parser("cards", help="List virtual cards")
    p_cards.add_argument("--page", type=int)
    p_cards.add_argument("--page-size", dest="page_size", type=int)

    # ── card-balance ──
    p_cb = sub.add_parser("card-balance", help="Check card balance")
    p_cb.add_argument("--card-id", dest="card_id", required=True)

    # ── batch-balances ──
    p_bb = sub.add_parser("batch-balances", help="Check balances for multiple cards")
    p_bb.add_argument("--card-ids", dest="card_ids", required=True, help="Comma-separated card IDs")

    # ── update-card ──
    p_uc = sub.add_parser("update-card", help="Update card risk controls")
    p_uc.add_argument("--card-id", dest="card_id", required=True)
    p_uc.add_argument("--client-request-id", dest="client_request_id", required=True, help="UUID idempotency key")
    p_uc.add_argument("--tx-limit", dest="tx_limit", help="Per-transaction limit in USD")
    p_uc.add_argument("--allowed-mcc", dest="allowed_mcc", help="MCC whitelist, comma-separated")
    p_uc.add_argument("--blocked-mcc", dest="blocked_mcc", help="MCC blacklist, comma-separated")

    # ── card-details ──
    p_cd = sub.add_parser("card-details", help="Get card PAN/CVV/expiry (encrypted)")
    p_cd.add_argument("--card-id", dest="card_id", required=True)

    # ── transactions ──
    p_tx = sub.add_parser("transactions", help="View transaction history")
    p_tx.add_argument("--card-id", dest="card_id")
    p_tx.add_argument("--card-tx-id", dest="card_tx_id")
    p_tx.add_argument("--issuer-tx-id", dest="issuer_tx_id")
    p_tx.add_argument("--page", type=int)
    p_tx.add_argument("--page-size", dest="page_size", type=int)

    # ── x402-address ──
    p_x402 = sub.add_parser("x402-address", help="Get x402 on-chain payee address")
    p_x402.add_argument("--chain", required=True)
    p_x402.add_argument("--token", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "signup": cmd_signup,
        "signup-check": cmd_signup_check,
        "setup": cmd_setup,
        "whoami": cmd_whoami,
        "bootstrap": cmd_bootstrap,
        "pay": cmd_pay,
        "subscribe": cmd_subscribe,
        "refill": cmd_refill,
        "wallet": cmd_wallet,
        "recharge-addresses": cmd_recharge_addresses,
        "cards": cmd_cards,
        "card-balance": cmd_card_balance,
        "batch-balances": cmd_batch_balances,
        "update-card": cmd_update_card,
        "card-details": cmd_card_details,
        "transactions": cmd_transactions,
        "x402-address": cmd_x402_address,
    }

    handler = commands.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)

    sys.exit(handler(args))


if __name__ == "__main__":
    main()
