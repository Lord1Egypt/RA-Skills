#!/usr/bin/env python3
"""
查找大文件脚本
扫描指定目录中的大文件
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def find_large_files(directory: str, min_size_mb: float = 100, limit: int = 50) -> list:
    """查找大文件"""
    results = []
    min_size_bytes = min_size_mb * 1024 * 1024
    
    print(f"\n扫描目录：{directory}")
    print(f"最小大小：{min_size_mb} MB")
    print("扫描中...", end="", flush=True)
    
    scanned = 0
    try:
        for root, dirs, files in os.walk(directory):
            # 跳过系统目录
            skip_dirs = ["Windows", "Program Files", "Program Files (x86)", 
                        "System Volume Information", "$Recycle.Bin"]
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                try:
                    file_path = Path(root) / file
                    size = file_path.stat().st_size
                    
                    if size > min_size_bytes:
                        results.append({
                            "path": str(file_path),
                            "size_mb": round(size / (1024 * 1024), 2),
                            "size_gb": round(size / (1024**3), 2),
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
                    
                    scanned += 1
                    if scanned % 1000 == 0:
                        print(".", end="", flush=True)
                        
                except (PermissionError, OSError):
                    continue
            
            if len(results) >= limit:
                break
                
    except KeyboardInterrupt:
        print("\n扫描已中断")
    
    print(f"\n扫描完成，共检查 {scanned} 个文件")
    
    # 按大小排序
    results.sort(key=lambda x: x["size_mb"], reverse=True)
    return results


def print_results(results: list):
    """打印结果"""
    if not results:
        print("\n未找到符合条件的大文件")
        return
    
    print("\n" + "="*70)
    print(f"  找到 {len(results)} 个大文件")
    print("="*70)
    
    total_size = sum(r["size_mb"] for r in results)
    
    print(f"\n{'大小':>10}  {'修改时间':<25}  路径")
    print("-"*70)
    
    for item in results:
        size_str = f"{item['size_gb']:.2f} GB" if item['size_gb'] >= 1 else f"{item['size_mb']:.0f} MB"
        print(f"{size_str:>10}  {item['modified']:<25}  {item['path'][:50]}")
    
    print("-"*70)
    print(f"总计：{total_size/1024:.2f} GB")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="查找大文件")
    parser.add_argument("--dir", default="C:\\Users", help="扫描目录")
    parser.add_argument("--min-size", type=float, default=100, help="最小大小 (MB)")
    parser.add_argument("--limit", type=int, default=50, help="最大结果数")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--output", help="输出到文件")
    
    args = parser.parse_args()
    
    results = find_large_files(args.dir, args.min_size, args.limit)
    
    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"结果已保存到：{args.output}")
        else:
            print(output)
    else:
        print_results(results)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                for item in results:
                    f.write(f"{item['path']}\n")
            print(f"\n列表已保存到：{args.output}")


if __name__ == "__main__":
    main()
