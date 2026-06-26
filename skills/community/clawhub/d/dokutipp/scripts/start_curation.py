#!/usr/bin/env python3
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"
FILMLISTE = DATA_DIR / "Filmliste-akt.xz"
DOWNLOAD_URL = "https://liste.mediathekview.de/Filmliste-akt.xz"
MAX_AGE_SECONDS = 24 * 3600


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


DATA_DIR.mkdir(exist_ok=True)


def needs_download():
    if not FILMLISTE.exists():
        return True
    return time.time() - FILMLISTE.stat().st_mtime > MAX_AGE_SECONDS


if needs_download():
    log("Downloading Filmliste-akt.xz ...")
    result = subprocess.run(["curl", "-fsSL", "-o", str(FILMLISTE), DOWNLOAD_URL])
    if result.returncode != 0:
        print("Error: Download of Filmliste-akt.xz failed.", file=sys.stderr)
        sys.exit(1)
    log("Download complete.")
else:
    log("Filmliste-akt.xz is fresh, skipping download.")

parser = Path(__file__).parent / "parse_filmliste.py"
log("Starting parse_filmliste.py ...")
subprocess.run(
    [sys.executable, str(parser), str(FILMLISTE), "--limit", "1337", "--min-duration", "42"],
    check=True,
)
