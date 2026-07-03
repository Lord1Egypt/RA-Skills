"""
🛠️ axiom-jwt-inspector — JWT Decoder & Inspector
==================================================

⚠️ LIMITATIONS CONNUES :
- Vérif signature HS256/HS384/HS512 seulement (pas RS256/ES256)
- Pas de validation `aud`, `iss`, `nbf`, `exp` (parsing only)
- Pas de support JWE (encrypted JWT)

DÉCODE ET INSPECTE LES JSON WEB TOKENS
"""

import base64
import hashlib
import hmac
import json
import re
import sys
import time


def _b64url_decode(s: str) -> bytes:
    """Base64url decode with padding."""
    s = s.replace("-", "+").replace("_", "/")
    # Add padding
    s += "=" * (-len(s) % 4)
    return base64.b64decode(s)


def _b64url_encode(b: bytes) -> str:
    """Base64url encode without padding."""
    return base64.b64encode(b).decode("ascii").rstrip("=").replace("+", "-").replace("/", "_")


def decode(jwt_token: str) -> dict:
    """
    Decode a JWT (header + payload). Does NOT verify signature.

    Returns dict with: header, payload, signature, valid_format, errors
    """
    if not isinstance(jwt_token, str):
        return {"valid_format": False, "error": "JWT must be a string"}

    parts = jwt_token.strip().split(".")
    if len(parts) != 3:
        return {
            "valid_format": False,
            "error": f"JWT must have 3 parts separated by '.', got {len(parts)}",
            "original": jwt_token,
        }

    header_b64, payload_b64, signature_b64 = parts

    try:
        header_bytes = _b64url_decode(header_b64)
        header = json.loads(header_bytes)
    except Exception as e:
        return {"valid_format": False, "error": f"Invalid header: {e}", "original": jwt_token}

    try:
        payload_bytes = _b64url_decode(payload_b64)
        payload = json.loads(payload_bytes)
    except Exception as e:
        return {"valid_format": False, "error": f"Invalid payload: {e}", "original": jwt_token}

    # Signature info
    try:
        signature = _b64url_decode(signature_b64)
        signature_hex = signature.hex()
    except Exception as e:
        signature = None
        signature_hex = f"<error: {e}>"

    # Check exp
    exp_info = None
    if "exp" in payload:
        exp = payload["exp"]
        now = int(time.time())
        exp_info = {
            "exp": exp,
            "now": now,
            "expired": now > exp,
            "seconds_until_expiry": exp - now,
        }

    return {
        "valid_format": True,
        "header": header,
        "payload": payload,
        "signature": signature_hex,
        "signature_algorithm": header.get("alg"),
        "token_type": header.get("typ"),
        "exp_info": exp_info,
        "raw_header_b64": header_b64,
        "raw_payload_b64": payload_b64,
        "raw_signature_b64": signature_b64,
    }


def verify_hmac(jwt_token: str, secret: str) -> dict:
    """
    Verify HMAC signature (HS256, HS384, HS512).

    Returns dict with: signature_valid, algorithm_used
    """
    decoded = decode(jwt_token)
    if not decoded.get("valid_format"):
        return {"signature_valid": False, "error": decoded.get("error")}

    alg = decoded["header"].get("alg", "")
    if alg not in ("HS256", "HS384", "HS512"):
        return {
            "signature_valid": False,
            "error": f"Algorithm {alg} not supported (HS256/384/512 only)",
        }

    # Map alg → hash function
    hash_funcs = {"HS256": hashlib.sha256, "HS384": hashlib.sha384, "HS512": hashlib.sha512}
    hash_func = hash_funcs[alg]

    # Reconstruct signing input
    parts = jwt_token.split(".")
    signing_input = f"{parts[0]}.{parts[1]}".encode("utf-8")

    # Compute expected signature
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hash_func).digest()
    actual_sig_b64 = parts[2]
    actual_sig = _b64url_decode(actual_sig_b64)

    signature_valid = hmac.compare_digest(expected_sig, actual_sig)

    return {
        "signature_valid": signature_valid,
        "algorithm_used": alg,
        "expected_signature": expected_sig.hex(),
        "actual_signature": actual_sig.hex(),
    }


def create(payload: dict, secret: str, alg: str = "HS256") -> str:
    """
    Create a JWT with the given payload and HMAC signature.

    Returns the JWT string.
    """
    if alg not in ("HS256", "HS384", "HS512"):
        raise ValueError(f"Algorithm {alg} not supported")

    header = {"alg": alg, "typ": "JWT"}

    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    hash_funcs = {"HS256": hashlib.sha256, "HS384": hashlib.sha384, "HS512": hashlib.sha512}
    signature = hmac.new(secret.encode("utf-8"), signing_input, hash_funcs[alg]).digest()
    signature_b64 = _b64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-jwt-inspector ")
    parser.add_argument("jwt", nargs="?", help="JWT to decode")
    parser.add_argument("--secret", help="Verify HMAC signature with this secret")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--create", help="Create a JWT (JSON payload)")
    parser.add_argument("--secret-create", help="Secret for creating JWT")
    args = parser.parse_args()

    if args.create:
        if not args.secret_create:
            print("❌ --secret-create required for --create", file=sys.stderr)
            return 1
        try:
            payload = json.loads(args.create)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}", file=sys.stderr)
            return 1
        jwt = create(payload, args.secret_create)
        print(jwt)
        return 0

    if not args.jwt:
        # Demo
        demo_payload = {"sub": "1234567890", "name": "Demo", "iat": int(time.time())}
        demo_jwt = create(demo_payload, "secret")
        print(f"Demo JWT: {demo_jwt}")
        result = decode(demo_jwt)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"\nHeader:  {result['header']}")
            print(f"Payload: {result['payload']}")
            print(f"Algorithm: {result['signature_algorithm']}")
            if result.get("exp_info"):
                print(f"Expiration: {result['exp_info']}")
        return 0

    result = decode(args.jwt)
    if args.secret:
        verify = verify_hmac(args.jwt, args.secret)
        result["signature_verification"] = verify

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        if not result.get("valid_format"):
            print(f"❌ {result.get('error', 'invalid')}")
            return 1
        print(f"Header:    {result['header']}")
        print(f"Payload:   {result['payload']}")
        print(f"Signature: {result['signature'][:32]}... ({result['signature_algorithm']})")
        if result.get("exp_info"):
            exp = result["exp_info"]
            icon = "✅" if not exp["expired"] else "❌"
            print(f"Expiry:    {icon} {exp['seconds_until_expiry']}s ({'expired' if exp['expired'] else 'valid'})")
        if "signature_verification" in result:
            v = result["signature_verification"]
            icon = "✅" if v["signature_valid"] else "❌"
            print(f"HMAC:      {icon} {v['algorithm_used']} {'valid' if v['signature_valid'] else 'INVALID'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
