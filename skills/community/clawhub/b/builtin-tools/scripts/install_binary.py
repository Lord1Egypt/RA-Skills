#!/usr/bin/env python3
"""install_binary — 下载并安装运行时（Python / Node.js）"""
import sys, os, json, zipfile, tarfile, shutil, tempfile, stat, urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

HEADERS = {"User-Agent": "builtin-tools/1.0"}


# ─── 下载源配置 ────────────────────────────────────────────
PYTHON_DOWNLOADS = {
    "windows": {
        "url_template": "https://www.python.org/ftp/python/{version}/python-{version}-embed-amd64.zip",
        "ext": ".zip",
    },
    "darwin": {
        "url_template": "https://www.python.org/ftp/python/{version}/python-{version}-macos11.pkg",
        "ext": ".pkg",
    },
    "linux": {
        "url_template": "https://www.python.org/ftp/python/{version}/Python-{version}.tgz",
        "ext": ".tgz",
    },
}

NODE_DOWNLOADS = {
    "windows": {
        "url_template": "https://nodejs.org/dist/v{version}/node-v{version}-win-x64.zip",
        "ext": ".zip",
    },
    "darwin": {
        "url_template": "https://nodejs.org/dist/v{version}/node-v{version}-darwin-x64.tar.gz",
        "ext": ".tgz",
    },
    "linux": {
        "url_template": "https://nodejs.org/dist/v{version}/node-v{version}-linux-x64.tar.xz",
        "ext": ".txz",
    },
}


def detect_platform():
    """检测当前平台"""
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "darwin"
    else:
        return "linux"


def get_install_dir(binary_type, version):
    """获取安装目标目录"""
    base = home_dir() / ".builtin-tools" / "binaries" / binary_type / "versions" / version
    return base


def download_file(url, dest_dir, timeout=300):
    """下载文件到目录，返回下载的文件路径"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1].split("?")[0]
    dest_path = dest_dir / filename

    if dest_path.exists():
        return dest_path

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 8192

        with open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
        return dest_path
    except Exception as e:
        if dest_path.exists():
            dest_path.unlink()
        raise e


def extract_archive(archive_path, dest_dir):
    """解压压缩包"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    ext = archive_path.suffix.lower()

    if ext == ".zip":
        with zipfile.ZipFile(str(archive_path), "r") as zf:
            zf.extractall(str(dest_dir))
    elif ext in (".gz", ".tgz", ".bz2", ".xz"):
        with tarfile.open(str(archive_path), "r:*") as tf:
            tf.extractall(str(dest_dir))
    else:
        raise ValueError(f"不支持的压缩格式: {ext}")


def find_binary(dest_dir, binary_names):
    """在目录中查找可执行文件"""
    for root, dirs, files in os.walk(str(dest_dir)):
        for name in binary_names:
            if name in files:
                return Path(root) / name
            # Windows 可执行文件
            if name + ".exe" in files:
                return Path(root) / (name + ".exe")
    return None


def main():
    params = parse_input()
    binary_type = get_param(params, "type", required=True)
    version = get_param(params, "version", required=True)
    dest = get_param(params, "dest")
    force = get_param(params, "force", False)

    if binary_type not in ("python", "node"):
        output_error(f"不支持的类型: {binary_type}（仅支持 python, node）", EXIT_PARAM_ERROR)

    install_dir = get_install_dir(binary_type, version) if not dest else resolve_path(str(dest))

    # 检查是否已安装
    if install_dir.exists() and not force:
        binary_names = ["python3", "python"] if binary_type == "python" else ["node"]
        existing = find_binary(install_dir, binary_names)
        if existing:
            output_ok({
                "status": "already_installed",
                "type": binary_type,
                "version": version,
                "path": str(existing),
                "install_dir": str(install_dir),
            })

    # 构建下载 URL
    platform = detect_platform()
    if binary_type == "python":
        config = PYTHON_DOWNLOADS.get(platform)
    else:
        config = NODE_DOWNLOADS.get(platform)

    if not config:
        output_error(f"不支持的平台: {platform}", EXIT_UNSUPPORTED_OS)

    url = config["url_template"].format(version=version)

    # 下载
    tmp_dir = Path(tempfile.mkdtemp(prefix="builtin-install-"))
    try:
        archive_path = download_file(url, tmp_dir)
        output_ok({
            "status": "downloaded",
            "type": binary_type,
            "version": version,
            "url": url,
            "archive": str(archive_path),
            "message": "下载完成，开始解压...",
        })

        # 解压
        extract_dir = install_dir
        extract_archive(archive_path, extract_dir)

        # 查找可执行文件
        binary_names = ["python3", "python"] if binary_type == "python" else ["node"]
        binary_path = find_binary(extract_dir, binary_names)

        if not binary_path:
            output_error(
                f"安装后未找到可执行文件 (查找: {binary_names})",
                EXIT_EXEC_ERROR,
            )

        # 设置可执行权限（非 Windows）
        if platform != "windows":
            binary_path.chmod(binary_path.stat().st_mode | stat.S_IEXEC)

        output_ok({
            "status": "installed",
            "type": binary_type,
            "version": version,
            "path": str(binary_path),
            "install_dir": str(install_dir),
            "platform": platform,
        })

    except Exception as e:
        output_error(f"安装失败: {e}", EXIT_EXEC_ERROR)
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(str(tmp_dir), ignore_errors=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()
