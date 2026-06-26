#!/usr/bin/env python3
"""
Zsh 和 Oh-My-Zsh 配置脚本（中国网络优化版，带进度提示）

功能：
- 安装 zsh
- 安装 oh-my-zsh（Gitee 镜像）
- 安装常用插件（Gitee 镜像）
- 配置主题
- 设置为默认 shell
"""

import argparse
import os
import sys
import subprocess
import shutil
import re


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


def run_command(cmd, shell=False, check=True, input_text=None, show_output=True):
    """执行命令"""
    try:
        if show_output:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300, input=input_text)
        else:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=300, input=input_text)
        
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)


def check_zsh_installed():
    """检查 zsh 是否已安装"""
    return shutil.which('zsh') is not None


def check_oh_my_zsh_installed():
    """检查 oh-my-zsh 是否已安装"""
    return os.path.exists(os.path.expanduser("~/.oh-my-zsh"))


def install_zsh(use_sudo=False):
    """安装 zsh"""
    total_steps = 2
    
    if check_zsh_installed():
        print_success("zsh 已安装，跳过")
        return True, "已安装"
    
    print_step(1, total_steps, "更新包列表")
    update_cmd = ["apt", "update"]
    if use_sudo:
        update_cmd.insert(0, "sudo")
    
    print_progress("正在更新包列表...")
    run_command(update_cmd, check=False, show_output=False)
    
    print_step(2, total_steps, "安装 zsh")
    install_cmd = ["apt", "install", "-y", "zsh"]
    if use_sudo:
        install_cmd.insert(0, "sudo")
    
    print_progress("正在安装 zsh...")
    success, output = run_command(install_cmd, check=False, show_output=False)
    
    if success:
        print_success("zsh 安装完成")
        return True, "安装成功"
    else:
        print_error(f"zsh 安装失败: {output}")
        return False, f"安装失败"


def install_oh_my_zsh(use_china_mirror=True):
    """安装 oh-my-zsh"""
    if check_oh_my_zsh_installed():
        print_success("oh-my-zsh 已安装，跳过")
        return True, "已安装"
    
    if use_china_mirror:
        print_progress("使用 Gitee 国内镜像安装...")
        install_url = "https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh"
    else:
        print_progress("使用 GitHub 官方源安装...")
        install_url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    
    print_progress("正在下载并安装 oh-my-zsh...")
    
    success, output = run_command(
        ["sh", "-c", f"curl -fsSL {install_url}"],
        shell=True,
        check=False,
        input_text="n\n",
        show_output=False
    )
    
    if check_oh_my_zsh_installed():
        print_success("oh-my-zsh 安装完成")
        return True, "安装成功"
    
    print_error(f"oh-my-zsh 安装失败: {output}")
    return False, f"安装失败"


def install_zsh_plugins(plugins, use_china_mirror=True):
    """安装 zsh 插件"""
    print_progress(f"准备安装插件: {', '.join(plugins)}")
    
    zsh_custom = os.path.expanduser("~/.oh-my-zsh/custom/plugins")
    os.makedirs(zsh_custom, exist_ok=True)
    
    plugin_map = {
        "zsh-autosuggestions": {
            "github": "https://github.com/zsh-users/zsh-autosuggestions",
            "gitee": "https://gitee.com/zsh-users/zsh-autosuggestions"
        },
        "zsh-syntax-highlighting": {
            "github": "https://github.com/zsh-users/zsh-syntax-highlighting",
            "gitee": "https://gitee.com/Annihilater/zsh-syntax-highlighting"
        }
    }
    
    installed = []
    for i, plugin in enumerate(plugins, 1):
        if plugin not in plugin_map:
            print_warning(f"未知插件: {plugin}，跳过")
            continue
        
        plugin_dir = os.path.join(zsh_custom, plugin)
        
        if os.path.exists(plugin_dir):
            print_success(f"[{i}/{len(plugins)}] {plugin} 已存在")
            installed.append(plugin)
            continue
        
        # 选择镜像
        if use_china_mirror and "gitee" in plugin_map[plugin]:
            url = plugin_map[plugin]["gitee"]
            source = "Gitee"
        else:
            url = plugin_map[plugin]["github"]
            source = "GitHub"
        
        print_progress(f"[{i}/{len(plugins)}] 正在从 {source} 克隆 {plugin}...")
        
        success, output = run_command(["git", "clone", url, plugin_dir], check=False, show_output=False)
        
        if success:
            print_success(f"[{i}/{len(plugins)}] {plugin} 安装完成")
            installed.append(plugin)
        else:
            print_error(f"[{i}/{len(plugins)}] {plugin} 安装失败")
    
    return installed


def configure_zshrc(plugins, theme="robbyrussell"):
    """配置 .zshrc"""
    print_progress("正在配置 .zshrc...")
    
    zshrc_path = os.path.expanduser("~/.zshrc")
    
    if not os.path.exists(zshrc_path):
        template_path = os.path.expanduser("~/.oh-my-zsh/templates/zshrc.zsh-template")
        if os.path.exists(template_path):
            shutil.copy2(template_path, zshrc_path)
            print_success("已创建 .zshrc")
        else:
            print_error("找不到模板文件")
            return False
    
    with open(zshrc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改主题
    content = re.sub(r'ZSH_THEME="[^"]*"', f'ZSH_THEME="{theme}"', content)
    print_success(f"已设置主题: {theme}")
    
    # 修改插件
    if plugins:
        plugins_str = ' '.join(plugins)
        content = re.sub(r'plugins=\([^)]*\)', f'plugins=({plugins_str})', content)
        print_success(f"已配置插件: {plugins_str}")
    
    with open(zshrc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def set_default_shell():
    """设置 zsh 为默认 shell"""
    current_shell = os.environ.get('SHELL', '')
    
    if 'zsh' in current_shell:
        print_success("zsh 已是默认 shell")
        return True, "已是默认 shell"
    
    zsh_path = shutil.which('zsh')
    if not zsh_path:
        return False, "找不到 zsh 路径"
    
    print_progress(f"正在设置默认 shell...")
    
    success, output = run_command(["chsh", "-s", zsh_path], check=False, show_output=False)
    
    if success:
        print_success("已设置 zsh 为默认 shell")
        print_warning("需要注销并重新登录后生效")
        return True, "设置成功"
    
    print_warning("设置默认 shell 可能需要手动执行: chsh -s $(which zsh)")
    return True, "已提示"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Zsh 和 Oh-My-Zsh 配置工具（带进度提示）')
    
    parser.add_argument('--use-sudo', action='store_true', help='使用 sudo 权限')
    parser.add_argument('--install-zsh', action='store_true', help='安装 zsh')
    parser.add_argument('--install-oh-my-zsh', action='store_true', help='安装 oh-my-zsh')
    parser.add_argument('--plugins', help='插件列表（空格分隔）')
    parser.add_argument('--theme', default='robbyrussell', help='主题名称')
    parser.add_argument('--china-mirror', action='store_true', default=True, help='使用国内镜像')
    parser.add_argument('--no-china-mirror', action='store_true', help='不使用国内镜像')
    parser.add_argument('--set-default-shell', action='store_true', help='设置默认 shell')
    parser.add_argument('--all', action='store_true', help='完整配置')
    
    args = parser.parse_args()
    
    use_china_mirror = not args.no_china_mirror
    
    if args.all:
        args.install_zsh = True
        args.install_oh_my_zsh = True
        args.set_default_shell = True
        if not args.plugins:
            args.plugins = "git zsh-autosuggestions zsh-syntax-highlighting"
    
    # sudo 提示
    if args.use_sudo and args.install_zsh:
        print("\n" + "="*60)
        print("Zsh 配置工具")
        print("="*60)
        print("说明: 安装 zsh 和 oh-my-zsh")
        print("时间: 约 1-2 分钟")
        print("权限: 安装 zsh 需要 sudo 权限")
        
        try:
            response = input("\n是否继续? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("用户取消操作")
                return 1
        except EOFError:
            pass
    
    total_steps = 0
    current_step = 0
    
    if args.install_zsh:
        total_steps += 1
    if args.install_oh_my_zsh:
        total_steps += 1
    if args.plugins:
        total_steps += 1
    if args.set_default_shell:
        total_steps += 1
    
    success = True
    
    # 安装 zsh
    if args.install_zsh:
        current_step += 1
        print_step(current_step, total_steps, "安装 zsh")
        if not install_zsh(args.use_sudo)[0]:
            success = False
    
    # 安装 oh-my-zsh
    if args.install_oh_my_zsh and success:
        current_step += 1
        print_step(current_step, total_steps, "安装 oh-my-zsh")
        if not install_oh_my_zsh(use_china_mirror)[0]:
            success = False
    
    # 安装插件
    if args.plugins and success:
        current_step += 1
        print_step(current_step, total_steps, "安装插件")
        plugins = args.plugins.split()
        installed = install_zsh_plugins(plugins, use_china_mirror)
        if installed:
            configure_zshrc(installed, args.theme)
    
    # 设置默认 shell
    if args.set_default_shell:
        current_step += 1
        print_step(current_step, total_steps, "设置默认 shell")
        set_default_shell()
    
    if success:
        print("\n" + "="*60)
        print("✅ Zsh 配置完成")
        print("="*60)
        if args.set_default_shell:
            print("需要注销并重新登录后生效")
        else:
            print("执行 'zsh' 或重新打开终端体验新配置")
        return 0
    else:
        print_error("配置过程中出现错误")
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
