#!/usr/bin/env python3
"""
license.py — License key validation for competitive-radar.

Validates Gumroad license keys against the Gumroad API.
Stores validated license locally so it only needs to phone home once.

Usage:
  python3 license.py --activate <license_key>   # validate + store
  python3 license.py --check                    # check local license status
  python3 license.py --status                   # print tier (free / paid)
"""

from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
LICENSE_FILE = DATA_DIR / "license.json"

# Replace with your actual Gumroad product permalink once created
GUMROAD_PRODUCT_ID = "competitive-radar"
GUMROAD_API = "https://api.gumroad.com/v2/licenses/verify"

FREE_TIER_LIMIT = 1


# ---------------------------------------------------------------------------
# License file helpers
# ---------------------------------------------------------------------------

def load_license() -> dict:
    if not LICENSE_FILE.exists():
        return {"tier": "free", "license_key": None, "validated_at": None, "email": None}
    try:
        return json.loads(LICENSE_FILE.read_text())
    except Exception:
        return {"tier": "free", "license_key": None, "validated_at": None, "email": None}


def save_license(data: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(data, indent=2))


def is_paid() -> bool:
    return load_license().get("tier") == "paid"


def get_tier() -> str:
    return load_license().get("tier", "free")


# ---------------------------------------------------------------------------
# Gumroad API validation
# ---------------------------------------------------------------------------

def validate_with_gumroad(license_key: str) -> dict:
    """
    Call Gumroad's license verification API.
    Returns dict with success bool + purchase details.
    """
    try:
        result = subprocess.run(
            [
                "curl", "-sS", "-X", "POST", GUMROAD_API,
                "--data-urlencode", f"product_permalink={GUMROAD_PRODUCT_ID}",
                "--data-urlencode", f"license_key={license_key}",
                "--data-urlencode", "increment_uses_count=false",
            ],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return {"success": False, "message": "Network error — check your connection"}
        resp = json.loads(result.stdout)
        return resp
    except json.JSONDecodeError:
        return {"success": False, "message": "Invalid response from license server"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------------------------------------------------------------------------
# Activate
# ---------------------------------------------------------------------------

def activate(license_key: str) -> dict:
    """Validate key with Gumroad and store locally if valid."""
    license_key = license_key.strip()
    print(f"[license] Validating key with Gumroad...")

    resp = validate_with_gumroad(license_key)

    if not resp.get("success"):
        msg = resp.get("message", "Invalid license key")
        return {"success": False, "message": msg}

    purchase = resp.get("purchase", {})
    email = purchase.get("email", "")
    product_name = purchase.get("product_name", "")
    refunded = purchase.get("refunded", False)
    chargebacked = purchase.get("chargebacked", False)

    if refunded or chargebacked:
        return {"success": False, "message": "This license has been refunded or charged back"}

    # Store validated license
    license_data = {
        "tier": "paid",
        "license_key": license_key,
        "email": email,
        "product_name": product_name,
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "gumroad_response": {
            "sale_id": purchase.get("id"),
            "created_at": purchase.get("created_at"),
        }
    }
    save_license(license_data)

    return {
        "success": True,
        "message": f"License activated for {email}. Unlimited competitors unlocked.",
        "email": email,
        "tier": "paid",
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitive-radar license manager")
    parser.add_argument("--activate", metavar="KEY", help="Activate a Gumroad license key")
    parser.add_argument("--check", action="store_true", help="Check local license status")
    parser.add_argument("--status", action="store_true", help="Print tier only (free/paid)")
    args = parser.parse_args()

    if args.status:
        print(get_tier())
        return

    if args.check:
        lic = load_license()
        if lic["tier"] == "paid":
            print(f"✓ Paid license active")
            print(f"  Email: {lic.get('email', 'unknown')}")
            print(f"  Validated: {lic.get('validated_at', 'unknown')}")
        else:
            print(f"Free tier — 1 competitor max")
            print(f"  Upgrade: https://manjotpahwa.gumroad.com/l/competitive-radar")
        print(json.dumps(lic, indent=2))
        return

    if args.activate:
        result = activate(args.activate)
        if result["success"]:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ {result['message']}", file=sys.stderr)
            sys.exit(1)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
