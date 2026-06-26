#!/usr/bin/env python3
"""
文件管理大师 - 核心实现
"""

import os
import sys
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import argparse
import json
import yaml

class FileMaster:
    """文件管理大师核心类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self.load_config(config_path)
        self.operation_log = []
        self.backup_dir = Path.home() / ".file-master" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "confirm_deletion": True,
            "backup_before_rename": True,
            "log_level": "info",
            "default_paths": {
                "downloads": str(Path.home() / "Downloads"),
                "documents": str(Path.home() / "Documents"),
                "pictures": str(Path.home() / "Pictures")
            },
            "rules": {
                "auto_organize_downloads": False,
                "clean_temp_files_daily": False
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                        user_config = yaml.safe_load(f)
                    else:
                        user_config = json.load(f)
                
                # 合并配置
                default_config.update(user_config)
            except Exception as e:
                print(f"警告：配置文件加载失败: {e}")
        
        return default_config
    
    def log_operation(self, operation: str, details: Dict[str, Any]):
        """记录操作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "success": True
        }
        self.operation_log.append(log_entry)
        
        if self.config["log_level"] in ["info", "debug"]:
            print(f"[操作日志] {operation}: {details}")
    
    def create_backup(self, file_path: str) -> str:
        """创建文件备份"""
        if not self.config["backup_before_rename"]:
            return ""
        
        source = Path(file_path)
        if not source.exists():
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source.stem}_{timestamp}{source.suffix}"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copy2(source, backup_path)
            return str(backup_path)
        except Exception as e:
            print(f"警告：备份失败 {file_path}: {e}")
            return ""
    
    def rename_files(self, directory: str, pattern: str, recursive: bool = False) -> Dict[str, Any]:
        """批量重命名文件"""
        result = {
            "total": 0,
            "renamed": 0,
            "failed": 0,
            "details": []
        }
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {**result, "error": f"目录不存在: {directory}"}
        
        # 收集文件
        files = []
        if recursive:
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    files.append(file_path)
        else:
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    files.append(file_path)
        
        result["total"] = len(files)
        
        # 按修改时间排序，确保顺序一致
        files.sort(key=lambda x: x.stat().st_mtime)
        
        for idx, file_path in enumerate(files, 1):
            try:
                # 创建备份
                backup_path = self.create_backup(str(file_path))
                
                # 生成新文件名
                if "{num" in pattern:
                    new_name = pattern.replace("{num}", f"{idx:03d}")
                    new_name = new_name.replace("{num:03d}", f"{idx:03d}")
                    new_name = new_name.replace("{num:04d}", f"{idx:04d}")
                else:
                    new_name = pattern
                
                # 替换日期变量
                if "{date" in new_name:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    new_name = new_name.replace("{date:YYYYMMDD}", mtime.strftime("%Y%m%d"))
                    new_name = new_name.replace("{date:YYYY-MM-DD}", mtime.strftime("%Y-%m-%d"))
                
                new_path = file_path.parent / new_name
                
                # 避免文件名冲突
                counter = 1
                original_new_path = new_path
                while new_path.exists():
                    stem = original_new_path.stem
                    suffix = original_new_path.suffix
                    new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                # 执行重命名
                file_path.rename(new_path)
                
                result["renamed"] += 1
                result["details"].append({
                    "old": str(file_path),
                    "new": str(new_path),
                    "backup": backup_path
                })
                
                self.log_operation("rename", {
                    "old": str(file_path),
                    "new": str(new_path),
                    "backup": backup_path
                })
                
            except Exception as e:
                result["failed"] += 1
                result["details"].append({
                    "file": str(file_path),
                    "error": str(e)
                })
        
        return result
    
    def organize_by_type(self, directory: str, recursive: bool = False) -> Dict[str, Any]:
        """按文件类型整理"""
        result = {
            "total": 0,
            "organized": 0,
            "failed": 0,
            "folders_created": [],
            "details": []
        }
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {**result, "error": f"目录不存在: {directory}"}
        
        # 文件类型分类
        type_folders = {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            "documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"],
            "videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv"],
            "audio": [".mp3", ".wav", ".flac", ".m4a"],
            "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "code": [".py", ".js", ".html", ".css", ".json", ".xml"],
            "executables": [".exe", ".msi", ".bat", ".sh"]
        }
        
        # 收集文件
        files = []
        if recursive:
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    files.append(file_path)
        else:
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    files.append(file_path)
        
        result["total"] = len(files)
        
        for file_path in files:
            try:
                suffix = file_path.suffix.lower()
                
                # 确定文件类型
                file_type = "others"
                for type_name, extensions in type_folders.items():
                    if suffix in extensions:
                        file_type = type_name
                        break
                
                # 创建类型文件夹
                type_dir = dir_path / file_type
                if not type_dir.exists():
                    type_dir.mkdir()
                    result["folders_created"].append(str(type_dir))
                
                # 移动文件
                new_path = type_dir / file_path.name
                
                # 避免文件名冲突
                counter = 1
                original_new_path = new_path
                while new_path.exists():
                    stem = original_new_path.stem
                    suffix = original_new_path.suffix
                    new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                # 创建备份
                backup_path = self.create_backup(str(file_path))
                
                # 移动文件
                shutil.move(str(file_path), str(new_path))
                
                result["organized"] += 1
                result["details"].append({
                    "file": str(file_path),
                    "type": file_type,
                    "new_location": str(new_path),
                    "backup": backup_path
                })
                
                self.log_operation("organize", {
                    "file": str(file_path),
                    "type": file_type,
                    "new_location": str(new_path)
                })
                
            except Exception as e:
                result["failed"] += 1
                result["details"].append({
                    "file": str(file_path),
                    "error": str(e)
                })
        
        return result
    
    def search_files(self, directory: str, content: Optional[str] = None, 
                    recursive: bool = True) -> Dict[str, Any]:
        """搜索文件"""
        result = {
            "total_searched": 0,
            "found": 0,
            "files": []
        }
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {**result, "error": f"目录不存在: {directory}"}
        
        # 收集文件
        files = []
        if recursive:
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    files.append(file_path)
        else:
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    files.append(file_path)
        
        result["total_searched"] = len(files)
        
        for file_path in files:
            try:
                file_info = {
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "type": file_path.suffix.lower()
                }
                
                # 内容搜索
                if content:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            file_content = f.read()
                            if content in file_content:
                                file_info["content_match"] = True
                                result["found"] += 1
                                result["files"].append(file_info)
                    except:
                        # 二进制文件跳过内容搜索
                        pass
                else:
                    # 仅文件信息
                    result["found"] += 1
                    result["files"].append(file_info)
                    
            except Exception as e:
                # 跳过无法访问的文件
                continue
        
        return result
    
    def find_duplicates(self, directory: str, recursive: bool = True) -> Dict[str, Any]:
        """查找重复文件"""
        result = {
            "total_files": 0,
            "duplicate_groups": 0,
            "duplicate_files": 0,
            "groups": []
        }
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {**result, "error": f"目录不存在: {directory}"}
        
        # 收集文件
        files = []
        if recursive:
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    files.append(file_path)
        else:
            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    files.append(file_path)
        
        result["total_files"] = len(files)
        
        # 按文件大小分组
        size_groups = {}
        for file_path in files:
            try:
                size = file_path.stat().st_size
                if size not in size_groups:
                    size_groups[size] = []
                size_groups[size].append(file_path)
            except:
                continue
        
        # 计算文件哈希（仅对大小相同的文件）
        hash_groups = {}
        for size, file_list in size_groups.items():
            if len(file_list) > 1:  # 只有大小相同的多个文件才需要计算哈希
                for file_path in file_list:
                    try:
                        file_hash = self.calculate_file_hash(file_path)
                        if file_hash not in hash_groups:
                            hash_groups[file_hash] = []
                        hash_groups[file_hash].append(file_path)
                    except:
                        continue
        
        # 整理结果
        for file_hash, file_list in hash_groups.items():
            if len(file_list) > 1:  # 真正的重复文件
                result["duplicate_groups"] += 1
                result["duplicate_files"] += len(file_list)
                
                group_info = {
                    "hash": file_hash,
                    "size": file_list[0].stat().st_size,
                    "files": [str(f) for f in file_list],
                    "suggested_keep": str(file_list[0])  # 建议保留第一个文件
                }
                result["groups"].append(group_info)
        
        return result
    
    def calculate_file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """计算文件哈希"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def get_operation_log(self) -> List[Dict[str, Any]]:
        """获取操作日志"""
        return self.operation_log
    
    def save_operation_log(self, file_path: str):
        """保存操作日志到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.operation_log, f, ensure_ascii=False, indent=2)

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="文件管理大师")
    parser.add_argument("--config", help="配置文件路径")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # rename命令
    rename_parser = subparsers.add_parser("rename", help="批量重命名文件")
    rename_parser.add_argument("directory", help="目录路径")
    rename_parser.add_argument("--pattern", required=True, help="重命名模式")
    rename_parser.add_argument("--recursive", action="store_true", help="递归处理")
    
    # organize命令
    organize_parser = subparsers.add_parser("organize", help="按类型整理文件")
    organize_parser.add_argument("directory", help="目录路径")
    organize_parser.add_argument("--recursive", action="store_true", help="递归处理")
    
    # search命令
    search_parser = subparsers.add_parser("search", help="搜索文件")
    search_parser.add_argument("directory", help="目录路径")
    search_parser.add_argument("--content", help="搜索内容")
    search_parser.add_argument("--recursive", action="store_true", help="递归搜索")
    
    # find-duplicates命令
    dup_parser = subparsers.add_parser("find-duplicates", help="查找重复文件")
    dup_parser.add_argument("directory", help="目录路径")
    dup_parser.add_argument("--recursive", action="store_true", help="递归查找")
    
    args = parser.parse_args()
    
    fm = FileMaster(args.config)
    
    if args.command == "rename":
        result = fm.rename_files(args.directory, args.pattern, args.recursive)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "organize":
        result = fm.organize_by_type(args.directory, args.recursive)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "search":
        result = fm.search_files(args.directory, args.content, args.recursive)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "find-duplicates":
        result = fm.find_duplicates(args.directory, args.recursive)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()