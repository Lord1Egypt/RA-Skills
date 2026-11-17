#!/usr/bin/env python3
"""
archive_reader.py — 自进化压缩文件阅读器的核心脚本。
支持自动检测格式、提取、预览，以及学习记忆管理。
"""
import os, sys, json, time, hashlib
import zipfile, tarfile
from pathlib import Path

LEARN_FILE = Path.home() / ".workbuddy" / "skills" / "archive-smart-reader" / "learned_patterns.json"
SUPPORTED = {
    ".zip": "zipfile",
    ".tar": "tarfile",
    ".gz":  "gzip+tarfile",
    ".tgz": "gzip+tarfile",
    ".bz2": "bz2+tarfile",
    ".xz":  "lzma+tarfile",
    ".7z":  "py7zr (optional)",
    ".rar": "rarfile",
}

def load_learning():
    try:
        return json.loads(LEARN_FILE.read_text())
    except:
        return {
            "version": 1, "totalOps": 0, "totalErrors": 0,
            "formatStats": {}, "errorPatterns": {},
            "optimizations": {"preferTempDir": True, "autoCleanup": True},
        }

def save_learning(data):
    LEARN_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEARN_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def _ensure_rar_tool():
    """查找外部 RAR 解压工具（unrar 或 7za）。
    rarfile 仅用纯 Python 解析目录结构(列出文件)，但读取/提取内容需要外部工具。
    返回 True 表示已找到并配置好工具；False 表示未找到（此时仅 'list' 可用）。
    """
    import rarfile, shutil
    # 已配置且可用？
    try:
        if getattr(rarfile, "UNRAR_TOOL", "unrar") not in (None, "", "unrar") or \
           getattr(rarfile, "SEVENZIP_TOOL", None):
            rarfile.tool_setup(force=True)
            return True
    except Exception:
        pass
    home = str(Path.home())
    candidates = []
    # 1) PATH 中的 unrar / 7za / 7z
    for name in ("unrar", "7za", "7z"):
        p = shutil.which(name)
        if p:
            candidates.append(p)
    # 2) 常见安装/下载位置（含中文用户名路径也支持，Windows 用宽字符 API）
    extra = [
        os.path.join(home, "Downloads", "unrar.exe"),
        os.path.join(home, "Downloads", "7za.exe"),
        os.path.join(home, "AppData", "Local", "Temp", "unrar.exe"),
        os.path.join(home, "WorkBuddy", "Claw", "UnRAR.exe"),
        r"C:\tmp_rt\unrar.exe",
        r"C:\tmp_rt\7za.exe",
    ]
    candidates.extend(extra)
    for p in candidates:
        if not os.path.isfile(p):
            continue
        low = p.lower()
        try:
            if low.endswith("7za.exe") or low.endswith("7z.exe"):
                rarfile.SEVENZIP_TOOL = p
            else:
                rarfile.UNRAR_TOOL = p
            rarfile.CURRENT_SETUP = None
            rarfile.tool_setup(force=True)
            return True
        except Exception:
            continue
    return False

def guess_format(path):
    ext = Path(path).suffix.lower()
    name = Path(path).name.lower()
    if name.endswith(".tar.gz") or name.endswith(".tgz"):
        return ".tgz"
    if name.endswith(".tar.bz2"):
        return ".bz2"
    if name.endswith(".tar.xz"):
        return ".xz"
    return ext

def list_archive(path):
    """列出压缩包内容"""
    ext = guess_format(path)
    fmt_map = {
        ".zip": ("zipfile", _list_zip),
        ".tar": ("tarfile", _list_tar),
        ".tgz": ("tarfile", _list_tar),
        ".gz":  ("tarfile", _list_tar),
        ".bz2": ("tarfile", _list_tar),
        ".xz":  ("tarfile", _list_tar),
        ".rar": ("rarfile", _list_rar),
    }
    engine, func = fmt_map.get(ext, (None, None))
    if not func:
        return [False, f"不支持格式: {ext}。尝试安装 py7zr/rarfile 后可支持 7z/rar"]
    try:
        result = func(path)
        return [True, result]
    except Exception as e:
        return [False, str(e)]

def _list_zip(path):
    with zipfile.ZipFile(path, 'r') as z:
        infos = z.infolist()
        items = []
        for i in infos:
            items.append({
                "name": i.filename,
                "size": i.file_size,
                "compress": i.compress_size,
                "ratio": f"{i.compress_size/i.file_size*100:.0f}%" if i.file_size else "-",
                "is_dir": i.filename.endswith("/"),
            })
        return items

def _list_tar(path):
    with tarfile.open(path, 'r:*') as t:
        members = t.getmembers()
        items = []
        for m in members:
            items.append({
                "name": m.name,
                "size": m.size,
                "is_dir": m.isdir(),
                "type": "dir" if m.isdir() else "file",
            })
        return items

def _list_rar(path):
    import rarfile
    with rarfile.RarFile(path, 'r') as rf:
        infos = rf.infolist()
        items = []
        for i in infos:
            items.append({
                "name": i.filename,
                "size": i.file_size,
                "compress": i.compress_size,
                "ratio": f"{i.compress_size/i.file_size*100:.0f}%" if i.file_size else "-",
                "is_dir": i.is_dir(),
                "type": "dir" if i.is_dir() else "file",
            })
        return items

def peek_file(archive_path, file_path_in_archive):
    """预览压缩包内某个文件的内容（文本）"""
    ext = guess_format(archive_path)
    if ext == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as z:
            content = z.read(file_path_in_archive)
            return content.decode("utf-8", errors="replace")[:50000]
    elif ext == ".rar":
        import rarfile
        if not _ensure_rar_tool():
            raise RuntimeError(
                "RAR 内容预览需要外部解压工具（unrar 或 7-Zip）。已在常见位置自动查找但未找到。"
                "请安装 7-Zip 或将 unrar.exe 放到 Downloads 目录后重试。"
                "（仅 'list 列出文件' 功能无需外部工具）"
            )
        with rarfile.RarFile(archive_path, 'r') as rf:
            content = rf.read(file_path_in_archive)
            return content.decode("utf-8", errors="replace")[:50000]
    else:
        with tarfile.open(archive_path, 'r:*') as t:
            f = t.extractfile(file_path_in_archive)
            if f:
                content = f.read()
                return content.decode("utf-8", errors="replace")[:50000]
            return None

def extract_all(archive_path, output_dir):
    """解压到指定目录"""
    ext = guess_format(archive_path)
    os.makedirs(output_dir, exist_ok=True)
    if ext == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as z:
            z.extractall(output_dir)
    elif ext == ".rar":
        import rarfile
        if not _ensure_rar_tool():
            raise RuntimeError(
                "RAR 解压需要外部解压工具（unrar 或 7-Zip）。已在常见位置自动查找但未找到。"
                "请安装 7-Zip 或将 unrar.exe 放到 Downloads 目录后重试。"
            )
        with rarfile.RarFile(archive_path, 'r') as rf:
            rf.extractall(output_dir)
    else:
        with tarfile.open(archive_path, 'r:*') as t:
            t.extractall(output_dir)
    files = list(Path(output_dir).rglob("*"))
    return len([f for f in files if f.is_file()])

def extract_file(archive_path, file_path_in_archive, output_path):
    """提取单个文件"""
    ext = guess_format(archive_path)
    os.makedirs(Path(output_path).parent, exist_ok=True)
    if ext == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as z:
            with open(output_path, 'wb') as f:
                f.write(z.read(file_path_in_archive))
    elif ext == ".rar":
        import rarfile
        if not _ensure_rar_tool():
            raise RuntimeError(
                "RAR 单文件提取需要外部解压工具（unrar 或 7-Zip）。已在常见位置自动查找但未找到。"
                "请安装 7-Zip 或将 unrar.exe 放到 Downloads 目录后重试。"
            )
        with rarfile.RarFile(archive_path, 'r') as rf:
            with open(output_path, 'wb') as fout:
                fout.write(rf.read(file_path_in_archive))
    else:
        with tarfile.open(archive_path, 'r:*') as t:
            f = t.extractfile(file_path_in_archive)
            if f:
                with open(output_path, 'wb') as fout:
                    fout.write(f.read())
    return output_path

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "list":
        ok, data = list_archive(sys.argv[2])
        if ok:
            for item in data:
                tag = "📁" if item["is_dir"] else "📄"
                size = item.get("size", 0)
                print(f"{tag} {item['name']}  ({size:,} bytes)")
        else:
            print(f"❌ {data}", file=sys.stderr)
            sys.exit(1)

    elif cmd == "peek":
        try:
            content = peek_file(sys.argv[2], sys.argv[3])
        except RuntimeError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(1)
        if content:
            print(content)
        else:
            print("❌ 无法读取该文件（可能是二进制或路径错误）", file=sys.stderr)
            sys.exit(1)

    elif cmd == "extract":
        try:
            count = extract_all(sys.argv[2], sys.argv[3])
        except RuntimeError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ 已解压 {count} 个文件到 {sys.argv[3]}")

    elif cmd == "extract-file":
        try:
            path = extract_file(sys.argv[2], sys.argv[3], sys.argv[4])
        except RuntimeError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ 已提取到 {path}")
