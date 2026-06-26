#!/usr/bin/env python3
"""
subtitle_manager.py - B站字幕收藏管理器

功能:
    add     - 添加一条字幕记录（手动粘贴或从识别结果导入）
    list    - 列出所有已保存的字幕
    delete  - 按编号删除字幕
    export  - 导出为 Markdown / TXT 文件
    search  - 按关键词搜索字幕内容

存储:
    所有字幕保存在 ~/.workbuddy/skills/bilibili-summarizer/cache/subtitles.json

用法:
    python3 subtitle_manager.py add --bvid BVxxxx --title "视频标题" --text "字幕纯文本" [--timed "带时间戳文本"]
    python3 subtitle_manager.py add --json-file result.json  （从 speech_to_text.py 或 bilibili_fetcher.py 的输出导入）
    python3 subtitle_manager.py list [--limit N]
    python3 subtitle_manager.py delete <编号>
    python3 subtitle_manager.py export [--format md|txt] [--output path] [--ids 1,3,5]
    python3 subtitle_manager.py search <关键词>
"""

import sys
import os
import json
import re
from datetime import datetime
from pathlib import Path

# 存储路径
DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "cache", "subtitles.json"
)


def load_db(db_path: str) -> list:
    """加载字幕数据库"""
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_db(db_path: str, records: list):
    """保存字幕数据库"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def cmd_add(args, db_path: str):
    """添加字幕记录"""
    records = load_db(db_path)

    # 模式1: 从 JSON 文件导入
    if "--json-file" in args:
        idx = args.index("--json-file")
        if idx + 1 >= len(args):
            print("错误: --json-file 需要指定文件路径", file=sys.stderr)
            sys.exit(1)

        json_file = args[idx + 1]
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 自动识别来源：bilibili_fetcher 还是 speech_to_text
        if "info" in data:
            # 来自 bilibili_fetcher.py
            info = data["info"]
            sub = data.get("subtitle", {})
            record = {
                "bvid": info.get("bvid", ""),
                "title": info.get("title", ""),
                "owner": info.get("owner", ""),
                "timed_text": sub.get("timed_text", ""),
                "plain_text": sub.get("plain_text", ""),
                "source": "bilibili_subtitle",
                "char_count": sub.get("char_count", 0),
                "added_at": datetime.now().isoformat(),
            }
        elif "engine" in data:
            # 来自 speech_to_text.py
            sub = data.get("subtitle", {})
            # 从音频路径推断 bvid
            audio_path = data.get("audio_path", "")
            bvid_match = re.search(r"(BV[0-9A-Za-z]{10})", audio_path)
            record = {
                "bvid": bvid_match.group(1) if bvid_match else "",
                "title": "",
                "owner": "",
                "timed_text": sub.get("timed_text", ""),
                "plain_text": sub.get("plain_text", ""),
                "source": f"asr_{data.get('engine', 'unknown')}",
                "char_count": sub.get("char_count", 0),
                "added_at": datetime.now().isoformat(),
            }
        else:
            print("错误: 无法识别 JSON 文件格式", file=sys.stderr)
            sys.exit(1)

    else:
        # 模式2: 手动指定参数
        def get_arg(name):
            if name in args:
                idx = args.index(name)
                if idx + 1 < len(args):
                    return args[idx + 1]
            return ""

        bvid = get_arg("--bvid")
        title = get_arg("--title")
        text = get_arg("--text")
        timed = get_arg("--timed")
        source = get_arg("--source") or "manual"

        if not text:
            print("错误: 需要提供 --text 或 --json-file", file=sys.stderr)
            sys.exit(1)

        record = {
            "bvid": bvid,
            "title": title,
            "owner": "",
            "timed_text": timed,
            "plain_text": text,
            "source": source,
            "char_count": len(text),
            "added_at": datetime.now().isoformat(),
        }

    # 去重：同 bvid + 同 source 只保留最新
    records = [r for r in records
               if not (r.get("bvid") == record["bvid"] and r.get("source") == record["source"])]

    records.append(record)
    save_db(db_path, records)

    idx_num = len(records)
    print(json.dumps({
        "status": "ok",
        "id": idx_num,
        "bvid": record["bvid"],
        "title": record["title"],
        "source": record["source"],
        "char_count": record["char_count"],
        "total_records": idx_num,
    }, ensure_ascii=False, indent=2))


def cmd_list(args, db_path: str):
    """列出所有字幕"""
    records = load_db(db_path)
    limit = 50
    if "--limit" in args:
        idx = args.index("--limit")
        if idx + 1 < len(args):
            limit = int(args[idx + 1])

    # 展示最近的记录
    shown = records[-limit:]
    result = []
    for i, r in enumerate(shown):
        global_id = len(records) - len(shown) + i + 1
        preview = r.get("plain_text", "")[:100] + "..." if len(r.get("plain_text", "")) > 100 else r.get("plain_text", "")
        result.append({
            "id": global_id,
            "bvid": r.get("bvid", ""),
            "title": r.get("title", ""),
            "source": r.get("source", ""),
            "char_count": r.get("char_count", 0),
            "added_at": r.get("added_at", ""),
            "preview": preview,
        })

    print(json.dumps({
        "total": len(records),
        "shown": len(result),
        "records": result,
    }, ensure_ascii=False, indent=2))


def cmd_delete(args, db_path: str):
    """删除指定编号的字幕"""
    if len(args) < 1 or not args[0].isdigit():
        print("错误: 请指定要删除的编号", file=sys.stderr)
        sys.exit(1)

    target_id = int(args[0])
    records = load_db(db_path)

    if target_id < 1 or target_id > len(records):
        print(f"错误: 编号 {target_id} 不存在（共 {len(records)} 条记录）", file=sys.stderr)
        sys.exit(1)

    removed = records.pop(target_id - 1)
    save_db(db_path, records)

    print(json.dumps({
        "status": "ok",
        "deleted_id": target_id,
        "bvid": removed.get("bvid", ""),
        "title": removed.get("title", ""),
        "remaining": len(records),
    }, ensure_ascii=False, indent=2))


def cmd_export(args, db_path: str):
    """导出字幕为 Markdown 或纯文本"""
    records = load_db(db_path)
    if not records:
        print(json.dumps({"error": "没有可导出的字幕记录"}))
        sys.exit(1)

    # 筛选指定 ID
    export_ids = None
    if "--ids" in args:
        idx = args.index("--ids")
        if idx + 1 < len(args):
            export_ids = [int(x.strip()) for x in args[idx + 1].split(",")]

    fmt = "md"
    if "--format" in args:
        idx = args.index("--format")
        if idx + 1 < len(args):
            fmt = args[idx + 1]

    output_path = None
    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_path = args[idx + 1]

    # 筛选记录
    if export_ids:
        selected = [records[i - 1] for i in export_ids if 1 <= i <= len(records)]
    else:
        selected = records

    if fmt == "md":
        content = _export_markdown(selected)
    else:
        content = _export_txt(selected)

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(json.dumps({
            "status": "ok",
            "format": fmt,
            "output": os.path.abspath(output_path),
            "records_exported": len(selected),
        }, ensure_ascii=False, indent=2))
    else:
        # 输出到 stdout
        print(content)


def cmd_search(args, db_path: str):
    """搜索字幕内容"""
    if not args:
        print("错误: 请提供搜索关键词", file=sys.stderr)
        sys.exit(1)

    keyword = args[0]
    records = load_db(db_path)

    results = []
    for i, r in enumerate(records):
        plain = r.get("plain_text", "")
        title = r.get("title", "")
        if keyword.lower() in plain.lower() or keyword.lower() in title.lower():
            # 提取关键词上下文
            ctx_start = plain.lower().find(keyword.lower())
            ctx_start = max(0, ctx_start - 30)
            ctx_end = min(len(plain), ctx_start + len(keyword) + 80)
            context = plain[ctx_start:ctx_end]

            results.append({
                "id": i + 1,
                "bvid": r.get("bvid", ""),
                "title": r.get("title", ""),
                "source": r.get("source", ""),
                "context": context,
                "char_count": r.get("char_count", 0),
            })

    print(json.dumps({
        "keyword": keyword,
        "total_records": len(records),
        "matches": len(results),
        "results": results,
    }, ensure_ascii=False, indent=2))


def _export_markdown(records: list) -> str:
    """导出为 Markdown 格式"""
    lines = [
        "# B站视频字幕合集",
        "",
        f"> 导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 共 {len(records)} 条记录",
        "",
        "---",
        "",
    ]

    for i, r in enumerate(records, 1):
        title = r.get("title", "无标题")
        bvid = r.get("bvid", "")
        owner = r.get("owner", "")
        source = r.get("source", "")
        char_count = r.get("char_count", 0)
        timed = r.get("timed_text", "")
        plain = r.get("plain_text", "")

        lines.append(f"## {i}. {title}")
        if bvid:
            lines.append(f"- **BV号**: {bvid}")
        if owner:
            lines.append(f"- **UP主**: {owner}")
        lines.append(f"- **来源**: {source}")
        lines.append(f"- **字数**: {char_count}")
        lines.append("")

        if timed:
            lines.append("### 字幕（带时间戳）")
            lines.append("")
            lines.append("```")
            lines.append(timed)
            lines.append("```")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _export_txt(records: list) -> str:
    """导出为纯文本"""
    lines = []
    for i, r in enumerate(records, 1):
        title = r.get("title", "无标题")
        bvid = r.get("bvid", "")
        plain = r.get("plain_text", "")

        lines.append(f"{'='*60}")
        lines.append(f"[{i}] {title} ({bvid})")
        lines.append(f"{'='*60}")
        lines.append("")
        lines.append(plain)
        lines.append("")

    return "\n".join(lines)


def main():
    db_path = DEFAULT_DB_PATH

    # 允许通过 --db 指定数据库路径
    args = [a for a in sys.argv[1:] if a != "--db"]
    if "--db" in sys.argv[1:]:
        idx = sys.argv[1:].index("--db")
        if idx + 1 < len(sys.argv[1:]):
            db_path = sys.argv[1:][idx + 1]

    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    rest = args[1:]

    if cmd == "add":
        cmd_add(rest, db_path)
    elif cmd == "list":
        cmd_list(rest, db_path)
    elif cmd == "delete":
        cmd_delete(rest, db_path)
    elif cmd == "export":
        cmd_export(rest, db_path)
    elif cmd == "search":
        cmd_search(rest, db_path)
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        print("可用命令: add, list, delete, export, search", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
