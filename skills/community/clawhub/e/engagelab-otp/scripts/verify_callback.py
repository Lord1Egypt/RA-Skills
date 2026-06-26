"""
EngageLab OTP callback signature verifier.

Validates the X-CALLBACK-ID header on incoming webhook requests to confirm
they originate from EngageLab. Use this in your callback endpoint handler.

Usage (Flask example):

    from verify_callback import verify_engagelab_callback

    @app.route("/otp-callback", methods=["POST"])
    def otp_callback():
        header = request.headers.get("X-CALLBACK-ID", "")
        if not verify_engagelab_callback(header, "my_secret"):
            return "Unauthorized", 401
        data = request.get_json()
        for row in data.get("rows", []):
            status = row.get("status", {}).get("message_status")
            print(f"Message {row['message_id']}: {status}")
        return "", 200
"""

import hashlib
import hmac
from typing import Optional


def parse_callback_header(header: str) -> Optional[dict]:
    """
    Parse the X-CALLBACK-ID header into its components.

    Header format:
        timestamp={ts};nonce={nonce};username={user};signature={sig}

    Returns dict with keys: timestamp, nonce, username, signature.
    Returns None if the header cannot be parsed.
    """
    parts = {}
    for segment in header.split(";"):
        if "=" not in segment:
            return None
        key, value = segment.split("=", 1)
        parts[key.strip()] = value.strip()

    required = {"timestamp", "nonce", "username", "signature"}
    if not required.issubset(parts.keys()):
        return None
    return parts


def compute_signature(secret: str, timestamp: str, nonce: str, username: str) -> str:
    """Compute HMAC-SHA256 signature matching EngageLab's algorithm."""
    message = f"{timestamp}{nonce}{username}"
    return hmac.new(
        key=secret.encode(),
        msg=message.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()


def verify_engagelab_callback(header: str, secret: str) -> bool:
    """
    Verify an EngageLab OTP callback request.

    Args:
        header: The value of the X-CALLBACK-ID HTTP header.
        secret: Your configured callback secret.

    Returns:
        True if the signature is valid, False otherwise.
    """
    parsed = parse_callback_header(header)
    if parsed is None:
        return False

    expected = compute_signature(
        secret,
        parsed["timestamp"],
        parsed["nonce"],
        parsed["username"],
    )
    return hmac.compare_digest(expected, parsed["signature"])


if __name__ == "__main__":
    # Quick self-test
    test_secret = "my_secret"
    test_ts = "1701234567"
    test_nonce = "abc123"
    test_user = "my_user"
    sig = compute_signature(test_secret, test_ts, test_nonce, test_user)

    test_header = f"timestamp={test_ts};nonce={test_nonce};username={test_user};signature={sig}"
    assert verify_engagelab_callback(test_header, test_secret), "Valid signature should pass"
    assert not verify_engagelab_callback(test_header, "wrong_secret"), "Wrong secret should fail"
    assert not verify_engagelab_callback("malformed", test_secret), "Malformed header should fail"
    print("All checks passed.")
