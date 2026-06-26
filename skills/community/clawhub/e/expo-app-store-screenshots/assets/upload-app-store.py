#!/usr/bin/env python3
"""Upload PNG screenshots to App Store Connect for one (locale, device) slot.

Auth — App Store Connect API key (.p8). Generate at
App Store Connect → Users and Access → Integrations → App Store Connect API.
The key needs the "App Manager" role (or finer-grained "App Metadata" with
write access) on the target app.

Usage:
  python3 upload-app-store.py \\
      --key-id ABC1234567 \\
      --issuer-id 11111111-2222-3333-4444-555555555555 \\
      --key-path ./AuthKey_ABC1234567.p8 \\
      --app-id 1234567890 \\
      --locale en-US \\
      --device iphone \\
      --dir screenshots/en-US/iphone

Auth args fall back to env: ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_PATH.

Locale note: App Store Connect uses Apple's locale codes, not the BCP-47 tags
this project uses for the screenshots/ tree. Map before invoking — common ones:
  en-US     → en-US      (same)
  zh-CN     → zh-Hans
  zh-TW     → zh-Hant
  pt-BR     → pt-BR      (same)
  fr-FR     → fr-FR      (same)
See https://developer.apple.com/documentation/appstoreconnectapi/appstoreversionlocalization
for the full list.

Behavior:
  - Picks the *editable* iOS appStoreVersion (PREPARE_FOR_SUBMISSION, METADATA_REJECTED,
    REJECTED, DEVELOPER_REJECTED, etc.). Won't touch a version that's READY_FOR_SALE
    or in review.
  - Creates the appStoreVersionLocalization for --locale if missing.
  - Creates the appScreenshotSet for --device's display type if missing.
  - By default deletes any existing screenshots in that slot, then uploads PNGs in
    sorted-filename order. Pass --keep-existing to append instead.

Requires: requests, pyjwt[crypto].
  pip install 'pyjwt[crypto]' requests
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import time
from pathlib import Path

import jwt
import requests

BASE = "https://api.appstoreconnect.apple.com/v1"

# device shorthand -> ASC screenshotDisplayType
DEVICE_DISPLAY_TYPE = {
    "iphone-65": "APP_IPHONE_65",  # 1242x2688 (iPhone 11 Pro Max class)
    "iphone-67": "APP_IPHONE_67",  # 1290x2796 / 1284x2778 (iPhone 14/15 Pro Max class)
    "iphone-69": "APP_IPHONE_69",  # 1320x2868 (iPhone 16 Pro Max)
    "ipad-129": "APP_IPAD_PRO_3GEN_129",  # 2064x2752 (M4) / 2048x2732 (older 12.9")
    # default aliases — match the device folder names used by the rest of the skill
    "iphone": "APP_IPHONE_67",
    "ipad": "APP_IPAD_PRO_3GEN_129",
}

EDITABLE_STATES = {
    "PREPARE_FOR_SUBMISSION",
    "METADATA_REJECTED",
    "REJECTED",
    "DEVELOPER_REJECTED",
    "INVALID_BINARY",
    "WAITING_FOR_REVIEW",
    "DEVELOPER_REMOVED_FROM_SALE",
}


def make_token(key_id: str, issuer_id: str, key_path: str) -> str:
    private_key = Path(key_path).read_text()
    headers = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": issuer_id,
        "iat": now,
        "exp": now + 19 * 60,  # ASC max is 20 min
        "aud": "appstoreconnect-v1",
    }
    return jwt.encode(payload, private_key, algorithm="ES256", headers=headers)


class ASC:
    def __init__(self, token: str) -> None:
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"

    def _req(self, method: str, path: str, **kw) -> requests.Response:
        url = path if path.startswith("http") else f"{BASE}{path}"
        r = self.s.request(method, url, **kw)
        if not r.ok:
            sys.exit(f"{method} {url} → {r.status_code}\n{r.text}")
        return r

    def get(self, path: str, **kw) -> dict:
        return self._req("GET", path, **kw).json()

    def post(self, path: str, body: dict) -> dict:
        return self._req("POST", path, json=body).json()

    def patch(self, path: str, body: dict) -> dict:
        return self._req("PATCH", path, json=body).json()

    def delete(self, path: str) -> None:
        self._req("DELETE", path)


def find_editable_version(asc: ASC, app_id: str) -> dict:
    data = asc.get(
        f"/apps/{app_id}/appStoreVersions",
        params={"filter[platform]": "IOS", "limit": 50},
    )
    for v in data["data"]:
        if v["attributes"]["appStoreState"] in EDITABLE_STATES:
            return v
    sys.exit(
        "no editable iOS appStoreVersion found — need a draft or rejected version "
        "(states: " + ", ".join(sorted(EDITABLE_STATES)) + ")"
    )


def find_or_create_localization(asc: ASC, version_id: str, locale: str) -> str:
    locs = asc.get(
        f"/appStoreVersions/{version_id}/appStoreVersionLocalizations",
        params={"limit": 200},
    )
    for loc in locs["data"]:
        if loc["attributes"]["locale"] == locale:
            return loc["id"]
    created = asc.post(
        "/appStoreVersionLocalizations",
        {
            "data": {
                "type": "appStoreVersionLocalizations",
                "attributes": {"locale": locale},
                "relationships": {
                    "appStoreVersion": {
                        "data": {"type": "appStoreVersions", "id": version_id}
                    }
                },
            }
        },
    )
    return created["data"]["id"]


def find_or_create_screenshot_set(asc: ASC, loc_id: str, display_type: str) -> str:
    sets = asc.get(f"/appStoreVersionLocalizations/{loc_id}/appScreenshotSets")
    for s in sets["data"]:
        if s["attributes"]["screenshotDisplayType"] == display_type:
            return s["id"]
    created = asc.post(
        "/appScreenshotSets",
        {
            "data": {
                "type": "appScreenshotSets",
                "attributes": {"screenshotDisplayType": display_type},
                "relationships": {
                    "appStoreVersionLocalization": {
                        "data": {
                            "type": "appStoreVersionLocalizations",
                            "id": loc_id,
                        }
                    }
                },
            }
        },
    )
    return created["data"]["id"]


def clear_set(asc: ASC, set_id: str) -> None:
    existing = asc.get(f"/appScreenshotSets/{set_id}/appScreenshots")
    for s in existing["data"]:
        asc.delete(f"/appScreenshots/{s['id']}")
        print(f"  deleted existing screenshot {s['id']}")


def upload_one(asc: ASC, set_id: str, path: Path) -> str:
    data = path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    reservation = asc.post(
        "/appScreenshots",
        {
            "data": {
                "type": "appScreenshots",
                "attributes": {"fileSize": len(data), "fileName": path.name},
                "relationships": {
                    "appScreenshotSet": {
                        "data": {"type": "appScreenshotSets", "id": set_id}
                    }
                },
            }
        },
    )
    sid = reservation["data"]["id"]
    ops = reservation["data"]["attributes"]["uploadOperations"]
    for op in ops:
        headers = {h["name"]: h["value"] for h in op["requestHeaders"]}
        chunk = data[op["offset"] : op["offset"] + op["length"]]
        r = requests.request(op["method"], op["url"], headers=headers, data=chunk)
        r.raise_for_status()
    asc.patch(
        f"/appScreenshots/{sid}",
        {
            "data": {
                "type": "appScreenshots",
                "id": sid,
                "attributes": {"uploaded": True, "sourceFileChecksum": md5},
            }
        },
    )
    return sid


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--key-id", default=os.environ.get("ASC_KEY_ID"))
    ap.add_argument("--issuer-id", default=os.environ.get("ASC_ISSUER_ID"))
    ap.add_argument("--key-path", default=os.environ.get("ASC_KEY_PATH"))
    ap.add_argument("--app-id", required=True, help="numeric App Store Connect app id")
    ap.add_argument("--locale", required=True, help="Apple locale code, e.g. en-US, zh-Hans")
    ap.add_argument(
        "--device",
        required=True,
        choices=sorted(DEVICE_DISPLAY_TYPE),
        help="iphone | ipad | iphone-65 | iphone-67 | iphone-69 | ipad-129",
    )
    ap.add_argument("--dir", required=True, help="directory of *.png files (uploaded in sorted-filename order)")
    ap.add_argument(
        "--keep-existing",
        action="store_true",
        help="append instead of replacing existing screenshots in this slot",
    )
    args = ap.parse_args()

    for attr, flag in (("key_id", "--key-id"), ("issuer_id", "--issuer-id"), ("key_path", "--key-path")):
        if not getattr(args, attr):
            sys.exit(f"missing {flag} (or ASC_{attr.upper()} env var)")

    pngs = sorted(Path(args.dir).glob("*.png"))
    if not pngs:
        sys.exit(f"no PNGs in {args.dir}")

    display_type = DEVICE_DISPLAY_TYPE[args.device]
    token = make_token(args.key_id, args.issuer_id, args.key_path)
    asc = ASC(token)

    version = find_editable_version(asc, args.app_id)
    print(
        f"version {version['id']} "
        f"(state={version['attributes']['appStoreState']}, "
        f"v={version['attributes']['versionString']})"
    )
    loc_id = find_or_create_localization(asc, version["id"], args.locale)
    print(f"localization {args.locale} → {loc_id}")
    set_id = find_or_create_screenshot_set(asc, loc_id, display_type)
    print(f"screenshot set {display_type} → {set_id}")

    if not args.keep_existing:
        clear_set(asc, set_id)

    for p in pngs:
        sid = upload_one(asc, set_id, p)
        print(f"  uploaded {p.name} → {sid}")

    print(f"done — {len(pngs)} screenshots uploaded to {args.locale}/{display_type}")


if __name__ == "__main__":
    main()
