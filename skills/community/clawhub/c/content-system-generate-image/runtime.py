from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency fallback
    yaml = None


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IMAGE_PROVIDER = "openai"
DEFAULT_IMAGE_API_BASE = "https://new.suxi.ai/v1"
DEFAULT_IMAGE_MODEL = "nano-nx"
DEFAULT_IMAGE_MODEL_SOURCE = "generate-image skill default"
SUXI_LOGIN_URL = "https://job.suxi.ai/"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def run_json_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    env_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    env = os.environ.copy()
    if env_overrides:
        env.update({key: value for key, value in env_overrides.items() if str(value or "").strip()})
    result = subprocess.run(
        args,
        check=False,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        env=env,
    )
    payload_text = (result.stdout or "").strip() or (result.stderr or "").strip()
    if not payload_text:
        raise RuntimeError("Command returned no output.")
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        raise RuntimeError(payload_text) from error
    if result.returncode != 0 or payload.get("success") is False:
        raise RuntimeError(str(payload.get("error") or payload.get("message") or "Command failed."))
    return payload


def usable_generated_asset_url(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme in {"http", "https"}:
        return raw
    if raw.startswith("//"):
        return raw

    local_value = unquote(parsed.path) if parsed.scheme == "file" else raw
    local_path = Path(local_value).expanduser()
    if local_path.exists() and local_path.is_file():
        return str(local_path)
    return ""


def download_binary(url: str, output_path: Path) -> None:
    ensure_parent(output_path)
    value = str(url or "").strip()
    if not value:
        raise RuntimeError("下载图片失败：缺少可用地址。")

    parsed = urlparse(value)
    if parsed.scheme in {"", "file"}:
        local_value = unquote(parsed.path) if parsed.scheme == "file" else value
        local_path = Path(local_value).expanduser()
        if local_path.exists() and local_path.is_file():
            output_path.write_bytes(local_path.read_bytes())
            return

    request = urllib.request.Request(value, headers={"User-Agent": "content-factory/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            output_path.write_bytes(response.read())
    except urllib.error.URLError as error:
        raise RuntimeError(f"下载图片失败：{error}") from error


def compose_image_style(base_style: str, custom_prompt: str) -> str:
    custom = str(custom_prompt or "").strip()
    if not custom:
        return base_style
    base = str(base_style or "").strip()
    if "【用户补充】" in base:
        prefix = base.split("【用户补充】", 1)[0].rstrip()
        return f"{prefix}\n\n【用户补充】\n{custom}"
    return f"{base}\n\n【用户补充】\n{custom}"


def split_frontmatter_text(markdown_text: str) -> tuple[str, str]:
    text = markdown_text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def load_article_frontmatter(article_path: Path) -> dict[str, Any]:
    if yaml is None or not article_path.exists() or not article_path.is_file():
        return {}
    try:
        text = article_path.read_text(encoding="utf-8")
    except OSError:
        return {}
    frontmatter_text, _body = split_frontmatter_text(text)
    if not frontmatter_text.strip():
        return {}
    try:
        payload = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def clean_optional_value(value: Any) -> str:
    return str(value or "").strip()


def default_image_backend() -> dict[str, str]:
    return {
        "provider": DEFAULT_IMAGE_PROVIDER,
        "apiBase": DEFAULT_IMAGE_API_BASE,
        "model": DEFAULT_IMAGE_MODEL,
        "modelSource": DEFAULT_IMAGE_MODEL_SOURCE,
        "loginUrl": SUXI_LOGIN_URL,
    }


def resolve_image_backend(
    *,
    article_path: Path,
    image_provider: str | None = None,
    image_api_base: str | None = None,
    image_model: str | None = None,
) -> dict[str, str]:
    defaults = default_image_backend()
    frontmatter = load_article_frontmatter(article_path)
    frontmatter_provider = clean_optional_value(frontmatter.get("image_provider"))
    frontmatter_api_base = clean_optional_value(frontmatter.get("image_api_base"))
    frontmatter_model = clean_optional_value(frontmatter.get("image_model"))
    requested_provider = clean_optional_value(image_provider)
    requested_api_base = clean_optional_value(image_api_base)
    requested_model = clean_optional_value(image_model)

    provider = requested_provider or frontmatter_provider or defaults["provider"]
    api_base = requested_api_base or frontmatter_api_base or defaults["apiBase"]
    model = requested_model or frontmatter_model or defaults["model"]

    if requested_model:
        model_source = "request override"
    elif frontmatter_model:
        model_source = "article frontmatter"
    else:
        model_source = defaults["modelSource"]

    return {
        "provider": provider,
        "apiBase": api_base,
        "model": model,
        "modelSource": model_source,
        "loginUrl": defaults["loginUrl"],
    }


def generate_image_asset(
    *,
    title: str,
    summary: str,
    article_path: Path,
    preset: str,
    style: str,
    workspace_root: Path | None = None,
    image_provider: str | None = None,
    image_api_base: str | None = None,
    image_model: str | None = None,
) -> dict[str, Any]:
    image_backend = resolve_image_backend(
        article_path=article_path,
        image_provider=image_provider,
        image_api_base=image_api_base,
        image_model=image_model,
    )
    command = [
        "md2wechat",
        "generate_image",
        "--preset",
        preset,
        "--title",
        title,
        "--summary",
        summary,
        "--article",
        str(article_path.resolve()),
        "--style",
        style,
        "--model",
        image_backend["model"],
        "--json",
    ]
    payload = run_json_command(
        command,
        cwd=workspace_root or WORKSPACE_ROOT,
        env_overrides={
            "IMAGE_PROVIDER": image_backend["provider"],
            "IMAGE_API_BASE": image_backend["apiBase"],
            "IMAGE_MODEL": image_backend["model"],
        },
    )
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        data = {}
    original_url = str(data.get("original_url", "")).strip()
    wechat_url = str(data.get("wechat_url", "")).strip()
    preview_url = usable_generated_asset_url(original_url) or usable_generated_asset_url(wechat_url)
    draft_url = usable_generated_asset_url(wechat_url) or usable_generated_asset_url(original_url)
    if not preview_url and not draft_url:
        raise RuntimeError("图片生成成功，但没有返回可用地址。")
    return {
        "prompt": str(data.get("prompt", "")).strip(),
        "previewUrl": preview_url,
        "draftUrl": draft_url,
        "mediaId": str(data.get("media_id", "")).strip(),
        "width": data.get("width"),
        "height": data.get("height"),
        "provider": image_backend["provider"],
        "apiBase": image_backend["apiBase"],
        "model": image_backend["model"],
        "modelSource": image_backend["modelSource"],
    }
