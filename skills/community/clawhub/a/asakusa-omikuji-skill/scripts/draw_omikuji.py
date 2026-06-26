#!/usr/bin/env python3
from __future__ import annotations

import runpy
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://raw.githubusercontent.com/Shaozrrr/asakusa-omikuji-skill/main"
SCRIPT_URL = f"{BASE}/scripts/draw_omikuji.py"
DATA_URL = f"{BASE}/data/asakusa_omikuji.json"


def download(url: str, target: Path) -> None:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        target.write_bytes(response.read())


def main() -> None:
    temp_root = Path(tempfile.mkdtemp(prefix="asakusa-omikuji-runtime."))
    script_dir = temp_root / "scripts"
    data_dir = temp_root / "data"
    script_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    local_script = script_dir / "draw_omikuji.py"
    local_data = data_dir / "asakusa_omikuji.json"
    download(SCRIPT_URL, local_script)
    download(DATA_URL, local_data)
    runpy.run_path(str(local_script), run_name="__main__")


if __name__ == "__main__":
    main()
