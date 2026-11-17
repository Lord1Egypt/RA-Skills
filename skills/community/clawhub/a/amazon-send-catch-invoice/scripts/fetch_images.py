#!/usr/bin/env python3
"""Fetch and normalise product photos for the customs invoice.

    python3 fetch_images.py images.json           # {"<key>": "<image url>", ...}
    python3 fetch_images.py images.json --size 48
    python3 fetch_images.py --list                # show what is already cached

Writes `<key>.bmp` into the per-user cache directory (see paths.py). BMP because
xlwt — the only library that can write the .xls format the portal template uses
— accepts nothing else.

    pip3 install pillow

Two rules that matter
---------------------
1. CONTAIN, never COVER. Amazon main images are often not square. A centre crop
   of a 1500x1029 image cuts 16% off each side, so the product looks blown up
   and clipped — which reads as "stretched" to whoever reviews the invoice.
   Scale uniformly and pad with white. Amazon main images are already on white,
   so the padding is invisible.

2. Write equal X/Y DPI into the BMP header. Excel reads the header DPI when it
   places a bitmap; mismatched axes distort the image before your row/column
   sizing ever gets a say.

Where to get the URLs
---------------------
Use the SP-API catalog, not a scraped og:image (which is a small, sometimes
wrong variant):

    GET /catalog/2022-04-01/items/{ASIN}?marketplaceIds=<mk>&includedData=images
    -> images[0].images, pick variant == "MAIN" with the largest height

Some items have no main image in the catalog. Do not substitute an unrelated
photo — use another product from the same declaration line, or ask the user for
a real photo of the goods. A photo that does not match the goods is worse than
a plain one at inspection.
"""
from __future__ import annotations

import argparse
import io
import json
import struct
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import cache_dir  # noqa: E402

DEFAULT_SIZE = 48


def fit_square(img, size=DEFAULT_SIZE, bg=(255, 255, 255)):
    """Letterbox onto a square canvas — never crop, never stretch."""
    from PIL import Image
    w, h = img.size
    k = min(size / w, size / h)                 # min = contain; max would be cover
    nw, nh = max(1, round(w * k)), max(1, round(h * k))
    canvas = Image.new("RGB", (size, size), bg)
    canvas.paste(img.resize((nw, nh), Image.LANCZOS), ((size - nw) // 2, (size - nh) // 2))
    return canvas


def patch_bmp_dpi(path: Path, dpi=96):
    """Write equal X/Y pixels-per-metre into the BMP header."""
    ppm = int(dpi / 0.0254)                     # 96 dpi -> 3780 ppm
    with open(path, "r+b") as f:
        f.seek(38)
        f.write(struct.pack("<i", ppm))
        f.seek(42)
        f.write(struct.pack("<i", ppm))


def fetch(key: str, url: str, size=DEFAULT_SIZE, force=False) -> Path | None:
    from PIL import Image
    out = cache_dir() / f"{key}.bmp"
    if out.exists() and not force:
        return out
    try:
        if url.startswith(("http://", "https://")):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
            img = Image.open(io.BytesIO(data))
        else:
            img = Image.open(Path(url).expanduser())     # local file path
        fit_square(img.convert("RGB"), size).save(out, "BMP")
        patch_bmp_dpi(out)
        return out
    except Exception as e:                               # noqa: BLE001
        print(f"  ! failed {key}: {e}")
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="?", help='JSON: {"<key>": "<url or local path>"}')
    ap.add_argument("--size", type=int, default=DEFAULT_SIZE)
    ap.add_argument("--force", action="store_true", help="re-download cached entries")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list or not args.images:
        cached = sorted(cache_dir().glob("*.bmp"))
        print(f"{len(cached)} cached in {cache_dir()}")
        for p in cached:
            print(f"  {p.name}")
        return

    mapping = json.loads(Path(args.images).read_text(encoding="utf-8"))
    ok = 0
    for key, url in mapping.items():
        p = fetch(key, url, args.size, args.force)
        print(f"  {key} {'ok' if p else 'FAILED'}")
        ok += bool(p)
    print(f"\n{ok}/{len(mapping)} images in {cache_dir()}")


if __name__ == "__main__":
    main()
