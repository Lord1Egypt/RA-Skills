from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

from skill_runtime.feishu_auth import (
    clean_text,
    load_user_token_cache,
    redirect_uri,
    run_browser_authorization,
    token_cache_path,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_timeout_seconds(input_path: Path) -> int:
    if not input_path.exists():
        return 300
    text = read_text(input_path)
    match = re.search(r"`?timeout_seconds`?\s*[：:]\s*(\d+)", text)
    if not match:
        return 300
    return max(int(match.group(1)), 30)


def build_manifest(
    *,
    input_path: Path,
    published_path: Path,
    status: str,
    cache: dict[str, Any] | None,
    error_message: str = "",
    auth_url: str = "",
    opened_browser: bool | None = None,
) -> str:
    lines = [
        "# 飞书用户授权结果",
        "",
        "## 基础信息",
        "",
        f"- `status`：{status}",
        f"- `input_path`：{input_path}",
        f"- `published_path`：{published_path}",
        f"- `redirect_uri`：{redirect_uri()}",
        f"- `cache_path`：{token_cache_path()}",
        f"- `generated_at`：{datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    if auth_url:
        lines.append(f"- `auth_url`：{auth_url}")
    if opened_browser is not None:
        lines.append(f"- `opened_browser`：{'yes' if opened_browser else 'no'}")
    if error_message:
        lines.extend(
            [
                "",
                "## 错误信息",
                "",
                f"- {error_message}",
            ]
        )
    if cache:
        lines.extend(
            [
                "",
                "## 授权结果",
                "",
                f"- `name`：{clean_text(cache.get('name') or cache.get('en_name')) or '未返回'}",
                f"- `open_id`：{clean_text(cache.get('open_id')) or '未返回'}",
                f"- `issued_at`：{clean_text(cache.get('issued_at')) or '未返回'}",
                f"- `expires_at`：{clean_text(cache.get('expires_at')) or '未返回'}",
                f"- `refresh_expires_at`：{clean_text(cache.get('refresh_expires_at')) or '未返回'}",
                "",
                "## 下一步",
                "",
                "- 现在可以重新运行 `feishu-bitable-sync`。",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## 下一步",
                "",
                "- 确认飞书应用已开启网页应用能力。",
                "- 确认飞书应用回调地址包含 `http://127.0.0.1:14578/callback`。",
                "- 重新运行 `feishu-user-auth` 完成授权。",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def run_feishu_user_auth(input_path: Path, *, workspace_root: Path) -> dict[str, Any]:
    published_path = workspace_root / "content-production" / "published" / f"{datetime.now().strftime('%Y%m%d')}-feishu-user-auth.md"
    timeout_seconds = parse_timeout_seconds(input_path)

    status = "success"
    error_message = ""
    cache: dict[str, Any] | None = None
    auth_url = ""
    opened_browser: bool | None = None

    try:
        result = run_browser_authorization(timeout_seconds=timeout_seconds)
        cache = result.get("cache") or load_user_token_cache()
        auth_url = clean_text(result.get("auth_url"))
        opened_browser = bool(result.get("opened_browser"))
    except Exception as error:  # noqa: BLE001
        status = "failed"
        error_message = clean_text(error) or str(error)
        cache = load_user_token_cache()

    write_text(
        published_path,
        build_manifest(
            input_path=input_path,
            published_path=published_path,
            status=status,
            cache=cache,
            error_message=error_message,
            auth_url=auth_url,
            opened_browser=opened_browser,
        ),
    )

    return {
        "status": status,
        "cache_path": str(token_cache_path()),
        "redirect_uri": redirect_uri(),
        "manifest_path": published_path,
        "expires_at": clean_text((cache or {}).get("expires_at")),
        "open_id": clean_text((cache or {}).get("open_id")),
    }
