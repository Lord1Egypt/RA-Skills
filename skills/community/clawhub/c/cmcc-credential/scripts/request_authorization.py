#!/usr/bin/env python3
"""
CMCC Digital Credential - Authorization Request

This script requests authorization for sensitive operations by calling the
CMVC credential authorization API.
"""

import json
import hashlib
import hmac
import secrets
import time
import base64
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BASE_URL = "https://vctest.cmccsign.com"

# Predefined constants
TEMPLATE_ID = "qfx9pkizs42up7y61jsehs9v8e1xms4m"


def md5_hash(text: str) -> bytes:
    """Generate MD5 hash of text."""
    return hashlib.md5(text.encode('utf-8')).digest()


def encrypt_phone_aes_ecb(phone_no: str, app_key: str) -> str:
    """
    Encrypt phone number using AES/ECB/PKCS5Padding.

    Based on Java AESUtil.encodeAES:
    1. MD5 hash of appKey as 16-byte key
    2. AES/ECB/PKCS5Padding encryption
    3. Base64 encode result

    Args:
        phone_no: Phone number to encrypt
        app_key: Application secret key

    Returns:
        Base64-encoded encrypted phone number
    """
    # Derive 16-byte key from appKey using MD5
    key_bytes = md5_hash(app_key)

    # Convert phone number to bytes
    phone_bytes = phone_no.encode('utf-8')

    # Encrypt using AES/ECB/PKCS5Padding
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(phone_bytes, AES.block_size))

    # Return Base64-encoded result
    return base64.b64encode(encrypted).decode('utf-8')


def generate_signature(app_id: str, app_key: str, body: str) -> str:
    """
    Generate HMAC-SHA256 signature.

    Based on Java SignUtil.encryptWithKeyToHEX:
    1. Sort JSON object by dictionary order and serialize to string
    2. Calculate HMAC using HmacSHA256 and secretKey
    3. Convert binary result to uppercase hexadecimal string

    Args:
        app_id: Application ID
        app_key: Application secret key
        body: Request body JSON string (must be sorted)

    Returns:
        64-character uppercase hex signature
    """
    # The body string must already be sorted JSON
    # Calculate HMAC-SHA256 using appKey as secret
    signature = hmac.new(
        app_key.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()

    # Convert to uppercase hexadecimal string
    return signature.hex().upper()


def generate_nonce() -> str:
    """Generate 16-character random nonce."""
    return secrets.token_hex(8)  # 8 bytes = 16 hex chars


def request_authorization(app_id: str, app_key: str, phone_no: str,
                         return_url: str = "", notify_url: str = "") -> dict:
    """
    Request credential authorization.

    Args:
        app_id: Application ID (24 characters)
        app_key: Application secret key
        phone_no: User's phone number
        return_url: Optional redirect URL after authorization
        notify_url: Optional callback URL for authorization result

    Returns:
        Dictionary with authRecordId and trustedAuthUrl

    Raises:
        Exception: If request fails

    Note:
        Signature based on Java SignUtil.encryptWithKeyToHEX:
        1. Sort JSON by dictionary order
        2. Calculate HmacSHA256
        3. Convert to uppercase hex
    """
    # Generate nonce and timestamp
    nonce = generate_nonce()
    timestamp = int(time.time() * 1000)

    # Encrypt phone number
    encrypted_phone = encrypt_phone_aes_ecb(phone_no, app_key)

    # Build request body
    body = {
        "nonce": nonce,
        "timestamp": timestamp,
        "phoneNo": encrypted_phone,
        "templateId": TEMPLATE_ID,
        "sendSmsFlag": "0",  # Don't send SMS by default
    }

    # Add optional fields
    if return_url:
        body["returnUrl"] = return_url
    if notify_url:
        body["notifyUrl"] = notify_url

    # Convert to JSON string with sorted keys (dictionary order)
    body_json = json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

    # Generate signature using sorted JSON body
    signature = generate_signature(app_id, app_key, body_json)

    # Build request headers (new format: appId and signValue)
    headers = {
        "appId": app_id,
        "signValue": signature,
        "Content-Type": "application/json"
    }

    # Send request
    import urllib.request
    import urllib.error

    url = f"{BASE_URL}/cmvc-tocp-server/vc/auth/request"

    req = urllib.request.Request(
        url,
        data=body_json.encode('utf-8'),
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            # Check response code
            if response_data.get("code") != 0:
                raise Exception(f"API error: {response_data.get('desc', 'Unknown error')}")

            # Return authRecordId and trustedAuthUrl
            return {
                "authRecordId": response_data["authRecordId"],
                "trustedAuthUrl": response_data["trustedAuthUrl"]
            }

    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8')) if e.readable() else {}
        raise Exception(f"HTTP {e.code}: {error_data.get('desc', str(e))}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {str(e)}")


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Request CMCC Digital Credential Authorization')
    parser.add_argument('--appId', required=True, help='Application ID')
    parser.add_argument('--appKey', required=True, help='Application secret key')
    parser.add_argument('--phoneNo', required=True, help='User phone number')
    parser.add_argument('--returnUrl', default='', help='Optional redirect URL')
    parser.add_argument('--notifyUrl', default='', help='Optional callback URL')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='Output format')

    args = parser.parse_args()

    try:
        result = request_authorization(
            args.appId,
            args.appKey,
            args.phoneNo,
            args.returnUrl,
            args.notifyUrl
        )

        if args.output == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Authorization requested successfully")
            print(f"Auth Record ID: {result['authRecordId']}")
            print(f"Authorization URL: {result['trustedAuthUrl']}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
