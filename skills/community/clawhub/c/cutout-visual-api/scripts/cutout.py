"""
Cutout.Pro Visual API Skill — Main Script

Supports: Background Removal, Face Cutout, Photo Enhancement.
Accepts both local file upload and image URL as input.
Returns binary stream or Base64-encoded results.

Usage:
    python cutout.py --api bg-remover --image photo.jpg --output out.png
    python cutout.py --api bg-remover --url "https://example.com/photo.jpg"
    python cutout.py --api bg-remover --image photo.jpg --crop --bgcolor FFFFFF
    python cutout.py --api face-cutout --image portrait.jpg --base64 --face-analysis
    python cutout.py --api photo-enhancer --image blurry.jpg --face-model anime
    python cutout.py --api bg-remover --image photo.jpg --preview

Version: 1.0.0
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))

from config import (
    API_BASE,
    ENDPOINTS,
    MATTING_TYPE,
    OUTPUT_DIR,
    OUTPUT_SETTINGS,
    USER_AGENT,
    get_api_key,
    validate_image_file,
)


# ── Exceptions ────────────────────────────────────────────────────────────────


class APIError(Exception):
    """Generic Cutout.Pro API error."""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(APIError):
    """Invalid or missing API Key."""
    pass


class InsufficientCreditsError(APIError):
    """Insufficient account balance."""
    pass


class RateLimitError(APIError):
    """Rate limit exceeded (429)."""
    pass


# ── API Calls ─────────────────────────────────────────────────────────────────


def _call_api_upload(
    endpoint: str,
    api_key: str,
    image_path: Path,
    params: dict,
    timeout: int = 120,
) -> tuple[bytes | dict, str]:
    """
    File upload API call (POST multipart/form-data).

    Returns (data, content_type):
    - Binary mode: data = bytes
    - Base64 mode: data = dict (parsed JSON)
    """
    url = f"{API_BASE}{endpoint}"
    headers = {
        "APIKEY": api_key,
        "User-Agent": USER_AGENT,
    }

    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        resp = requests.post(
            url,
            params=params,
            files=files,
            headers=headers,
            timeout=timeout,
        )

    _raise_for_status(resp)
    content_type = resp.headers.get("Content-Type", "")
    if "application/json" in content_type:
        return resp.json(), "application/json"
    return resp.content, content_type


def _call_api_url(
    endpoint: str,
    api_key: str,
    image_url: str,
    params: dict,
    timeout: int = 120,
) -> tuple[dict, str]:
    """
    Image URL API call (GET).

    Returns (data, "application/json").
    """
    url = f"{API_BASE}{endpoint}"
    headers = {
        "APIKEY": api_key,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    all_params = {"url": image_url, **params}

    resp = requests.get(url, params=all_params, headers=headers, timeout=timeout)
    _raise_for_status(resp)
    return resp.json(), "application/json"


def _raise_for_status(resp: requests.Response) -> None:
    """Raise the appropriate exception based on HTTP status code."""
    if resp.status_code == 200:
        return
    try:
        body = resp.json()
        msg = body.get("msg") or json.dumps(body, ensure_ascii=False)
    except Exception:
        msg = resp.text[:300]

    if resp.status_code == 401:
        raise AuthenticationError(f"Invalid or missing API Key: {msg}", resp.status_code)
    if resp.status_code == 429:
        raise RateLimitError(f"Rate limit exceeded: {msg}", resp.status_code)
    # Business error codes
    try:
        code = resp.json().get("code", 0)
        if code == 1001:
            raise InsufficientCreditsError(f"Insufficient balance: {msg}", code)
    except (InsufficientCreditsError, AuthenticationError, RateLimitError):
        raise
    except Exception:
        pass
    raise APIError(f"HTTP {resp.status_code}: {msg}", resp.status_code)


# ── Core Processing ───────────────────────────────────────────────────────────


def process_image(
    api: str,
    image_path: str | None = None,
    image_url: str | None = None,
    output_path: Path | None = None,
    use_base64: bool = False,
    crop: bool = False,
    bgcolor: str | None = None,
    preview: bool = False,
    output_format: str = "png",
    crop_margin: str | None = None,
    face_analysis: bool = False,
    face_model: str = "quality",
    api_key: str | None = None,
) -> dict:
    """
    Call the Cutout.Pro API to process an image.

    Returns a result dictionary:
    {
        "path": Path | None,           # Saved file path (binary mode)
        "base64": str | None,          # Base64 string (Base64 mode)
        "face_analysis": dict | None,  # Facial landmarks (face-cutout only)
        "size_kb": float,
        "time_s": float,
    }
    """
    # Get API Key
    key = api_key or get_api_key()
    if not key:
        print(
            "\nError: CUTOUT_API_KEY not found!\n"
            "Add it to your .env file: CUTOUT_API_KEY=your_key_here\n"
            "Get your key at: https://www.cutout.pro/user/secret-key\n",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build request parameters
    params: dict = {}
    if api in ("bg-remover", "face-cutout"):
        params["mattingType"] = MATTING_TYPE[api]
        if crop:
            params["crop"] = "true"
        if bgcolor:
            params["bgcolor"] = bgcolor
        if preview:
            params["preview"] = "true"
        if output_format != "png":
            params["outputFormat"] = output_format
        if crop_margin:
            params["cropMargin"] = crop_margin
        if face_analysis and use_base64:
            params["faceAnalysis"] = "true"
    elif api == "photo-enhancer":
        if output_format != "png":
            params["outputFormat"] = output_format
        if face_model != "quality":
            params["faceModel"] = face_model

    # Select endpoint
    api_key_map = api.replace("-", "_")
    if image_url:
        endpoint_key = f"{api_key_map}_url"
    elif use_base64:
        endpoint_key = f"{api_key_map}_base64"
    else:
        endpoint_key = f"{api_key_map}_binary"

    endpoint = ENDPOINTS[endpoint_key]

    # Execute call with retry
    max_retries = 3
    start_time = time.time()
    data = None
    content_type = ""

    for attempt in range(max_retries):
        try:
            if image_url:
                data, content_type = _call_api_url(endpoint, key, image_url, params)
            else:
                validated = validate_image_file(image_path)
                data, content_type = _call_api_upload(endpoint, key, validated, params)
            break

        except AuthenticationError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        except InsufficientCreditsError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        except RateLimitError:
            wait = 15 * (attempt + 1)
            print(f"Rate limit exceeded. Retrying in {wait}s...", file=sys.stderr)
            time.sleep(wait)

        except APIError as e:
            if attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"Request failed. Retrying in {wait}s ({attempt + 1}/{max_retries})...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}", file=sys.stderr)
            if attempt >= max_retries - 1:
                sys.exit(1)
            time.sleep(5)

    elapsed = time.time() - start_time

    if data is None:
        print("Error: All retries failed.", file=sys.stderr)
        sys.exit(1)

    # Handle response
    result: dict = {
        "path": None,
        "base64": None,
        "face_analysis": None,
        "size_kb": 0.0,
        "time_s": round(elapsed, 1),
    }

    if isinstance(data, bytes):
        # Binary stream mode
        output_dir = output_path.parent if output_path else OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        if output_path:
            filepath = output_path
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = OUTPUT_DIR / f"{api}_{timestamp}.png"

        filepath.write_bytes(data)
        size_kb = len(data) / 1024
        result["path"] = filepath
        result["size_kb"] = round(size_kb, 1)

        # Save metadata
        if OUTPUT_SETTINGS["save_metadata"]:
            meta = {
                "api": api,
                "image_path": str(image_path) if image_path else None,
                "image_url": image_url,
                "params": params,
                "generation_time_seconds": round(elapsed, 2),
                "file_size_kb": round(size_kb, 1),
                "generated_at": datetime.now().isoformat(),
            }
            meta_path = filepath.parent / f"{filepath.name}.meta.json"
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    elif isinstance(data, dict):
        # Base64 / JSON mode
        resp_data = data.get("data", {})
        img_b64 = resp_data.get("imageBase64", "")
        result["base64"] = img_b64
        result["size_kb"] = round(len(img_b64) * 3 / 4 / 1024, 1)

        # Facial landmarks
        if "faceAnalysis" in resp_data:
            result["face_analysis"] = resp_data["faceAnalysis"]

        # If an output path is specified, decode and save
        if output_path and img_b64:
            import base64
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(base64.b64decode(img_b64))
            result["path"] = output_path

    return result


# ── CLI ───────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Cutout.Pro Visual API — Background Removal / Face Cutout / Photo Enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cutout.py --api bg-remover --image photo.jpg --output out.png\n"
            "  python cutout.py --api bg-remover --url \"https://example.com/photo.jpg\"\n"
            "  python cutout.py --api bg-remover --image photo.jpg --crop --bgcolor FFFFFF\n"
            "  python cutout.py --api face-cutout --image portrait.jpg --base64 --face-analysis\n"
            "  python cutout.py --api photo-enhancer --image blurry.jpg --face-model anime\n"
            "  python cutout.py --api bg-remover --image photo.jpg --preview\n"
        ),
    )

    # Required
    parser.add_argument(
        "--api",
        required=True,
        choices=["bg-remover", "face-cutout", "photo-enhancer"],
        help="Select API: bg-remover, face-cutout, or photo-enhancer",
    )

    # Input
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--image", type=str, help="Local image file path")
    input_group.add_argument("--url", type=str, help="Image URL (URL mode)")

    # Output
    parser.add_argument("--output", type=Path, default=None, help="Output file path (default: data/outputs/)")
    parser.add_argument("--base64", action="store_true", help="Return Base64 JSON instead of binary stream")
    parser.add_argument("--json", action="store_true", help="Output result info as JSON")

    # Background Remover / Face Cutout parameters
    parser.add_argument("--crop", action="store_true", help="Crop whitespace (bg-remover/face-cutout only)")
    parser.add_argument("--bgcolor", type=str, default=None, help="Background color, hex (e.g. FFFFFF) or blur")
    parser.add_argument("--preview", action="store_true", help="Preview mode, max 500×500, costs 0.25 credits")
    parser.add_argument("--output-format", type=str, default="png", help="Output format: png, webp, jpg_75, etc. (default: png)")
    parser.add_argument("--crop-margin", type=str, default=None, help="Crop margin, e.g. 30px or 10%% (only applies when --crop is set)")

    # Face Cutout exclusive
    parser.add_argument("--face-analysis", action="store_true", help="Return 68 facial landmark points (face-cutout --base64 only)")

    # Photo Enhancer exclusive
    parser.add_argument(
        "--face-model",
        type=str,
        default="quality",
        choices=["quality", "anime"],
        help="Enhancement model: quality (real photos, default) or anime (cartoon images)",
    )

    args = parser.parse_args()

    # URL mode forces Base64
    use_base64 = args.base64 or bool(args.url)

    print("=" * 55)
    print("  Cutout.Pro Visual API")
    print("=" * 55)
    print(f"  API:           {args.api}")
    if args.image:
        print(f"  Image:         {args.image}")
    if args.url:
        print(f"  Image URL:     {args.url}")
    if args.crop:
        print(f"  Crop:          Yes")
    if args.bgcolor:
        print(f"  Background:    {args.bgcolor}")
    if args.preview:
        print(f"  Preview mode:  Yes (0.25 credits)")
    if args.api == "photo-enhancer":
        print(f"  Model:         {args.face_model}")
    print("=" * 55)
    print()

    result = process_image(
        api=args.api,
        image_path=args.image,
        image_url=args.url,
        output_path=args.output,
        use_base64=use_base64,
        crop=args.crop,
        bgcolor=args.bgcolor,
        preview=args.preview,
        output_format=args.output_format,
        crop_margin=args.crop_margin,
        face_analysis=args.face_analysis,
        face_model=args.face_model,
    )

    if args.json:
        output_info = {
            "api": args.api,
            "path": str(result["path"]) if result["path"] else None,
            "has_base64": bool(result["base64"]),
            "has_face_analysis": bool(result["face_analysis"]),
            "size_kb": result["size_kb"],
            "time_s": result["time_s"],
        }
        print(json.dumps(output_info, indent=2, ensure_ascii=False))
    else:
        if result["path"]:
            print(f"✅ Image saved: {result['path']}")
            print(f"   Size: {result['size_kb']:.1f} KB")
        if result["base64"] and not result["path"]:
            print(f"✅ Base64 data received ({result['size_kb']:.1f} KB)")
            print(f"   First 64 chars: {result['base64'][:64]}...")
        if result["face_analysis"]:
            fa = result["face_analysis"]
            print(f"   Faces detected: {fa.get('face_num', 0)}")
            print(f"   Landmarks: {len(fa.get('point', [[]])[0]) if fa.get('point') else 0}")
        print(f"   Processing time: {result['time_s']}s")


if __name__ == "__main__":
    main()
