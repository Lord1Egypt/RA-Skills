#!/usr/bin/env python3
"""
Get access token from Gangtise Open Platform API.
"""
import json
import sys
from pathlib import Path

# Add scripts directory to path for importing configure module
sys.path.insert(0, str(Path(__file__).parent))

from configure import get_credentials, check_configured

BASE_URL = "https://open.gangtise.com"
LOGIN_ENDPOINT = "/application/auth/oauth/open/loginV2"


def get_access_token():
    """Authenticate and get access token."""
    # Check if configured
    if not check_configured():
        print("=" * 60, file=sys.stderr)
        print("ERROR: Gangtise Knowledge Base is not configured.", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(file=sys.stderr)
        print("Please run the configuration script first:", file=sys.stderr)
        print(file=sys.stderr)
        print("  python3 scripts/configure.py", file=sys.stderr)
        print(file=sys.stderr)
        print("You can obtain your Access Key and Secret Key from:", file=sys.stderr)
        print("  https://open.gangtise.com", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        return None

    ACCESS_KEY, SECRET_KEY = get_credentials()

    import urllib.request
    import urllib.error
    import ssl

    url = f"{BASE_URL}{LOGIN_ENDPOINT}"

    # Prepare request data
    data = {
        "accessKey": ACCESS_KEY,
        "secretAccessKey": SECRET_KEY
    }

    # Create request
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        method='POST'
    )

    # Handle SSL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

            # Extract token from response
            # V2接口返回的accessToken已经携带了Bearer前缀
            if result and result.get('code') == '000000' and 'data' in result:
                token = result['data'].get('accessToken')
                if token:
                    return token  # 已经包含Bearer前缀

            print(f"Unexpected response: {json.dumps(result, indent=2)}", file=sys.stderr)
            return None

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode('utf-8')
            print(f"Response: {error_body}", file=sys.stderr)
        except:
            pass
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    token = get_access_token()
    if token:
        print(token)
        sys.exit(0)
    else:
        sys.exit(1)
