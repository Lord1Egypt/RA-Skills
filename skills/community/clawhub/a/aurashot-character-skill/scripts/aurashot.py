#!/usr/bin/env python3
"""AuraShot AI Character Design Platform — Agent Skill client."""
import argparse
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error, parse, request

DEFAULT_BASE_URL = "https://www.aurashot.art"
SIGNUP_URL = "https://www.aurashot.art/login"
KEYS_URL = "https://www.aurashot.art/studio?tab=keys"

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

CONFIG_FILE_NAME = ".aurashot.env"


def _find_config_file() -> Optional[Path]:
    """Walk up from cwd looking for .aurashot.env, also check ~/."""
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        candidate = d / CONFIG_FILE_NAME
        if candidate.is_file():
            return candidate
    home = Path.home() / CONFIG_FILE_NAME
    if home.is_file():
        return home
    return None


def _load_config_file() -> Dict[str, str]:
    """Load key=value pairs from .aurashot.env file."""
    path = _find_config_file()
    if not path:
        return {}
    result: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def resolve_key() -> str:
    # 1. Environment variables (highest priority)
    for name in ("AURASHOT_API_KEY", "AURASHOT_STUDIO_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value

    # 2. Local config file (.aurashot.env)
    config = _load_config_file()
    for name in ("AURASHOT_API_KEY", "AURASHOT_STUDIO_KEY"):
        value = config.get(name, "").strip()
        if value:
            return value

    print(
        json.dumps(
            {
                "error": "Missing AuraShot API key.",
                "message": "Set AURASHOT_API_KEY or AURASHOT_STUDIO_KEY before running this skill.",
                "signupUrl": SIGNUP_URL,
                "keysUrl": KEYS_URL,
            },
            ensure_ascii=False,
            indent=2,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def base_url_from_args(args: argparse.Namespace) -> str:
    return (args.base_url or os.environ.get("AURASHOT_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------

def is_remote_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def to_local_path(value: str) -> Path:
    if value.startswith("file://"):
        return Path(parse.unquote(parse.urlparse(value).path)).expanduser()
    return Path(value).expanduser()


def encode_multipart(field_name: str, file_path: Path) -> tuple:
    boundary = f"----AuraShot{uuid.uuid4().hex}"
    filename = file_path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    body = b"".join([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode(),
        f"Content-Type: {content_type}\r\n\r\n".encode(),
        file_path.read_bytes(),
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return body, boundary


def upload_file(file_path: Path, api_key: str, base_url: str = DEFAULT_BASE_URL) -> str:
    """Upload a local image via AuraShot /v1/uploads and return the public URL."""
    body, boundary = encode_multipart("file", file_path)
    req = request.Request(
        f"{base_url}/v1/uploads",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    opener = _build_url_opener()
    try:
        with opener.open(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "ignore")
        raise SystemExit(json.dumps(
            {"error": "Image upload failed.", "status": exc.code, "detail": detail, "path": str(file_path)},
            ensure_ascii=False, indent=2,
        ))
    except error.URLError as exc:
        raise SystemExit(json.dumps(
            {"error": "Image upload failed.", "detail": str(exc.reason), "path": str(file_path)},
            ensure_ascii=False, indent=2,
        ))

    result = json.loads(raw)
    url = result.get("url")
    if not isinstance(url, str) or not url.strip():
        raise SystemExit(json.dumps(
            {"error": "Image upload failed.", "detail": "No URL in response.", "raw": result},
            ensure_ascii=False, indent=2,
        ))
    return url


def resolve_image(value: Optional[str], api_key: str, field: str, base_url: str = DEFAULT_BASE_URL) -> Optional[str]:
    if not value:
        return None
    v = value.strip()
    if is_remote_url(v):
        return v
    p = to_local_path(v)
    if p.exists() and p.is_file():
        print(f"[aurashot] Uploading local file for {field}: {p}", file=sys.stderr)
        return upload_file(p, api_key, base_url)
    raise SystemExit(json.dumps(
        {"error": f"Invalid {field}.", "message": "Use a public URL or an existing local file path.", "value": v},
        ensure_ascii=False, indent=2,
    ))


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _build_url_opener() -> request.OpenerDirector:
    """Build a URL opener with proxy support and relaxed SSL for compatibility."""
    import ssl
    ctx = ssl.create_default_context()
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    except AttributeError:
        pass
    https_handler = request.HTTPSHandler(context=ctx)
    proxy_handler = request.ProxyHandler()  # reads *_proxy env vars automatically
    return request.build_opener(proxy_handler, https_handler)


def download_image(url: str, output_path: Path) -> Path:
    """Download an image URL to a local file path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    req = request.Request(url, method="GET")
    req.add_header("User-Agent", "AuraShot-Skill/1.0")
    opener = _build_url_opener()
    try:
        with opener.open(req, timeout=120) as resp:
            data = resp.read()
            if len(data) < 1024:
                raise SystemExit(json.dumps(
                    {"error": "Downloaded image too small.", "size": len(data), "url": url},
                    ensure_ascii=False, indent=2,
                ))
            output_path.write_bytes(data)
            print(f"[aurashot] Downloaded {len(data)} bytes → {output_path}", file=sys.stderr)
            return output_path
    except error.HTTPError as exc:
        raise SystemExit(json.dumps(
            {"error": "Image download failed.", "status": exc.code, "url": url},
            ensure_ascii=False, indent=2,
        ))
    except error.URLError as exc:
        # Retry once with unverified SSL as fallback (some CDNs have cert issues)
        import ssl
        try:
            ctx = ssl._create_unverified_context()
            with request.urlopen(req, timeout=120, context=ctx) as resp:
                data = resp.read()
                if len(data) < 1024:
                    raise SystemExit(json.dumps(
                        {"error": "Downloaded image too small.", "size": len(data), "url": url},
                        ensure_ascii=False, indent=2,
                    ))
                output_path.write_bytes(data)
                print(f"[aurashot] Downloaded {len(data)} bytes → {output_path} (SSL fallback)", file=sys.stderr)
                return output_path
        except Exception:
            pass
        raise SystemExit(json.dumps(
            {"error": "Image download failed.", "detail": str(exc.reason), "url": url},
            ensure_ascii=False, indent=2,
        ))


def maybe_download_outputs(result: Dict[str, Any], output_dir: Optional[str]) -> Dict[str, Any]:
    """If --output is set and result has output URLs, download them and add local paths.

    Download failures are captured in the result JSON instead of crashing the script,
    so the Agent can fall back to remote URLs.
    """
    if not output_dir:
        return result
    outputs = result.get("outputs", [])
    if not outputs:
        return result
    out_path = Path(output_dir).expanduser()
    downloaded = []
    download_errors = []
    for i, item in enumerate(outputs):
        url = item.get("url", "")
        if not url or not is_remote_url(url):
            continue
        # Derive filename from URL or use index
        url_path = parse.urlparse(url).path
        fname = Path(url_path).name if url_path else f"output_{i}.png"
        try:
            local = download_image(url, out_path / fname)
            downloaded.append({"url": url, "localPath": str(local)})
        except SystemExit:
            # download_image raises SystemExit on failure — catch it so the
            # script can still return the remote URL for the Agent to use.
            download_errors.append({
                "url": url,
                "error": "Download failed. The remote URL is still valid — provide it to the user directly."
            })
            print(f"[aurashot] WARNING: Failed to download {url}, remote URL still available", file=sys.stderr)
    if downloaded:
        result["downloaded"] = downloaded
    if download_errors:
        result["downloadErrors"] = download_errors
    return result


def make_request(method: str, url: str, api_key: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    req = request.Request(url, data=body, headers=headers, method=method)
    opener = _build_url_opener()
    try:
        with opener.open(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "ignore")
        raise SystemExit(json.dumps({"error": "AuraShot request failed.", "status": exc.code, "detail": detail}, ensure_ascii=False, indent=2))
    except error.URLError as exc:
        raise SystemExit(json.dumps({"error": "AuraShot request failed.", "detail": str(exc.reason)}, ensure_ascii=False, indent=2))




# ---------------------------------------------------------------------------
# Commands — Legacy (aesthetic workflows)
# ---------------------------------------------------------------------------

def cmd_generate(args: argparse.Namespace) -> None:
    api_key = resolve_key()
    base_url = base_url_from_args(args)

    if args.workflow == "virtual_try_on":
        for flag, name in [("--product-image", "product_image"), ("--model-image", "model_image"), ("--scene-image", "scene_image")]:
            if not getattr(args, name, None):
                raise SystemExit(json.dumps({"error": f"virtual_try_on requires {flag}."}, ensure_ascii=False, indent=2))

        description_type = "custom" if args.description else "auto"
        payload: Dict[str, Any] = {
            "workflow": "virtual_try_on",
            "waitForResult": args.wait,
            "input": {
                "productImage": resolve_image(args.product_image, api_key, "productImage", base_url),
                "modelImage": resolve_image(args.model_image, api_key, "modelImage", base_url),
                "sceneImage": resolve_image(args.scene_image, api_key, "sceneImage", base_url),
                "generateVersion": args.version or "weshopFlash",
                "descriptionType": description_type,
                **({"textDescription": args.description} if args.description else {}),
            },
        }

    else:  # pose_change
        if not args.original_image:
            raise SystemExit(json.dumps({"error": "pose_change requires --original-image."}, ensure_ascii=False, indent=2))
        if not args.description:
            raise SystemExit(json.dumps({"error": "pose_change requires --description."}, ensure_ascii=False, indent=2))

        payload = {
            "workflow": "pose_change",
            "waitForResult": args.wait,
            "input": {
                "originalImage": resolve_image(args.original_image, api_key, "originalImage", base_url),
                "generateVersion": args.version or "lite",
                "textDescription": args.description,
            },
        }

    result = make_request("POST", f"{base_url}/api/aesthetic/generate", api_key, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_query(args: argparse.Namespace) -> None:
    api_key = resolve_key()
    base_url = base_url_from_args(args)

    # Legacy aesthetic query
    if not args.workflow:
        raise SystemExit(json.dumps({"error": "query requires --workflow + --execution-id/--task-id (aesthetic)."}, ensure_ascii=False, indent=2))

    if not args.execution_id and not args.task_id:
        raise SystemExit(json.dumps({"error": "query requires --execution-id or --task-id."}, ensure_ascii=False, indent=2))

    payload = {
        "workflow": args.workflow,
        **({"executionId": args.execution_id} if args.execution_id else {}),
        **({"taskId": args.task_id} if args.task_id else {}),
    }
    result = make_request("POST", f"{base_url}/api/aesthetic/query", api_key, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Commands — Character design (new /v1/character/* endpoints)
# ---------------------------------------------------------------------------

def cmd_id_photo(args: argparse.Namespace) -> None:
    """Generate character ID photo (四合一)."""
    api_key = resolve_key()
    base_url = base_url_from_args(args)

    face_url = resolve_image(args.face_image, api_key, "face", base_url)
    if not face_url:
        raise SystemExit(json.dumps({"error": "id-photo requires --face-image."}, ensure_ascii=False, indent=2))

    payload: Dict[str, Any] = {
        "images": {"face": face_url},
        "waitForResult": args.wait,
    }
    if getattr(args, "description", None):
        payload["prompt"] = args.description

    result = make_request("POST", f"{base_url}/v1/character/id-photo", api_key, payload)
    result = maybe_download_outputs(result, getattr(args, "output", None))
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_edit(args: argparse.Namespace) -> None:
    """Edit an existing image with natural language description."""
    api_key = resolve_key()
    base_url = base_url_from_args(args)

    target_url = resolve_image(args.target_image, api_key, "target", base_url)
    if not target_url:
        raise SystemExit(json.dumps({"error": "edit requires --target-image."}, ensure_ascii=False, indent=2))

    if not args.description:
        raise SystemExit(json.dumps({"error": "edit requires --description."}, ensure_ascii=False, indent=2))

    payload: Dict[str, Any] = {
        "prompt": args.description,
        "images": {"target": target_url},
        "waitForResult": args.wait,
    }

    result = make_request("POST", f"{base_url}/v1/character/edit", api_key, payload)
    result = maybe_download_outputs(result, getattr(args, "output", None))
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_character_generate(args: argparse.Namespace) -> None:
    """Reference-driven character generation."""
    api_key = resolve_key()
    base_url = base_url_from_args(args)

    face_url = resolve_image(args.face_image, api_key, "face", base_url)
    if not face_url:
        raise SystemExit(json.dumps({"error": "character-generate requires --face-image."}, ensure_ascii=False, indent=2))

    if not args.description:
        raise SystemExit(json.dumps({"error": "character-generate requires --description."}, ensure_ascii=False, indent=2))

    images: Dict[str, Any] = {"face": face_url}
    clothes_url = resolve_image(getattr(args, "clothes_image", None), api_key, "clothes", base_url)
    if clothes_url:
        images["clothes"] = clothes_url
    scene_url = resolve_image(getattr(args, "scene_image", None), api_key, "scene", base_url)
    if scene_url:
        images["scene"] = scene_url

    payload: Dict[str, Any] = {
        "prompt": args.description,
        "images": images,
        "waitForResult": args.wait,
    }

    result = make_request("POST", f"{base_url}/v1/character/generate", api_key, payload)
    result = maybe_download_outputs(result, getattr(args, "output", None))
    print(json.dumps(result, ensure_ascii=False, indent=2))



# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AuraShot AI Character Design Platform — Agent Skill client")
    parser.add_argument("--base-url", dest="base_url", default=None)
    subs = parser.add_subparsers(dest="command", required=True)

    # --- Character design commands (new) ---

    id_photo = subs.add_parser("id-photo", help="Generate character ID photo (四合一)")
    id_photo.add_argument("--face-image", dest="face_image", required=True, help="Face image URL or local path")
    id_photo.add_argument("--description", dest="description", default=None, help="Custom prompt for ID photo generation (e.g. anime style)")
    id_photo.add_argument("--output", dest="output", default=None, help="Directory to download result images to")
    id_photo.add_argument("--wait", action="store_true", help="Block until job completes")
    id_photo.set_defaults(func=cmd_id_photo)

    edit = subs.add_parser("edit", help="Edit an existing image")
    edit.add_argument("--target-image", dest="target_image", required=True, help="Target image URL or local path")
    edit.add_argument("--description", dest="description", required=True, help="Natural language edit description")
    edit.add_argument("--output", dest="output", default=None, help="Directory to download result images to")
    edit.add_argument("--wait", action="store_true", help="Block until job completes")
    edit.set_defaults(func=cmd_edit)

    char_gen = subs.add_parser("character-generate", help="Reference-driven character generation")
    char_gen.add_argument("--face-image", dest="face_image", required=True, help="Face image URL or local path")
    char_gen.add_argument("--description", dest="description", required=True, help="Natural language generation description")
    char_gen.add_argument("--clothes-image", dest="clothes_image", default=None, help="Clothes reference image URL or local path")
    char_gen.add_argument("--scene-image", dest="scene_image", default=None, help="Scene reference image URL or local path")
    char_gen.add_argument("--output", dest="output", default=None, help="Directory to download result images to")
    char_gen.add_argument("--wait", action="store_true", help="Block until job completes")
    char_gen.set_defaults(func=cmd_character_generate)

    # --- Legacy aesthetic commands (kept for backward compatibility) ---

    gen = subs.add_parser("generate", help="Submit an aesthetic workflow job (legacy)")
    gen.add_argument("--workflow", choices=["virtual_try_on", "pose_change"], required=True)
    gen.add_argument("--product-image", dest="product_image")
    gen.add_argument("--model-image", dest="model_image")
    gen.add_argument("--scene-image", dest="scene_image")
    gen.add_argument("--original-image", dest="original_image")
    gen.add_argument("--description", dest="description")
    gen.add_argument("--version", dest="version")
    gen.add_argument("--wait", action="store_true", help="Block until job completes")
    gen.set_defaults(func=cmd_generate)

    # --- Query (legacy aesthetic only) ---

    qry = subs.add_parser("query", help="Query a job status")
    qry.add_argument("--workflow", choices=["virtual_try_on", "pose_change"], required=True)
    qry.add_argument("--execution-id", dest="execution_id")
    qry.add_argument("--task-id", dest="task_id")
    qry.set_defaults(func=cmd_query)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
