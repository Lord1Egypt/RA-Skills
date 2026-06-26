#!/usr/bin/env python3
"""
打开日报页面。

优先使用本地 HTTP 服务地址（如果 data/.server_port 存在），
否则回退到 file:// 打开本地 HTML 文件。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def resolve_root_dir() -> Path:
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (
            (candidate / "SKILL.md").exists()
            and (candidate / "reference" / "daily_example.html").exists()
            and (candidate / "scripts" / "open_daily.py").exists()
        ):
            return candidate

    return script_dir.parent


ROOT_DIR = resolve_root_dir()
OUTPUT_DIR = ROOT_DIR / "output" / "daily"
PORT_FILE = ROOT_DIR / "data" / ".server_port"


def find_daily_file(date: str | None) -> Path:
    if date:
        candidate = OUTPUT_DIR / f"{date}.html"
        if not candidate.exists():
            raise FileNotFoundError(f"未找到日报文件: {candidate}")
        return candidate

    candidates = sorted(OUTPUT_DIR.glob("*.html"))
    if not candidates:
        raise FileNotFoundError("output/daily/ 下没有可打开的 HTML 日报文件")
    return candidates[-1]


def read_server_port() -> int | None:
    if not PORT_FILE.exists():
        return None
    try:
        return int(PORT_FILE.read_text(encoding="utf-8").strip())
    except ValueError:
        return None


def _is_server_alive(port: int, timeout: float = 1.0) -> bool:
    """Check if the feedback server is actually responding."""
    try:
        import urllib.request
        url = f"http://localhost:{port}/"
        req = urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except Exception:
        return False


def build_target(daily_file: Path, mode: str) -> str:
    port = read_server_port()
    if mode in {"auto", "http"} and port:
        if _is_server_alive(port):
            return f"http://localhost:{port}/daily/{daily_file.name}"
        if mode == "http":
            raise RuntimeError(
                f"data/.server_port 指向端口 {port}，但服务未响应。"
                "请确认 feedback_server.py 是否仍在运行。"
            )
        # mode == "auto": server not alive, fall back to file
    elif mode == "http":
        raise RuntimeError("未检测到 data/.server_port，无法构建 HTTP 访问地址")
    return daily_file.resolve().as_uri()


def open_target(target: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", target], check=True)
        return
    if sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", target], check=True)
        return
    if sys.platform.startswith("win"):
        os.startfile(target)  # type: ignore[attr-defined]
        return
    raise RuntimeError(f"暂不支持的平台: {sys.platform}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open a generated daily page")
    parser.add_argument("date", nargs="?", help="日报日期，格式 YYYY-MM-DD；默认打开最新一份")
    parser.add_argument(
        "--mode",
        choices=["auto", "http", "file"],
        default="auto",
        help="auto: 优先 HTTP，否则 file；http: 只打开服务地址；file: 只打开本地文件",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="只输出目标地址，不真正打开",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    daily_file = find_daily_file(args.date)
    target = build_target(daily_file, args.mode)
    print(target)
    if not args.print_only:
        open_target(target)


if __name__ == "__main__":
    main()
