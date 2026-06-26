#!/usr/bin/env python3
"""
File Auto Organizer - 文件自动整理工具
"""
import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# 文件类型映射
FILE_TYPES = {
    "Images": ["jpg", "jpeg", "png", "gif", "webp", "svg", "psd", "ai", "bmp", "ico", "tiff"],
    "Documents": ["pdf", "doc", "docx", "txt", "md", "xls", "xlsx", "ppt", "pptx", "odt", "rtf"],
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"],
    "Videos": ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm"],
    "Audio": ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"],
    "Code": ["py", "js", "java", "cpp", "c", "h", "html", "css", "json", "xml", "sh", "go", "rs"],
}

def get_category(ext):
    ext = ext.lower().strip(".")
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_by_type(folder_path, report=False):
    folder = Path(folder_path).expanduser().resolve()
    if not folder.exists():
        print(f"❌ 文件夹不存在: {folder}")
        return
    
    stats = defaultdict(int)
    moved = []
    
    for item in folder.iterdir():
        if item.is_file():
            ext = item.suffix
            category = get_category(ext)
            target_dir = folder / category
            
            if not target_dir.exists():
                target_dir.mkdir(exist_ok=True)
            
            new_path = target_dir / item.name
            # 避免覆盖同名文件
            if new_path.exists():
                new_path = target_dir / f"{item.stem}_{item.suffix}"
            
            shutil.move(str(item), str(new_path))
            moved.append((item.name, category))
            stats[category] += 1
    
    print(f"✅ 整理完成！共移动 {len(moved)} 个文件")
    print()
    
    if report:
        print("📊 分类统计:")
        for cat, count in sorted(stats.items(), key=lambda x: -x[1]):
            print(f"   {cat}: {count}")

def organize_by_date(folder_path, report=False):
    folder = Path(folder_path).expanduser().resolve()
    if not folder.exists():
        print(f"❌ 文件夹不存在: {folder}")
        return
    
    now = datetime.now()
    today = now.date()
    
    date_folders = {
        "Today": today,
        "Yesterday": today.replace(day=max(1, today.day - 1)),
        "This Week": None,
        "This Month": None,
        "Older": None,
    }
    
    stats = defaultdict(int)
    moved = []
    
    for item in folder.iterdir():
        if item.is_file():
            mtime = datetime.fromtimestamp(item.stat().st_mtime).date()
            
            if mtime == today:
                target = "Today"
            elif mtime == date_folders["Yesterday"]:
                target = "Yesterday"
            elif (today - mtime).days < 7:
                target = "This Week"
            elif (today - mtime).days < 30:
                target = "This Month"
            else:
                target = "Older"
            
            target_dir = folder / target
            if not target_dir.exists():
                target_dir.mkdir(exist_ok=True)
            
            new_path = target_dir / item.name
            if new_path.exists():
                new_path = target_dir / f"{item.stem}_{item.suffix}"
            
            shutil.move(str(item), str(new_path))
            moved.append((item.name, target))
            stats[target] += 1
    
    print(f"✅ 整理完成！共移动 {len(moved)} 个文件")
    
    if report:
        print()
        print("📊 分类统计:")
        for cat in ["Today", "Yesterday", "This Week", "This Month", "Older"]:
            if cat in stats:
                print(f"   {cat}: {stats[cat]}")

def show_stats(folder_path):
    folder = Path(folder_path).expanduser().resolve()
    if not folder.exists():
        print(f"❌ 文件夹不存在: {folder}")
        return
    
    stats = defaultdict(int)
    total_size = 0
    
    for item in folder.iterdir():
        if item.is_file():
            ext = item.suffix
            category = get_category(ext)
            stats[category] += 1
            total_size += item.stat().st_size
    
    print(f"📁 {folder}")
    print(f"📊 文件统计:")
    
    for cat, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count} 个文件")
    
    print(f"\n💾 总大小: {total_size / 1024 / 1024:.2f} MB")

def main():
    parser = argparse.ArgumentParser(description="File Auto Organizer")
    subparsers = parser.add_subparsers()
    
    p_org = subparsers.add_parser("organize", help="整理文件夹（按类型）")
    p_org.add_argument("folder", help="要整理的文件夹路径")
    p_org.add_argument("--report", action="store_true", help="生成报告")
    p_org.set_defaults(func=lambda args: organize_by_type(args.folder, args.report))
    
    p_type = subparsers.add_parser("by-type", help="按类型整理")
    p_type.add_argument("folder", help="要整理的文件夹路径")
    p_type.add_argument("--report", action="store_true", help="生成报告")
    p_type.set_defaults(func=lambda args: organize_by_type(args.folder, args.report))
    
    p_date = subparsers.add_parser("by-date", help="按日期整理")
    p_date.add_argument("folder", help="要整理的文件夹路径")
    p_date.add_argument("--report", action="store_true", help="生成报告")
    p_date.set_defaults(func=lambda args: organize_by_date(args.folder, args.report))
    
    p_stats = subparsers.add_parser("stats", help="查看统计")
    p_stats.add_argument("folder", help="文件夹路径")
    p_stats.set_defaults(func=show_stats)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
