#!/usr/bin/env python3
"""
Jackal Memory client for AI agents.

Usage:
  python client.py keygen                 — show/generate AES encryption key
  python client.py walletgen              — generate Jackal wallet and register with API
  python client.py wallet                 — show current Jackal wallet address
  python client.py save <key> <content>
  python client.py load <key>
  python client.py usage                  — show storage quota usage
  python client.py list [prefix]          — list known saved keys from local manifest
  python client.py manifest-export [path] — export local key manifest JSON

Setup — two paths:
  A) Pre-provisioned (existing credentials):
       JACKAL_MEMORY_ENCRYPTION_KEY=<hex>
       JACKAL_MEMORY_WALLET_MNEMONIC=<24 words>
     save/load work without an API key.

  B) Fresh setup via Obsideo API:
       JACKAL_MEMORY_API_KEY=<key>
     Run: python client.py walletgen — generates wallet and provisions storage.
     After walletgen, same as path A.

Requires: pip install cryptography
"""

import base64
import hashlib
import hmac
import json
import os
import pathlib
import re
import struct
import subprocess
import sys
import urllib.error
import urllib.request

_WORDLIST_FILE = pathlib.Path(__file__).parent / "data" / "bip39_english.txt"

BASE_URL = "https://web-production-5cce7.up.railway.app"

_KEY_FILE      = pathlib.Path.home() / ".config" / "jackal-memory" / "key"
_WALLET_FILE   = pathlib.Path.home() / ".config" / "jackal-memory" / "jackal-mnemonic"
_MANIFEST_FILE = pathlib.Path.home() / ".config" / "jackal-memory" / "manifest.json"


def _write_secret_file(path: pathlib.Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value)
    os.chmod(path, 0o600)


# ── Encryption (mandatory) ────────────────────────────────────────────────────

def _encryption_key() -> bytes:
    key_hex = os.environ.get("JACKAL_MEMORY_ENCRYPTION_KEY", "").strip()
    if key_hex:
        return bytes.fromhex(key_hex)

    if _KEY_FILE.exists():
        return bytes.fromhex(_KEY_FILE.read_text().strip())

    key_hex = os.urandom(32).hex()
    _write_secret_file(_KEY_FILE, key_hex)
    print(
        "\n[jackal-memory] Generated a new encryption key and saved it to:\n"
        f"  {_KEY_FILE}\n\n"
        "Your memories are encrypted with this key. Back it up:\n"
        f"  export JACKAL_MEMORY_ENCRYPTION_KEY={key_hex}\n",
        file=sys.stderr,
    )
    return bytes.fromhex(key_hex)


def _encrypt(plaintext: str) -> str:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key   = _encryption_key()
    nonce = os.urandom(12)
    ct    = AESGCM(key).encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ct).decode()


def _decrypt(ciphertext_b64: str) -> str:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key  = _encryption_key()
    data = base64.b64decode(ciphertext_b64)
    nonce, ct = data[:12], data[12:]
    return AESGCM(key).decrypt(nonce, ct, None).decode()


def _load_manifest() -> dict:
    if not _MANIFEST_FILE.exists():
        return {"entries": {}}
    try:
        data = json.loads(_MANIFEST_FILE.read_text())
        if not isinstance(data, dict):
            return {"entries": {}}
        data.setdefault("entries", {})
        return data
    except Exception:
        return {"entries": {}}


def _save_manifest(manifest: dict) -> None:
    _MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    _MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def _manifest_upsert(key: str, cid: str, plaintext: str) -> None:
    from datetime import datetime, timezone
    m = _load_manifest()
    entries = m.setdefault("entries", {})
    entries[key] = {
        "cid": cid,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "bytes_plaintext": len(plaintext.encode("utf-8")),
    }
    _save_manifest(m)


# ── Jackal wallet (BIP39/BIP44 — no extra dependencies) ──────────────────────

_BIP39_WORDS = None  # lazy-loaded

def _load_wordlist() -> list:
    global _BIP39_WORDS
    if _BIP39_WORDS is None:
        try:
            _BIP39_WORDS = _WORDLIST_FILE.read_text().split()
        except Exception:
            print(f"[jackal-memory] Could not load local BIP39 wordlist at {_WORDLIST_FILE}.", file=sys.stderr)
            sys.exit(1)
        if len(_BIP39_WORDS) != 2048:
            print("[jackal-memory] Invalid BIP39 wordlist (expected 2048 words).", file=sys.stderr)
            sys.exit(1)
    return _BIP39_WORDS


def _generate_mnemonic() -> str:
    """Generate a 24-word BIP39 mnemonic from 256 bits of entropy."""
    words = _load_wordlist()
    entropy = os.urandom(32)  # 256 bits
    # Checksum: first (256/32)=8 bits of SHA256(entropy)
    h = hashlib.sha256(entropy).digest()
    bits = bin(int.from_bytes(entropy, 'big'))[2:].zfill(256) + bin(h[0])[2:].zfill(8)
    return ' '.join(words[int(bits[i*11:(i+1)*11], 2)] for i in range(24))


def _mnemonic_to_seed(mnemonic: str) -> bytes:
    """BIP39: mnemonic → 64-byte seed via PBKDF2-HMAC-SHA512."""
    return hashlib.pbkdf2_hmac(
        'sha512',
        mnemonic.encode('utf-8'),
        b'mnemonic',
        2048,
    )


_SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def _bip32_derive(seed: bytes, path: str) -> bytes:
    """Derive a private key from seed using BIP32/BIP44 path (e.g. m/44'/118'/0'/0/0)."""
    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    key, chain = I[:32], I[32:]

    for part in path.lstrip('m/').split('/'):
        hardened = part.endswith("'")
        index = int(part.rstrip("'")) + (0x80000000 if hardened else 0)
        if hardened:
            data = b'\x00' + key + struct.pack('>I', index)
        else:
            data = _privkey_to_pubkey(key) + struct.pack('>I', index)
        I = hmac.new(chain, data, hashlib.sha512).digest()
        il = int.from_bytes(I[:32], 'big')
        key_int = (il + int.from_bytes(key, 'big')) % _SECP256K1_ORDER
        key = key_int.to_bytes(32, 'big')
        chain = I[32:]

    return key


def _privkey_to_pubkey(privkey: bytes) -> bytes:
    """secp256k1 compressed public key from private key."""
    from cryptography.hazmat.primitives.asymmetric.ec import (
        SECP256K1, derive_private_key, EllipticCurvePublicKey,
    )
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    priv = derive_private_key(int.from_bytes(privkey, 'big'), SECP256K1())
    return priv.public_key().public_bytes(Encoding.X962, PublicFormat.CompressedPoint)


def _pubkey_to_address(pubkey: bytes, hrp: str) -> str:
    """Cosmos address: RIPEMD160(SHA256(pubkey)) → bech32(hrp)."""
    sha = hashlib.sha256(pubkey).digest()
    try:
        rip = hashlib.new('ripemd160', sha).digest()
    except ValueError:
        # OpenSSL 3.0+ may disable RIPEMD160 — use cryptography library fallback
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.hashes import Hash
        h = Hash(hashes.RIPEMD160())
        h.update(sha)
        rip = h.finalize()
    return _bech32_encode(hrp, rip)


def _bech32_encode(hrp: str, data: bytes) -> str:
    """Standard bech32 encoding (Cosmos compatible)."""
    CHARSET = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]

    def polymod(values):
        chk = 1
        for v in values:
            b = chk >> 25
            chk = (chk & 0x1ffffff) << 5 ^ v
            for i in range(5):
                chk ^= GEN[i] if (b >> i) & 1 else 0
        return chk

    def hrp_expand(s):
        return [ord(x) >> 5 for x in s] + [0] + [ord(x) & 31 for x in s]

    def convertbits(data, frombits, tobits):
        acc = bits = 0
        ret = []
        maxv = (1 << tobits) - 1
        for v in data:
            acc = ((acc << frombits) | v) & 0xffffffff
            bits += frombits
            while bits >= tobits:
                bits -= tobits
                ret.append((acc >> bits) & maxv)
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
        return ret

    data5 = convertbits(data, 8, 5)
    chk = polymod(hrp_expand(hrp) + data5 + [0] * 6) ^ 1
    checksum = [(chk >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + '1' + ''.join(CHARSET[d] for d in data5 + checksum)


def _jackal_mnemonic() -> str | None:
    """Return the stored Jackal wallet mnemonic, or None if not set up yet."""
    env = os.environ.get("JACKAL_MEMORY_WALLET_MNEMONIC", "").strip()
    if env:
        return env
    if _WALLET_FILE.exists():
        return _WALLET_FILE.read_text().strip()
    return None


def _mnemonic_to_jackal_address(mnemonic: str) -> str:
    """Derive jkl1... address from BIP39 mnemonic via m/44'/118'/0'/0/0."""
    seed    = _mnemonic_to_seed(mnemonic)
    privkey = _bip32_derive(seed, "m/44'/118'/0'/0/0")
    pubkey  = _privkey_to_pubkey(privkey)
    return _pubkey_to_address(pubkey, "jkl")


# ── API ───────────────────────────────────────────────────────────────────────

def _api_key() -> str:
    key = os.environ.get("JACKAL_MEMORY_API_KEY", "")
    if not key:
        print("Error: JACKAL_MEMORY_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def _request(method: str, path: str, body: dict | None = None) -> dict:
    url  = BASE_URL + path
    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error = json.loads(e.read())
        print(f"Error {e.code}: {error.get('detail', e.reason)}", file=sys.stderr)
        sys.exit(1)


def _ensure_wallet_registered() -> None:
    """
    On first save: generate a Jackal wallet if none exists, then register
    the jkl1... address with the API (only if API key is available).

    Two paths:
      A) Mnemonic already set (pre-provisioned) — skip API registration entirely.
      B) No mnemonic + API key present — generate wallet and register for provisioning.
      C) No mnemonic + no API key — error with helpful message.
    """
    mnemonic = _jackal_mnemonic()
    api_key  = os.environ.get("JACKAL_MEMORY_API_KEY", "").strip()

    if mnemonic is None:
        if not api_key:
            print(
                "[jackal-memory] No Jackal wallet found.\n"
                "  To use existing credentials: set JACKAL_MEMORY_WALLET_MNEMONIC\n"
                "  To set up fresh:             set JACKAL_MEMORY_API_KEY and run: python client.py walletgen",
                file=sys.stderr,
            )
            sys.exit(1)
        # Fresh setup — generate wallet and provision via API
        mnemonic = _generate_mnemonic()
        _write_secret_file(_WALLET_FILE, mnemonic)
        address = _mnemonic_to_jackal_address(mnemonic)
        print(
            "\n[jackal-memory] Generated your Jackal wallet and saved the mnemonic to:\n"
            f"  {_WALLET_FILE}\n\n"
            f"  Jackal address: {address}\n\n"
            "  This wallet will own your storage on-chain. Back up the mnemonic:\n"
            f"  python client.py wallet\n",
            file=sys.stderr,
        )
    else:
        address = _mnemonic_to_jackal_address(mnemonic)

    # Register with API only if key is available (not required for pre-provisioned wallets)
    if api_key:
        try:
            _request("POST", "/register-wallet", {"jackal_address": address})
        except SystemExit:
            pass  # Registration failure is non-fatal


# ── Jackal client subprocess ──────────────────────────────────────────────────

_SKILL_DIR     = pathlib.Path(__file__).parent
_JACKAL_CLIENT = _SKILL_DIR / "jackal-client.js"
_NODE_MODULES  = _SKILL_DIR / "node_modules"


def _parse_node_result(stdout: str) -> dict:
    """
    Parse the JSON result line from jackal-client.js stdout.

    The subprocess writes exactly one JSON line (starting with '{') to stdout.
    If the SDK emits unexpected content before it, scan for the last '{' line.
    """
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith('{'):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                pass
    raise ValueError(f"No JSON result found in subprocess output:\n{stdout}")


def _ensure_jackal_client() -> None:
    """Install node_modules next to jackal-client.js on first use."""
    if not _JACKAL_CLIENT.exists():
        print("[jackal-memory] jackal-client.js not found — skill installation may be incomplete.",
              file=sys.stderr)
        sys.exit(1)
    if not _NODE_MODULES.exists():
        print("[jackal-memory] Installing Jackal dependencies (first run — takes ~30s)...",
              file=sys.stderr)
        r = subprocess.run(
            ["npm", "install", "--prefix", str(_SKILL_DIR)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"[jackal-memory] npm install failed:\n{r.stderr}", file=sys.stderr)
            sys.exit(1)
        print("[jackal-memory] Dependencies installed.", file=sys.stderr)


def _jackal_upload(key: str, data_b64: str) -> str:
    """Upload base64-encoded ciphertext to the user's own Jackal VFS. Returns CID."""
    mnemonic = _jackal_mnemonic()
    if not mnemonic:
        print("[jackal-memory] No Jackal wallet found. Run: python client.py walletgen",
              file=sys.stderr)
        sys.exit(1)
    address = _mnemonic_to_jackal_address(mnemonic)
    env = {**os.environ, "JACKAL_MNEMONIC": mnemonic, "JACKAL_ADDRESS": address}

    r = subprocess.run(
        ["node", str(_JACKAL_CLIENT), "upload", key],
        input=data_b64, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env,
    )
    if r.returncode != 0:
        print(r.stderr, end="", file=sys.stderr)
        print("[jackal-memory] Upload failed.", file=sys.stderr)
        sys.exit(1)

    try:
        resp = _parse_node_result(r.stdout)
    except ValueError as e:
        print(f"[jackal-memory] {e}", file=sys.stderr)
        sys.exit(1)

    if not resp.get("ok"):
        print(f"[jackal-memory] Upload failed: {resp.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    return resp["cid"]


def _jackal_download(key: str) -> str:
    """Download ciphertext from the user's own Jackal VFS. Returns base64 ciphertext."""
    mnemonic = _jackal_mnemonic()
    if not mnemonic:
        print("[jackal-memory] No Jackal wallet found.", file=sys.stderr)
        sys.exit(1)
    address = _mnemonic_to_jackal_address(mnemonic)

    # CID is deterministic — mirrors the sanitisation in jackal-client.js
    safe_key = re.sub(r'[^a-zA-Z0-9._-]', '_', key)
    cid = f"Home/jackal-memory/{safe_key}"

    env = {**os.environ, "JACKAL_MNEMONIC": mnemonic, "JACKAL_ADDRESS": address}

    r = subprocess.run(
        ["node", str(_JACKAL_CLIENT), "download", cid],
        text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env,
    )
    if r.returncode != 0:
        print(r.stderr, end="", file=sys.stderr)
        print("[jackal-memory] Download failed.", file=sys.stderr)
        sys.exit(1)

    try:
        resp = _parse_node_result(r.stdout)
    except ValueError as e:
        print(f"[jackal-memory] {e}", file=sys.stderr)
        sys.exit(1)

    if not resp.get("ok"):
        print(f"[jackal-memory] Download failed: {resp.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    return resp["data_b64"]


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_keygen() -> None:
    key = _encryption_key()
    key_hex = key.hex()
    print(f"\nActive encryption key:\n\n  {key_hex}\n")
    print("Set this in your environment to use the same key on other machines:")
    print(f"  export JACKAL_MEMORY_ENCRYPTION_KEY={key_hex}\n")
    print("Keep this key safe — lose it and your encrypted memories are unrecoverable.")


def cmd_walletgen() -> None:
    """Generate a Jackal wallet, save the mnemonic locally, and register with the API."""
    existing = _jackal_mnemonic()
    if existing:
        address = _mnemonic_to_jackal_address(existing)
        print(f"\nJackal wallet already exists.")
        print(f"  Address:  {address}")
        print(f"  Mnemonic: {existing}")
        print(f"\nTo regenerate, delete {_WALLET_FILE} first.")
        return

    mnemonic = _generate_mnemonic()
    _write_secret_file(_WALLET_FILE, mnemonic)
    address = _mnemonic_to_jackal_address(mnemonic)

    print(f"\nJackal wallet generated.")
    print(f"  Address:  {address}")
    print(f"  Mnemonic: {mnemonic}")
    print(f"\nSaved to: {_WALLET_FILE}")
    print("\nRegistering with API...")

    try:
        _request("POST", "/register-wallet", {"jackal_address": address})
        print("Registered. Your storage will be provisioned under this address on first save.")
    except SystemExit:
        print("Registration failed — check your API key.", file=sys.stderr)


def cmd_wallet() -> None:
    """Show the current Jackal wallet address. Use --show-mnemonic to reveal the mnemonic."""
    mnemonic = _jackal_mnemonic()
    if not mnemonic:
        print("No Jackal wallet found. Run: python client.py walletgen")
        return
    address = _mnemonic_to_jackal_address(mnemonic)
    show = "--show-mnemonic" in sys.argv
    print(f"\nJackal address: {address}")
    if show:
        print(f"Mnemonic:       {mnemonic}")
        print(f"\n  export JACKAL_MEMORY_WALLET_MNEMONIC=\"{mnemonic}\"")
    else:
        print(f"\nMnemonic: [hidden — run: python client.py wallet --show-mnemonic]")
    print(f"\nBack up the mnemonic — it controls your on-chain storage.")


def cmd_save(key: str, content: str) -> None:
    _ensure_jackal_client()
    _ensure_wallet_registered()  # server provisions storage under user's own address
    cid = _jackal_upload(key, _encrypt(content))
    _manifest_upsert(key, cid, content)
    print(f"Saved — key: {key}  cid: {cid}")


def cmd_load(key: str) -> None:
    _ensure_jackal_client()
    print(_decrypt(_jackal_download(key)))


def cmd_usage() -> None:
    data     = _request("GET", "/usage")
    used_mb  = data["bytes_used"] / 1024 ** 2
    quota_mb = data["quota_bytes"] / 1024 ** 2
    pct      = data["percent_used"] * 100
    print(f"Storage: {used_mb:.1f} MB / {quota_mb:.0f} MB ({pct:.1f}% used)")


def cmd_list(prefix: str | None = None) -> None:
    m = _load_manifest()
    entries = m.get("entries", {})
    keys = sorted(entries.keys())
    if prefix:
        keys = [k for k in keys if k.startswith(prefix)]
    if not keys:
        print("No matching keys in local manifest.")
        print(f"Manifest: {_MANIFEST_FILE}")
        return
    print(f"Known keys ({len(keys)}):")
    for k in keys:
        meta = entries.get(k, {})
        print(f"- {k}  ({meta.get('updated_at', 'unknown')})")


def cmd_manifest_export(out_path: str | None = None) -> None:
    m = _load_manifest()
    if out_path:
        p = pathlib.Path(out_path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(m, indent=2, sort_keys=True))
        print(f"Exported manifest to: {p}")
    else:
        print(json.dumps(m, indent=2, sort_keys=True))


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "keygen" and len(args) == 1:
        cmd_keygen()
    elif cmd == "walletgen" and len(args) == 1:
        cmd_walletgen()
    elif cmd == "wallet" and len(args) in (1, 2) and (len(args) == 1 or args[1] == "--show-mnemonic"):
        cmd_wallet()
    elif cmd == "save" and len(args) == 3:
        cmd_save(args[1], args[2])
    elif cmd == "load" and len(args) == 2:
        cmd_load(args[1])
    elif cmd == "usage" and len(args) == 1:
        cmd_usage()
    elif cmd == "list" and len(args) in (1, 2):
        cmd_list(args[1] if len(args) == 2 else None)
    elif cmd == "manifest-export" and len(args) in (1, 2):
        cmd_manifest_export(args[1] if len(args) == 2 else None)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
