#!/usr/bin/env python3
"""
Checkpoint 管理脚本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
功能:
  - 列出所有 checkpoint 及大小
  - 清理旧 checkpoint（保留 best + 每 N 步一个）
  - 归档 checkpoint 到指定位置
  - 磁盘用量统计

用法:
  python3 checkpoint_mgmt.py --name MyProject list            # 列出所有 checkpoint
  python3 checkpoint_mgmt.py --name MyProject clean --keep 3  # 每个运行只保留最近3个
  python3 checkpoint_mgmt.py --name MyProject archive --to /archive/path
  python3 checkpoint_mgmt.py --name MyProject stats           # 磁盘用量统计
  python3 checkpoint_mgmt.py --name MyProject clean --dry-run # 预览清理
"""

import argparse
import os
import sys
import shutil
from datetime import datetime


def human_size(size_bytes: int) -> str:
    """字节转可读大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def find_all_checkpoints(base: str) -> list:
    """扫描项目中所有 checkpoint"""
    checkpoints = []
    for root, dirs, files in os.walk(base):
        if 'checkpoints' in root:
            for f in files:
                if f.startswith('.') or f == '.gitkeep':
                    continue
                fpath = os.path.join(root, f)
                size = os.path.getsize(fpath)
                mtime = os.path.getmtime(fpath)
                rel = os.path.relpath(fpath, base)
                checkpoints.append({
                    "path": fpath,
                    "rel_path": rel,
                    "size": size,
                    "mtime": mtime,
                    "run_dir": os.path.dirname(os.path.dirname(fpath)),
                })
    return sorted(checkpoints, key=lambda x: x["size"], reverse=True)


def cmd_list(base: str, project_name: str):
    """列出所有 checkpoint"""
    print(f"\n{'='*60}")
    print(f"📦 Checkpoint 清单: {project_name}")
    print(f"{'='*60}\n")

    ckpts = find_all_checkpoints(base)
    if not ckpts:
        print("  🕐 未找到任何 checkpoint")
        return

    total_size = sum(c["size"] for c in ckpts)
    print(f"  📊 共 {len(ckpts)} 个 checkpoint，总大小 {human_size(total_size)}\n")
    print(f"  {'大小':<12} {'修改时间':<20} {'路径'}")
    print(f"  {'─'*12} {'─'*20} {'─'*40}")

    # 按运行分组显示
    run_groups = {}
    for c in ckpts:
        run_key = c.get("run_dir", "unknown")
        if run_key not in run_groups:
            run_groups[run_key] = []
        run_groups[run_key].append(c)

    for run_dir, items in sorted(run_groups.items()):
        run_name = os.path.relpath(run_dir, base)
        run_size = sum(i["size"] for i in items)
        print(f"\n  📁 {run_name} ({len(items)} 个, {human_size(run_size)})")
        for item in items[:10]:  # 每个运行最多显示10个
            mtime = datetime.fromtimestamp(item["mtime"]).strftime("%Y-%m-%d %H:%M")
            print(f"     {human_size(item['size']):<12} {mtime:<20} {os.path.basename(item['rel_path'])}")
        if len(items) > 10:
            print(f"     ... 还有 {len(items) - 10} 个文件")


def cmd_clean(base: str, project_name: str, keep: int = 3, dry_run: bool = False):
    """清理旧 checkpoint，每个运行只保留最近 N 个"""
    print(f"\n{'='*60}")
    print(f"🧹 Checkpoint 清理: {project_name}")
    if dry_run:
        print(f"   🔍 预览模式（不会实际删除）")
    print(f"   📌 每个运行保留最近 {keep} 个 checkpoint")
    print(f"{'='*60}\n")

    ckpts = find_all_checkpoints(base)
    if not ckpts:
        print("  🕐 未找到任何 checkpoint")
        return

    # 按运行分组，每组保留 keep 个最新的
    run_groups = {}
    for c in ckpts:
        run_key = c.get("run_dir", "unknown")
        if run_key not in run_groups:
            run_groups[run_key] = []
        run_groups[run_key].append(c)

    total_deleted = 0
    total_freed = 0

    for run_dir, items in sorted(run_groups.items()):
        run_name = os.path.relpath(run_dir, base)
        # 按修改时间排序，最新的在前
        items_sorted = sorted(items, key=lambda x: x["mtime"], reverse=True)
        to_delete = items_sorted[keep:]
        to_keep = items_sorted[:keep]

        if not to_delete:
            print(f"  ✅ {run_name}: {len(items)} 个 (全部保留)")
            continue

        freed = sum(d["size"] for d in to_delete)
        total_deleted += len(to_delete)
        total_freed += freed

        print(f"  🗑 {run_name}: 保留 {len(to_keep)} 个, 删除 {len(to_delete)} 个 "
              f"(释放 {human_size(freed)})")

        if not dry_run:
            for d in to_delete:
                try:
                    os.remove(d["path"])
                    print(f"     ❌ 删除: {os.path.basename(d['rel_path'])}")
                except OSError as e:
                    print(f"     ⚠️ 删除失败: {os.path.basename(d['rel_path'])} - {e}")

    if total_deleted > 0:
        action = "将删除" if dry_run else "已删除"
        print(f"\n  📊 {action} {total_deleted} 个 checkpoint, 释放 {human_size(total_freed)}")
    else:
        print(f"\n  ✅ 无需清理")


def cmd_archive(base: str, project_name: str, archive_to: str):
    """归档所有 checkpoint 到指定位置"""
    print(f"\n{'='*60}")
    print(f"📦 Checkpoint 归档: {project_name}")
    print(f"   目标: {archive_to}")
    print(f"{'='*60}\n")

    ckpts = find_all_checkpoints(base)
    if not ckpts:
        print("  🕐 未找到任何 checkpoint")
        return

    os.makedirs(archive_to, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    archive_dir = os.path.join(archive_to, f"{project_name}_ckpt_{today}")
    os.makedirs(archive_dir, exist_ok=True)

    total_size = sum(c["size"] for c in ckpts)
    print(f"  📊 共 {len(ckpts)} 个 checkpoint, {human_size(total_size)}")
    print(f"  📁 归档到: {archive_dir}\n")

    copied = 0
    for c in ckpts:
        # 保持目录结构
        rel = os.path.relpath(c["path"], base)
        dest = os.path.join(archive_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            shutil.copy2(c["path"], dest)
            copied += 1
            if copied % 10 == 0:
                print(f"  ✅ 已复制 {copied}/{len(ckpts)} ...")
        except OSError as e:
            print(f"  ⚠️ 复制失败: {rel} - {e}")

    print(f"\n  ✅ 归档完成: {copied} 个文件 → {archive_dir}")


def cmd_stats(base: str, project_name: str):
    """磁盘用量统计"""
    print(f"\n{'='*60}")
    print(f"💾 磁盘用量统计: {project_name}")
    print(f"{'='*60}\n")

    # 按模块统计
    modules = {
        "01_data": "数据层",
        "02_tokenization": "分词层",
        "03_models": "模型层",
        "04_experiments": "实验管理",
        "05_docs": "文档",
        "06_shared": "共享资源",
    }

    total = 0
    for mod_dir, mod_name in modules.items():
        mod_path = os.path.join(base, mod_dir)
        if not os.path.isdir(mod_path):
            continue
        mod_size = 0
        for dirpath, dirnames, filenames in os.walk(mod_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    mod_size += os.path.getsize(fp)
        total += mod_size
        print(f"  {mod_name:<10} {human_size(mod_size):>12}")

    print(f"  {'─'*25}")
    print(f"  {'总计':<10} {human_size(total):>12}")

    # Checkpoint 专项统计
    ckpts = find_all_checkpoints(base)
    if ckpts:
        ckpt_size = sum(c["size"] for c in ckpts)
        print(f"\n  📦 Checkpoint: {len(ckpts)} 个, {human_size(ckpt_size)} "
              f"({ckpt_size/total*100:.1f}% 总空间)")


def main():
    parser = argparse.ArgumentParser(
        description="AI 项目 Checkpoint 管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  checkpoint_mgmt.py --name MyLLM list                        # 列出所有 checkpoint
  checkpoint_mgmt.py --name MyLLM clean --keep 3               # 每运行保留3个最新
  checkpoint_mgmt.py --name MyLLM clean --keep 3 --dry-run     # 预览清理
  checkpoint_mgmt.py --name MyLLM archive --to /backup/ckpts   # 归档
  checkpoint_mgmt.py --name MyLLM stats                        # 磁盘统计
        """)

    parser.add_argument("--name", type=str, required=True, help="项目名称")
    parser.add_argument("--output", type=str, default=".", help="项目父目录")
    parser.add_argument("command", choices=["list", "clean", "archive", "stats"],
                        help="操作命令")
    parser.add_argument("--keep", type=int, default=3,
                        help="每个运行保留的 checkpoint 数量 (用于 clean, 默认3)")
    parser.add_argument("--to", type=str, help="归档目标路径 (用于 archive)")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际删除")
    args = parser.parse_args()

    base = os.path.join(args.output, args.name)
    if not os.path.isdir(base):
        print(f"❌ 项目不存在: {base}")
        sys.exit(1)

    if args.command == "list":
        cmd_list(base, args.name)
    elif args.command == "clean":
        cmd_clean(base, args.name, keep=args.keep, dry_run=args.dry_run)
    elif args.command == "archive":
        if not args.to:
            parser.error("archive 命令需要 --to <目标路径>")
        cmd_archive(base, args.name, args.to)
    elif args.command == "stats":
        cmd_stats(base, args.name)


if __name__ == "__main__":
    main()
