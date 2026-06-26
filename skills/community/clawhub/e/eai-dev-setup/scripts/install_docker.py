#!/usr/bin/env python3
"""
Docker 安装脚本（中国网络优化版，带进度提示）

功能：
- 使用阿里云镜像安装 Docker
- 显示安装进度
- 配置国内镜像加速器
"""

import argparse
import os
import sys
import subprocess
import json


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


def run_command(cmd, shell=False, check=True, use_sudo=False, show_output=True):
    """执行命令"""
    if use_sudo and not cmd.startswith("sudo"):
        if isinstance(cmd, list):
            cmd = ["sudo"] + cmd
        else:
            cmd = f"sudo {cmd}"
    
    try:
        if show_output:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
        else:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300)
        
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)


def check_docker_installed():
    """检查 Docker 是否已安装"""
    success, output = run_command(["docker", "--version"], check=False)
    return success


def remove_old_docker(use_sudo=True):
    """卸载旧版本 Docker"""
    print_step(1, 6, "卸载旧版本 Docker")
    
    old_packages = ["docker", "docker-engine", "docker.io", "containerd", "runc"]
    cmd = ["apt", "remove", "-y"] + old_packages
    
    print_progress("正在清理旧版本...")
    success, output = run_command(cmd, use_sudo=use_sudo, check=False, show_output=False)
    
    print_success("旧版本清理完成")
    return True


def install_dependencies(use_sudo=True):
    """安装依赖包"""
    print_step(2, 6, "安装依赖包")
    
    deps = ["ca-certificates", "curl", "gnupg", "lsb-release"]
    
    print_progress("正在安装依赖包...")
    for dep in deps:
        print(f"   - {dep}")
    
    cmd = ["apt", "install", "-y"] + deps
    success, output = run_command(cmd, use_sudo=use_sudo, show_output=False)
    
    if success:
        print_success("依赖包安装完成")
        return True
    else:
        print_error(f"依赖包安装失败: {output}")
        return False


def add_aliyun_key(use_sudo=True):
    """添加阿里云 Docker GPG 密钥"""
    print_step(3, 6, "添加 GPG 密钥（阿里云镜像）")
    
    print_progress("正在下载并添加 GPG 密钥...")
    
    keyrings_dir = "/etc/apt/keyrings"
    run_command(["mkdir", "-p", keyrings_dir], use_sudo=use_sudo, check=False, show_output=False)
    
    key_url = "https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg"
    
    success, output = run_command(
        f"curl -fsSL {key_url} | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        shell=True,
        use_sudo=False,
        show_output=False
    )
    
    if success or os.path.exists("/etc/apt/keyrings/docker.gpg"):
        print_success("GPG 密钥添加完成")
        return True
    else:
        print_error(f"GPG 密钥添加失败: {output}")
        return False


def add_docker_repository(use_sudo=True):
    """添加 Docker 软件源"""
    print_step(4, 6, "添加 Docker 软件源（阿里云镜像）")
    
    print_progress("正在添加软件源...")
    
    success, codename = run_command(["lsb_release", "-cs"], check=False)
    if not success:
        codename = "jammy"
    codename = codename.strip()
    
    repo_content = f"deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu {codename} stable"
    
    success, output = run_command(
        f'echo "{repo_content}" | sudo tee /etc/apt/sources.list.d/docker.list',
        shell=True,
        use_sudo=False,
        show_output=False
    )
    
    if success:
        print_success(f"软件源添加完成（Ubuntu {codename}）")
        return True
    else:
        print_error(f"软件源添加失败: {output}")
        return False


def install_docker_ce(use_sudo=True):
    """安装 Docker CE"""
    print_step(5, 6, "安装 Docker CE")
    
    print_progress("正在更新包列表...")
    run_command(["apt", "update"], use_sudo=use_sudo, check=False, show_output=False)
    
    packages = ["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]
    
    print_progress("正在安装 Docker CE（约 2-5 分钟）...")
    print("   安装组件:")
    for pkg in packages:
        print(f"   - {pkg}")
    
    cmd = ["apt", "install", "-y"] + packages
    success, output = run_command(cmd, use_sudo=use_sudo, show_output=False)
    
    if success:
        print_success("Docker CE 安装完成")
        return True
    else:
        print_error(f"Docker CE 安装失败: {output}")
        return False


def configure_mirror_accelerator(mirror_url=None, use_sudo=True):
    """配置 Docker 镜像加速器"""
    print_step(6, 6, "配置镜像加速器")
    
    if mirror_url is None:
        mirror_url = "https://2jgearuk.mirror.aliyuncs.com"
    
    print_progress(f"正在配置镜像加速器...")
    print(f"   镜像地址: {mirror_url}")
    
    daemon_json = {"registry-mirrors": [mirror_url]}
    config_content = json.dumps(daemon_json, indent=2)
    
    run_command(["mkdir", "-p", "/etc/docker"], use_sudo=use_sudo, check=False, show_output=False)
    
    success, output = run_command(
        f'echo \'{config_content}\' | sudo tee /etc/docker/daemon.json',
        shell=True,
        use_sudo=False,
        show_output=False
    )
    
    if success:
        print_success("镜像加速器配置完成")
        return True
    else:
        print_warning(f"镜像加速器配置失败: {output}")
        return False


def add_user_to_docker_group():
    """将当前用户添加到 docker 组"""
    print_progress("正在配置用户权限...")
    
    username = os.environ.get("USER", "root")
    
    success, output = run_command(
        ["usermod", "-aG", "docker", username],
        use_sudo=True,
        check=False,
        show_output=False
    )
    
    if success:
        print_success(f"已将用户 {username} 添加到 docker 组")
        print_warning("请执行 'newgrp docker' 或重新登录以生效")
        return True
    else:
        print_warning(f"添加用户到 docker 组失败: {output}")
        return False


def start_docker_service(use_sudo=True):
    """启动 Docker 服务"""
    print_progress("正在启动 Docker 服务...")
    
    run_command(["systemctl", "start", "docker"], use_sudo=use_sudo, check=False, show_output=False)
    run_command(["systemctl", "enable", "docker"], use_sudo=use_sudo, check=False, show_output=False)
    
    success, output = run_command(["systemctl", "status", "docker"], use_sudo=use_sudo, check=False, show_output=False)
    
    if "active (running)" in output or success:
        print_success("Docker 服务已启动")
        return True
    else:
        print_warning("Docker 服务状态检查失败")
        return False


def verify_docker():
    """验证 Docker 安装"""
    print_progress("正在验证 Docker 安装...")
    
    success, output = run_command(["docker", "--version"], check=False, show_output=False)
    if success:
        print(f"   版本: {output.strip()}")
    
    print_progress("运行测试镜像 hello-world...")
    success, output = run_command(["docker", "run", "--rm", "hello-world"], check=False, show_output=False)
    
    if "Hello from Docker" in output:
        print_success("Docker 运行正常")
        return True
    else:
        print_warning("Docker 测试失败，可能需要配置镜像加速器")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Docker 安装工具（中国网络优化版，带进度提示）')
    
    parser.add_argument('--install', action='store_true', help='完整安装 Docker')
    parser.add_argument('--config-mirror', action='store_true', help='配置镜像加速器')
    parser.add_argument('--mirror-url', help='镜像加速器 URL')
    parser.add_argument('--no-user-group', action='store_true', help='不将当前用户添加到 docker 组')
    parser.add_argument('--verify', action='store_true', help='仅验证 Docker 安装')
    
    args = parser.parse_args()
    
    if args.verify:
        return 0 if verify_docker() else 1
    
    if args.install:
        print("\n" + "="*60)
        print("Docker 安装工具（阿里云镜像）")
        print("="*60)
        print("说明: 使用阿里云镜像安装 Docker CE")
        print("时间: 预计 3-5 分钟")
        print("权限: 需要 sudo 权限")
        
        try:
            response = input("\n是否继续? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("用户取消操作")
                return 1
        except EOFError:
            pass
        
        # 执行安装步骤
        remove_old_docker()
        
        if not install_dependencies():
            return 1
        
        if not add_aliyun_key():
            return 1
        
        if not add_docker_repository():
            return 1
        
        if not install_docker_ce():
            return 1
        
        configure_mirror_accelerator(args.mirror_url)
        start_docker_service()
        
        if not args.no_user_group:
            add_user_to_docker_group()
        
        verify_docker()
        
        print("\n" + "="*60)
        print("✅ Docker 安装完成")
        print("="*60)
        print("镜像加速器: 已配置阿里云镜像")
        if not args.no_user_group:
            print("用户组: 请执行 'newgrp docker' 或重新登录")
        return 0
    
    if args.config_mirror:
        print("\n" + "="*60)
        print("配置 Docker 镜像加速器")
        print("="*60)
        
        if configure_mirror_accelerator(args.mirror_url):
            run_command(["systemctl", "daemon-reload"], use_sudo=True, show_output=False)
            run_command(["systemctl", "restart", "docker"], use_sudo=True, show_output=False)
            print_success("镜像加速器配置完成，Docker 服务已重启")
            return 0
        return 1
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print_error(f"错误: {str(e)}")
        sys.exit(1)
