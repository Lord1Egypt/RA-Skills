"""
setup_resources.py - 下载并部署 ai-literacy-expert-v7-1 所需的外部资源。

当前实现：
  - ffmpeg.exe / ffprobe.exe -> <SKILL_DIR>/bin/

用法：
    python setup_resources.py            # 仅下载缺失资源
    python setup_resources.py --force    # 强制重新下载
    set HTTPS_PROXY=http://127.0.0.1:7890 & python setup_resources.py
    python setup_resources.py --ffmpeg-url <URL>  # 指定自定义下载源

SKILL_DIR 自动解析为本脚本所在 scripts/ 目录的上一级，即 ai-literacy-expert-v7-1/。
ffmpeg 下载源复用 video-editing-skills-main/scripts/setup_resources.py 的 FFMPEG_ZIP_URLS。
"""


# --- UTF-8 stdout/stderr (Windows 中文输出防乱码) -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径常量（self-contained：当前 skill 尚未提供 skill_runtime.py）
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
BIN_DIR = SKILL_DIR / "bin"
FFMPEG_PATH = BIN_DIR / "ffmpeg.exe"
FFPROBE_PATH = BIN_DIR / "ffprobe.exe"

# ---------------------------------------------------------------------------
# ffmpeg 下载源（与 video-editing-skills-main/scripts/setup_resources.py 保持一致）
# ---------------------------------------------------------------------------
FFMPEG_ZIP_URLS = [
    "https://github.com/GyanD/codexffmpeg/releases/download/8.0.1/ffmpeg-8.0.1-full_build.zip",
]

DOWNLOAD_TIMEOUT = 120  # 秒


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _find_in_zip(zf: zipfile.ZipFile, filename: str) -> str | None:
    """在 zip 里找到 filename（只取文件名，不含路径），返回 zip 内完整路径。"""
    for name in zf.namelist():
        if Path(name).name == filename:
            return name
    return None


def _verify_exe(exe_path: Path, flags: tuple[str, ...] = ("-version",)) -> bool:
    """运行 exe 并尝试给定参数，返回是否成功（用于校验下载是否完整）。"""
    for flag in flags:
        try:
            result = subprocess.run(
                [str(exe_path), flag],
                capture_output=True,
                timeout=15,
            )
            if result.returncode == 0:
                return True
        except Exception:
            continue
    return False


def _install_proxy_opener() -> None:
    """根据环境变量 HTTPS_PROXY / HTTP_PROXY 安装 urllib 的代理。"""
    proxy = (
        os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)


def _download_with_progress(url: str, dest: Path, timeout: int = DOWNLOAD_TIMEOUT) -> None:
    """下载 URL 到 dest。"""
    log.info(f"  正在下载:{url}")
    log.warn(f"  目标位置:{dest}(超时 {timeout}s)")

    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        urllib.request.urlretrieve(url, str(dest))
    finally:
        socket.setdefaulttimeout(old_timeout)


# ---------------------------------------------------------------------------
# 核心功能:下载 ffmpeg / ffprobe
# ---------------------------------------------------------------------------

def setup_ffmpeg(force: bool = False) -> bool:
    """
    从内置 URL 下载 ffmpeg .zip,将 ffmpeg.exe 和 ffprobe.exe 部署到 <SKILL_DIR>/bin/。
    支持环境变量 HTTPS_PROXY / HTTP_PROXY。

    Args:
        force: True 时强制重新下载,即使目标文件已存在且可用。

    Returns:
        True 表示成功(含「已存在跳过」),False 表示失败。
    """
    ffmpeg_dest = BIN_DIR / "ffmpeg.exe"
    ffprobe_dest = BIN_DIR / "ffprobe.exe"

    # 1. 检查是否已存在且可用
    if not force and ffmpeg_dest.exists() and ffprobe_dest.exists():
        if _verify_exe(ffmpeg_dest, ("-version",)):
            log.warn(f"[ffmpeg] 已存在且可用,跳过。({ffmpeg_dest})")
            return True
        else:
            log.warn("[ffmpeg] 文件已存在但校验失败,将重新安装。")

    BIN_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir = Path(tmp_str)
        zip_path = tmp_dir / "ffmpeg.zip"

        # 2. 联网下载(支持代理)
        _install_proxy_opener()
        downloaded_ok = False
        for url in FFMPEG_ZIP_URLS:
            try:
                _download_with_progress(url, zip_path)
                if zip_path.stat().st_size == 0:
                    continue
                with zipfile.ZipFile(zip_path, "r") as zf:
                    if _find_in_zip(zf, "ffmpeg.exe") and _find_in_zip(zf, "ffprobe.exe"):
                        downloaded_ok = True
                        break
            except Exception as e:
                log.warn(f"[ffmpeg] 当前源失败:{e}")
                continue
        if not downloaded_ok:
            log.error(
                "[ffmpeg] 所有下载源均失败，请设置 HTTPS_PROXY / HTTP_PROXY 后重试。"
            )
            return False

        # 3. 解压并复制 ffmpeg.exe / ffprobe.exe
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                ffmpeg_zip_path = _find_in_zip(zf, "ffmpeg.exe")
                ffprobe_zip_path = _find_in_zip(zf, "ffprobe.exe")
                if not ffmpeg_zip_path or not ffprobe_zip_path:
                    log.error("[ffmpeg] zip 包内未找到 ffmpeg.exe 或 ffprobe.exe")
                    return False

                with zf.open(ffmpeg_zip_path) as src, open(ffmpeg_dest, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                with zf.open(ffprobe_zip_path) as src, open(ffprobe_dest, "wb") as dst:
                    shutil.copyfileobj(src, dst)

        except zipfile.BadZipFile as e:
            log.error(f"[ffmpeg] zip 文件损坏:{e}")
            return False
        except Exception as e:
            log.error(f"[ffmpeg] 解压失败:{e}")
            return False

    # 4. 校验
    if _verify_exe(ffmpeg_dest, ("-version",)):
        log.info(f"[ffmpeg] ✓ 安装成功:{ffmpeg_dest}")
        log.info(f"[ffmpeg] ✓ 安装成功:{ffprobe_dest}")
        return True
    else:
        log.error("[ffmpeg] 警告:下载后校验失败,可能需要手动检查。")
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="下载并部署 ai-literacy-expert-v7-1 所需外部资源(ffmpeg / ffprobe)。"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新下载(即使目标文件已存在)。",
    )
    parser.add_argument(
        "--ffmpeg-url",
        dest="ffmpeg_url",
        default=None,
        help="指定单个 ffmpeg .zip 下载 URL(未指定时使用内置多源顺序尝试)。",
    )
    return parser.parse_args()


def main() -> int:
    """主入口。"""
    log = get_logger("setup_resources")
    args = parse_args()

    global FFMPEG_ZIP_URLS
    if args.ffmpeg_url:
        FFMPEG_ZIP_URLS = [args.ffmpeg_url]

    log.info("=" * 60)
    log.info("ai-literacy-expert-v7-1 资源安装脚本")
    log.info(f"SKILL_DIR   : {SKILL_DIR}")
    log.info(f"BIN_DIR     : {BIN_DIR}")
    log.info("=" * 60)

    log.info("\n[1/1] ffmpeg / ffprobe")
    ok = setup_ffmpeg(force=args.force)

    print()
    if ok:
        log.info("✓ 所有资源安装完成。")
        return 0
    else:
        log.error("✗ 部分资源安装失败,请查看上方错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
