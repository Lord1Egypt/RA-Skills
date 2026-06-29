"""Download 8 public-domain landmark photos from Wikimedia and strip EXIF.

Run once before executing the end-to-end test.

The exact Wikimedia thumbnail URLs are pinned to keep the test reproducible.
If Wikimedia rotates the underlying file, update the URL here and bump the
filename mapping below.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import piexif
from PIL import Image


# (filename in e2e/landmarks/, source URL on Wikimedia thumbnails)
LANDMARKS = [
    ("01_eiffel.jpg",   "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg/960px-Tour_Eiffel_Wikimedia_Commons.jpg"),
    ("02_liberty.jpg",  "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Statue_of_Liberty_7.jpg/960px-Statue_of_Liberty_7.jpg"),
    ("03_opera.jpg",    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Sydney_Opera_House_-_Dec_2008.jpg/960px-Sydney_Opera_House_-_Dec_2008.jpg"),
    ("04_greatwall.jpg","https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Great_Wall_of_China_at_Jinshanling-edit.jpg/960px-The_Great_Wall_of_China_at_Jinshanling-edit.jpg"),
    ("05_tajmahal.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/960px-Taj_Mahal_%28Edited%29.jpeg"),
    ("06_colosseum.jpg","https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/960px-Colosseo_2020.jpg"),
    ("07_christ.jpg",   "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Christ_the_Redeemer_-_Cristo_Redentor.jpg/960px-Christ_the_Redeemer_-_Cristo_Redentor.jpg"),
    ("08_bigben.jpg",   "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/London_Parliament_2007-1.jpg/960px-London_Parliament_2007-1.jpg"),
]

USER_AGENT = "geo-tag-photos-e2e/1.0 (https://github.com/ucsdzehualiu/my_openclaw_skill)"


def _download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=60) as resp:
        return resp.read()


def _strip_exif_to_jpg(blob: bytes, dest: Path) -> None:
    img = Image.open(io.BytesIO(blob)).convert("RGB")
    # Strip everything by saving without exif=, then verify with piexif.
    img.save(dest, "JPEG", quality=88)
    # Belt and braces: explicitly remove any residual EXIF.
    try:
        piexif.remove(str(dest))
    except Exception:
        pass


def main() -> int:
    out_dir = Path(__file__).parent / "landmarks"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, url in LANDMARKS:
        target = out_dir / name
        if target.exists():
            print(f"[skip] {name} (already exists)")
            continue
        print(f"[get ] {name}")
        try:
            blob = _download(url)
        except Exception as e:
            print(f"[fail] {name}: {e}", file=sys.stderr)
            return 1
        _strip_exif_to_jpg(blob, target)
        print(f"[ok  ] {target}")
    print(f"\nDone. Landmarks at: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
