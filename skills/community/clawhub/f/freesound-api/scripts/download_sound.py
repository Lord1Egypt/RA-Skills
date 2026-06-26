import argparse
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import requests

from api_utils import get_auth_headers_and_params, get_json


def infer_extension(info: dict, response: requests.Response) -> str:
    original = info.get("original_filename") or ""
    suffix = Path(original).suffix
    if suffix:
        return suffix
    name = info.get("name") or ""
    suffix = Path(name).suffix
    if suffix:
        return suffix
    content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip()
    guessed = mimetypes.guess_extension(content_type) if content_type else None
    if guessed:
        return guessed
    path_suffix = Path(urlparse(str(response.url)).path).suffix
    if path_suffix:
        return path_suffix
    sound_type = info.get("type")
    if sound_type:
        return f'.{sound_type}'
    return ".bin"


def safe_name(info: dict, response: requests.Response) -> str:
    original = info.get("original_filename") or ""
    if original and Path(original).suffix:
        return original
    base = info.get("name") or f"sound-{info.get('id', 'unknown')}"
    ext = infer_extension(info, response)
    if not Path(base).suffix:
        base = f"{base}{ext}"
    return ''.join('_' if ch in '<>:"/\\|?*' else ch for ch in base)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a Freesound sound by ID.")
    parser.add_argument("sound_id", type=int)
    parser.add_argument("--out-dir", default=".")
    parser.add_argument("--preview", choices=["hq-mp3", "lq-mp3", "hq-ogg", "lq-ogg"])
    args = parser.parse_args()

    info = get_json(
        f"/sounds/{args.sound_id}/",
        {"fields": "id,name,original_filename,type,download,previews"},
    )

    if args.preview:
        key = f"preview-{args.preview}"
        download_url = (info.get("previews") or {}).get(key)
        if not download_url:
            raise SystemExit(f"Preview URL not available for {key}.")
    else:
        download_url = info.get("download")
        if not download_url:
            raise SystemExit("No download URL returned for this sound.")

    headers, params = get_auth_headers_and_params()
    response = requests.get(download_url, headers=headers, params=params, stream=True, timeout=60)
    response.raise_for_status()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_name(info, response)
    out_path = out_dir / filename

    with out_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            if chunk:
                f.write(chunk)

    print(out_path)


if __name__ == "__main__":
    main()
