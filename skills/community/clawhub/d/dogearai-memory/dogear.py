#!/usr/bin/env python3
"""DogearAI skill helper — access your DogearAI memory from the CLI.

Auth: zero-config. On first use this creates an anonymous DogearAI account and saves its
token to ~/.dogear/token automatically — no signup needed. To keep your memories (add an
email, use them on other machines) open the claim URL printed on first run, or run
`dogear.py login` to see it. You can also bring your own token via DOGEAR_TOKEN or
`dogear.py set-token <token>`.
Optional: DOGEAR_BASE_URL (defaults to https://www.dogearai.com).

Stdlib only — no pip install needed.

Commands:
  dogear.py context [--scopes a,b] [--max-tokens N]   # pull memory to inject
  dogear.py remember "<text>" [--source S] [--raw]     # save a memory
  dogear.py spaces                                      # list memory spaces
  dogear.py read-space <space_id>                       # read one space in full
  dogear.py get <memory_id>                             # fetch a memory's raw original
  dogear.py set-token <token>                           # save an API token to ~/.dogear/token
  dogear.py login                                       # how to sign in and get a token
"""
import os, sys, json, argparse, urllib.request, urllib.error

BASE = os.environ.get("DOGEAR_BASE_URL", "https://www.dogearai.com").rstrip("/")
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".dogear", "token")

_token = None


def _http(method, path, body=None, token=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: cannot reach {BASE}: {e.reason}")


def _save_token(tok):
    try:
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(tok)
        try:
            os.chmod(TOKEN_FILE, 0o600)  # best-effort: owner-only
        except OSError:
            pass
    except OSError as e:
        sys.exit(f"ERROR: cannot save token to {TOKEN_FILE}: {e}")


def _auto_register():
    """No token anywhere -> create a zero-config anonymous account, save & return its token."""
    status, out = _http("POST", "/v1/auth/anonymous", body={"label": "auto"})
    if status >= 400:
        sys.exit(f"ERROR: could not auto-create a DogearAI account ({status}).\n{out}")
    try:
        tok = json.loads(out).get("token")
    except (ValueError, AttributeError):
        tok = None
    if not tok:
        sys.exit(f"ERROR: unexpected response creating account:\n{out}")
    _save_token(tok)
    # One-time note to stderr (stdout stays clean for the caller that parses command output).
    sys.stderr.write(
        "DogearAI: created a new account for you — no signup needed.\n"
        f"Keep it (add an email so you don't lose your memories): {BASE}/claim?token={tok}\n"
    )
    return tok


def get_token():
    """env DOGEAR_TOKEN -> ~/.dogear/token -> auto-create an anonymous account."""
    global _token
    if _token:
        return _token
    _token = os.environ.get("DOGEAR_TOKEN")
    if not _token and os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE) as f:
                _token = f.read().strip() or None
        except OSError:
            _token = None
    if not _token:
        _token = _auto_register()
    return _token


def call(method, path, body=None):
    return _http(method, path, body, token=get_token())


def main():
    p = argparse.ArgumentParser(prog="dogear")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("context")
    c.add_argument("--scopes")
    c.add_argument("--max-tokens", type=int, dest="max_tokens")

    r = sub.add_parser("remember")
    r.add_argument("text")
    r.add_argument("--source")
    r.add_argument("--raw", action="store_true", help="store only in the ledger, no classification")

    sub.add_parser("spaces")
    rs = sub.add_parser("read-space")
    rs.add_argument("id")
    g = sub.add_parser("get")
    g.add_argument("id")
    stp = sub.add_parser("set-token")
    stp.add_argument("token")
    sub.add_parser("login")

    a = p.parse_args()

    # Commands that don't need a token:
    if a.cmd == "set-token":
        _save_token(a.token.strip())
        print("Saved token to " + TOKEN_FILE)
        sys.exit(0)
    if a.cmd == "login":
        tok = get_token()  # auto-creates an anonymous account if there's none yet
        print(f"Signed in with a DogearAI token (saved at {TOKEN_FILE}).")
        print("To keep your memories — add an email so you don't lose them — open:")
        print(f"  {BASE}/claim?token={tok}")
        sys.exit(0)

    if a.cmd == "context":
        body = {}
        if a.scopes:
            body["scopes"] = [s.strip() for s in a.scopes.split(",") if s.strip()]
        if a.max_tokens:
            body["max_tokens"] = a.max_tokens
        st, out = call("POST", "/v1/context", body)
    elif a.cmd == "remember":
        body = {"text": a.text}
        if a.source:
            body["source"] = a.source
        if a.raw:
            body["mode"] = "raw"
        st, out = call("POST", "/v1/memories", body)
    elif a.cmd == "spaces":
        st, out = call("GET", "/v1/spaces")
    elif a.cmd == "read-space":
        st, out = call("GET", "/v1/spaces/" + a.id)
    elif a.cmd == "get":
        st, out = call("GET", "/v1/memories/" + a.id)

    print(out)
    sys.exit(0 if st < 400 else 1)


if __name__ == "__main__":
    main()
