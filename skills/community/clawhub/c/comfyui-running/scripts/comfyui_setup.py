#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI 自动配置脚本
==================

【功能】
    1. 自动检测 ComfyUI 安装路径
    2. 检测 ComfyUI 是否正在运行
    3. 生成/更新 config.json

【用法】
    python comfyui_setup.py

【跨平台支持】
    - Windows: 自动扫描 D:/ E:/ H:/ 等盘符
    - Linux: 检测 /opt/ComfyUI, ~/ComfyUI 等
    - WSL: 检测 /mnt/h/ 等 Windows 盘符
"""
import os
import sys

# 添加父目录到路径，以便导入 lib 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.comfyui_config import (
    detect_and_save_config,
    diagnose_comfyui_installations,
    get_comfyui_root,
    get_comfyui_port,
    get_workflows_dir,
    get_output_dir,
    get_python_path,
    _get_system,
    _is_wsl,
)


def print_header():
    """打印标题"""
    print("=" * 60)
    print("  ComfyUI Running Skill - 自动配置工具")
    print("=" * 60)
    print()


def print_system_info():
    """打印系统信息"""
    system = _get_system()
    is_wsl = _is_wsl()
    
    print(f"[系统信息]")
    print(f"  平台: {system}" + (" (WSL)" if is_wsl else ""))
    print()
    
    if system == "windows" and is_wsl:
        print("  ⚠️ 检测到 WSL 环境，将同时搜索 Windows 盘符")
        print()
    elif system == "windows":
        print("  💻 Windows 环境")
        print()
    elif system == "linux":
        print("  🐧 Linux 环境")
        print()
    elif system == "darwin":
        print("  🍎 macOS 环境")
        print()


def print_current_config():
    """打印当前配置"""
    print("[当前配置]")
    
    root = get_comfyui_root()
    port = get_comfyui_port()
    workflows = get_workflows_dir()
    output = get_output_dir()
    python = get_python_path()
    
    print(f"  ComfyUI 路径: {root or '(未设置)'}")
    print(f"  端口: {port}")
    print(f"  工作流目录: {workflows or '(未设置)'}")
    print(f"  输出目录: {output or '(未设置)'}")
    print(f"  Python: {python or '(未设置)'}")
    print()


def print_detection_results():
    """打印检测结果"""
    print("[检测结果]")
    
    results = diagnose_comfyui_installations()
    
    if not results:
        print("  ❌ 未找到 ComfyUI 安装")
        print()
        print("  请手动配置 config.json 中的 comfyui_root")
        print("  或确保 ComfyUI 正在运行（将自动检测端口）")
        print()
        return False
    
    print(f"  找到 {len(results)} 个 ComfyUI 安装:")
    print()
    
    for i, d in enumerate(results[:5], 1):  # 最多显示5个
        is_running = "✅ 运行中" if d.get('is_running') else "⏸️ 未运行"
        version = d.get('version', 'unknown')
        score = d.get('score', 0)
        
        print(f"  {i}. {d.get('detected_path', 'N/A')}")
        print(f"     版本: {version} | {is_running} | 评分: {score:.1f}")
        print()
    
    return True


def run_auto_setup():
    """运行自动配置"""
    print("[自动配置]")
    print("  正在检测并保存配置...")
    print()
    
    config = detect_and_save_config()
    
    if config:
        print("  ✅ 配置已保存到 config.json")
        print()
        print(f"  comfyui_root: {config.get('comfyui_root')}")
        print(f"  comfyui_port: {config.get('comfyui_port')}")
        print(f"  ui_type: {config.get('ui_type', 'official')}")
        print()
        
        if config.get('_is_running'):
            print("  ✅ ComfyUI 正在运行中")
        else:
            print("  ⚠️ ComfyUI 未运行，将在首次生成时自动启动")
        print()
        
        return True
    else:
        print("  ❌ 自动检测失败")
        print()
        print("  请手动创建 config.json，示例：")
        print()
        print('  {')
        print('    "comfyui_root": "H:/ComfyUI-aki-v3/ComfyUI",')
        print('    "python_path": "H:/ComfyUI-aki-v3/python/python.exe",')
        print('    "comfyui_port": 8188')
        print('  }')
        print()
        return False


def print_next_steps():
    """打印后续步骤"""
    print("[后续步骤]")
    print("  1. 确保 config.json 中的路径正确")
    print("  2. 运行测试生成:")
    print()
    
    system = _get_system()
    if system == "windows":
        print('  python -m lib.comfyui_automation "a cute cat"')
    else:
        print('  python3 -m lib.comfyui_automation "a cute cat"')
    print()
    print("  3. 详细文档请查看 新手教程.md")
    print()


def main():
    """主函数"""
    print_header()
    print_system_info()
    print_current_config()
    
    found = print_detection_results()
    
    if not found:
        # 即使没找到也尝试保存配置（会检测正在运行的）
        run_auto_setup()
    else:
        # 找到多个版本，让用户确认
        response = input("是否使用评分最高的安装进行配置? (Y/n): ").strip().lower()
        if response != 'n':
            run_auto_setup()
    
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
