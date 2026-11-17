"""Small, consent-preserving cache for user-provided local application paths.

The cache contains only a product id and a normalized path.  It never starts a
process and it never stores credentials or command-line arguments.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import ntpath
import os
from pathlib import Path
import re
import tempfile
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = 1
CACHE_ENV = "DCC_MCP_APP_PATH_CACHE"
PRODUCT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def cache_path() -> Path:
    override = os.environ.get(CACHE_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    else:
        root = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(root) / "dcc-mcp" / "app-paths.json"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _normalize_path(value: str) -> str:
    raw = str(value or "").strip().strip('"')
    parsed = urlparse(raw)
    if "://" in raw or parsed.scheme.casefold() in {"file", "http", "https", "ftp"}:
        raise ValueError("application path must be a local absolute path, not a URL")
    expanded = os.path.expandvars(os.path.expanduser(raw))
    if not Path(expanded).is_absolute() and not ntpath.isabs(expanded):
        raise ValueError("application path must be absolute")
    # Resolve local paths when possible, while retaining a Windows path when a
    # caller supplies one on another host for a shared configuration file.
    if ntpath.isabs(expanded) and not Path(expanded).is_absolute():
        return ntpath.normpath(expanded)
    return str(Path(expanded).resolve(strict=False))


def _path_exists(value: str) -> bool:
    return Path(value).exists()


def _read() -> dict[str, Any]:
    path = cache_path()
    if not path.is_file():
        return {"schema_version": SCHEMA_VERSION, "entries": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != SCHEMA_VERSION
        or not isinstance(data.get("entries"), dict)
    ):
        raise ValueError("application path cache has an unsupported schema")
    return data


def _write(data: dict[str, Any]) -> None:
    path = cache_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix="app-paths-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
        if os.name != "nt":
            path.chmod(0o600)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def set_path(product_id: str, value: str) -> dict[str, Any]:
    if not isinstance(product_id, str) or PRODUCT_ID_RE.fullmatch(product_id) is None:
        raise ValueError("product id must be a lowercase identifier")
    normalized = _normalize_path(value)
    data = _read()
    timestamp = _now()
    data["entries"][product_id] = {
        "path": normalized,
        "path_kind": "file" if Path(normalized).is_file() else "directory",
        "recorded_at": timestamp,
        "last_verified_at": timestamp if _path_exists(normalized) else None,
        "source": "user",
    }
    _write(data)
    return data["entries"][product_id]


def get_path(product_id: str, *, verify: bool = True) -> dict[str, Any] | None:
    entry = _read()["entries"].get(product_id)
    if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
        return None
    if verify and not _path_exists(entry["path"]):
        return {**entry, "stale": True}
    if verify:
        entry = {**entry, "stale": False, "last_verified_at": _now()}
    return entry


def clear_path(product_id: str) -> bool:
    data = _read()
    removed = data["entries"].pop(product_id, None) is not None
    if removed:
        _write(data)
    return removed


def launch_prompt(
    product_id: str,
    display_name: str | None = None,
    *,
    install_available: bool = False,
    host_install_url: str | None = None,
) -> str:
    name = display_name or product_id
    entry = get_path(product_id)
    if host_install_url is not None and not host_install_url.startswith("https://"):
        raise ValueError("host install URL must use https")
    install_question = (
        f"如果 {name} 尚未安装，是否需要我先提供官方安装方式？下载、安装和启动都需要你的明确确认；"
        "不会仅凭路径缺失自动执行。"
    )
    if entry and not entry.get("stale"):
        return (
            f"已找到 {name} 的本地路径：{entry['path']}。是否要启动这个软件？"
            " 请明确回复“启动/是”后再执行。"
        )
    install_hint = (
        f'如需安装，可运行：dcc-mcp-cli install --dcc-type {product_id} '
        f'--dcc-path "<软件绝对路径>"。'
        if install_available
        else ""
    )
    host_install_hint = f"官方安装页面：{host_install_url}。" if host_install_url else ""
    if entry and entry.get("stale"):
        return (
            f"之前缓存的 {name} 路径已不存在：{entry['path']}。请提供新的软件绝对路径，"
            f"例如 C:\\Program Files\\...\\{product_id}.exe，或者明确告诉我需要安装它。"
            f"{install_question}{host_install_hint}{install_hint}"
        )
    return (
        f"尚未找到 {name} 的本地安装路径。请提供软件的绝对路径（例如 "
        f"C:\\Program Files\\...\\{product_id}.exe），或者明确告诉我需要安装它。"
        f"我会记住你提供的路径，并在启动前再次询问。{install_question}"
        f"{host_install_hint}{install_hint}"
    )


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    setter = subparsers.add_parser("set")
    setter.add_argument("--product", required=True)
    setter.add_argument("--path", required=True)
    getter = subparsers.add_parser("get")
    getter.add_argument("--product", required=True)
    prompter = subparsers.add_parser("prompt")
    prompter.add_argument("--product", required=True)
    prompter.add_argument("--name")
    prompter.add_argument("--install-available", action="store_true")
    prompter.add_argument("--host-install-url")
    clearer = subparsers.add_parser("clear")
    clearer.add_argument("--product", required=True)
    args = parser.parse_args()
    if args.command == "set":
        print(json.dumps(set_path(args.product, args.path), ensure_ascii=False))
    elif args.command == "get":
        print(json.dumps(get_path(args.product), ensure_ascii=False))
    elif args.command == "prompt":
        print(
            launch_prompt(
                args.product,
                args.name,
                install_available=args.install_available,
                host_install_url=args.host_install_url,
            )
        )
    else:
        print(json.dumps({"removed": clear_path(args.product)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
