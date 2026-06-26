#!/usr/bin/env python3
"""Check Bonito API connectivity.

Hits api.getbonito.com/health and reports status.
Exit code 0 = healthy, 1 = unhealthy or unreachable.
"""

import sys
import urllib.request
import urllib.error
import json
import ssl

API_URL = "https://api.getbonito.com/health"
TIMEOUT_SECONDS = 10


def check_health():
    """Ping the Bonito API health endpoint."""
    try:
        # Create SSL context (some environments need this)
        ctx = ssl.create_default_context()
        req = urllib.request.Request(API_URL, method="GET")
        req.add_header("User-Agent", "bonito-skill-health-check/1.0")

        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS, context=ctx) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")

            if status == 200:
                print(f"✅ Bonito API is healthy (HTTP {status})")
                try:
                    data = json.loads(body)
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"   Response: {body[:500]}")
                return True
            else:
                print(f"⚠️  Bonito API returned HTTP {status}")
                print(f"   Response: {body[:500]}")
                return False

    except urllib.error.HTTPError as e:
        print(f"⚠️  Bonito API returned HTTP {e.code}")
        try:
            body = e.read().decode("utf-8", errors="replace")
            print(f"   Response: {body[:500]}")
        except Exception:
            pass
        return False

    except urllib.error.URLError as e:
        print(f"❌ Cannot reach Bonito API: {e.reason}")
        return False

    except TimeoutError:
        print(f"❌ Bonito API timed out after {TIMEOUT_SECONDS}s")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    healthy = check_health()
    if not healthy:
        print("\nThe API may be temporarily down. You can still install bonito-cli")
        print("and configure your project — deploy will work once the API is back.")
    sys.exit(0 if healthy else 1)
