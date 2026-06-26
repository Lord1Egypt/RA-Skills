#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_tool.py — 目录文本搜索工具（支持压缩包递归查找、多关键词搜索）

功能：
  - 递归遍历目标目录下所有文本文件
  - 支持 .zip / .rar / .tar / .tar.gz / .tar.bz2 / .7z 等压缩格式
  - 支持正则表达式搜索
  - 支持同时搜索多个关键词（结果按关键词分组）
  - 多编码自动探测（UTF-8 → GBK → latin-1）
  - 结果写入 search_result.txt
  - 自动清理临时解压目录

依赖安装：
  pip install rarfile          # RAR 支持（还需系统安装 unrar 命令行工具）
  pip install py7zr             # 7z 支持
  pip install chardet           # 可选：更准确的编码检测

用法（单关键词）：
  python search_tool.py --path ./data --pattern "error"
  python search_tool.py --path ./data --pattern "\\d{4}-\\d{2}-\\d{2}"

用法（多关键词，逗号分隔）：
  python search_tool.py --path ./data --patterns "error,warn,failed"
  python search_tool.py --path ./data --patterns "Account_Main,Login,Logout"

交互模式：
  python search_tool.py
"""

import os
import re
import sys
import zipfile
import tarfile
import shutil
import tempfile
import argparse
import traceback
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────
# 可配置项
# ──────────────────────────────────────────────

# 视为文本文件的扩展名（小写）
TEXT_EXTENSIONS = {
    ".txt", ".log", ".cfg", ".conf", ".ini", ".md",
    ".csv", ".xml", ".json", ".yaml", ".yml",
    ".properties", ".toml", ".sh", ".bat", ".py",
    ".java", ".kt", ".c", ".cpp", ".h", ".js", ".ts",
    ".html", ".htm", ".sql",
}

# 视为压缩包的扩展名（小写）
ARCHIVE_EXTENSIONS = {
    ".zip", ".rar", ".tar", ".gz", ".bz2", ".xz", ".7z",
}

# 文件大小上限（超过则跳过，单位字节）
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# 尝试的编码列表（按优先级）
ENCODINGS = ["utf-8", "gbk", "latin-1"]

# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────

def is_text_file(path: str) -> bool:
    """根据扩展名判断是否为文本文件"""
    return Path(path).suffix.lower() in TEXT_EXTENSIONS


def is_archive(path: str) -> bool:
    """根据扩展名判断是否为压缩包"""
    name = path.lower()
    # 处理 .tar.gz / .tar.bz2 / .tar.xz 双扩展名
    for ext in [".tar.gz", ".tar.bz2", ".tar.xz", ".tgz", ".tbz2"]:
        if name.endswith(ext):
            return True
    return Path(path).suffix.lower() in ARCHIVE_EXTENSIONS


def read_lines(file_path: str) -> list[tuple[int, str]] | None:
    """
    读取文本文件，返回 [(行号, 行内容), ...] 或 None（失败时）。
    自动按 ENCODINGS 顺序尝试解码。
    """
    try:
        size = os.path.getsize(file_path)
        if size > MAX_FILE_SIZE:
            print(f"  [跳过] 文件过大（{size // 1024 // 1024} MB）：{file_path}")
            return None
    except OSError as e:
        print(f"  [警告] 无法获取文件大小：{file_path} → {e}")
        return None

    for enc in ENCODINGS:
        try:
            with open(file_path, "r", encoding=enc, errors="strict") as f:
                return [(i + 1, line.rstrip("\r\n")) for i, line in enumerate(f)]
        except (UnicodeDecodeError, UnicodeError):
            continue
        except PermissionError as e:
            print(f"  [警告] 权限不足：{file_path} → {e}")
            return None
        except OSError as e:
            print(f"  [警告] 读取失败：{file_path} → {e}")
            return None

    # 所有编码均失败，最后用 latin-1 强制读取（不会报错，只是可能乱码）
    try:
        with open(file_path, "r", encoding="latin-1", errors="replace") as f:
            return [(i + 1, line.rstrip("\r\n")) for i, line in enumerate(f)]
    except Exception as e:
        print(f"  [警告] 无法读取文件：{file_path} → {e}")
        return None


def read_lines_from_bytes(data: bytes, display_path: str) -> list[tuple[int, str]] | None:
    """
    从字节内容读取行（压缩包内文件用），自动探测编码。
    """
    if len(data) > MAX_FILE_SIZE:
        print(f"  [跳过] 压缩包内文件过大（{len(data) // 1024 // 1024} MB）：{display_path}")
        return None

    for enc in ENCODINGS:
        try:
            text = data.decode(enc, errors="strict")
            lines = text.splitlines()
            return [(i + 1, line) for i, line in enumerate(lines)]
        except (UnicodeDecodeError, UnicodeError):
            continue

    # 最终回退
    try:
        text = data.decode("latin-1", errors="replace")
        lines = text.splitlines()
        return [(i + 1, line) for i, line in enumerate(lines)]
    except Exception:
        return None


def match_lines(
    lines: list[tuple[int, str]],
    patterns: list[tuple[str, re.Pattern]],
) -> list[tuple[int, str, list[str]]]:
    """
    在行列表中搜索多个匹配项，返回 [(行号, 行内容, [匹配的关键词列表]), ...]
    按行号排序，同一行匹配多个关键词时合并展示
    """
    # 先收集每行的匹配情况
    line_matches: dict[int, tuple[str, set[str]]] = {}
    for lineno, content in lines:
        matched_patterns = []
        for pat_name, pat in patterns:
            if pat.search(content):
                matched_patterns.append(pat_name)
        if matched_patterns:
            if lineno in line_matches:
                # 合并已存在的匹配关键词
                existing_content, existing_patterns = line_matches[lineno]
                line_matches[lineno] = (existing_content, existing_patterns | set(matched_patterns))
            else:
                line_matches[lineno] = (content, set(matched_patterns))

    # 转换为列表并按行号排序
    results = [(lineno, content, sorted(list(patterns))) for lineno, (content, patterns) in sorted(line_matches.items())]
    return results


# ──────────────────────────────────────────────
# 压缩包处理
# ──────────────────────────────────────────────

def safe_extract_zip(zf: zipfile.ZipFile, dest_dir: str):
    """安全解压 ZIP，防止路径遍历攻击"""
    dest = Path(dest_dir).resolve()
    for member in zf.infolist():
        # 过滤绝对路径和 .. 路径遍历
        member_path = Path(member.filename)
        parts = member_path.parts
        if any(p in ("..", "/", "\\") or p.startswith("/") for p in parts):
            print(f"  [安全] 跳过危险路径：{member.filename}")
            continue
        target = (dest / member.filename).resolve()
        if not str(target).startswith(str(dest)):
            print(f"  [安全] 拒绝路径遍历：{member.filename}")
            continue
        zf.extract(member, dest_dir)


def scan_archive(
    archive_path: str,
    display_prefix: str,
    patterns: list[tuple[str, re.Pattern]],
    results: list,
    depth: int = 0,
):
    """
    递归扫描压缩包（支持嵌套），将匹配项追加到 results。

    results 格式: [(display_path, [(行号, 行内容, [匹配关键词列表]), ...]), ...]
    patterns 格式: [(pattern_name, compiled_pattern), ...]
    """
    MAX_DEPTH = 8  # 最多嵌套层数，防止无限递归
    if depth > MAX_DEPTH:
        print(f"  [跳过] 嵌套层数超过 {MAX_DEPTH}：{archive_path}")
        return

    tmp_dir = tempfile.mkdtemp(prefix="search_tool_")
    try:
        _extract_and_scan(archive_path, display_prefix, patterns, results, tmp_dir, depth)
    finally:
        # 无论如何清理临时目录
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception:
            pass


def _extract_and_scan(
    archive_path: str,
    display_prefix: str,
    patterns: list[tuple[str, re.Pattern]],
    results: list,
    tmp_dir: str,
    depth: int,
):
    """实际解压并扫描逻辑"""
    name_lower = archive_path.lower()

    # ── ZIP ──
    if name_lower.endswith(".zip"):
        try:
            with zipfile.ZipFile(archive_path, "r") as zf:
                safe_extract_zip(zf, tmp_dir)
        except zipfile.BadZipFile as e:
            print(f"  [错误] 损坏的 ZIP：{archive_path} → {e}")
            return
        except Exception as e:
            print(f"  [错误] 解压 ZIP 失败：{archive_path} → {e}")
            return

    # ── TAR / TAR.GZ / TAR.BZ2 / TAR.XZ / TGZ ──
    elif tarfile.is_tarfile(archive_path):
        try:
            with tarfile.open(archive_path, "r:*") as tf:
                # Python 3.12+ 支持 filter 参数防路径遍历
                try:
                    tf.extractall(tmp_dir, filter="data")
                except TypeError:
                    # 旧版本 Python，手动过滤
                    safe_members = []
                    for m in tf.getmembers():
                        if ".." in m.name or m.name.startswith("/"):
                            print(f"  [安全] 跳过危险路径：{m.name}")
                            continue
                        safe_members.append(m)
                    tf.extractall(tmp_dir, members=safe_members)
        except tarfile.TarError as e:
            print(f"  [错误] 损坏的 TAR：{archive_path} → {e}")
            return
        except Exception as e:
            print(f"  [错误] 解压 TAR 失败：{archive_path} → {e}")
            return

    # ── RAR ──
    elif name_lower.endswith(".rar"):
        try:
            import rarfile  # noqa: F401
        except ImportError:
            print(
                "\n  [错误] 需要安装 rarfile 库才能处理 RAR 文件。\n"
                "  请运行：pip install rarfile\n"
                "  还需安装系统工具 unrar：\n"
                "    Windows: https://www.rarlab.com/rar_add.htm\n"
                "    macOS:   brew install unrar\n"
                "    Linux:   sudo apt install unrar\n"
            )
            return
        try:
            with rarfile.RarFile(archive_path, "r") as rf:
                rf.extractall(tmp_dir)
        except rarfile.BadRarFile as e:
            print(f"  [错误] 损坏的 RAR：{archive_path} → {e}")
            return
        except rarfile.RarCannotExec:
            print(
                f"\n  [错误] 系统未安装 unrar 命令行工具，无法解压 RAR 文件：{archive_path}\n"
                "  请安装 unrar：\n"
                "    Windows: https://www.rarlab.com/rar_add.htm\n"
                "    macOS:   brew install unrar\n"
                "    Linux:   sudo apt install unrar\n"
            )
            return
        except Exception as e:
            print(f"  [错误] 解压 RAR 失败：{archive_path} → {e}")
            return

    # ── 7Z ──
    elif name_lower.endswith(".7z"):
        try:
            import py7zr
        except ImportError:
            print(
                "\n  [错误] 需要安装 py7zr 库才能处理 7z 文件。\n"
                "  请运行：pip install py7zr\n"
            )
            return
        try:
            with py7zr.SevenZipFile(archive_path, mode="r") as sz:
                sz.extractall(path=tmp_dir)
        except py7zr.exceptions.Bad7zFile as e:
            print(f"  [错误] 损坏的 7z：{archive_path} → {e}")
            return
        except Exception as e:
            print(f"  [错误] 解压 7z 失败：{archive_path} → {e}")
            return

    else:
        print(f"  [跳过] 不支持的压缩格式：{archive_path}")
        return

    # 扫描解压后的临时目录
    scan_directory(tmp_dir, patterns, results, base_dir=tmp_dir,
                   display_prefix=display_prefix, depth=depth + 1)


# ──────────────────────────────────────────────
# 核心扫描逻辑
# ──────────────────────────────────────────────

def scan_directory(
    directory: str,
    patterns: list[tuple[str, re.Pattern]],
    results: list,
    base_dir: str | None = None,
    display_prefix: str = "",
    depth: int = 0,
):
    """
    递归扫描目录中的所有文件。

    - 文本文件：直接搜索
    - 压缩包：解压后递归扫描
    - 其他文件：跳过

    patterns 格式: [(pattern_name, compiled_pattern), ...]
    results 格式: [(display_path, [(行号, 行内容, [匹配关键词列表]), ...]), ...]
    """
    if not patterns:
        return
    if base_dir is None:
        base_dir = directory

    try:
        all_entries = list(os.scandir(directory))
    except PermissionError as e:
        print(f"  [警告] 无权限访问目录：{directory} → {e}")
        return
    except OSError as e:
        print(f"  [警告] 无法扫描目录：{directory} → {e}")
        return

    # 目录和文件分别按文件名排序：先递归子目录，再处理当前层文件
    dirs  = sorted([e for e in all_entries if e.is_dir()  and not e.is_symlink()], key=lambda e: e.name)
    files = sorted([e for e in all_entries if e.is_file() and not e.is_symlink()], key=lambda e: e.name)

    # ── 先递归所有子目录（按名称字母序）──
    for entry in dirs:
        try:
            scan_directory(
                entry.path, patterns, results,
                base_dir=base_dir, display_prefix=display_prefix, depth=depth
            )
        except Exception as e:
            print(f"  [错误] 处理目录 {entry.path} 时发生异常：{e}")
            traceback.print_exc()

    # ── 再处理当前目录下的文件（按名称字母序）──
    for entry in files:
        try:
            # 计算显示路径
            rel = os.path.relpath(entry.path, base_dir)
            if display_prefix:
                display_path = display_prefix + "/" + rel.replace("\\", "/")
            else:
                display_path = rel.replace("\\", "/")

            if is_text_file(entry.path):
                print(f"已处理：{display_path}")
                lines = read_lines(entry.path)
                if lines is not None:
                    matches = match_lines(lines, patterns)
                    if matches:
                        results.append((display_path, matches))

            elif is_archive(entry.path):
                print(f"已处理：{display_path}（压缩包，递归扫描中）")
                scan_archive(entry.path, display_path, patterns, results, depth)

            # 其他类型文件静默跳过

        except Exception as e:
            print(f"  [错误] 处理 {entry.path} 时发生异常：{e}")
            traceback.print_exc()


# ──────────────────────────────────────────────
# 输出结果
# ──────────────────────────────────────────────

def write_results(
    results: list,
    output_path: str,
    pattern_strs: list[str],
    total_patterns: int,
):
    """将搜索结果写入文件，按行号顺序展示，同一行匹配多个关键词时合并显示"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"搜索模式：{', '.join(pattern_strs)}\n")
        f.write(f"关键词数量：{total_patterns}\n")
        f.write(f"匹配文件数：{len(results)}\n")
        f.write("=" * 60 + "\n\n")

        if not results:
            f.write("未找到匹配项\n")
            return

        for display_path, line_matches in results:
            f.write(f"========== 文件：{display_path} ==========\n")
            # 按行号顺序输出
            for lineno, content, matched_patterns in line_matches:
                if len(matched_patterns) == 1:
                    f.write(f"{lineno}: {content}\n")
                else:
                    # 同一行匹配多个关键词，标注出来
                    patterns_str = ", ".join(matched_patterns)
                    f.write(f"{lineno}: [{patterns_str}] {content}\n")
            f.write("\n")


# ──────────────────────────────────────────────
# 入口
# ──────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="目录文本搜索工具（支持压缩包递归查找、多关键词搜索）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--path", "-p",
        help="要搜索的目标目录路径",
        default=None,
    )
    parser.add_argument(
        "--pattern", "-t",
        help="搜索文本或正则表达式（单个关键词）",
        default=None,
    )
    parser.add_argument(
        "--patterns",
        help="多个搜索关键词，用逗号分隔（如：error,warn,failed）",
        default=None,
    )
    parser.add_argument(
        "--output", "-o",
        help="结果保存目录（默认：脚本所在目录下的 search_results/）",
        default=None,
    )
    parser.add_argument(
        "--no-regex",
        action="store_true",
        help="将 pattern/patterns 作为普通字符串（自动转义正则元字符）",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # ── 获取目标目录 ──
    search_path = args.path
    if not search_path:
        search_path = input("请输入要搜索的目标目录路径：").strip()
    search_path = os.path.abspath(search_path)

    if not os.path.isdir(search_path):
        print(f"[错误] 路径不存在或不是目录：{search_path}")
        sys.exit(1)

    # ── 获取搜索模式（支持单关键词或多关键词）──
    pattern_strs: list[str] = []

    if args.patterns:
        # 多关键词模式：逗号分隔
        pattern_strs = [p.strip() for p in args.patterns.split(",") if p.strip()]
    elif args.pattern:
        # 单关键词模式
        pattern_strs = [args.pattern]
    else:
        # 交互式输入
        user_input = input("请输入要搜索的文本（支持正则表达式，多个用逗号分隔）：").strip()
        if not user_input:
            print("[错误] 搜索模式不能为空")
            sys.exit(1)
        pattern_strs = [p.strip() for p in user_input.split(",") if p.strip()]

    if not pattern_strs:
        print("[错误] 搜索模式不能为空")
        sys.exit(1)

    # ── 编译所有正则 ──
    patterns: list[tuple[str, re.Pattern]] = []
    for pat_str in pattern_strs:
        if args.no_regex:
            pat_display = pat_str
            pat_regex = re.escape(pat_str)
        else:
            pat_display = pat_str
            pat_regex = pat_str

        try:
            compiled = re.compile(pat_regex, re.IGNORECASE)
            patterns.append((pat_display, compiled))
        except re.error as e:
            print(f"[错误] 无效的正则表达式：{pat_str} → {e}")
            print("提示：使用 --no-regex 参数可将搜索文本作为普通字符串处理")
            sys.exit(1)

    # ── 确定结果保存目录 ──
    if args.output:
        output_dir = os.path.abspath(args.output)
    else:
        # 默认保存在脚本所在目录的 search_results 子目录下
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "search_results")

    os.makedirs(output_dir, exist_ok=True)

    # 文件名：时间戳 + 搜索关键词（过滤非法字符）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_patterns = "_".join(re.sub(r'[\\/:*?"<>|]', "_", p)[:20] for p in pattern_strs)[:50]
    output_filename = f"{timestamp}_{safe_patterns}.txt"
    output_path = os.path.join(output_dir, output_filename)

    print(f"\n正在扫描目录：{search_path}")
    print(f"搜索关键词：{', '.join(pattern_strs)}")
    print(f"关键词数量：{len(patterns)}")
    print(f"结果将保存至：{output_path}\n")
    print("-" * 60)

    results = []
    try:
        scan_directory(search_path, patterns, results, base_dir=search_path)
    except KeyboardInterrupt:
        print("\n[中断] 用户取消搜索")

    print("-" * 60)
    print(f"\n搜索完成，共在 {len(results)} 个文件中找到匹配项。")

    write_results(results, output_path, pattern_strs, len(patterns))
    print(f"结果已保存至 {output_path}")


if __name__ == "__main__":
    main()
