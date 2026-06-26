#!/usr/bin/env python3
"""
Flash Thoughts - 闪念记录脚本

快速记录灵感闪念，按日期存储，分隔线分隔每个想法。
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


# 默认存储路径（可通过环境变量 FLASH_THOUGHTS_DIR 自定义）
import os
FLASH_DIR = Path(os.environ.get("FLASH_THOUGHTS_DIR", "~/biji/闪念")).expanduser()


def ensure_dir():
    """确保存储目录存在"""
    FLASH_DIR.mkdir(parents=True, exist_ok=True)


def get_today_file() -> Path:
    """获取今天的闪念文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    return FLASH_DIR / f"{today}.md"


def format_entry(content: str) -> str:
    """格式化一条闪念"""
    time_str = datetime.now().strftime("%H:%M")
    return f"\n---\n\n## {time_str} - {content}\n"


def add_thought(content: str) -> dict:
    """添加一条闪念"""
    ensure_dir()
    file_path = get_today_file()

    # 如果文件不存在，创建带标题的文件
    if not file_path.exists():
        today = datetime.now().strftime("%Y-%m-%d")
        header = f"# {today} 闪念\n"
        file_path.write_text(header, encoding="utf-8")

    # 追加新闪念
    entry = format_entry(content)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

    return {
        "success": True,
        "file": str(file_path),
        "time": datetime.now().strftime("%H:%M"),
        "content": content
    }


def search_thoughts(keyword: str, days: int = 30) -> list:
    """搜索闪念"""
    results = []
    pattern = re.compile(keyword, re.IGNORECASE)

    # 获取最近的文件
    files = sorted(FLASH_DIR.glob("*.md"), reverse=True)[:days]

    for file_path in files:
        content = file_path.read_text(encoding="utf-8")
        if pattern.search(content):
            results.append({
                "file": file_path.name,
                "matches": len(pattern.findall(content))
            })

    return results


def show_day(date_str: str) -> Optional[str]:
    """显示某天的闪念"""
    file_path = FLASH_DIR / f"{date_str}.md"
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return None


def show_recent(days: int = 7) -> list:
    """显示最近N天的闪念文件列表"""
    files = sorted(FLASH_DIR.glob("*.md"), reverse=True)[:days]
    return [f.name for f in files]


def main():
    parser = argparse.ArgumentParser(
        description="Flash Thoughts - 闪念记录"
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加闪念")
    add_parser.add_argument("content", help="闪念内容")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索闪念")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--days", type=int, default=30, help="搜索最近N天")

    # show 命令
    show_parser = subparsers.add_parser("show", help="显示某天的闪念")
    show_parser.add_argument("date", help="日期 (YYYY-MM-DD)")

    # recent 命令
    recent_parser = subparsers.add_parser("recent", help="显示最近N天的闪念")
    recent_parser.add_argument("days", type=int, nargs="?", default=7, help="天数")

    args = parser.parse_args()

    if args.command == "add":
        result = add_thought(args.content)
        print(f"✅ 已记录到 {result['file']}")
        print(f"⏰ {result['time']}")
        print(f"📝 {result['content']}")

    elif args.command == "search":
        results = search_thoughts(args.keyword, args.days)
        if results:
            print(f"🔍 找到 {len(results)} 个文件包含 '{args.keyword}':")
            for r in results:
                print(f"  - {r['file']} ({r['matches']} 处匹配)")
        else:
            print(f"🔍 没有找到包含 '{args.keyword}' 的闪念")

    elif args.command == "show":
        content = show_day(args.date)
        if content:
            print(content)
        else:
            print(f"❌ 没有找到 {args.date} 的闪念")

    elif args.command == "recent":
        files = show_recent(args.days)
        if files:
            print(f"📅 最近 {args.days} 天的闪念文件:")
            for f in files:
                print(f"  - {f}")
        else:
            print("📭 还没有任何闪念记录")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()