import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://api.finam.ru/v1"
ASSETS_DIR = Path(__file__).parent.parent / "assets"
DEBUG = False


def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def get_token():
    cached = os.environ.get("FINAM_JWT_TOKEN")
    if cached:
        dprint("Using JWT token from FINAM_JWT_TOKEN.")
        return cached

    api_key = os.environ.get("FINAM_API_KEY")
    if not api_key:
        print("Error: FINAM_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    dprint("Obtaining JWT token...")
    url = f"{BASE_URL}/sessions"
    payload = json.dumps({"secret": api_key}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"Error: failed to authenticate: {e}", file=sys.stderr)
        sys.exit(1)
    token = data["token"]
    os.environ["FINAM_JWT_TOKEN"] = token
    dprint("Token obtained and saved to FINAM_JWT_TOKEN.")
    return token


def load_equities(market):
    path = ASSETS_DIR / f"top_{market}_equities.json"
    with open(path) as f:
        return json.load(f)
