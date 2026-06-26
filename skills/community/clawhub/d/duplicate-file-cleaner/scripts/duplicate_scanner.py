#!/usr/bin/env python3
"""
重复文件扫描器
扫描指定目录，通过文件内容哈希值识别完全相同的重复文件
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def calculate_file_hash(file_path: str, chunk_size: int = 8192) -> Optional[str]:
    """
    计算文件的MD5哈希值

    Args:
        file_path: 文件路径
        chunk_size: 每次读取的块大小

    Returns:
        文件的MD5哈希值，如果出错返回None
    """
    try:
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except (IOError, OSError, PermissionError) as e:
        print(f"警告：无法读取文件 {file_path}: {e}", file=sys.stderr)
        return None


def get_file_info(file_path: str) -> Dict:
    """
    获取文件信息

    Args:
        file_path: 文件路径

    Returns:
        包含文件信息的字典
    """
    try:
        stat = os.stat(file_path)
        modified_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "path": file_path,
            "size": stat.st_size,
            "modified": modified_time
        }
    except (IOError, OSError, PermissionError):
        return {
            "path": file_path,
            "size": 0,
            "modified": "unknown"
        }


def scan_directory(
    directory: str,
    min_size: int = 1024,
    extensions: Optional[List[str]] = None
) -> Dict[str, List[Dict]]:
    """
    扫描目录并按哈希值分组文件

    Args:
        directory: 要扫描的目录
        min_size: 最小文件大小（字节）
        extensions: 文件扩展名过滤列表（不包含点号）

    Returns:
        字典，键为哈希值，值为文件信息列表
    """
    hash_map = {}
    total_files = 0

    if extensions:
        extensions = [ext.lower().lstrip('.') for ext in extensions]

    print(f"开始扫描目录: {directory}")
    print(f"最小文件大小: {min_size} 字节")
    if extensions:
        print(f"文件类型过滤: {', '.join(extensions)}")
    print("-" * 60)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # 跳过符号链接
            if os.path.islink(file_path):
                continue

            # 检查文件大小
            try:
                file_size = os.path.getsize(file_path)
                if file_size < min_size:
                    continue
            except (OSError, PermissionError):
                continue

            # 检查文件扩展名
            if extensions:
                file_ext = Path(filename).suffix.lower().lstrip('.')
                if file_ext not in extensions:
                    continue

            # 计算文件哈希
            file_hash = calculate_file_hash(file_path)
            if file_hash is None:
                continue

            # 添加到哈希映射
            if file_hash not in hash_map:
                hash_map[file_hash] = []

            hash_map[file_hash].append(get_file_info(file_path))
            total_files += 1

            # 进度提示（每100个文件）
            if total_files % 100 == 0:
                print(f"已扫描 {total_files} 个文件...")

    print(f"扫描完成！共扫描 {total_files} 个文件")
    return hash_map


def find_duplicate_groups(hash_map: Dict[str, List[Dict]]) -> List[Dict]:
    """
    找出重复的文件组

    Args:
        hash_map: 哈希值到文件列表的映射

    Returns:
        重复文件组列表，每组包含哈希值和文件列表
    """
    duplicate_groups = []

    for file_hash, files in hash_map.items():
        if len(files) > 1:
            # 按修改时间排序，旧文件在前
            sorted_files = sorted(files, key=lambda x: x["modified"])
            duplicate_groups.append({
                "hash": file_hash,
                "file_size": files[0]["size"],
                "files": sorted_files
            })

    # 按文件大小降序排序（大文件优先）
    duplicate_groups.sort(key=lambda x: x["file_size"], reverse=True)

    return duplicate_groups


def generate_report(
    duplicate_groups: List[Dict],
    total_files: int,
    scan_directory: str
) -> Dict:
    """
    生成扫描报告

    Args:
        duplicate_groups: 重复文件组列表
        total_files: 扫描的文件总数
        scan_directory: 扫描的目录

    Returns:
        包含扫描结果的字典
    """
    total_duplicate_files = sum(len(group["files"]) for group in duplicate_groups)
    total_wasted_space = sum(
        (len(group["files"]) - 1) * group["file_size"]
        for group in duplicate_groups
    )

    return {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_directory": scan_directory,
        "total_files_scanned": total_files,
        "duplicate_groups_count": len(duplicate_groups),
        "total_duplicate_files": total_duplicate_files,
        "total_wasted_space_bytes": total_wasted_space,
        "total_wasted_space_mb": round(total_wasted_space / (1024 * 1024), 2),
        "duplicate_groups": duplicate_groups
    }


def format_size(bytes_size: int) -> str:
    """
    格式化文件大小

    Args:
        bytes_size: 字节大小

    Returns:
        格式化后的字符串（如 "1.23 MB"）
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def print_summary(report: Dict):
    """
    打印扫描摘要

    Args:
        report: 扫描报告
    """
    print("\n" + "=" * 60)
    print("扫描摘要")
    print("=" * 60)
    print(f"扫描目录: {report['scan_directory']}")
    print(f"扫描时间: {report['scan_time']}")
    print(f"扫描文件总数: {report['total_files_scanned']}")
    print(f"发现重复组数: {report['duplicate_groups_count']}")
    print(f"重复文件总数: {report['total_duplicate_files']}")
    print(f"可释放空间: {report['total_wasted_space_mb']} MB")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="扫描目录并识别重复文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描照片目录
  python duplicate_scanner.py --directory ~/Pictures --extensions jpg,png

  # 扫描整个用户目录，最小文件100KB
  python duplicate_scanner.py --directory ~ --min-size 102400 --output report.json

  # 扫描并输出JSON格式报告
  python duplicate_scanner.py --directory ~/Downloads --output duplicates.json
        """
    )

    parser.add_argument(
        "--directory",
        required=True,
        help="要扫描的目录路径"
    )

    parser.add_argument(
        "--output",
        help="输出报告文件路径（JSON格式）"
    )

    parser.add_argument(
        "--min-size",
        type=int,
        default=1024,
        help="最小文件大小（字节），默认1024（1KB）"
    )

    parser.add_argument(
        "--extensions",
        help="文件扩展名过滤，逗号分隔（如 jpg,png,gif）"
    )

    args = parser.parse_args()

    # 验证目录
    if not os.path.isdir(args.directory):
        print(f"错误：目录不存在或无法访问: {args.directory}", file=sys.stderr)
        sys.exit(1)

    # 解析扩展名列表
    extensions = None
    if args.extensions:
        extensions = [ext.strip() for ext in args.extensions.split(',')]

    # 执行扫描
    hash_map = scan_directory(args.directory, args.min_size, extensions)
    duplicate_groups = find_duplicate_groups(hash_map)

    # 生成报告
    report = generate_report(
        duplicate_groups,
        total_files=sum(len(files) for files in hash_map.values()),
        scan_directory=args.directory
    )

    # 打印摘要
    print_summary(report)

    # 输出结果
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n详细报告已保存到: {args.output}")
        except IOError as e:
            print(f"错误：无法写入输出文件: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\n详细报告:")
        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
