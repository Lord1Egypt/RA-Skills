
#!/usr/bin/env python3
"""
File Sorter - 文件智能分类工具
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
import shutil


class FileSorter:
    DEFAULT_CATEGORIES = {
        "documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"],
        "videos": [".mp4", ".avi", ".mov", ".mkv"],
        "audio": [".mp3", ".wav", ".flac", ".aac"],
        "installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
        "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    }

    DEFAULT_SIZE_RULES = {
        "small": (0, 1024 * 1024),  # < 1MB
        "medium": (1024 * 1024, 100 * 1024 * 1024),  # 1MB - 100MB
        "large": (100 * 1024 * 1024, None),  # > 100MB
    }

    def __init__(self, input_dir, output_dir=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir
        self.backup_file = self.output_dir / ".file-sorter-backup.json"
        self.backup_data = []

    def load_backup(self):
        if self.backup_file.exists():
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)
        return self.backup_data

    def save_backup(self, operations):
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(operations, f, indent=2, ensure_ascii=False)

    def get_files(self):
        files = []
        for item in self.input_dir.iterdir():
            if item.is_file():
                files.append(item)
        return sorted(files)

    def get_category_by_type(self, file_path, categories=None):
        cats = categories or self.DEFAULT_CATEGORIES
        suffix = file_path.suffix.lower()
        for category, extensions in cats.items():
            if suffix in extensions:
                return category
        return "others"

    def get_category_by_size(self, file_path, size_rules=None):
        rules = size_rules or self.DEFAULT_SIZE_RULES
        size = file_path.stat().st_size
        for category, (min_size, max_size) in rules.items():
            if min_size <= size:
                if max_size is None or size < max_size:
                    return category
        return "others"

    def get_category_by_date(self, file_path, date_type="modified"):
        stat = file_path.stat()
        if date_type == "created":
            ts = stat.st_ctime
        elif date_type == "accessed":
            ts = stat.st_atime
        else:  # modified
            ts = stat.st_mtime
        dt = datetime.fromtimestamp(ts)
        return f"{dt.year}/{dt.month:02d}/{dt.day:02d}"

    def organize(self, by_type=False, by_size=False, by_date=None, 
                 action="move", categories=None, size_rules=None, preview=False):
        files = self.get_files()
        operations = []

        for file_path in files:
            target_category = None

            # 优先级：类型 > 大小 > 日期
            if by_type:
                target_category = self.get_category_by_type(file_path, categories)
            elif by_size:
                target_category = self.get_category_by_size(file_path, size_rules)
            elif by_date:
                target_category = self.get_category_by_date(file_path, by_date)

            if target_category:
                target_dir = self.output_dir / target_category
                target_path = target_dir / file_path.name
                operations.append({
                    "source": str(file_path),
                    "target": str(target_path),
                    "action": action
                })

                if preview:
                    print(f"预览: {file_path.name} -> {target_category}/{file_path.name} [{action}]")

        if preview:
            return operations

        if not operations:
            print("没有需要整理的文件")
            return []

        confirm = input(f"即将整理 {len(operations)} 个文件，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return []

        # 保存备份
        self.save_backup(operations)

        # 执行操作
        for op in operations:
            source = Path(op["source"])
            target = Path(op["target"])
            target.parent.mkdir(parents=True, exist_ok=True)

            if op["action"] == "move":
                shutil.move(str(source), str(target))
                print(f"移动: {source.name} -> {target.parent.name}/{source.name}")
            elif op["action"] == "copy":
                shutil.copy2(str(source), str(target))
                print(f"复制: {source.name} -> {target.parent.name}/{source.name}")
            elif op["action"] == "link":
                target.symlink_to(source)
                print(f"链接: {source.name} -> {target.parent.name}/{source.name}")

        return operations

    def undo(self):
        backup = self.load_backup()
        if not backup:
            print("没有找到备份文件，无法撤销")
            return False

        count = 0
        # 反向操作，从后往前
        for op in reversed(backup):
            source = Path(op["source"])
            target = Path(op["target"])

            if op["action"] == "move":
                if target.exists() and not source.exists():
                    source.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(target), str(source))
                    print(f"撤销移动: {target.name} -> {source.parent.name}/{target.name}")
                    count += 1
            elif op["action"] == "copy":
                if target.exists():
                    target.unlink()
                    print(f"撤销复制: 删除 {target.name}")
                    count += 1
            elif op["action"] == "link":
                if target.exists() and target.is_symlink():
                    target.unlink()
                    print(f"撤销链接: 删除 {target.name}")
                    count += 1

        if count > 0:
            # 删除备份文件
            self.backup_file.unlink(missing_ok=True)
            print(f"已撤销 {count} 个操作")
            return True
        else:
            print("没有需要撤销的操作")
            return False


def main():
    parser = argparse.ArgumentParser(description="文件智能分类工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # organize 命令
    organize_parser = subparsers.add_parser("organize", help="整理文件")
    organize_parser.add_argument("input_dir", help="输入目录")
    organize_parser.add_argument("--output", help="输出目录（默认同输入目录）")
    organize_parser.add_argument("--by-type", action="store_true", help="按文件类型分类")
    organize_parser.add_argument("--by-size", action="store_true", help="按文件大小分类")
    organize_parser.add_argument("--by-date", choices=["created", "modified", "accessed"], help="按文件日期分类")
    organize_parser.add_argument("--action", choices=["move", "copy", "link"], default="move", help="操作类型（默认：move）")
    organize_parser.add_argument("--preview", action="store_true", help="预览模式")

    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销整理")
    undo_parser.add_argument("output_dir", help="输出目录")

    args = parser.parse_args()

    if args.command == "organize":
        sorter = FileSorter(args.input_dir, args.output)
        sorter.organize(
            by_type=args.by_type,
            by_size=args.by_size,
            by_date=args.by_date,
            action=args.action,
            preview=args.preview
        )
    elif args.command == "undo":
        sorter = FileSorter(args.output_dir, args.output_dir)
        sorter.undo()


if __name__ == "__main__":
    main()
