#!/usr/bin/env python3
from typing import Any
# -*- coding: utf-8 -*-
"""
错误处理器

功能：处理导入过程中的错误，包括备份、日志记录
"""

import shutil
from datetime import datetime
from pathlib import Path


class ErrorLog:
    """错误日志"""

    def __init__(self) -> None:
        self.errors = []
        self.warnings = []

    def add_error(self, error_message) -> None:
        """添加错误"""
        self.errors.append({"timestamp": datetime.now().isoformat(), "message": error_message})

    def add_warning(self, warning_message) -> None:
        """添加警告"""
        self.warnings.append({"timestamp": datetime.now().isoformat(), "message": warning_message})

    def has_errors(self) -> Any:
        """是否有错误"""
        return len(self.errors) > 0

    def save(self, log_path) -> None:
        """保存错误日志到文件"""
        log_file = Path(log_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"导入错误日志\n")
            f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            if self.errors:
                f.write(f"错误 ({len(self.errors)} 条):\n")
                for error in self.errors:
                    f.write(f"[{error['timestamp']}] {error['message']}\n")
                f.write("\n")

            if self.warnings:
                f.write(f"警告 ({len(self.warnings)} 条):\n")
                for warning in self.warnings:
                    f.write(f"[{warning['timestamp']}] {warning['message']}\n")


def backup_file(source_path, backup_path) -> Any:
    """备份文件

    Args:
        source_path: 源文件路径
        backup_path: 备份文件路径

    Returns:
        Path: 备份文件路径
    """
    source = Path(source_path)
    backup = Path(backup_path)

    backup.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source, backup)

    return backup


def log_error(error_message, error_log) -> None:
    """记录错误到日志

    Args:
        error_message: 错误消息
        error_log: ErrorLog 对象
    """
    error_log.add_error(error_message)
