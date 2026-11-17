#!/usr/bin/env python3
"""
validate_library.py — 批量校验一个人物档案库。

用法:
  python validate_library.py path/to/library/
  python validate_library.py path/to/library/ --report

输出:
  表格形式列出每份档案的通过情况
  --report 模式打印完整报告

退出码:
  0: 全部通过
  1: 有档案未通过
"""
import os
import sys
import argparse
from pathlib import Path
from validate_archive import validate

INDEX_FILES = ["人物-README.md", "person-README.md", "README.md"]


def is_archive_file(fname: str) -> bool:
    """判断是否是人物档案文件（排除索引文件）。"""
    if not fname.endswith(".md"):
        return False
    return fname not in INDEX_FILES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="档案库目录")
    parser.add_argument("--report", action="store_true", help="打印详细报告")
    parser.add_argument("--profile", choices=["generic", "obsidian"], default="generic",
                        help="校验配置：generic 不强制 frontmatter 字段（默认）；obsidian 强制知识库 frontmatter 规范")
    args = parser.parse_args()
    
    lib_path = Path(args.path)
    if not lib_path.exists():
        print(f"错误: 目录不存在: {args.path}")
        sys.exit(1)
    
    archives = sorted([
        f for f in os.listdir(lib_path)
        if is_archive_file(f)
    ])
    
    if not archives:
        print(f"错误: 目录中没有档案文件: {args.path}")
        sys.exit(1)
    
    print(f"{'档案':<25} {'状态':>5} {'问题数':>6} {'说明':<40}")
    print("=" * 80)
    
    total_issues = 0
    passed = 0
    
    for fname in archives:
        path = lib_path / fname
        issues = validate(str(path), profile=args.profile)
        
        if issues:
            status = "❌"
            total_issues += len(issues)
            desc = issues[0][:38] + ("..." if len(issues[0]) > 38 else "")
            if args.report:
                print(f"{fname:<25} {status:>5} {len(issues):>6} {desc}")
                for i in issues[1:]:
                    print(f"{'':<25} {'':>5} {'':>6} - {i}")
            else:
                print(f"{fname:<25} {status:>5} {len(issues):>6} {desc}")
        else:
            status = "✅"
            passed += 1
            print(f"{fname:<25} {status:>5} {0:>6} {'OK':<40}")
    
    print("=" * 80)
    print(f"通过: {passed}/{len(archives)}   总问题数: {total_issues}")
    
    sys.exit(0 if passed == len(archives) else 1)


if __name__ == "__main__":
    main()
