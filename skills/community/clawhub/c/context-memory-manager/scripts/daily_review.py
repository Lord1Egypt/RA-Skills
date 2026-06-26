#!/usr/bin/env python3
"""
Daily Memory Review - Incremental Scanner
扫描 workspace 中的记忆文件，做增量对比，输出结构化报告供 agent 执行复盘。

用法:
    python3 daily_review.py --workspace /path/to/workspace [--days 7] [--dry-run]
                            [--archive-days 30]

输出 JSON 格式，包含：
- 上次复盘时间
- 新增/变更的文件列表（增量）
- 文件分类统计
- token 估算（帮助 agent 判断复盘消耗）
- agent 执行指令
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta


def read_last_review(workspace):
    """读取上次复盘时间戳"""
    last_review_file = os.path.join(workspace, ".last_review")
    if os.path.exists(last_review_file):
        with open(last_review_file, "r") as f:
            return f.read().strip()
    return None


def write_last_review(workspace):
    """写入本次复盘时间戳"""
    last_review_file = os.path.join(workspace, ".last_review")
    with open(last_review_file, "w") as f:
        f.write(datetime.now().isoformat())


def scan_memory_files(workspace, days=7):
    """扫描记忆目录，分类文件"""
    memory_base = os.path.join(workspace, "memory")
    chat_dir = os.path.join(memory_base, "chat")
    project_dir = os.path.join(memory_base, "projects")

    result = {
        "chat_files": [],
        "project_files": [],
        "memory_md": None,
    }

    # 扫描聊天日志
    if os.path.exists(chat_dir):
        for fname in sorted(os.listdir(chat_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(chat_dir, fname)
            stat = os.stat(fpath)
            result["chat_files"].append({
                "file": fname,
                "path": fpath,
                "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 1),
            })

    # 扫描项目日志
    if os.path.exists(project_dir):
        for project_name in sorted(os.listdir(project_dir)):
            project_path = os.path.join(project_dir, project_name)
            if not os.path.isdir(project_path):
                continue
            for fname in sorted(os.listdir(project_path)):
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(project_path, fname)
                stat = os.stat(fpath)
                result["project_files"].append({
                    "project": project_name,
                    "file": fname,
                    "path": fpath,
                    "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size_bytes": stat.st_size,
                    "size_kb": round(stat.st_size / 1024, 1),
                })

    # MEMORY.md
    memory_md = os.path.join(workspace, "MEMORY.md")
    if os.path.exists(memory_md):
        stat = os.stat(memory_md)
        result["memory_md"] = {
            "path": memory_md,
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 1),
            "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }

    return result


def filter_incremental(files, since_iso=None):
    """根据时间戳过滤出新增/变更的文件"""
    if not since_iso:
        return files  # 首次复盘，返回全部

    try:
        since = datetime.fromisoformat(since_iso)
        # 统一去掉时区信息，避免 naive/aware 比较报错
        if since.tzinfo is not None:
            since = since.replace(tzinfo=None)
    except ValueError:
        return files  # 解析失败，返回全部

    result = []
    for f in files:
        try:
            ftime = datetime.fromisoformat(f["mtime"])
            if ftime.tzinfo is not None:
                ftime = ftime.replace(tzinfo=None)
            if ftime > since:
                result.append(f)
        except (ValueError, KeyError):
            continue
    return result


def estimate_tokens(byte_count):
    """
    根据字节数估算 token 量。
    中文约 1.5-2 字节/token，英文约 4 字节/token。
    Markdown 混合内容取保守值 2.5 字节/token。
    """
    return round(byte_count / 2.5)


def archive_old_files(workspace, archive_days=30):
    """
    将超过指定天数的聊天日志归档到 memory/archive/ 目录。
    """
    memory_base = os.path.join(workspace, "memory")
    chat_dir = os.path.join(memory_base, "chat")
    archive_dir = os.path.join(memory_base, "archive")

    if not os.path.exists(chat_dir):
        return {"archived": [], "total_archived_kb": 0}

    cutoff = datetime.now() - timedelta(days=archive_days)
    archived = []
    total_archived_bytes = 0

    for fname in sorted(os.listdir(chat_dir)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(chat_dir, fname)
        mtime = datetime.fromtimestamp(os.stat(fpath).st_mtime)
        if mtime < cutoff:
            os.makedirs(archive_dir, exist_ok=True)
            archive_path = os.path.join(archive_dir, fname)
            shutil.move(fpath, archive_path)
            stat = os.stat(archive_path)
            archived.append({
                "file": fname,
                "size_kb": round(stat.st_size / 1024, 1),
                "archived_to": archive_path,
            })
            total_archived_bytes += stat.st_size

    return {
        "archived": archived,
        "total_archived_kb": round(total_archived_bytes / 1024, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="每日记忆复盘 - 增量扫描器")
    parser.add_argument("--workspace", type=str, required=True,
                        help="Agent workspace 路径")
    parser.add_argument("--days", type=int, default=7,
                        help="扫描最近 N 天的文件 (default: 7)")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅扫描，不执行修改")
    parser.add_argument("--update-timestamp", action="store_true",
                        help="扫描后更新 .last_review 时间戳")
    parser.add_argument("--archive-days", type=int, default=30,
                        help="超过 N 天的聊天日志自动归档 (default: 30, 0=禁用)")
    args = parser.parse_args()

    workspace = os.path.expanduser(args.workspace)
    if not os.path.isdir(workspace):
        print(json.dumps({
            "error": f"workspace 不存在: {workspace}",
            "timestamp": datetime.now().isoformat()
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    # 上次复盘时间
    last_review = read_last_review(workspace)

    # 扫描所有文件
    all_files = scan_memory_files(workspace, args.days)

    # 增量过滤
    incremental_chat = filter_incremental(all_files["chat_files"], last_review)
    incremental_projects = filter_incremental(all_files["project_files"], last_review)

    # 分类统计
    stats = {
        "total_chat": len(all_files["chat_files"]),
        "new_chat": len(incremental_chat),
        "total_projects": len(all_files["project_files"]),
        "new_projects": len(incremental_projects),
    }

    # Token 估算（帮助 agent 判断复盘会消耗多少上下文）
    incremental_chat_bytes = sum(f["size_bytes"] for f in incremental_chat)
    incremental_project_bytes = sum(f["size_bytes"] for f in incremental_projects)
    memory_md_bytes = all_files["memory_md"]["size_bytes"] if all_files["memory_md"] else 0
    total_review_bytes = incremental_chat_bytes + incremental_project_bytes + memory_md_bytes

    report = {
        "timestamp": datetime.now().isoformat(),
        "workspace": workspace,
        "mode": "dry_run" if args.dry_run else "full_review",
        "last_review": last_review,
        "is_first_review": last_review is None,
        "statistics": stats,
        "incremental": {
            "chat_files": incremental_chat,
            "project_files": incremental_projects,
        },
        "all_files": all_files,
        "token_estimate": {
            "description": "复盘需读取的文件总 token 估算",
            "formula": "字节数 / 2.5（中文 Markdown 混合内容保守值）",
            "chat_bytes": incremental_chat_bytes,
            "chat_tokens": estimate_tokens(incremental_chat_bytes),
            "project_bytes": incremental_project_bytes,
            "project_tokens": estimate_tokens(incremental_project_bytes),
            "memory_md_bytes": memory_md_bytes,
            "memory_md_tokens": estimate_tokens(memory_md_bytes),
            "total_bytes": total_review_bytes,
            "total_tokens": estimate_tokens(total_review_bytes),
            "note": (
                "此 token 量是 agent 复盘时需要读取的输入量。"
                "如 total_tokens 超过模型上下文窗口的 30%，建议分批处理。"
            ),
        },
        "agent_instructions": {
            "step1": "读取 MEMORY.md 作为基线（如存在）",
            "step2": "读取 incremental.chat_files 中的聊天日志",
            "step3": "读取 incremental.project_files 中的项目日志",
            "step4": "分析并提炼：用户偏好、决策、待办、项目进展",
            "step5": "更新 MEMORY.md（用户偏好 + 项目索引）",
            "step6": "更新/创建项目日志（如有新的沉淀内容）",
            "step7": "输出复盘摘要报告",
            "step8": f"{'跳过' if args.dry_run else '执行'} --update-timestamp 写入 .last_review"
        },
    }

    # 归档旧文件
    if args.archive_days > 0 and not args.dry_run:
        archive_result = archive_old_files(workspace, args.archive_days)
        report["archive"] = archive_result

    # 更新 .last_review（如果要求）
    if args.update_timestamp and not args.dry_run:
        write_last_review(workspace)
        report["last_review_updated"] = True

    # 输出到 stdout（供 cron 日志捕获）
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # 持久化报告到磁盘，供 Agent 被唤醒时检查处理
    report_dir = "/tmp"
    report_path = os.path.join(report_dir, "cmm_review_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
