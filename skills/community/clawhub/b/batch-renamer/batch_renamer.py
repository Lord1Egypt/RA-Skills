#!/usr/bin/env python3
"""
Batch Renamer - 批量文件重命名工具
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path


class BatchRenamer:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.backup_file = self.directory / ".batch-renamer-backup.json"
        self.backup_data = {}

    def load_backup(self):
        if self.backup_file.exists():
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)
        return self.backup_data

    def save_backup(self, mappings):
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

    def get_files(self, extensions=None):
        files = []
        for item in self.directory.iterdir():
            if item.is_file():
                if extensions:
                    if item.suffix.lower() in extensions:
                        files.append(item)
                else:
                    files.append(item)
        return sorted(files)

    def generate_name(self, pattern, index, original_path):
        name = pattern
        original_stem = original_path.stem
        original_ext = original_path.suffix.lstrip('.')

        # 替换序号
        name = name.replace('{001}', f'{index+1:03d}')
        name = name.replace('{01}', f'{index+1:02d}')
        name = name.replace('{1}', f'{index+1}')

        # 替换日期
        now = datetime.now()
        name = name.replace('{YYYY}', f'{now.year:04d}')
        name = name.replace('{MM}', f'{now.month:02d}')
        name = name.replace('{DD}', f'{now.day:02d}')
        name = name.replace('{HH}', f'{now.hour:02d}')
        name = name.replace('{mm}', f'{now.minute:02d}')

        # 替换原始文件名
        name = name.replace('{original}', original_stem)
        name = name.replace('{ext}', original_ext)

        return name

    def apply_regex(self, filename, pattern):
        if pattern.startswith('s/'):
            parts = pattern.split('/')
            if len(parts) >= 3:
                search = parts[1]
                replace = parts[2]
                flags = 0
                if len(parts) > 3 and 'g' in parts[3]:
                    flags = re.GLOBAL
                return re.sub(search, replace, filename, count=0 if flags else 1)
        return filename

    def rename(self, pattern=None, regex=None, preview=False):
        files = self.get_files()
        mappings = {}

        for i, file_path in enumerate(files):
            old_name = file_path.name
            if pattern:
                new_name = self.generate_name(pattern, i, file_path)
            elif regex:
                new_name = self.apply_regex(old_name, regex)
            else:
                continue

            new_path = self.directory / new_name
            mappings[str(file_path)] = str(new_path)

            if preview:
                print(f"预览: {old_name} -> {new_name}")

        if preview:
            return mappings

        confirm = input(f"即将重命名 {len(mappings)} 个文件，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return {}

        # 保存备份
        self.save_backup(mappings)

        # 执行重命名
        for old_str, new_str in mappings.items():
            old_path = Path(old_str)
            new_path = Path(new_str)
            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)
                print(f"重命名: {old_path.name} -> {new_path.name}")

        return mappings

    def undo(self):
        backup = self.load_backup()
        if not backup:
            print("没有找到备份文件，无法撤销")
            return False

        # 反向映射来撤销
        reverse_mappings = {v: k for k, v in backup.items()}
        count = 0

        for new_str, old_str in reverse_mappings.items():
            new_path = Path(new_str)
            old_path = Path(old_str)
            if new_path.exists() and not old_path.exists():
                new_path.rename(old_path)
                print(f"撤销: {new_path.name} -> {old_path.name}")
                count += 1

        if count > 0:
            # 删除备份文件
            self.backup_file.unlink(missing_ok=True)
            print(f"已撤销 {count} 个文件的重命名")
            return True
        else:
            print("没有需要撤销的文件")
            return False


def main():
    parser = argparse.ArgumentParser(description="批量文件重命名工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # rename 命令
    rename_parser = subparsers.add_parser("rename", help="重命名文件")
    rename_parser.add_argument("directory", help="目标目录")
    rename_parser.add_argument("--pattern", help="命名模式")
    rename_parser.add_argument("--regex", help="正则表达式替换")
    rename_parser.add_argument("--preview", action="store_true", help="预览模式")

    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销重命名")
    undo_parser.add_argument("directory", help="目标目录")

    args = parser.parse_args()

    if args.command == "rename":
        renamer = BatchRenamer(args.directory)
        renamer.rename(pattern=args.pattern, regex=args.regex, preview=args.preview)
    elif args.command == "undo":
        renamer = BatchRenamer(args.directory)
        renamer.undo()


if __name__ == "__main__":
    main()
