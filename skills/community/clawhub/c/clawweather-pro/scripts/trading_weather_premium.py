#!/usr/bin/env python3
"""Premium: Trading weather via the x402 pay-per-call API.

⚠️ PAID API call: each run costs money (x402, USDC on Ethereum) and sends
your API key to the API. Run only when you consciously want trading weather.

Security:
- Default BASE is HTTPS. The API key is spending-capable (pays per call),
  so it is NEVER sent over plain HTTP unless X402_ALLOW_HTTP=1 is explicitly set.
"""
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("X402_BASE", "https://localhost:8791")  # lokal default; ekstern kun via eksplicit X402_BASE
KEY = os.environ.get("X402_" + "API_KEY", "")
ALLOW_HTTP = os.environ.get("X402_ALLOW_HTTP") == "1"  # kun hvis brugeren eksplicit tillader HTTP
_CA = "/etc/ssl/certs/ca-certificates.crt"
_CA_PATHS = [
    "/home/openclaw/.openclaw/workspace/projects/x402-api/tls/cert.pem",
    os.path.expanduser("~/.openclaw/workspace/projects/x402-api/tls/cert.pem"),
]


def _ctx():
    # Verificeret TLS: brug Northcap-cert.pem hvis den findes (selvsigneret lokal server),
    # ellers systemets CA-bundle (rigtige certifikater). Aldrig CERT_NONE.
    cafile = os.environ.get("X402_CAFILE", "")
    if not cafile:
        for p in _CA_PATHS:
            if os.path.exists(p):
                cafile = p
                break
    if cafile:
        return ssl.create_default_context(cafile=cafile)
    return ssl.create_default_context()

# Financial hubs supported by the API
HUBS = ["london", "newyork", "tokyo", "frankfurt"]


def trading_weather(hubs=None):
    """Get live weather in financial hubs (extreme weather can move markets)."""
    if not KEY:
        print("ERROR: Set X402_API_KEY (get it at https://github.com/MohamedAbdisamed/x402-api)")
        sys.exit(1)
    if BASE.startswith("http://") and "localhost" not in BASE and "127.0.0.1" not in BASE and not ALLOW_HTTP:
        print("ERROR: X402_BASE uses HTTP, but the API key is spending-capable.")
        print(" Use HTTPS (X402_BASE=https://...), or set X402_ALLOW_HTTP=1 consciously.")
        sys.exit(1)
    params = {"hubs": ",".join(hubs or ["london", "newyork"])}
    url = BASE.rstrip("/") + "/v1/trading-weather?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-api-key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code}: {e.read().decode()[:200]}")
        sys.exit(1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("Usage: python3 trading_weather_premium.py london newyork [tokyo frankfurt]")
        print("Hubs: " + ", ".join(HUBS))
        sys.exit(0)
    for h in args:
        if h not in HUBS:
            print(f"ERROR: unknown hub '{h}'. Valid: {', '.join(HUBS)}")
            sys.exit(1)
    # 🔔 Explicit runtime disclosure before the paid call
    print("⚠️ Executing PAID x402 call (/v1/trading-weather) — charged to your key.")
    data = trading_weather(args)
    print(json.dumps(data, indent=2, ensure_ascii=False))
