#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 文件操作工具 - 工具化封装
支持文件/目录的读取、写入、搜索、遍历等操作
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, Any, List
import datetime


def json_output(status: str, data: Any = None, error: str = None, metadata: Dict = None) -> str:
    """统一 JSON 输出格式"""
    result = {
        "status": status,
        "data": data,
        "error": error,
        "metadata": metadata or {},
        "timestamp": datetime.datetime.now().isoformat()
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def action_read(path: str, encoding: str = "utf-8", max_lines: int = None) -> str:
    """读取文件内容"""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return json_output("error", error=f"文件不存在: {path}")

        lines = path_obj.read_text(encoding=encoding, errors='ignore').split('\n')

        if max_lines:
            lines = lines[:max_lines]

        return json_output(
            "success",
            data={
                "content": '\n'.join(lines),
                "total_lines": len(lines),
                "encoding": encoding,
                "truncated": max_lines is not None and len(lines) >= max_lines
            },
            metadata={"path": str(path_obj.absolute()), "size": path_obj.stat().st_size}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_write(path: str, content: str, mode: str = "write", encoding: str = "utf-8") -> str:
    """写入文件内容"""
    try:
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        if mode == "append":
            with open(path_obj, 'a', encoding=encoding) as f:
                f.write(content)
        else:
            path_obj.write_text(content, encoding=encoding)

        return json_output(
            "success",
            data={"bytes_written": len(content.encode(encoding))},
            metadata={"path": str(path_obj.absolute()), "mode": mode}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_list(path: str, recursive: bool = False, show_hidden: bool = False) -> str:
    """列出目录内容"""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return json_output("error", error=f"目录不存在: {path}")

        if not path_obj.is_dir():
            return json_output("error", error=f"不是目录: {path}")

        items = []
        if recursive:
            for item in path_obj.rglob('*'):
                if not show_hidden and item.name.startswith('.'):
                    continue
                items.append({
                    "name": item.name,
                    "path": str(item.relative_to(path_obj)),
                    "type": "dir" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })
        else:
            for item in path_obj.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                items.append({
                    "name": item.name,
                    "path": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })

        return json_output(
            "success",
            data={"items": items, "count": len(items)},
            metadata={"path": str(path_obj.absolute()), "recursive": recursive}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_search(path: str, pattern: str, file_pattern: str = None) -> str:
    """搜索文件内容"""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return json_output("error", error=f"路径不存在: {path}")

        results = []
        search_files = []

        if path_obj.is_file():
            search_files = [path_obj]
        else:
            if file_pattern:
                search_files = list(path_obj.rglob(file_pattern))
            else:
                search_files = list(path_obj.rglob('*'))

        for file_path in search_files:
            if not file_path.is_file():
                continue

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')

                matches = []
                for line_num, line in enumerate(lines, 1):
                    if pattern.lower() in line.lower():
                        matches.append({
                            "line_number": line_num,
                            "content": line.strip(),
                            "match": pattern
                        })

                if matches:
                    results.append({
                        "file": str(file_path.relative_to(path_obj)),
                        "matches": matches,
                        "match_count": len(matches)
                    })
            except:
                continue

        return json_output(
            "success",
            data={"results": results, "total_files": len(results)},
            metadata={"path": str(path_obj.absolute()), "pattern": pattern}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_delete(path: str, recursive: bool = False) -> str:
    """删除文件或目录"""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return json_output("error", error=f"路径不存在: {path}")

        if path_obj.is_dir():
            if recursive:
                shutil.rmtree(path_obj)
            else:
                path_obj.rmdir()
        else:
            path_obj.unlink()

        return json_output(
            "success",
            data={"deleted": str(path_obj.absolute())},
            metadata={"type": "dir" if path_obj.is_dir() else "file"}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_move(src: str, dst: str) -> str:
    """移动文件或目录"""
    try:
        src_obj = Path(src)
        dst_obj = Path(dst)
        dst_obj.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src_obj), str(dst_obj))

        return json_output(
            "success",
            data={"from": str(src_obj.absolute()), "to": str(dst_obj.absolute())}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_copy(src: str, dst: str) -> str:
    """复制文件或目录"""
    try:
        src_obj = Path(src)
        dst_obj = Path(dst)
        dst_obj.parent.mkdir(parents=True, exist_ok=True)

        if src_obj.is_dir():
            if dst_obj.exists():
                shutil.rmtree(dst_obj)
            shutil.copytree(str(src_obj), str(dst_obj))
        else:
            shutil.copy2(str(src_obj), str(dst_obj))

        return json_output(
            "success",
            data={"from": str(src_obj.absolute()), "to": str(dst_obj.absolute())}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_mkdir(path: str, parents: bool = True) -> str:
    """创建目录"""
    try:
        path_obj = Path(path)
        path_obj.mkdir(parents=parents, exist_ok=True)

        return json_output(
            "success",
            data={"created": str(path_obj.absolute())},
            metadata={"parents": parents}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_stat(path: str) -> str:
    """获取文件/目录详细信息"""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return json_output("error", error=f"路径不存在: {path}")

        stat = path_obj.stat()
        return json_output(
            "success",
            data={
                "name": path_obj.name,
                "path": str(path_obj.absolute()),
                "type": "dir" if path_obj.is_dir() else "file",
                "size": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "permissions": oct(stat.st_mode),
                "readable": os.access(path_obj, os.R_OK),
                "writable": os.access(path_obj, os.W_OK),
                "executable": os.access(path_obj, os.X_OK)
            }
        )
    except Exception as e:
        return json_output("error", error=str(e))


def main():
    parser = argparse.ArgumentParser(description="CLI 文件操作工具")
    parser.add_argument("--action", required=True, choices=[
        "read", "write", "list", "search", "delete", "move", "copy", "mkdir", "stat"
    ], help="操作类型")

    # 读取参数
    parser.add_argument("--path", help="文件/目录路径")
    parser.add_argument("--encoding", default="utf-8", help="文件编码")
    parser.add_argument("--max-lines", type=int, help="最大读取行数")

    # 写入参数
    parser.add_argument("--content", help="写入内容")
    parser.add_argument("--mode", choices=["write", "append"], default="write", help="写入模式")

    # 列表参数
    parser.add_argument("--recursive", action="store_true", help="递归列出")
    parser.add_argument("--show-hidden", action="store_true", help="显示隐藏文件")

    # 搜索参数
    parser.add_argument("--pattern", help="搜索内容模式")
    parser.add_argument("--file-pattern", help="文件名模式")

    # 移动/复制参数
    parser.add_argument("--src", help="源路径")
    parser.add_argument("--dst", help="目标路径")

    # 删除参数
    parser.add_argument("--recursive-delete", action="store_true", help="递归删除")

    # 创建目录参数
    parser.add_argument("--parents", action="store_true", default=True, help="创建父目录")

    args = parser.parse_args()

    # 路由到对应操作
    if args.action == "read":
        result = action_read(args.path, args.encoding, args.max_lines)
    elif args.action == "write":
        result = action_write(args.path, args.content, args.mode, args.encoding)
    elif args.action == "list":
        result = action_list(args.path, args.recursive, args.show_hidden)
    elif args.action == "search":
        result = action_search(args.path, args.pattern, args.file_pattern)
    elif args.action == "delete":
        result = action_delete(args.path, args.recursive_delete)
    elif args.action == "move":
        result = action_move(args.src, args.dst)
    elif args.action == "copy":
        result = action_copy(args.src, args.dst)
    elif args.action == "mkdir":
        result = action_mkdir(args.path, args.parents)
    elif args.action == "stat":
        result = action_stat(args.path)
    else:
        result = json_output("error", error=f"未知操作: {args.action}")

    print(result)


if __name__ == "__main__":
    main()
