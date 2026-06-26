#!/usr/bin/env python3
"""
C 盘空间扫描分析脚本
扫描 C 盘使用情况，生成分析报告
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class CDriveScanner:
    def __init__(self, drive: str = "C:"):
        self.drive = drive
        self.root = Path(f"{drive}\\")
        self.user_home = Path(os.environ.get("USERPROFILE", f"{drive}\\Users\\Default"))
    
    def get_disk_info(self) -> dict:
        """获取磁盘基本信息"""
        import shutil
        total, used, free = shutil.disk_usage(self.drive)
        return {
            "drive": self.drive,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "used_percent": round((used / total) * 100, 1)
        }
    
    def scan_directory_size(self, path: Path) -> int:
        """计算目录总大小"""
        total_size = 0
        try:
            for item in path.rglob("*"):
                try:
                    if item.is_file():
                        total_size += item.stat().st_size
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass
        return total_size
    
    def scan_user_directories(self) -> list:
        """扫描用户目录"""
        results = []
        user_dirs = [
            "Desktop", "Documents", "Downloads", "Pictures", 
            "Videos", "Music", "AppData"
        ]
        
        for dir_name in user_dirs:
            dir_path = self.user_home / dir_name
            if dir_path.exists():
                size = self.scan_directory_size(dir_path)
                if size > 0:
                    results.append({
                        "name": dir_name,
                        "path": str(dir_path),
                        "size_gb": round(size / (1024**3), 2),
                        "size_mb": round(size / (1024**2), 2)
                    })
        
        return sorted(results, key=lambda x: x["size_gb"], reverse=True)
    
    def scan_appdata(self) -> list:
        """扫描 AppData 目录"""
        results = []
        appdata_local = self.user_home / "AppData" / "Local"
        
        if not appdata_local.exists():
            return results
        
        for item in appdata_local.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                try:
                    size = self.scan_directory_size(item)
                    if size > 100 * 1024 * 1024:  # > 100MB
                        results.append({
                            "name": item.name,
                            "path": str(item),
                            "size_gb": round(size / (1024**3), 2)
                        })
                except (PermissionError, OSError):
                    continue
        
        return sorted(results, key=lambda x: x["size_gb"], reverse=True)[:20]
    
    def scan_program_files(self) -> list:
        """扫描 Program Files"""
        results = []
        program_dirs = [
            self.root / "Program Files",
            self.root / "Program Files (x86)"
        ]
        
        for prog_dir in program_dirs:
            if prog_dir.exists():
                for item in prog_dir.iterdir():
                    if item.is_dir():
                        try:
                            size = self.scan_directory_size(item)
                            if size > 500 * 1024 * 1024:  # > 500MB
                                results.append({
                                    "name": item.name,
                                    "path": str(item),
                                    "size_gb": round(size / (1024**3), 2)
                                })
                        except (PermissionError, OSError):
                            continue
        
        return sorted(results, key=lambda x: x["size_gb"], reverse=True)[:15]
    
    def find_cleanable_files(self) -> dict:
        """查找可清理的文件"""
        cleanable = {
            "temp_files": [],
            "cache_files": [],
            "update_cache": []
        }
        
        # 临时文件
        temp_paths = [
            self.user_home / "AppData" / "Local" / "Temp",
            self.root / "Windows" / "Temp"
        ]
        
        for temp_path in temp_paths:
            if temp_path.exists():
                size = self.scan_directory_size(temp_path)
                cleanable["temp_files"].append({
                    "path": str(temp_path),
                    "size_gb": round(size / (1024**3), 2)
                })
        
        # Windows 更新缓存
        update_cache = self.root / "Windows" / "SoftwareDistribution" / "Download"
        if update_cache.exists():
            size = self.scan_directory_size(update_cache)
            cleanable["update_cache"].append({
                "path": str(update_cache),
                "size_gb": round(size / (1024**3), 2)
            })
        
        # 浏览器缓存
        browser_caches = [
            self.user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
            self.user_home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache"
        ]
        
        for cache_path in browser_caches:
            if cache_path.exists():
                size = self.scan_directory_size(cache_path)
                cleanable["cache_files"].append({
                    "path": str(cache_path),
                    "size_gb": round(size / (1024**3), 2)
                })
        
        return cleanable
    
    def generate_report(self, full: bool = False) -> dict:
        """生成完整报告"""
        report = {
            "scan_time": datetime.now().isoformat(),
            "disk_info": self.get_disk_info(),
            "user_directories": self.scan_user_directories(),
            "appdata_local": self.scan_appdata(),
            "program_files": self.scan_program_files(),
            "cleanable": self.find_cleanable_files()
        }
        
        # 计算可清理总量
        total_cleanable = 0
        for category in report["cleanable"].values():
            for item in category:
                total_cleanable += item.get("size_gb", 0)
        
        report["estimated_cleanable_gb"] = round(total_cleanable, 2)
        
        return report


def print_report(report: dict):
    """打印报告"""
    print("\n" + "="*60)
    print("  C 盘空间分析报告")
    print("="*60)
    
    # 磁盘信息
    disk = report["disk_info"]
    print(f"\n【磁盘信息】")
    print(f"  总容量：  {disk['total_gb']} GB")
    print(f"  已使用：  {disk['used_gb']} GB ({disk['used_percent']}%)")
    print(f"  剩余：    {disk['free_gb']} GB")
    
    # 状态提示
    if disk['free_gb'] < 10:
        print(f"\n  ⚠️  警告：C 盘空间严重不足！")
    elif disk['free_gb'] < 20:
        print(f"\n  ⚠️  注意：C 盘空间紧张")
    else:
        print(f"\n  ✅ C 盘空间充足")
    
    # 用户目录
    print(f"\n【用户目录占用】")
    for item in report["user_directories"][:5]:
        print(f"  {item['name']:15} {item['size_gb']:>8} GB")
    
    # AppData
    print(f"\n【AppData\\Local 占用 Top 10】")
    for item in report["appdata_local"][:10]:
        print(f"  {item['name']:20} {item['size_gb']:>8} GB")
    
    # Program Files
    print(f"\n【Program Files 占用 Top 10】")
    for item in report["program_files"][:10]:
        print(f"  {item['name']:25} {item['size_gb']:>8} GB")
    
    # 可清理文件
    print(f"\n【可清理文件预估】")
    cleanable = report["cleanable"]
    total = report["estimated_cleanable_gb"]
    
    for category, items in cleanable.items():
        for item in items:
            if item['size_gb'] > 0:
                print(f"  {item['path']:50} {item['size_gb']:>6} GB")
    
    print(f"\n  预估可清理总量：{total} GB")
    
    print("\n" + "="*60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="C 盘空间扫描分析")
    parser.add_argument("--full", action="store_true", help="完整扫描（更详细）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--drive", default="C:", help="要扫描的驱动器")
    
    args = parser.parse_args()
    
    scanner = CDriveScanner(args.drive)
    report = scanner.generate_report(full=args.full)
    
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
