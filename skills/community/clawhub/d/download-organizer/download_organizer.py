#!/usr/bin/env python3
"""
Download Organizer - 下载文件自动分类工具
"""

import os
import json
import argparse
from pathlib import Path
from shutil import copy2


class DownloadOrganizer:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir / "Organized"
        self.backup_file = self.output_dir / ".download-organizer-backup.json"
        self.backup_data = {}

        self.default_categories = {
            "documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"],
            "videos": [".mp4", ".avi", ".mov", ".mkv"],
            "audio": [".mp3", ".wav", ".flac", ".aac"],
            "installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
            "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".go", ".rs"],
        }

    def load_backup(self):
        if self.backup_file.exists():
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)
        return self.backup_data

    def save_backup(self, mappings):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

    def get_files(self):
        files = []
        for item in self.input_dir.iterdir():
            if item.is_file():
                files.append(item)
        return sorted(files)

    def get_category(self, file_path):
        suffix = file_path.suffix.lower()
        for category, extensions in self.default_categories.items():
            if suffix in extensions:
                return category
        return "others"

    def get_folder_path(self, file_path):
        category = self.get_category(file_path)
        return self.output_dir / category

    def organize(self, preview=False):
        files = self.get_files()
        mappings = {}

        for file_path in files:
            target_folder = self.get_folder_path(file_path)
            target_path = target_folder / file_path.name

            mappings[str(file_path)] = str(target_path)

            if preview:
                category = self.get_category(file_path)
                print(f"预览: {file_path.name} -> {category}/{file_path.name}")

        if preview:
            return mappings

        confirm = input(f"即将整理 {len(mappings)} 个文件，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return {}

        # 保存备份
        self.save_backup(mappings)

        # 执行整理
        for old_str, new_str in mappings.items():
            old_path = Path(old_str)
            new_path = Path(new_str)
            new_path.parent.mkdir(parents=True, exist_ok=True)
            if old_path.exists() and not new_path.exists():
                copy2(old_path, new_path)
                category = self.get_category(old_path)
                print(f"整理: {old_path.name} -> {category}/{old_path.name}")

        return mappings

    def undo(self):
        backup = self.load_backup()
        if not backup:
            print("没有找到备份文件，无法撤销")
            return False

        reverse_mappings = {v: k for k, v in backup.items()}
        count = 0

        for new_str, old_str in reverse_mappings.items():
            new_path = Path(new_str)
            old_path = Path(old_str)
            if new_path.exists() and not old_path.exists():
                copy2(new_path, old_path)
                new_path.unlink()
                print(f"撤销: {new_path.name} -> {old_path.name}")
                count += 1

        if count > 0:
            self.backup_file.unlink(missing_ok=True)
            print(f"已撤销 {count} 个文件的整理")
            return True
        else:
            print("没有需要撤销的文件")
            return False


def main():
    parser = argparse.ArgumentParser(description="下载文件自动分类工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # organize 命令
    organize_parser = subparsers.add_parser("organize", help="整理文件")
    organize_parser.add_argument("directory", help="要整理的目录")
    organize_parser.add_argument("--output", help="输出目录")
    organize_parser.add_argument("--preview", action="store_true", help="预览模式")

    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销整理")
    undo_parser.add_argument("directory", help="输出目录")

    args = parser.parse_args()

    if args.command == "organize":
        organizer = DownloadOrganizer(args.directory, args.output)
        organizer.organize(preview=args.preview)
    elif args.command == "undo":
        organizer = DownloadOrganizer(args.directory, args.directory)
        organizer.undo()


if __name__ == "__main__":
    main()
