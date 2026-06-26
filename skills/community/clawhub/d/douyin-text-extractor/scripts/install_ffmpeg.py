#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFmpeg 自动安装脚本
检测系统是否安装 FFmpeg，如未安装则自动下载静态编译版本
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import urllib.request
import zipfile
import tarfile
import stat


# FFmpeg 静态编译版本下载地址
FFMPEG_DOWNLOAD_URLS = {
    "darwin-arm64": "https://evermeet.cx/ffmpeg/getrelease/zip",
    "darwin-x64": "https://evermeet.cx/ffmpeg/getrelease/zip",
    "linux-x64": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
    "win-x64": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
}

# 国内镜像（备用）
FFMPEG_MIRROR_URLS = {
    "darwin-arm64": "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-macos-arm64.zip",
    "darwin-x64": "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-macos-x64.zip",
    "linux-x64": "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz",
    "win-x64": "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
}


def get_system_info():
    """获取系统信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # 映射到标准平台标识
    if system == "darwin":
        if machine == "arm64":
            return "darwin-arm64", "macOS (Apple Silicon)"
        else:
            return "darwin-x64", "macOS (Intel)"
    elif system == "linux":
        if machine in ["x86_64", "amd64"]:
            return "linux-x64", "Linux (x64)"
        elif machine in ["aarch64", "arm64"]:
            return "linux-arm64", "Linux (ARM64)"
    elif system == "windows":
        if machine in ["x86_64", "AMD64"]:
            return "win-x64", "Windows (x64)"
    
    return None, f"{system} ({machine})"


def check_ffmpeg_installed():
    """检查 FFmpeg 是否已安装"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, version_line
    except Exception:
        pass
    
    return False, None


def check_ffmpeg_in_dir(check_path: Path) -> bool:
    """检查指定目录是否有 FFmpeg"""
    ffmpeg_exe = check_path / "ffmpeg"
    if platform.system() == "Windows":
        ffmpeg_exe = ffmpeg_exe.with_suffix(".exe")
    
    return ffmpeg_exe.exists()


def get_download_path():
    """获取 FFmpeg 下载路径"""
    # 优先下载到 Skill 目录
    script_dir = Path(__file__).parent
    ffmpeg_dir = script_dir.parent / "ffmpeg"
    ffmpeg_dir.mkdir(exist_ok=True)
    return ffmpeg_dir


def download_file(url: str, dest_path: Path, show_progress: bool = True):
    """下载文件并显示进度"""
    print(f"正在下载：{url}")
    
    def report_progress(block_num, block_size, total_size):
        if show_progress:
            downloaded = block_num * block_size
            if downloaded < total_size:
                percent = min(downloaded * 100 / total_size, 100)
                print(f"\r下载进度：{percent:.1f}%", end="", flush=True)
            else:
                print(f"\r下载完成！")
    
    try:
        urllib.request.urlretrieve(url, dest_path, reporthook=report_progress)
        return True
    except Exception as e:
        print(f"\n下载失败：{e}")
        return False


def extract_archive(archive_path: Path, dest_dir: Path):
    """解压归档文件"""
    print(f"\n正在解压到：{dest_dir}")
    
    suffix = archive_path.suffix.lower()
    
    try:
        if suffix == ".zip":
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                # 获取根目录名
                root_dir = zip_ref.namelist()[0].split('/')[0]
                zip_ref.extractall(dest_dir.parent)
                
                # 移动到目标目录
                extracted_dir = dest_dir.parent / root_dir
                if extracted_dir.exists():
                    shutil.move(str(extracted_dir), str(dest_dir / "ffmpeg_bin"))
                    
        elif suffix in [".xz", ".gz", ".bz2"]:
            if suffix == ".xz":
                import lzma
                # 先解压 .xz
                temp_tar = archive_path.with_suffix("")
                with lzma.open(archive_path, 'rb') as f_in:
                    with open(temp_tar, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # 再解压 .tar
                with tarfile.open(temp_tar, 'r') as tar_ref:
                    root_dir = tar_ref.getnames()[0].split('/')[0]
                    tar_ref.extractall(dest_dir.parent)
                    temp_tar.unlink()
                
                # 移动到目标目录
                extracted_dir = dest_dir.parent / root_dir
                if extracted_dir.exists():
                    shutil.move(str(extracted_dir), str(dest_dir / "ffmpeg_bin"))
            else:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(dest_dir.parent)
        
        print("解压完成！")
        return True
        
    except Exception as e:
        print(f"解压失败：{e}")
        return False


def setup_ffmpeg():
    """主安装流程"""
    print("=" * 60)
    print("🎬 FFmpeg 自动安装脚本")
    print("=" * 60)
    
    # 1. 检查是否已安装
    print("\n📌 检查 FFmpeg 安装状态...")
    installed, version = check_ffmpeg_installed()
    
    if installed:
        print(f"✅ FFmpeg 已安装：{version}")
        print("\n💡 提示：如需使用最新版本的 FFmpeg，可以选择重新下载。")
        response = input("是否重新下载？[y/N]: ")
        if response.lower() != 'y':
            return True
    
    # 2. 获取系统信息
    platform_id, platform_name = get_system_info()
    print(f"\n💻 检测到系统：{platform_name}")
    
    if not platform_id:
        print("\n❌ 不支持的系统平台")
        print("\n请手动安装 FFmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: apt install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        return False
    
    # 3. 选择下载源
    print("\n🌐 选择下载源:")
    print("  1. 官方源（可能较慢）")
    print("  2. GitHub 镜像（推荐，国内访问快）")
    
    choice = input("请选择 [1/2]，默认 2: ").strip() or "2"
    
    if choice == "1":
        download_url = FFMPEG_DOWNLOAD_URLS.get(platform_id)
    else:
        download_url = FFMPEG_MIRROR_URLS.get(platform_id)
    
    if not download_url:
        print(f"\n❌ 未找到适用于 {platform_name} 的 FFmpeg 版本")
        return False
    
    print(f"\n📥 下载地址：{download_url}")
    
    # 4. 创建下载目录
    download_path = get_download_path()
    print(f"📁 安装目录：{download_path}")
    
    # 5. 下载文件
    archive_name = f"ffmpeg{'-win' if 'win' in platform_id else ''}.zip" if 'win' in platform_id or 'darwin' in platform_id else "ffmpeg.tar.xz"
    archive_path = download_path / archive_name
    
    if not download_file(download_url, archive_path):
        print("\n❌ 下载失败，请检查网络连接")
        print("\n手动安装 FFmpeg:")
        if platform_id.startswith("darwin"):
            print("  brew install ffmpeg")
        elif platform_id.startswith("linux"):
            print("  apt install ffmpeg  # Ubuntu/Debian")
            print("  yum install ffmpeg  # CentOS/RHEL")
        else:
            print("  https://ffmpeg.org/download.html")
        return False
    
    # 6. 解压文件
    if not extract_archive(archive_path, download_path):
        return False
    
    # 7. 清理归档文件
    print("\n🧹 清理临时文件...")
    if archive_path.exists():
        archive_path.unlink()
    
    # 8. 设置权限（Unix 系统）
    if platform.system() != "Windows":
        ffmpeg_bin_dir = download_path / "ffmpeg_bin"
        ffmpeg_exe = ffmpeg_bin_dir / "ffmpeg"
        ffprobe_exe = ffmpeg_bin_dir / "ffprobe"
        
        if ffmpeg_exe.exists():
            os.chmod(ffmpeg_exe, os.stat(ffmpeg_exe).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"✅ 设置执行权限：{ffmpeg_exe}")
        
        if ffprobe_exe.exists():
            os.chmod(ffprobe_exe, os.stat(ffprobe_exe).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    # 9. 添加到 PATH（提示用户）
    print("\n" + "=" * 60)
    print("✅ FFmpeg 安装完成！")
    print("=" * 60)
    
    ffmpeg_bin_dir = download_path / "ffmpeg_bin"
    
    if platform.system() == "Windows":
        print(f"\n📍 FFmpeg 路径：{ffmpeg_bin_dir}")
        print("\n请手动添加到系统 PATH:")
        print(f"  1. 右键'此电脑' → 属性 → 高级系统设置")
        print(f"  2. 环境变量 → 系统变量 → Path → 编辑")
        print(f"  3. 新建 → 添加路径：{ffmpeg_bin_dir}")
    else:
        print(f"\n📍 FFmpeg 路径：{ffmpeg_bin_dir}")
        print("\n添加到 PATH（选择以下一种方式）:")
        print(f"\n  临时生效（当前终端）:")
        print(f"    export PATH=\"{ffmpeg_bin_dir}:$PATH\"")
        print(f"\n  永久生效（添加到 shell 配置）:")
        
        shell_config = "~/.bashrc"
        if os.path.exists(os.path.expanduser("~/.zshrc")):
            shell_config = "~/.zshrc"
        
        print(f"    echo 'export PATH=\"{ffmpeg_bin_dir}:$PATH\"' >> {shell_config}")
        print(f"    source {shell_config}")
    
    # 10. 验证安装
    print("\n🧪 验证安装...")
    test_env = os.environ.copy()
    test_env["PATH"] = str(ffmpeg_bin_dir) + os.pathsep + test_env["PATH"]
    
    try:
        result = subprocess.run(
            [str(ffmpeg_bin_dir / "ffmpeg"), "-version"],
            capture_output=True,
            text=True,
            timeout=5,
            env=test_env
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ 验证成功：{version_line}")
        else:
            print("⚠️ 验证失败，请检查 PATH 配置")
    except Exception as e:
        print(f"⚠️ 验证失败：{e}")
    
    print("\n💡 提示：")
    print("  - 重启终端后生效")
    print("  - 或运行：export PATH=\"{}:$PATH\"".format(ffmpeg_bin_dir))
    
    return True


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FFmpeg 自动安装脚本")
    parser.add_argument("--force", action="store_true", help="强制重新下载")
    parser.add_argument("--quiet", action="store_true", help="安静模式")
    parser.add_argument("--check", action="store_true", help="仅检查安装状态")
    
    args = parser.parse_args()
    
    if args.check:
        installed, version = check_ffmpeg_installed()
        if installed:
            print(f"✅ FFmpeg 已安装：{version}")
            sys.exit(0)
        else:
            print("❌ FFmpeg 未安装")
            sys.exit(1)
    
    try:
        success = setup_ffmpeg()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ 安装已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
