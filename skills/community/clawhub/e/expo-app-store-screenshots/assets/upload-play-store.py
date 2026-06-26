#!/usr/bin/env python3
"""Upload PNG screenshots to a Google Play Console listing for one (locale, image-type) slot.

Auth — Google Cloud service account JSON. Setup:
  1. Google Cloud Console → enable "Google Play Android Developer API".
  2. Create a service account, download its JSON key.
  3. Play Console → Setup → API access → link the project, then grant the
     service account the "Manage store presence" permission on this app.

Usage:
  python3 upload-play-store.py \\
      --credentials ./play-service-account.json \\
      --package com.example.myapp \\
      --locale en-US \\
      --image-type phoneScreenshots \\
      --dir screenshots/en-US/android-phone

--credentials falls back to the PLAY_CREDENTIALS env var.

Image types (one slot per language):
  phoneScreenshots       — handsets
  sevenInchScreenshots   — 7" tablets
  tenInchScreenshots     — 10"+ tablets
  tvScreenshots          — Android TV
  wearScreenshots        — Wear OS

Locale note: Google Play uses BCP-47 (`en-US`, `zh-CN`, `ja-JP`, …). The locale
must already be enabled on the listing — add it once via Play Console
(Main store listing → Manage translations) before this script can target it.

Behavior:
  - Opens an edit, clears existing images in (locale, image-type), uploads PNGs in
    sorted-filename order, commits the edit. Pass --keep-existing to append.
  - Play caps each image-type slot at 8 screenshots; the script does not enforce
    that — your store will reject the commit if you exceed it.

Requires: requests, google-auth.
  pip install google-auth requests
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import service_account

SCOPE = "https://www.googleapis.com/auth/androidpublisher"
BASE = "https://androidpublisher.googleapis.com/androidpublisher/v3"
UPLOAD_BASE = "https://androidpublisher.googleapis.com/upload/androidpublisher/v3"

IMAGE_TYPES = {
    "phoneScreenshots",
    "sevenInchScreenshots",
    "tenInchScreenshots",
    "tvScreenshots",
    "wearScreenshots",
}


def auth_token(creds_path: str) -> str:
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=[SCOPE]
    )
    creds.refresh(GoogleAuthRequest())
    return creds.token


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--credentials", default=os.environ.get("PLAY_CREDENTIALS"))
    ap.add_argument("--package", required=True, help="e.g. com.example.myapp")
    ap.add_argument("--locale", required=True, help="BCP-47, e.g. en-US, zh-CN")
    ap.add_argument(
        "--image-type", required=True, choices=sorted(IMAGE_TYPES), dest="image_type"
    )
    ap.add_argument("--dir", required=True, help="directory of *.png files (uploaded in sorted-filename order)")
    ap.add_argument(
        "--keep-existing",
        action="store_true",
        help="append instead of replacing existing images in this slot",
    )
    args = ap.parse_args()

    if not args.credentials:
        sys.exit("missing --credentials (or PLAY_CREDENTIALS env var)")
    pngs = sorted(Path(args.dir).glob("*.png"))
    if not pngs:
        sys.exit(f"no PNGs in {args.dir}")

    token = auth_token(args.credentials)
    h = {"Authorization": f"Bearer {token}"}
    edits_url = f"{BASE}/applications/{args.package}/edits"
    upload_edits_url = f"{UPLOAD_BASE}/applications/{args.package}/edits"

    r = requests.post(edits_url, headers=h)
    r.raise_for_status()
    edit_id = r.json()["id"]
    print(f"edit {edit_id}")

    listing_path = f"/{edit_id}/listings/{args.locale}/{args.image_type}"

    if not args.keep_existing:
        r = requests.delete(f"{edits_url}{listing_path}", headers=h)
        # 200/204 ok; 404 means nothing to clear
        if r.status_code not in (200, 204, 404):
            sys.exit(f"DELETE {listing_path} → {r.status_code}\n{r.text}")
        print(f"  cleared {args.locale}/{args.image_type}")

    for p in pngs:
        data = p.read_bytes()
        url = f"{upload_edits_url}{listing_path}?uploadType=media"
        r = requests.post(
            url,
            headers={**h, "Content-Type": "image/png"},
            data=data,
        )
        if not r.ok:
            sys.exit(f"upload {p.name} → {r.status_code}\n{r.text}")
        print(f"  uploaded {p.name}")

    r = requests.post(f"{edits_url}/{edit_id}:commit", headers=h)
    if not r.ok:
        sys.exit(f"commit edit → {r.status_code}\n{r.text}")
    print(f"done — committed {len(pngs)} images to {args.locale}/{args.image_type}")


if __name__ == "__main__":
    main()
