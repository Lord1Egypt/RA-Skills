#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Everything Search v1 - Core Search Script
Windows 10/11 本地文件极速检索系统，基于 Everything es.exe CLI 工具

作者: OneToken
版本: 1.0.0
仓库: https://github.com/1TOKENer/everything-search-skill
"""

import csv
import io
import os
import sys
import subprocess
import time
from collections import namedtuple
from typing import Optional, List, Tuple

# 从 install.py 导入路径发现和配置函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from install import (
    find_es_exe,
    start_everything_background,
    save_path_config,
    discover_and_configure,
)

# ============================================================
# 常量定义
# ============================================================

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB"]


# ============================================================
# 工具函数
# ============================================================

def format_size(size_bytes: int) -> str:
    """将字节数转换为人类可读的格式"""
    if size_bytes < 0:
        return "N/A"
    unit_index = 0
    size = float(size_bytes)
    while size >= 1024.0 and unit_index < len(SIZE_UNITS) - 1:
        size /= 1024.0
        unit_index += 1
    return f"{int(size)} B" if unit_index == 0 else f"{size:.1f} {SIZE_UNITS[unit_index]}"


def get_file_extension(filename: str) -> str:
    """获取文件扩展名（含点号）"""
    _, ext = os.path.splitext(filename)
    return ext


# ============================================================
# 核心搜索功能
# ============================================================

# SearchResult namedtuple - 搜索结果数据结构
SearchResult = namedtuple("SearchResult", ["filename", "filepath", "size", "extension", "size_formatted"])


def create_search_result(filename: str, filepath: str, size: int) -> SearchResult:
    """创建 SearchResult 实例"""
    return SearchResult(
        filename=filename,
        filepath=filepath,
        size=size,
        extension=get_file_extension(filename),
        size_formatted=format_size(size)
    )

def _decode_bytes(raw_bytes: bytes) -> str:
    """
    使用多种编码尝试解码 es.exe 的输出

    es.exe 在不同系统 locale 下输出编码不同：
    - 中文 Windows: GBK / CP936
    - 英文 Windows: CP1252
    - 日文 Windows: CP932
    - UTF-8（部分新版 Everything）

    依次尝试常用编码，直到拿到可辨认的输出。

    Args:
        raw_bytes: es.exe 的标准输出/错误输出原始字节

    Returns:
        解码后的字符串
    """
    for encoding in ("utf-8", "gbk", "cp1252", "shift-jis", "utf-16-le"):
        try:
            text = raw_bytes.decode(encoding)
            # 检查是否包含典型可辨认字符
            if any(c in text for c in ("Filename", "Name", "Error", "IPC")):
                return text
        except (UnicodeDecodeError, LookupError):
            continue
    # 回退：utf-8 + replace，保证不崩溃
    return raw_bytes.decode("utf-8", errors="replace")


def parse_es_output(raw_bytes: bytes) -> List[SearchResult]:
    """
    解析 es.exe 的 CSV 输出

    依赖 es.exe 的 -csv 标志输出标准 CSV 格式：
        "Filename","Path","Size"
        "file.txt","C:\\path\\to\\file.txt","1234"

    相比旧版 split() 方案，CSV 解析正确处理：
    - 含空格的文件名和路径（如 Program Files）
    - 含逗号的文件名（CSV 引号转义）
    - 编码自动检测

    Args:
        raw_bytes: es.exe 的标准输出原始字节

    Returns:
        解析后的搜索结果列表
    """
    results = []
    output = _decode_bytes(raw_bytes).strip()

    if not output:
        return results

    reader = csv.reader(io.StringIO(output))
    try:
        header = next(reader)
    except StopIteration:
        return results

    # 定位列索引（兼容不同语言版本的 es.exe 表头）
    name_idx = path_idx = size_idx = None
    for i, col in enumerate(header):
        col_lower = col.strip().lower()
        if col_lower in ("filename", "name", "文件名", "名称"):
            name_idx = i
        elif col_lower in ("path", "路径"):
            path_idx = i
        elif col_lower in ("size", "大小"):
            size_idx = i

    # 回退：按位置假设 Name, Path, Size 顺序
    if name_idx is None:
        name_idx = 0
    if path_idx is None:
        path_idx = 1
    if size_idx is None:
        size_idx = 2

    for row in reader:
        if not row or all(cell.strip() == "" for cell in row):
            continue

        filename = row[name_idx].strip() if name_idx < len(row) else ""
        filepath = row[path_idx].strip() if path_idx < len(row) else ""
        size_str = row[size_idx].strip() if size_idx < len(row) else "0"

        try:
            size = int(size_str)
        except (ValueError, IndexError):
            size = 0

        if not filename:
            filename = os.path.basename(filepath)
        if not filepath and filename:
            filepath = filename

        results.append(create_search_result(filename, filepath, size))

    return results


def search_files(query: str, max_results: int = 100) -> Tuple[List[SearchResult], Optional[str]]:
    """
    搜索文件

    Args:
        query: 搜索关键词（支持 Everything 搜索语法）
        max_results: 最大返回结果数

    Returns:
        (搜索结果列表, 错误信息或None)
    """
    es_path = find_es_exe()

    if not es_path:
        return [], "ES_EXE_NOT_FOUND"

    # 构建基础命令（-csv 确保可靠解析含空格/逗号的文件名和路径）
    cmd = [es_path, "-csv", "-size", "-max-results", str(max_results)]
    
    # 搜索词原样传入 es.exe；Everything 原生支持空格 AND / 引号短语等语法
    cmd.append(query)

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=30)

        if result.returncode != 0:
            error_msg = _decode_bytes(result.stderr).strip()
            if "everything" in error_msg.lower() and ("not running" in error_msg.lower() or "ipc" in error_msg.lower()):
                return [], "EVERYTHING_NOT_RUNNING"
            return [], f"❌ es.exe 错误: {error_msg}"

        if not result.stdout.strip():
            return [], None  # 无结果，但不是错误

        results = parse_es_output(result.stdout)
        return results, None

    except subprocess.TimeoutExpired:
        return [], "❌ 搜索超时（30秒），请缩小搜索范围"
    except FileNotFoundError:
        return [], f"❌ 无法执行 es.exe: {es_path}"
    except Exception as e:
        return [], f"❌ 搜索异常: {str(e)}"


# ============================================================
# 输出格式化
# ============================================================

def _display_width(s: str) -> int:
    """计算字符串在终端的显示宽度（CJK/全角字符占 2 列，ASCII 占 1 列）"""
    w = 0
    for c in s:
        w += 2 if ord(c) > 127 else 1
    return w


def _pad_right(s: str, width: int) -> str:
    """按显示宽度左对齐填充"""
    return s + ' ' * max(0, width - _display_width(s))


def _pad_left(s: str, width: int) -> str:
    """按显示宽度右对齐填充"""
    return ' ' * max(0, width - _display_width(s)) + s


def _truncate_by_width(s: str, max_width: int, suffix: str = "..") -> str:
    """按显示宽度截断字符串，超出部分用 suffix 替代"""
    if _display_width(s) <= max_width:
        return s
    suffix_w = _display_width(suffix)
    if suffix_w >= max_width:
        return suffix[:max(1, max_width)] if max_width > 0 else ""
    target = max_width - suffix_w
    result = ""
    w = 0
    for c in s:
        cw = 2 if ord(c) > 127 else 1
        if w + cw > target:
            break
        result += c
        w += cw
    return result + suffix


def format_results_table(results: List[SearchResult]) -> str:
    """将搜索结果格式化为表格（按终端显示宽度对齐，正确处理 CJK 字符）"""
    if not results:
        return "📭 未找到匹配的文件"

    MAX_NAME_W = 40
    MAX_PATH_W = 80

    max_name = min(max(_display_width(r.filename) for r in results), MAX_NAME_W)
    max_ext = max(_display_width(r.extension) for r in results)
    max_size = max(_display_width(r.size_formatted) for r in results)
    max_path = min(max(_display_width(r.filepath) for r in results), MAX_PATH_W)

    header_name = _pad_right("文件名", max_name)
    header_ext = _pad_right("扩展名", max_ext)
    header_size = _pad_left("大小", max_size)
    header_path = _pad_right("路径", max_path)
    header = f"{header_name}  {header_ext}  {header_size}  {header_path}"

    sep_width = max_name + 2 + max_ext + 2 + max_size + 2 + max_path
    separator = "-" * sep_width
    lines = [header, separator]

    for r in results:
        name = _truncate_by_width(r.filename, max_name)
        path = _truncate_by_width(r.filepath, max_path)
        lines.append(
            f"{_pad_right(name, max_name)}  "
            f"{_pad_right(r.extension, max_ext)}  "
            f"{_pad_left(r.size_formatted, max_size)}  "
            f"{path}"
        )

    return "\n".join(lines)


def print_results(results: List[SearchResult], query: str) -> None:
    """打印搜索结果"""
    print(f"\n🔎 搜索: {query}")
    print(f"📊 找到 {len(results)} 个结果\n")
    print(format_results_table(results))
    print()


# ============================================================
# 主搜索流程（目前默认为：纯搜索，将来会更新）
# ============================================================

def main_search(query: str, max_results: int = 100) -> int:
    """
    主搜索流程

    启动机制：
    1. 直接搜索
    2. 如果 es.exe 未找到 → 自动运行 discover_and_configure 后重试
    3. 如果 Everything 未运行 → 自动后台启动后重试

    Returns:
        0=成功, 1=无结果, 2=错误
    """
    if not query or not query.strip():
        print("❌ 请提供搜索关键词")
        return 2

    query = query.strip()

    # 第一次尝试搜索
    results, error = search_files(query, max_results)

    if error is None:
        print_results(results, query)
        # 搜索成功，保存路径到 path.env
        _save_current_paths_once()
        return 0 if results else 1

    # ── es.exe 未找到 → 自动运行安装配置后重试 ──
    if error == "ES_EXE_NOT_FOUND":
        print("🔧 es.exe 未找到，正在自动配置 Everything...")
        if discover_and_configure(silent=True):
            print("✅ 配置成功，重新搜索中...")
            results, error = search_files(query, max_results)
            if error is None:
                print_results(results, query)
                _save_current_paths_once()
                return 0 if results else 1
            # 自动配置虽然成功但搜索仍失败（可能是 Everything 未运行等）
            # 继续走下面的分支处理
        else:
            print("❌ 自动配置失败")
            print("   请手动运行 install.py 进行配置")
            print("   或访问 https://www.voidtools.com/zh-cn/downloads/ 下载 Everything")
            return 2

    # ── 其他错误（非 Everything 未运行）→ 直接报错 ──
    if error is not None and error != "EVERYTHING_NOT_RUNNING":
        print(error)
        return 2

    # ── Everything 未运行 → 自动后台启动后重试 ──
    print("⚠️  Everything 未运行，正在尝试自动启动...")

    if start_everything_background():
        print("✅ Everything 已启动，重新搜索中...")
        time.sleep(1)
        results, error = search_files(query, max_results)
        if error is None:
            print_results(results, query)
            # 搜索成功，保存路径到 path.env
            _save_current_paths_once()
            return 0 if results else 1
        else:
            print(error)
            return 2
    else:
        print("❌ 无法自动启动 Everything")
        print("   请手动启动 Everything 或运行 install.py 进行配置")
        print("   下载地址: https://www.voidtools.com/zh-cn/downloads/")
        return 2


_paths_saved = False


def _save_current_paths_once() -> None:
    """保存当前 Everything/es.exe 路径到 path.env（进程生命周期内仅写一次）"""
    global _paths_saved
    if _paths_saved:
        return
    es_path = find_es_exe()
    if es_path:
        everything_path = os.path.dirname(es_path)
        save_path_config(everything_path, es_path)
        _paths_saved = True


# ============================================================
# 命令行入口
# ============================================================

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python search_core.py <搜索关键词> [最大结果数]")
        print()
        print("示例:")
        print('  python search_core.py "*.pdf"')
        print('  python search_core.py "report"')
        print('  python search_core.py "ext:docx;pdf"')
        print('  python search_core.py "size:>100mb"')
        print('  python search_core.py "path:C:\\Users"')
        print('  python search_core.py "*.txt" 50')
        print()
        print("搜索语法参考: https://www.voidtools.com/support/everything/searching/")
        return 2

    query = sys.argv[1]
    max_results = 100
    if len(sys.argv) > 2:
        try:
            max_results = int(sys.argv[2])
        except ValueError:
            print(f"⚠️  无效的最大结果数: {sys.argv[2]}，使用默认值 100")

    return main_search(query, max_results)


if __name__ == "__main__":
    sys.exit(main())
