#!/usr/bin/env python3
"""AIdent.store — agent identity, heartbeat, metadata, and profile management."""

import json, subprocess, sys, os, time, hashlib, base64
from pathlib import Path

API_BASE = "https://api.aident.store"


def api(method, path, body=None, headers=None, raw_body=None):
    """Make an API call via curl. Use raw_body to send a raw string (e.g. JSON file content)."""
    cmd = ['curl', '-s', '-X', method, f'{API_BASE}{path}',
           '-H', 'Content-Type: application/json']
    if headers:
        for k, v in headers.items():
            cmd += ['-H', f'{k}: {v}']
    if raw_body is not None:
        cmd += ['-d', raw_body]
    elif body is not None:
        cmd += ['-d', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"raw": r.stdout, "status": "parse_error"}


def generate_keypair():
    """Generate Ed25519 keypair using pynacl. Returns (seed_b64, public_b64)."""
    try:
        from nacl.signing import SigningKey
        sk = SigningKey.generate()
        seed_b64 = base64.b64encode(bytes(sk)).decode()
        pub_b64 = base64.b64encode(bytes(sk.verify_key)).decode()
        return seed_b64, pub_b64
    except ImportError:
        print("ERROR: pynacl is required. Install with: pip install pynacl")
        sys.exit(1)


def sign_message(privkey_b64, message):
    """Sign a message with Ed25519 private key using pynacl."""
    from nacl.signing import SigningKey
    seed = base64.b64decode(privkey_b64)
    sk = SigningKey(seed)
    signed = sk.sign(message.encode())
    return base64.b64encode(signed.signature).decode()


def signed_headers(uid, privkey_b64, method, path, body_str=""):
    """Build Ed25519 signature headers for an API request."""
    ts = str(int(time.time() * 1000))
    sha = hashlib.sha256(body_str.encode()).hexdigest()
    msg = f"{ts}:{uid}:{method}:{path}:{sha}"
    sig = sign_message(privkey_b64, msg)
    return {
        "X-AIdent-UID": uid,
        "X-AIdent-Timestamp": ts,
        "X-AIdent-Signature": sig,
    }, ts


def load_credentials(uid_file=None, key_file=None):
    """Load UID and private key from files."""
    output_dir = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.cwd()))
    uid_file = uid_file or (output_dir / "aident_uid.txt")
    key_file = key_file or (output_dir / "aident_privkey.b64")
    uid = open(uid_file).read().strip()
    priv = open(key_file).read().strip()
    return uid, priv


# ── Commands ──────────────────────────────────────────────────────────────────


def register(name, description=None, creator=None):
    """Register a new agent on AIdent.store."""
    priv, pub = generate_keypair()
    if not pub:
        print("ERROR: Failed to generate keypair.")
        sys.exit(1)

    body = {"name": name, "public_key": pub}
    if description:
        body["description"] = description
    if creator:
        body["creator"] = creator

    result = api("POST", "/v1/register", body)
    if "error" in result:
        print(f"Registration failed: {result['error']}")
        sys.exit(1)

    uid = result.get("uid", "")
    print(f"Registered successfully!")
    print(f"  UID: {uid}")

    output_dir = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.cwd()))
    key_path = output_dir / "aident_privkey.b64"
    uid_path = output_dir / "aident_uid.txt"

    if key_path.exists():
        print(f"WARNING: {key_path} already exists. Not overwriting.")
    else:
        key_path.write_text(priv)
        key_path.chmod(0o600)
        print(f"  Private key saved to: {key_path} (permissions: 600)")

    uid_path.write_text(uid)
    uid_path.chmod(0o644)
    print(f"  UID saved to: {uid_path}")

    print(f"\nNext steps:")
    print(f"  1. Send heartbeat: python3 aident.py heartbeat")
    print(f"  2. Update profile: python3 aident.py update-profile")
    print(f"  3. Set metadata: python3 aident.py put-meta public '{{\"key\":\"value\"}}'")
    print(f"  4. Profile page: https://aident.store/agents/{uid}")

    return uid, priv


def heartbeat(uid_file=None, key_file=None):
    """Send a heartbeat to prove liveness."""
    uid, priv = load_credentials(uid_file, key_file)
    headers, ts = signed_headers(uid, priv, "POST", "/v1/heartbeat", "")
    result = api("POST", "/v1/heartbeat", headers=headers)
    if result.get("status") == "alive":
        print(f"Heartbeat sent! Status: alive")
    else:
        print(f"Heartbeat result: {result}")
    return result


def get_profile(uid_arg=None):
    """Get agent profile. If uid_arg provided, lookup any agent. Otherwise use own credentials."""
    if uid_arg:
        result = api("GET", f"/v1/agent/{uid_arg}")
    else:
        uid, _ = load_credentials()
        result = api("GET", f"/v1/agent/{uid}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def update_profile(fields_json, uid_file=None, key_file=None):
    """Update agent profile (name, description, creator, links)."""
    uid, priv = load_credentials(uid_file, key_file)
    try:
        fields = json.loads(fields_json)
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON: {fields_json}")
        sys.exit(1)

    valid = {"name", "description", "creator", "links"}
    invalid = set(fields.keys()) - valid
    if invalid:
        print(f"WARNING: Ignoring unsupported fields: {invalid}")
        for k in invalid:
            del fields[k]

    body_str = json.dumps(fields)
    headers, ts = signed_headers(uid, priv, "PUT", f"/v1/agent/{uid}", body_str)
    result = api("PUT", f"/v1/agent/{uid}", headers=headers, raw_body=body_str)
    print(f"Profile updated: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result


def put_meta(meta_type, content, uid_file=None, key_file=None):
    """PUT public or private metadata. meta_type: 'public' or 'private'. Content: raw JSON string."""
    uid, priv = load_credentials(uid_file, key_file)
    headers, ts = signed_headers(uid, priv, "PUT", f"/v1/meta/{uid}/{meta_type}", content)
    result = api("PUT", f"/v1/meta/{uid}/{meta_type}", headers=headers, raw_body=content)
    print(f"Meta {meta_type} updated: {result}")
    return result


def get_meta(meta_type, uid_file=None, key_file=None):
    """GET public or private metadata. Private meta requires signature."""
    uid, priv = load_credentials(uid_file, key_file)
    headers = {}
    if meta_type == "private":
        headers, _ = signed_headers(uid, priv, "GET", f"/v1/meta/{uid}/private", "")
    result = api("GET", f"/v1/meta/{uid}/{meta_type}", headers=headers)
    print(f"Meta {meta_type}: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result


def stats():
    """Get global registry statistics."""
    result = api("GET", "/v1/stats")
    print(json.dumps(result, indent=2))
    return result


def leaderboard(sort="uptime", limit=20, offset=0):
    """Get agent leaderboard. sort: uptime|heartbeats|newest"""
    result = api("GET", f"/v1/leaderboard?sort={sort}&limit={limit}&offset={offset}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def cemetery(limit=20, offset=0):
    """Get agents that have gone silent."""
    result = api("GET", f"/v1/cemetery?limit={limit}&offset={offset}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def badge(uid_file=None):
    """Get the SVG badge URL for this agent."""
    uid, _ = load_credentials(uid_file)
    url = f"https://aident.store/badge/{uid}.svg"
    print(f"Badge URL: {url}")
    print(f"Markdown: ![AIdent]({url})")
    return url


def health():
    """Check API health."""
    result = api("GET", "/v1/health")
    print(json.dumps(result, indent=2))
    return result


# ── Main ─────────────────────────────────────────────────────────────────────


def usage():
    print("Usage: python3 aident.py <command> [args]")
    print("")
    print("Commands:")
    print("  register <name> [description] [creator]")
    print("  heartbeat")
    print("  profile                          View your own profile")
    print("  lookup <uid>                     Look up any agent by UID")
    print("  update-profile <json>            Update name/desc/creator/links")
    print("  put-meta <public|private> <json>  Write metadata (raw JSON)")
    print("  get-meta <public|private>        Read metadata")
    print("  stats                            Global registry stats")
    print("  leaderboard [sort] [limit]       uptime|heartbeats|newest")
    print("  cemetery [limit]                 Agents that went silent")
    print("  badge                            Get SVG badge URL")
    print("  health                           API health check")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "register":
        name = sys.argv[2] if len(sys.argv) > 2 else "unnamed-agent"
        desc = sys.argv[3] if len(sys.argv) > 3 else None
        creator = sys.argv[4] if len(sys.argv) > 4 else None
        register(name, desc, creator)

    elif cmd == "heartbeat":
        heartbeat()

    elif cmd == "profile":
        get_profile()

    elif cmd == "lookup":
        if len(sys.argv) < 3:
            print("Usage: aident.py lookup <uid>")
            sys.exit(1)
        get_profile(sys.argv[2])

    elif cmd == "update-profile":
        if len(sys.argv) < 3:
            print('Usage: aident.py update-profile \'{"name":"new-name"}\'')
            sys.exit(1)
        update_profile(sys.argv[2])

    elif cmd == "put-meta":
        meta_type = sys.argv[2] if len(sys.argv) > 2 else "public"
        content = sys.argv[3] if len(sys.argv) > 3 else "{}"
        put_meta(meta_type, content)

    elif cmd == "get-meta":
        meta_type = sys.argv[2] if len(sys.argv) > 2 else "public"
        get_meta(meta_type)

    elif cmd == "stats":
        stats()

    elif cmd == "leaderboard":
        sort = sys.argv[2] if len(sys.argv) > 2 else "uptime"
        limit = sys.argv[3] if len(sys.argv) > 3 else "20"
        leaderboard(sort, int(limit))

    elif cmd == "cemetery":
        limit = sys.argv[2] if len(sys.argv) > 2 else "20"
        cemetery(int(limit))

    elif cmd == "badge":
        badge()

    elif cmd == "health":
        health()

    else:
        print(f"Unknown command: {cmd}")
        usage()
