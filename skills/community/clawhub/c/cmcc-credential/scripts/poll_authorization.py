#!/usr/bin/env python3
"""
CMCC Digital Credential - Authorization Status Polling

This script polls the authorization status until authorized or timeout.
"""

import json
import hashlib
import hmac
import time
import sys

BASE_URL = "https://vctest.cmccsign.com"


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
    import secrets
    return secrets.token_hex(8)  # 8 bytes = 16 hex chars


def query_authorization(app_id: str, app_key: str, auth_record_id: str) -> dict:
    """
    Query authorization status.

    Args:
        app_id: Application ID
        app_key: Application secret key
        auth_record_id: Authorization record ID

    Returns:
        Dictionary with authorization status

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

    # Build request body
    body = {
        "authRecordId": auth_record_id
    }

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

    url = f"{BASE_URL}/api/cmvc-tocp-server/vc/auth/query"

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

            # Return authorization status
            return {
                "statusCode": response_data.get("statusCode"),
                "statusDesc": response_data.get("statusDesc"),
                "credentialSubject": response_data.get("credentialSubject", {})
            }

    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8')) if e.readable() else {}
        raise Exception(f"HTTP {e.code}: {error_data.get('desc', str(e))}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {str(e)}")


def poll_authorization(app_id: str, app_key: str, auth_record_id: str,
                      interval: int = 5, timeout: int = 600, verbose: bool = False) -> dict:
    """
    Poll authorization status until authorized or timeout.

    Args:
        app_id: Application ID
        app_key: Application secret key
        auth_record_id: Authorization record ID
        interval: Polling interval in seconds (default: 5)
        timeout: Maximum timeout in seconds (default: 600 = 10 minutes)
        verbose: Print polling status

    Returns:
        Dictionary with authorization status if authorized

    Raises:
        Exception: If timeout or polling fails
    """
    start_time = time.time()
    max_attempts = timeout // interval
    attempt = 0

    if verbose:
        print(f"Polling authorization status (interval: {interval}s, timeout: {timeout}s)...")

    while attempt < max_attempts:
        attempt += 1
        elapsed = time.time() - start_time

        try:
            status = query_authorization(app_id, app_key, auth_record_id)

            if verbose:
                print(f"Attempt {attempt}/{max_attempts}: {status['statusDesc']} (statusCode: {status['statusCode']})")

            # Check if authorized
            if status["statusCode"] == "000000":
                if verbose:
                    print(f"Authorization confirmed after {elapsed:.1f}s")
                return status

        except Exception as e:
            if verbose:
                print(f"Attempt {attempt}/{max_attempts}: Error - {str(e)}")

        # Check timeout
        if time.time() - start_time >= timeout:
            if verbose:
                print(f"Timeout after {timeout}s")
            raise Exception(f"Authorization polling timeout after {timeout}s")

        # Wait for next interval
        time.sleep(interval)

    raise Exception(f"Authorization failed after {max_attempts} attempts")


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Poll CMCC Digital Credential Authorization Status')
    parser.add_argument('--appId', required=True, help='Application ID')
    parser.add_argument('--appKey', required=True, help='Application secret key')
    parser.add_argument('--authRecordId', required=True, help='Authorization record ID')
    parser.add_argument('--interval', type=int, default=5, help='Polling interval in seconds (default: 5)')
    parser.add_argument('--timeout', type=int, default=600, help='Timeout in seconds (default: 600 = 10 minutes)')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print polling status')

    args = parser.parse_args()

    try:
        result = poll_authorization(
            args.appId,
            args.appKey,
            args.authRecordId,
            args.interval,
            args.timeout,
            args.verbose
        )

        if args.output == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Authorization successful!")
            print(f"Status: {result['statusDesc']}")
            print(f"Status Code: {result['statusCode']}")
            if result.get('credentialSubject'):
                print(f"Credential Subject: {json.dumps(result['credentialSubject'], indent=2, ensure_ascii=False)}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
