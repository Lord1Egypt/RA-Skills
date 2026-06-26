#!/usr/bin/env python3
"""
Ubuntu 软件包安装脚本（带进度提示）

功能：
- 支持 apt 安装
- 支持 deb 包安装（本地或 URL）
- 显示安装进度
- 检查软件是否已安装
"""

import argparse
import subprocess
import os
import sys
import tempfile
import shutil
from pathlib import Path


def print_step(step, total, message):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"[{step}/{total}] {message}")
    print('='*60)


def print_progress(message):
    """打印进度信息"""
    print(f"⏳ {message}")


def print_success(message):
    """打印成功信息"""
    print(f"✅ {message}")


def print_error(message):
    """打印错误信息"""
    print(f"❌ {message}")


def print_warning(message):
    """打印警告信息"""
    print(f"⚠️  {message}")


def run_command(cmd, shell=False, check=True, show_output=True):
    """执行命令并实时显示输出"""
    try:
        process = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        output_lines = []
        for line in process.stdout:
            output_lines.append(line)
            if show_output:
                print(f"   {line.rstrip()}")
        
        process.wait()
        
        output = ''.join(output_lines)
        if check and process.returncode != 0:
            return False, output
        return True, output
    
    except Exception as e:
        return False, str(e)


def check_package_installed(package_name):
    """检查包是否已安装"""
    result = subprocess.run(
        ["dpkg", "-l", package_name],
        capture_output=True,
        text=True
    )
    return result.returncode == 0 and package_name in result.stdout


def check_command_exists(command):
    """检查命令是否存在"""
    return shutil.which(command) is not None


def install_with_apt(package_name, use_sudo=False):
    """使用 apt 安装包"""
    total_steps = 2
    
    # 检查是否已安装
    if check_package_installed(package_name):
        print_success(f"{package_name} 已安装，跳过")
        return True, "已安装"
    
    print_step(1, total_steps, f"更新包列表")
    update_cmd = ["apt", "update"]
    if use_sudo:
        update_cmd.insert(0, "sudo")
    
    print_progress("正在更新包列表...")
    success, output = run_command(update_cmd, check=False, show_output=False)
    if not success:
        print_warning(f"更新包列表失败，继续尝试安装")
    
    print_step(2, total_steps, f"安装 {package_name}")
    install_cmd = ["apt", "install", "-y", package_name]
    if use_sudo:
        install_cmd.insert(0, "sudo")
    
    print_progress(f"正在安装 {package_name}（可能需要几分钟）...")
    success, output = run_command(install_cmd, check=False, show_output=True)
    
    if success:
        print_success(f"{package_name} 安装成功")
        return True, "安装成功"
    else:
        print_error(f"{package_name} 安装失败")
        return False, f"安装失败"


def install_from_deb_file(deb_path, use_sudo=False):
    """从本地 deb 文件安装"""
    if not os.path.exists(deb_path):
        print_error(f"文件不存在: {deb_path}")
        return False, f"文件不存在: {deb_path}"
    
    print_progress(f"正在安装 {os.path.basename(deb_path)}...")
    
    install_cmd = ["dpkg", "-i", deb_path]
    if use_sudo:
        install_cmd.insert(0, "sudo")
    
    success, output = run_command(install_cmd, check=False, show_output=False)
    
    if not success:
        print_progress("尝试修复依赖...")
        fix_cmd = ["apt", "install", "-f", "-y"]
        if use_sudo:
            fix_cmd.insert(0, "sudo")
        run_command(fix_cmd, check=False, show_output=False)
        success, output = run_command(install_cmd, check=False, show_output=False)
    
    if success:
        print_success("安装成功")
        return True, "安装成功"
    else:
        print_error("安装失败")
        return False, "安装失败"


def download_file(url, dest_path):
    """下载文件（带进度显示）"""
    try:
        import requests
        
        print_progress(f"正在下载...")
        print(f"   URL: {url}")
        print(f"   目标: {dest_path}")
        
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        size_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        print(f"\r   进度: {percent:.1f}% ({size_mb:.1f}/{total_mb:.1f} MB)", end='', flush=True)
        
        print()  # 换行
        print_success(f"下载完成 ({downloaded / (1024*1024):.1f} MB)")
        return True, "下载成功"
    
    except Exception as e:
        print_error(f"下载失败: {str(e)}")
        return False, f"下载失败: {str(e)}"


def install_from_url(url, use_sudo=False, temp_dir=None):
    """从 URL 下载并安装 deb 包"""
    if temp_dir is None:
        temp_dir = tempfile.gettempdir()
    
    # 从 URL 提取文件名
    filename = url.split('/')[-1]
    if not filename.endswith('.deb'):
        filename = 'package.deb'
    
    deb_path = os.path.join(temp_dir, filename)
    
    print_progress(f"准备从 URL 安装")
    
    # 下载文件
    success, msg = download_file(url, deb_path)
    if not success:
        return False, msg
    
    # 安装
    success, msg = install_from_deb_file(deb_path, use_sudo)
    
    # 清理临时文件
    try:
        if os.path.exists(deb_path):
            os.remove(deb_path)
            print_progress(f"已清理临时文件")
    except:
        pass
    
    return success, msg


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Ubuntu 软件包安装工具（带进度提示）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用 apt 安装 terminator
  python install_package.py --package-name terminator --install-type apt --use-sudo
  
  # 从 URL 安装 Chrome
  python install_package.py --package-name google-chrome-stable --install-type url \
      --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" --use-sudo
        """
    )
    
    parser.add_argument('--package-name', required=True, help='软件包名称')
    parser.add_argument('--install-type', choices=['apt', 'deb', 'url'], required=True,
                        help='安装方式: apt/deb/url')
    parser.add_argument('--deb-path', help='本地 deb 文件路径')
    parser.add_argument('--deb-url', help='deb 文件下载 URL')
    parser.add_argument('--use-sudo', action='store_true', help='使用 sudo 权限')
    parser.add_argument('--check-only', action='store_true', help='仅检查是否已安装')
    
    args = parser.parse_args()
    
    # 检查模式
    if args.check_only:
        installed = check_package_installed(args.package_name)
        if installed:
            print_success(f"{args.package_name} 已安装")
            return 0
        else:
            print_warning(f"{args.package_name} 未安装")
            return 1
    
    # sudo 提示
    if args.use_sudo:
        print("\n" + "="*60)
        print("⚠️  此操作需要 sudo 权限")
        print("="*60)
        print(f"即将安装: {args.package_name}")
        print(f"安装方式: {args.install_type}")
        if args.install_type == 'url' and args.deb_url:
            print(f"下载地址: {args.deb_url}")
        
        try:
            response = input("\n是否继续? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("用户取消操作")
                return 1
        except EOFError:
            # 非交互模式，继续执行
            pass
    
    # 执行安装
    print(f"\n{'='*60}")
    print(f"开始安装: {args.package_name}")
    print('='*60)
    
    if args.install_type == 'apt':
        success, msg = install_with_apt(args.package_name, args.use_sudo)
    elif args.install_type == 'deb':
        if not args.deb_path:
            print_error("install-type=deb 时必须指定 --deb-path")
            return 1
        success, msg = install_from_deb_file(args.deb_path, args.use_sudo)
    elif args.install_type == 'url':
        if not args.deb_url:
            print_error("install-type=url 时必须指定 --deb-url")
            return 1
        success, msg = install_from_url(args.deb_url, args.use_sudo)
    else:
        print_error(f"不支持的安装类型: {args.install_type}")
        return 1
    
    if success:
        print_success(f"{args.package_name} 安装完成")
        return 0
    else:
        print_error(f"{args.package_name} 安装失败: {msg}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print_error(f"错误: {str(e)}")
        sys.exit(1)
