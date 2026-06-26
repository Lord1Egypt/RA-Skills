#!/usr/bin/env python3
"""
C 盘清理脚本
执行安全清理操作
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

class CDriveCleaner:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.freed_space = 0
        self.cleaned_items = []
        self.errors = []
        self.user_home = Path(os.environ.get("USERPROFILE", "C:\\Users\\Default"))
    
    def clean_directory(self, dir_path: str, description: str) -> bool:
        """清理目录"""
        path = Path(dir_path)
        
        if not path.exists():
            return True
        
        try:
            # 计算大小
            size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            size_mb = round(size / (1024 * 1024), 2)
            
            if self.dry_run:
                print(f"  [预览] 将清理：{description}")
                print(f"          路径：{dir_path}")
                print(f"          大小：{size_mb} MB")
            else:
                # 执行清理
                for item in path.iterdir():
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except (PermissionError, OSError) as e:
                        self.errors.append(f"{dir_path}: {str(e)}")
                
                print(f"  [OK] 已清理：{description} ({size_mb} MB)")
            
            self.freed_space += size
            self.cleaned_items.append({
                "path": dir_path,
                "description": description,
                "size_mb": size_mb
            })
            return True
            
        except Exception as e:
            self.errors.append(f"{dir_path}: {str(e)}")
            return False
    
    def clean_temp_files(self) -> int:
        """清理临时文件"""
        print("\n[1/5] 清理临时文件...")
        count = 0
        
        temp_paths = [
            (str(self.user_home / "AppData" / "Local" / "Temp"), "用户临时文件"),
            (str(Path("C:\\Windows\\Temp")), "系统临时文件")
        ]
        
        for path, desc in temp_paths:
            if self.clean_directory(path, desc):
                count += 1
        
        return count
    
    def clean_update_cache(self) -> int:
        """清理 Windows 更新缓存"""
        print("\n[2/5] 清理 Windows 更新缓存...")
        
        update_path = str(Path("C:\\Windows\\SoftwareDistribution\\Download"))
        if self.clean_directory(update_path, "Windows 更新缓存"):
            return 1
        return 0
    
    def clean_browser_cache(self) -> int:
        """清理浏览器缓存"""
        print("\n[3/5] 清理浏览器缓存...")
        count = 0
        
        browser_paths = [
            (str(self.user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache"), "Chrome 缓存"),
            (str(self.user_home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache"), "Edge 缓存")
        ]
        
        for path, desc in browser_paths:
            if self.clean_directory(path, desc):
                count += 1
        
        return count
    
    def clean_package_cache(self) -> int:
        """清理包管理器缓存"""
        print("\n[4/5] 清理包管理器缓存...")
        count = 0
        
        package_paths = [
            (str(self.user_home / "AppData" / "Local" / "pip" / "Cache"), "pip 缓存"),
            (str(self.user_home / "AppData" / "Local" / "npm-cache"), "npm 缓存")
        ]
        
        for path, desc in package_paths:
            if self.clean_directory(path, desc):
                count += 1
        
        return count
    
    def clean_recycle_bin(self) -> bool:
        """清空回收站"""
        print("\n[5/5] 清空回收站...")
        
        if self.dry_run:
            print("  [预览] 将清空回收站")
            return True
        
        try:
            from ctypes import windll
            windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000001 | 0x00000002)
            print("  [OK] 回收站已清空")
            return True
        except Exception as e:
            print(f"  [FAIL] 回收站清空失败：{e}")
            return False
    
    def execute(self, level: str = "safe") -> dict:
        """执行清理"""
        print("\n" + "="*60)
        if self.dry_run:
            print("  C 盘清理 - 预览模式")
        else:
            print("  C 盘清理 - 执行中")
        print("="*60)
        
        # 安全级别
        self.clean_temp_files()
        self.clean_update_cache()
        
        if level in ["standard", "aggressive"]:
            self.clean_browser_cache()
            self.clean_package_cache()
        
        if level == "aggressive":
            self.clean_recycle_bin()
        
        # 总结
        freed_gb = round(self.freed_space / (1024 * 1024 * 1024), 2)
        freed_mb = round(self.freed_space / (1024 * 1024), 2)
        
        print("\n" + "="*60)
        print("  清理完成")
        print("="*60)
        print(f"\n  释放空间：{freed_gb} GB ({freed_mb} MB)")
        print(f"  清理项目：{len(self.cleaned_items)} 项")
        
        if self.errors:
            print(f"\n  警告：{len(self.errors)} 个错误")
            for error in self.errors[:5]:
                print(f"    - {error}")
        
        return {
            "freed_space_gb": freed_gb,
            "freed_space_mb": freed_mb,
            "cleaned_items": self.cleaned_items,
            "errors": self.errors
        }


def confirm_action() -> bool:
    """请求用户确认"""
    print("\n⚠️  此操作将删除文件，是否继续？")
    print("  输入 'yes' / 'y' / '确认' / '是' 继续：")
    
    confirm = input("> ").strip().lower()
    return confirm in ["yes", "y", "确认", "是"]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="C 盘清理脚本")
    parser.add_argument("--level", default="safe", choices=["safe", "standard", "aggressive"],
                       help="清理级别：safe=安全，standard=标准，aggressive=激进")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际删除")
    parser.add_argument("--yes", action="store_true", help="跳过确认")
    
    args = parser.parse_args()
    
    cleaner = CDriveCleaner(dry_run=args.dry_run)
    
    # 预览模式
    if args.dry_run:
        cleaner.execute(args.level)
        print("\n预览完成，未执行实际清理")
        print("执行清理请运行：python clean_c_drive.py --level", args.level)
        return
    
    # 请求确认
    if not args.yes:
        if not confirm_action():
            print("\n已取消")
            return
    
    # 执行清理
    result = cleaner.execute(args.level)
    
    # 保存日志
    log_path = Path("C:\\Users\\18785\\.openclaw\\workspace\\temp\\clean_log.txt")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{datetime.now().isoformat()} - Cleaned {result['freed_space_gb']} GB\n")


if __name__ == "__main__":
    main()
