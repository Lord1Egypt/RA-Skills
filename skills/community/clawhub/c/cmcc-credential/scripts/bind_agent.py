#!/usr/bin/env python3
"""
CMCC Digital Credential - Agent Binding

This script binds the agent to the credential system by calling the
CMVC agent binding API using appName and appId.
"""

import json
import hashlib
import hmac
import secrets
import time
import sys

BASE_URL = "https://vctest.cmccsign.com"

# Predefined constants
DEFAULT_APP_NAME = "Javis"



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


def bind_agent(app_name: str = None, app_id: str = None, app_key: str = None) -> dict:
    """
    Bind agent to the credential system.

    Args:
        app_name: Application name (defaults to "Javis")
        app_id: Application ID (凭证中对应的AppId)
        app_key: Application secret key

    Returns:
        Dictionary with response code and description

    Raises:
        Exception: If request fails

    Note:
        Signature based on Java SignUtil.encryptWithKeyToHEX:
        1. Sort JSON by dictionary order
        2. Calculate HmacSHA256
        3. Convert to uppercase hex
    """
    # Use default app name if not provided
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    # Build request body
    body = {
        "appName": app_name,
        "appId": app_id
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

    url = f"{BASE_URL}/api/cmvc-tocp-server/agent/bind"

    req = urllib.request.Request(
        url,
        data=body_json.encode('utf-8'),
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            # Return response
            return {
                "code": response_data.get("code"),
                "desc": response_data.get("desc", response_data.get("msg", ""))
            }

    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8')) if e.readable() else {}
        raise Exception(f"HTTP {e.code}: {error_data.get('desc', str(e))}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {str(e)}")


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Bind Agent to CMCC Digital Credential System')
    parser.add_argument('--appName', help=f'Application name (default: {DEFAULT_APP_NAME})')
    parser.add_argument('--appId', required=True, help='Application ID')
    parser.add_argument('--appKey', required=True, help='Application secret key')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='Output format')

    args = parser.parse_args()

    try:
        result = bind_agent(
            args.appName,
            args.appId,
            args.appKey
        )

        if args.output == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Binding response:")
            print(f"Code: {result['code']}")
            print(f"Description: {result['desc']}")

            if result['code'] == 0:
                print("✓ Agent binding successful")
                sys.exit(0)
            else:
                print("✗ Agent binding failed")
                sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
