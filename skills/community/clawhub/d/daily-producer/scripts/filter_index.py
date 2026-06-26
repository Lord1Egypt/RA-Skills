#!/usr/bin/env python3
"""
对 output/raw/{date}_index.txt 做时间窗口筛选。

解析各平台不同的时间格式，过滤掉超出时间窗口的条目。
没有时间字段的条目（如微博热搜）保留但标记为 time_status: unknown。

用法：
    python3 scripts/filter_index.py --date 2026-04-05 --window 3
    python3 scripts/filter_index.py --date 2026-04-05 --window 3 --dry-run
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
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
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if (c / "SKILL.md").exists() and (c / "config").is_dir():
            return c
    return script_dir.parent


def parse_time(time_str: str) -> datetime | None:
    """
    尝试解析各平台的时间格式，返回 datetime 或 None。

    支持的格式：
    - Twitter: "Fri Apr 03 14:00:17 +0000 2026"
    - 小红书: "2026-02-04"
    - ISO: "2026-04-03T14:00:17Z" / "2026-04-03 14:00:17"
    - 中文: "2026年4月3日" / "04月03日" / "昨天 17:58" / "3小时前"
    - Reddit: "2026-04-03T14:00:17.000Z"
    """
    if not time_str or time_str.strip() == "":
        return None

    time_str = time_str.strip()

    # Twitter 格式: "Fri Apr 03 14:00:17 +0000 2026"
    try:
        return datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=None)
    except (ValueError, TypeError):
        pass

    # ISO 日期: "2026-04-03" 或 "2026-02-04"
    try:
        return datetime.strptime(time_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        pass

    # ISO datetime: "2026-04-03T14:00:17Z"
    try:
        return datetime.strptime(time_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        pass

    # ISO datetime with ms: "2026-04-03T14:00:17.000Z"
    try:
        return datetime.strptime(time_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        pass

    # "2026-04-03 14:00:17"
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        pass

    # "2026-04-03 14:00" (无秒，Reddit API 转换后的格式)
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        pass

    # 中文日期: "2026年4月3日"
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", time_str)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # 相对时间: "3小时前", "2天前", "昨天"
    m = re.match(r"(\d+)\s*小时前", time_str)
    if m:
        return datetime.now() - timedelta(hours=int(m.group(1)))

    m = re.match(r"(\d+)\s*天前", time_str)
    if m:
        return datetime.now() - timedelta(days=int(m.group(1)))

    m = re.match(r"(\d+)\s*分钟前", time_str)
    if m:
        return datetime.now() - timedelta(minutes=int(m.group(1)))

    # YouTube 相对时间: "11 months ago", "2 days ago", "3 weeks ago", "1 year ago"
    m = re.match(r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago", time_str)
    if m:
        num = int(m.group(1))
        unit = m.group(2)
        delta_map = {
            "second": timedelta(seconds=num),
            "minute": timedelta(minutes=num),
            "hour": timedelta(hours=num),
            "day": timedelta(days=num),
            "week": timedelta(weeks=num),
            "month": timedelta(days=num * 30),
            "year": timedelta(days=num * 365),
        }
        return datetime.now() - delta_map.get(unit, timedelta())

    if "昨天" in time_str:
        return datetime.now() - timedelta(days=1)

    if "前天" in time_str:
        return datetime.now() - timedelta(days=2)

    # "今天08:04" / "今天 08:04"
    m = re.match(r"今天\s*(\d{1,2}):(\d{2})", time_str)
    if m:
        now = datetime.now()
        return now.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0, microsecond=0)

    # "04月03日" (没有年份，假设今年)
    m = re.match(r"(\d{1,2})月(\d{1,2})日", time_str)
    if m:
        return datetime(datetime.now().year, int(m.group(1)), int(m.group(2)))

    return None


def parse_index_file(text: str) -> list[dict]:
    """
    解析 _index.txt 文件，提取每个条目为结构化 dict。
    """
    entries = []
    current_block: dict | None = None
    current_items: list[dict] = []
    current_item: dict | None = None

    for line in text.splitlines():
        # 新的平台块
        if line.startswith("--- ["):
            # 保存上一个 block
            if current_block is not None:
                if current_item:
                    current_items.append(current_item)
                current_block["items"] = current_items
                entries.append(current_block)

            m = re.match(r"--- \[(.+?)\] \((.+?)\) ---", line)
            current_block = {
                "platform": m.group(1) if m else "unknown",
                "region": m.group(2) if m else "",
                "meta": {},
                "items": [],
            }
            current_items = []
            current_item = None

        elif current_block is not None:
            # 元信息行
            if line.startswith("command:"):
                current_block["meta"]["command"] = line.split(":", 1)[1].strip()
            elif line.startswith("keyword:"):
                current_block["meta"]["keyword"] = line.split(":", 1)[1].strip()
            elif line.startswith("status:"):
                current_block["meta"]["status"] = line.split(":", 1)[1].strip()
            elif line.startswith("count:"):
                current_block["meta"]["count"] = line.split(":", 1)[1].strip()

            # 条目行: "  [1] 标题内容"
            elif re.match(r"^\s+\[\d+\]\s", line):
                if current_item:
                    current_items.append(current_item)
                m = re.match(r"^\s+\[(\d+)\]\s+(.*)", line)
                current_item = {
                    "index": int(m.group(1)) if m else 0,
                    "title": m.group(2).strip() if m else "",
                    "content_lines": [],
                    "fields": {},
                }

            # 字段行: "      key: value"
            elif current_item and re.match(r"^\s{6}\w+:", line):
                m = re.match(r"^\s{6}(\w+):\s*(.*)", line)
                if m:
                    current_item["fields"][m.group(1)] = m.group(2).strip()

            # 正文续行：属于当前条目但不是字段行的文本（如 Twitter 推文多行正文）
            elif current_item and line.strip() and not line.startswith("---") and not line.startswith("#") and not line.startswith("command:") and not line.startswith("keyword:") and not line.startswith("status:") and not line.startswith("count:") and not line.startswith("fetch_stack:") and not line.startswith("error:"):
                current_item["content_lines"].append(line)

    # 保存最后一个 block
    if current_block is not None:
        if current_item:
            current_items.append(current_item)
        current_block["items"] = current_items
        entries.append(current_block)

    return entries


def filter_entries(
    entries: list[dict], cutoff: datetime
) -> tuple[list[dict], dict]:
    """
    按时间窗口筛选。返回 (过滤后的 entries, 统计信息)。
    """
    stats = {
        "total_items": 0,
        "kept": 0,
        "removed_old": 0,
        "no_time": 0,
        "by_platform": {},
    }

    filtered = []

    for block in entries:
        platform = block["platform"]
        region = block.get("region", "")
        if platform not in stats["by_platform"]:
            stats["by_platform"][platform] = {"total": 0, "kept": 0, "removed": 0, "no_time": 0}

        # 网站类（region=website）走的是 Google site: 搜索（自带 after: 时间过滤），直接保留
        is_website = region == "website"

        kept_items = []
        for item in block["items"]:
            stats["total_items"] += 1
            stats["by_platform"][platform]["total"] += 1

            if is_website:
                # 网站类优先用自身时间字段筛选；没有时间字段时信任 Google after: 过滤
                time_str = item["fields"].get("time", "")
                parsed = parse_time(time_str) if time_str else None
                if parsed is not None:
                    if parsed >= cutoff:
                        item["fields"]["time_status"] = "in_window"
                        item["fields"]["time_parsed"] = parsed.strftime("%Y-%m-%d")
                        kept_items.append(item)
                        stats["kept"] += 1
                        stats["by_platform"][platform]["kept"] += 1
                    else:
                        stats["removed_old"] += 1
                        stats["by_platform"][platform]["removed"] += 1
                else:
                    # 无时间字段，信任 Google site: after: 过滤
                    item["fields"]["time_status"] = "google_filtered"
                    kept_items.append(item)
                    stats["kept"] += 1
                    stats["by_platform"][platform]["kept"] += 1
                continue

            # 提取时间
            time_str = item["fields"].get("time", "")
            parsed = parse_time(time_str)

            if parsed is None:
                # 平台类无时间字段：opencli 抓取的热榜/搜索结果本身即为当前内容，直接保留
                item["fields"]["time_status"] = "no_time_kept"
                kept_items.append(item)
                stats["kept"] += 1
                stats["no_time"] += 1
                stats["by_platform"][platform]["kept"] += 1
                stats["by_platform"][platform]["no_time"] += 1
            elif parsed >= cutoff:
                # 在时间窗口内，保留
                item["fields"]["time_status"] = "in_window"
                item["fields"]["time_parsed"] = parsed.strftime("%Y-%m-%d")
                kept_items.append(item)
                stats["kept"] += 1
                stats["by_platform"][platform]["kept"] += 1
            else:
                # 超出时间窗口，移除
                stats["removed_old"] += 1
                stats["by_platform"][platform]["removed"] += 1

        new_block = dict(block)
        new_block["items"] = kept_items
        new_block["meta"] = dict(block["meta"])
        new_block["meta"]["count"] = str(len(kept_items))
        if kept_items:
            filtered.append(new_block)

    return filtered, stats


def format_filtered(entries: list[dict], date_str: str, stats: dict) -> str:
    """将筛选后的结果格式化为文本。"""
    lines = [
        f"# 日报候选池（筛选后）— {date_str}",
        f"# 筛选时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 原始条目: {stats['total_items']}",
        f"# 保留: {stats['kept']}（其中无时间标记: {stats['no_time']}）",
        f"# 移除（超出时间窗口）: {stats['removed_old']}",
        "",
        "# 各平台统计:",
    ]

    for platform, ps in stats["by_platform"].items():
        lines.append(f"#   {platform}: {ps['kept']}/{ps['total']} 保留, {ps['removed']} 移除, {ps['no_time']} 无时间")

    lines.append("")
    lines.append("=" * 70)
    lines.append("")

    for block in entries:
        platform = block["platform"]
        region = block["region"]
        meta = block["meta"]

        lines.append(f"--- [{platform}] ({region}) ---")
        for k, v in meta.items():
            lines.append(f"{k}: {v}")
        lines.append("")

        for item in block["items"]:
            lines.append(f"  [{item['index']}] {item['title']}")
            # 输出多行正文（如 Twitter 推文续行）
            for content_line in item.get("content_lines", []):
                lines.append(content_line)
            for k, v in item["fields"].items():
                lines.append(f"      {k}: {v}")
            lines.append("")

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="对候选池做时间窗口筛选")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="目标日期 (默认今天)",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="时间窗口天数 (默认 3)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只输出统计，不保存",
    )
    args = parser.parse_args()

    root = resolve_root_dir()

    # 读取 index 文件
    index_path = root / "output" / "raw" / f"{args.date}_index.txt"
    if not index_path.exists():
        print(f"ERROR: {index_path} 不存在，请先运行 collect", file=sys.stderr)
        sys.exit(1)

    text = index_path.read_text(encoding="utf-8")

    # 计算截止时间
    target = datetime.strptime(args.date, "%Y-%m-%d")
    cutoff = target - timedelta(days=args.window)

    print(f"时间窗口: {cutoff.strftime('%Y-%m-%d')} ~ {args.date}", file=sys.stderr)

    # 解析
    entries = parse_index_file(text)
    print(f"解析到 {len(entries)} 个采集块", file=sys.stderr)

    # 筛选
    filtered, stats = filter_entries(entries, cutoff)

    print(f"\n筛选结果:", file=sys.stderr)
    print(f"  原始: {stats['total_items']} 条", file=sys.stderr)
    print(f"  保留: {stats['kept']} 条（无时间: {stats['no_time']}）", file=sys.stderr)
    print(f"  移除: {stats['removed_old']} 条", file=sys.stderr)
    print(f"\n各平台:", file=sys.stderr)
    for platform, ps in stats["by_platform"].items():
        print(f"  {platform}: {ps['kept']}/{ps['total']} 保留, {ps['removed']} 移除", file=sys.stderr)

    # 输出
    output = format_filtered(filtered, args.date, stats)

    if args.dry_run:
        print("\n(dry-run 模式，不保存)", file=sys.stderr)
    else:
        save_path = root / "output" / "raw" / f"{args.date}_index_filtered.txt"
        save_path.write_text(output, encoding="utf-8")
        print(f"\n已保存到 {save_path}", file=sys.stderr)

    print(output)


if __name__ == "__main__":
    main()
