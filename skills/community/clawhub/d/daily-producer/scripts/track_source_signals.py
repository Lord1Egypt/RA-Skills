#!/usr/bin/env python3
"""
记录每次日报采集后的来源命中信号。

读取 output/raw/{date}_index.txt，统计各 sources.direct URL 的命中条数，
以及出现在 raw 文件中但不属于 sources.direct 的新来源，
结果写入 data/source_signals/{date}.json。

用法：
    python3 scripts/track_source_signals.py --date 2026-03-25
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
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

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "SKILL.md").exists() and (candidate / "config").is_dir():
            return candidate

    return script_dir.parent


def load_profile(root: Path) -> dict:
    config_path = root / "config" / "profile.yaml"
    if not config_path.exists():
        print(f"ERROR: {config_path} 不存在，请先运行 /daily-init", file=sys.stderr)
        sys.exit(1)

    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass

    # Fallback: simple parser for sources.direct only
    result: dict = {"sources": {"direct": [], "search_seeds": []}}
    text = config_path.read_text(encoding="utf-8")
    in_direct = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if " #" in stripped:
            stripped = stripped[: stripped.index(" #")].rstrip()
        indent = len(line) - len(line.lstrip())

        if stripped == "direct:":
            in_direct = True
        elif stripped == "search_seeds:":
            in_direct = False
        elif in_direct and stripped.startswith("- ") and indent >= 4:
            result["sources"].setdefault("direct", []).append(
                stripped[2:].strip().strip("'\"")
            )
        elif indent < 4 and not stripped.startswith("-") and in_direct:
            in_direct = False

    return result


def extract_domain(url: str) -> str:
    """从 URL 中提取域名（去除 scheme 和 www 前缀）。"""
    domain = re.sub(r"https?://(www\.)?", "", url.lower())
    return domain.split("/")[0]


def match_direct_url(article_url: str, direct_urls: list[str]) -> str | None:
    """将 article_url 的域名与 sources.direct 列表做匹配，返回匹配的 direct URL。"""
    article_domain = extract_domain(article_url)
    for direct_url in direct_urls:
        direct_domain = extract_domain(direct_url)
        if direct_domain and (direct_domain in article_domain or article_domain in direct_domain):
            return direct_url
    return None


def parse_raw_index(raw_path: Path) -> list[dict]:
    """
    解析 output/raw/{date}_index.txt，返回每个 block 的字段字典列表。
    支持新格式（={80} 分隔），旧格式降级返回空列表。
    """
    text = raw_path.read_text(encoding="utf-8")
    separator = "=" * 80

    if separator not in text:
        return []

    blocks = text.split(separator)
    result = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # 字段区域在 -{80} 之前
        dash_sep = "-" * 80
        header = block.split(dash_sep)[0] if dash_sep in block else block
        fields: dict[str, str] = {}
        for line in header.splitlines():
            line = line.strip()
            if ": " in line:
                k, v = line.split(": ", 1)
                fields[k.strip()] = v.strip()
        if fields:
            result.append(fields)

    return result


def build_signal(
    date: str,
    blocks: list[dict],
    direct_urls: list[str],
    raw_missing: bool = False,
) -> dict:
    """根据解析后的 block 列表构建 signal 数据。"""
    # 初始化每个 direct URL 的命中记录
    sources_direct: dict[str, dict] = {
        url: {"hit_count": 0, "urls": []} for url in direct_urls
    }
    new_sources: dict[str, dict] = {}

    for block in blocks:
        url = block.get("url", "").strip()
        if not url:
            continue

        matched = match_direct_url(url, direct_urls)
        if matched:
            sources_direct[matched]["hit_count"] += 1
            if url not in sources_direct[matched]["urls"]:
                sources_direct[matched]["urls"].append(url)
        else:
            domain = extract_domain(url)
            if domain:
                if domain not in new_sources:
                    new_sources[domain] = {"hit_count": 0, "sample_url": url, "urls": []}
                new_sources[domain]["hit_count"] += 1
                if url not in new_sources[domain]["urls"]:
                    new_sources[domain]["urls"].append(url)

    return {
        "date": date,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "raw_missing": raw_missing,
        "total_blocks": len(blocks),
        "sources_direct": sources_direct,
        "new_sources": new_sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="记录日报采集来源命中信号")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="目标日期，格式 YYYY-MM-DD（默认今天）",
    )
    args = parser.parse_args()

    root = resolve_root_dir()
    profile = load_profile(root)
    direct_urls: list[str] = (profile.get("sources") or {}).get("direct") or []

    raw_path = root / "output" / "raw" / f"{args.date}_index.txt"
    raw_missing = not raw_path.exists()

    if raw_missing:
        print(f"WARNING: raw 文件不存在: {raw_path}，写入空信号记录", file=sys.stderr)
        blocks: list[dict] = []
    else:
        blocks = parse_raw_index(raw_path)
        if not blocks:
            print(
                f"WARNING: {raw_path} 格式无法解析（可能是旧格式），写入空信号记录",
                file=sys.stderr,
            )

    signal = build_signal(args.date, blocks, direct_urls, raw_missing=raw_missing)

    out_dir = root / "data" / "source_signals"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.date}.json"
    out_path.write_text(
        json.dumps(signal, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"信号已写入: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
