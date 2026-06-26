#!/usr/bin/env python3
"""
从 filtered index 中提取需要深抓的条目，用 opencli web read 抓取正文。

逻辑：
- 平台类条目（time_status: in_window）已有完整内容（text/title），直接复制到 detail，不需要深抓
- 网站类条目（time_status: google_filtered）只有标题+URL，需要 opencli web read 抓正文

输出：output/raw/{date}_detail.txt

用法：
    python3 scripts/collect_detail.py --date 2026-04-05
    python3 scripts/collect_detail.py --date 2026-04-05 --dry-run
    python3 scripts/collect_detail.py --date 2026-04-05 --max-fetch 20
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

REQUEST_DELAY = 5


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
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if (c / "SKILL.md").exists() and (c / "config").is_dir():
            return c
    return script_dir.parent


def parse_filtered_index(text: str) -> tuple[list[dict], list[dict]]:
    """
    解析 filtered index，分为两类返回：
    - platform_items: 平台类条目（已有内容）
    - website_items: 网站类条目（需要深抓）
    """
    platform_items = []
    website_items = []

    current_block_meta: dict = {}
    current_item: dict | None = None

    for line in text.splitlines():
        # 新的平台块
        if line.startswith("--- ["):
            # 保存上一条
            if current_item:
                _classify_item(current_item, platform_items, website_items)
            m = re.match(r"--- \[(.+?)\] \((.+?)\) ---", line)
            current_block_meta = {
                "platform": m.group(1) if m else "unknown",
                "region": m.group(2) if m else "",
            }
            current_item = None

        elif line.startswith("command:"):
            current_block_meta["command"] = line.split(":", 1)[1].strip()
        elif line.startswith("keyword:"):
            current_block_meta["keyword"] = line.split(":", 1)[1].strip()

        # 条目行
        elif re.match(r"^\s+\[\d+\]\s", line):
            # 保存上一条
            if current_item:
                _classify_item(current_item, platform_items, website_items)
            m = re.match(r"^\s+\[(\d+)\]\s+(.*)", line)
            current_item = {
                "index": int(m.group(1)) if m else 0,
                "title": m.group(2).strip() if m else "",
                "content_lines": [],
                "platform": current_block_meta.get("platform", ""),
                "region": current_block_meta.get("region", ""),
                "keyword": current_block_meta.get("keyword", ""),
                "fields": {},
            }

        # 字段行
        elif current_item and re.match(r"^\s{6}\w+:", line):
            m = re.match(r"^\s{6}(\w+):\s*(.*)", line)
            if m:
                current_item["fields"][m.group(1)] = m.group(2).strip()

        # 正文续行（多行推文等）
        elif current_item and line.strip() and not line.startswith("---") and not line.startswith("#") and not line.startswith("command:") and not line.startswith("keyword:") and not line.startswith("status:") and not line.startswith("count:") and not line.startswith("fetch_stack:"):
            current_item["content_lines"].append(line)

    # 最后一条
    if current_item:
        _classify_item(current_item, platform_items, website_items)

    return platform_items, website_items


def _classify_item(item: dict, platform_items: list, website_items: list):
    time_status = item["fields"].get("time_status", "")
    if time_status == "google_filtered" or item["region"] == "website":
        website_items.append(item)
    else:
        platform_items.append(item)


def _read_exported_markdown(output_dir: Path) -> str:
    """读取 opencli web read --format md 导出的正文文件。"""
    md_files = sorted(output_dir.rglob("*.md"))
    if not md_files:
        return ""
    # 取最大文件，通常就是正文文件
    best = max(md_files, key=lambda p: p.stat().st_size)
    return best.read_text(encoding="utf-8", errors="ignore").strip()



def fetch_url(url: str, timeout: int = 60) -> dict:
    """用 opencli web read 抓取 URL 正文。使用 md 导出目录，再读回正文文件。"""
    env = os.environ.copy()
    env["DISPLAY"] = env.get("DISPLAY", ":99")

    work_dir = Path(tempfile.gettempdir()) / "dailynew-opencli-web" / hashlib.md5(url.encode("utf-8")).hexdigest()
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    cmd = f'opencli web read --url "{url}" --format md --output "{work_dir}"'

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, env=env
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode != 0:
            return {"success": False, "url": url, "error": stderr or stdout}

        content = _read_exported_markdown(work_dir)
        if not content:
            return {
                "success": False,
                "url": url,
                "error": "markdown export missing or empty",
                "stdout": stdout,
            }

        return {"success": True, "url": url, "content": content, "stdout": stdout}

    except subprocess.TimeoutExpired:
        return {"success": False, "url": url, "error": "timeout"}
    except Exception as e:
        return {"success": False, "url": url, "error": str(e)}
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def format_detail_output(
    platform_items: list[dict],
    website_items: list[dict],
    fetch_results: dict[str, dict],
    date_str: str,
) -> str:
    """格式化 detail 输出。"""
    lines = [
        f"# 日报候选详情 — {date_str}",
        f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 平台类条目（已有内容）: {len(platform_items)}",
        f"# 网站类条目（深抓正文）: {len(website_items)}",
        f"# 深抓成功: {sum(1 for r in fetch_results.values() if r.get('success'))}",
        f"# 深抓失败: {sum(1 for r in fetch_results.values() if not r.get('success'))}",
        "",
        "=" * 70,
        "",
        "# ━━ 第一部分：平台类条目（已有完整内容）━━",
        "",
    ]

    for item in platform_items:
        lines.append(f"--- [{item['platform']}] ({item['region']}) ---")
        lines.append(f"type: platform")
        lines.append(f"keyword: {item.get('keyword', '')}")
        lines.append(f"title: {item['title']}")
        for content_line in item.get("content_lines", []):
            lines.append(content_line)
        for k, v in item["fields"].items():
            lines.append(f"{k}: {v}")
        lines.append("")

    lines.append("")
    lines.append("# ━━ 第二部分：网站类条目（深抓正文）━━")
    lines.append("")

    for item in website_items:
        url = item["fields"].get("url", "")
        lines.append(f"--- [{item['platform']}] ({item['region']}) ---")
        lines.append(f"type: website_detail")
        lines.append(f"keyword: {item.get('keyword', '')}")
        lines.append(f"title: {item['title']}")
        for content_line in item.get("content_lines", []):
            lines.append(content_line)
        for k, v in item["fields"].items():
            lines.append(f"{k}: {v}")

        # 附加深抓结果
        if url and url in fetch_results:
            result = fetch_results[url]
            if result.get("success"):
                content = result.get("content", "")
                # 截取前 2000 字符避免文件过大
                if len(content) > 2000:
                    content = content[:2000] + "\n... [截断，共 " + str(len(result.get("content", ""))) + " 字符]"
                lines.append(f"fetch_status: success")
                lines.append(f"fetched_content:")
                lines.append(content)
            else:
                lines.append(f"fetch_status: FAILED")
                lines.append(f"fetch_error: {result.get('error', 'unknown')}")
        else:
            lines.append(f"fetch_status: skipped (no url or not fetched)")

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="从 filtered index 深抓网站类条目正文")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="目标日期")
    parser.add_argument("--dry-run", action="store_true", help="只输出统计，不实际抓取")
    parser.add_argument("--max-fetch", type=int, default=0, help="最多深抓多少个 URL，0=不限")
    parser.add_argument("--no-save", action="store_true", help="不保存结果到文件")
    args = parser.parse_args()

    root = resolve_root_dir()

    # 读取 filtered index
    filtered_path = root / "output" / "raw" / f"{args.date}_index_filtered.txt"
    if not filtered_path.exists():
        print(f"ERROR: {filtered_path} 不存在，请先运行 filter_index.py", file=sys.stderr)
        sys.exit(1)

    text = filtered_path.read_text(encoding="utf-8")
    platform_items, website_items = parse_filtered_index(text)

    print(f"平台类条目: {len(platform_items)} 条（已有内容，直接保留）", file=sys.stderr)
    print(f"网站类条目: {len(website_items)} 条（需要深抓正文）", file=sys.stderr)

    # 提取去重的 URL
    urls_to_fetch = []
    seen_urls: set[str] = set()
    for item in website_items:
        url = item["fields"].get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            urls_to_fetch.append(url)

    print(f"去重后需深抓 URL: {len(urls_to_fetch)} 个", file=sys.stderr)

    if args.max_fetch > 0:
        urls_to_fetch = urls_to_fetch[:args.max_fetch]
        print(f"限制最多深抓: {args.max_fetch} 个", file=sys.stderr)

    if args.dry_run:
        print(f"\n(dry-run 模式，不实际抓取)", file=sys.stderr)
        print(f"\n要深抓的 URL:")
        for i, url in enumerate(urls_to_fetch, 1):
            print(f"  [{i}] {url}")
        return

    # 执行深抓
    fetch_results: dict[str, dict] = {}
    for i, url in enumerate(urls_to_fetch, 1):
        print(f"  [{i}/{len(urls_to_fetch)}] {url[:80]}...", file=sys.stderr)
        result = fetch_url(url)
        fetch_results[url] = result
        status = "✅" if result.get("success") else "❌"
        print(f"    {status}", file=sys.stderr)
        time.sleep(REQUEST_DELAY)

    # 格式化输出
    output = format_detail_output(platform_items, website_items, fetch_results, args.date)

    if not args.no_save:
        raw_dir = root / "output" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        save_path = raw_dir / f"{args.date}_detail.txt"
        save_path.write_text(output, encoding="utf-8")
        print(f"\n已保存到 {save_path}", file=sys.stderr)

    # 统计
    ok = sum(1 for r in fetch_results.values() if r.get("success"))
    fail = sum(1 for r in fetch_results.values() if not r.get("success"))
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Detail 采集完成", file=sys.stderr)
    print(f"  平台类: {len(platform_items)} 条（直接保留）", file=sys.stderr)
    print(f"  网站深抓: {ok} 成功, {fail} 失败（共 {len(urls_to_fetch)} 个 URL）", file=sys.stderr)
    print(f"  总条目: {len(platform_items) + len(website_items)}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)


if __name__ == "__main__":
    main()
