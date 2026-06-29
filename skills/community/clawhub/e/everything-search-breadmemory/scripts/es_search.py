#!/usr/bin/env python3
"""
Everything 搜索封装
- 检测 es.exe 是否可用
- 不可用时引导下载 Everything 便携版
- 执行文件搜索，返回结构化 JSON
"""

import argparse
import json
import os
import subprocess
import sys
import shutil
import urllib.request
import zipfile
from pathlib import Path
from datetime import datetime

# 技能目录
SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "everything-search-breadmemory" / "data"
ES_EXE_PATH = SKILL_DIR / "es" / "es.exe"


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    config_path = DATA_DIR / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config):
    ensure_data_dir()
    with open(DATA_DIR / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def find_es_exe_in_path():
    """在 PATH 中查找 es.exe"""
    result = shutil.which("es")
    if result:
        return Path(result)
    return None


def find_es_exe_common_paths():
    """在常见安装路径中查找 es.exe"""
    common_paths = [
        Path("C:/Program Files/Everything/es.exe"),
        Path("C:/Program Files (x86)/Everything/es.exe"),
        Path("D:/Program Files/Everything/es.exe"),
        Path.home() / "scoop/apps/everything/current/es.exe",
    ]
    for p in common_paths:
        if p.exists():
            return p
    return None


def find_es_exe():
    """按优先级查找 es.exe：技能内置 > PATH > 常见路径"""
    if ES_EXE_PATH.exists():
        return ES_EXE_PATH
    path_es = find_es_exe_in_path()
    if path_es:
        return path_es
    common_es = find_es_exe_common_paths()
    if common_es:
        return common_es
    return None


def es_available():
    """检测 es.exe 是否可用（找到文件 且 能成功执行 -version）"""
    es_path = find_es_exe()
    if not es_path:
        return False, None
    try:
        result = subprocess.run(
            [str(es_path), "-version"],
            capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace"
        )
        if result.returncode == 0 or "version" in result.stdout.lower():
            return True, str(es_path)
        return False, str(es_path)
    except Exception:
        return False, str(es_path)


def download_everything_lite():
    """下载 Everything 便携版（精简CLI包）到技能目录"""
    ES_DIR = SKILL_DIR / "es"
    ES_DIR.mkdir(parents=True, exist_ok=True)

    # Everything CLI (es.exe) from voidtools
    # 使用 es-1.1.0.27.zip (约 500KB，仅 CLI)
    url = "https://www.voidtools.com/ES-1.1.0.27.zip"
    zip_path = ES_DIR / "es.zip"

    print(f"[everything-search] 正在从 {url} 下载 Everything CLI...", file=sys.stderr)
    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as e:
        print(f"[everything-search] 下载失败: {e}", file=sys.stderr)
        print(f"[everything-search] 请手动从 https://www.voidtools.com 下载 Everything", file=sys.stderr)
        print(f"[everything-search] 确保 es.exe 在 PATH 中或放在 {ES_DIR} 目录下", file=sys.stderr)
        return False

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(ES_DIR)

    zip_path.unlink()  # 删除 zip

    if ES_EXE_PATH.exists():
        print(f"[everything-search] Everything CLI 安装完成: {ES_EXE_PATH}", file=sys.stderr)
        return True
    else:
        print(f"[everything-search] 解压失败，未找到 es.exe", file=sys.stderr)
        return False


def ensure_es():
    """确保 es.exe 可用，不可用时尝试安装"""
    ok, path = es_available()
    if ok:
        return True, path

    print(f"[everything-search] es.exe 未找到或不可用", file=sys.stderr)
    print(f"[everything-search] 尝试下载 Everything CLI 便携版...", file=sys.stderr)

    if download_everything_lite():
        ok, path = es_available()
        if ok:
            return True, path

    return False, None


def search_files(query, max_results=100, search_path=None, match_case=False, match_whole_word=False, regex=False):
    """
    使用 es.exe 搜索文件
    返回结构化 JSON 列表
    """
    ok, es_path = ensure_es()
    if not ok:
        return {"error": "Everything/es.exe 不可用，请手动安装 Everything 并确保 es.exe 在 PATH 中", "files": []}

    cmd = [es_path, "-csv", "-size", "-date-modified", "-n", str(max_results)]

    if search_path:
        cmd.extend(["-path", search_path])
    if match_case:
        cmd.append("-case")
    if match_whole_word:
        cmd.append("-whole-word")
    if regex:
        cmd.append("-regex")

    cmd.append(query)

    try:
        # es.exe 输出编码取决于控制台代码页，中文 Windows 默认 GBK。
        # 先尝试 UTF-8，若包含替换字符则回退到 GBK。
        raw = subprocess.run(
            cmd,
            capture_output=True, timeout=30
        )
        stdout_bytes = raw.stdout
        stderr_bytes = raw.stderr

        # 尝试 UTF-8 解码
        stdout_text = stdout_bytes.decode("utf-8", errors="replace")
        if "\ufffd" in stdout_text:
            # 包含 Unicode 替换字符，尝试 GBK
            try:
                stdout_text = stdout_bytes.decode("gbk")
            except Exception:
                pass

        stderr_text = stderr_bytes.decode("utf-8", errors="replace")
        if "\ufffd" in stderr_text:
            try:
                stderr_text = stderr_bytes.decode("gbk")
            except Exception:
                pass

        result = type('Result', (), {
            'returncode': raw.returncode,
            'stdout': stdout_text,
            'stderr': stderr_text,
        })()
    except subprocess.TimeoutExpired:
        return {"error": "搜索超时（30秒），请缩小搜索范围", "files": []}
    except Exception as e:
        return {"error": f"搜索执行失败: {e}", "files": []}

    if result.returncode != 0 and result.returncode != 9:
        # returncode 9 = no results (not an error)
        err_msg = result.stderr.strip()
        if err_msg:
            return {"error": f"es.exe 错误 (code={result.returncode}): {err_msg}", "files": []}

    # 解析 CSV 输出
    files = []
    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        return {"total": 0, "files": files, "query": query, "es_path": es_path}

    # 先识别分隔符（可能逗号或制表符）
    header_line = lines[0].strip()
    delimiter = "," if "," in header_line else "\t"

    headers = [h.strip('"').strip() for h in header_line.split(delimiter)]

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # 处理 CSV 引号包裹
        values = []
        current = ""
        in_quotes = False
        for ch in line:
            if ch == '"':
                in_quotes = not in_quotes
            elif ch == delimiter and not in_quotes:
                values.append(current.strip().strip('"'))
                current = ""
            else:
                current += ch
        values.append(current.strip().strip('"'))

        entry = {}
        for i, h in enumerate(headers):
            if i < len(values):
                entry[h.lower()] = values[i]

        # 格式化关键字段
        file_path = entry.get("filename", entry.get("path", ""))
        file_name = entry.get("name", "")
        if not file_name and file_path:
            file_name = Path(file_path).name

        size_str = entry.get("size", "0")
        try:
            size_int = int(size_str)
        except (ValueError, TypeError):
            size_int = 0

        file_info = {
            "name": file_name,
            "path": file_path,
            "size_bytes": size_int,
            "date_modified": entry.get("date modified", entry.get("date_modified", "")),
            "extension": Path(file_name).suffix.lower() if file_name else "",
        }
        files.append(file_info)

    return {
        "total": len(files),
        "files": files,
        "query": query,
        "es_path": es_path,
        "search_path": search_path,
        "max_results": max_results
    }


def check_status():
    """检查 Everything 状态"""
    ok, path = es_available()
    everything_running = False
    if ok:
        try:
            r = subprocess.run([path], capture_output=True, timeout=5)
            everything_running = r.returncode != 8  # 8 = Everything service not running
        except Exception:
            pass

    return {
        "es_available": ok,
        "es_path": path,
        "everything_service_running": everything_running,
        "data_dir": str(DATA_DIR),
        "skill_dir": str(SKILL_DIR)
    }


def main():
    parser = argparse.ArgumentParser(description="Everything 搜索工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # status 子命令
    subparsers.add_parser("status", help="检查 Everything/es.exe 状态")

    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索文件")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--max", type=int, default=100, help="最大结果数（默认100）")
    search_parser.add_argument("--path", help="限定搜索路径")
    search_parser.add_argument("--case", action="store_true", help="区分大小写")
    search_parser.add_argument("--whole-word", action="store_true", help="全词匹配")
    search_parser.add_argument("--regex", action="store_true", help="正则表达式搜索")

    # install 子命令
    subparsers.add_parser("install", help="下载安装 Everything CLI")

    args = parser.parse_args()

    if args.command == "status":
        result = check_status()
    elif args.command == "search":
        result = search_files(
            args.query, max_results=args.max, search_path=args.path,
            match_case=args.case, match_whole_word=args.whole_word, regex=args.regex
        )
    elif args.command == "install":
        success = download_everything_lite()
        result = {"installed": success, "es_path": str(ES_EXE_PATH) if success else None}
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
