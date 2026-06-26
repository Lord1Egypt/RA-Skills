#!/usr/bin/env python3
"""
Boss 直聘技能 CLI 命令行接口
松耦合函数调用，独立命令执行
"""

import argparse
import subprocess
from pathlib import Path

from boss_automation import load_config, BossAutomation
from main import (
    get_config,
    get_scale,
    setup_directories,
    get_screenshot_path,
    load_chat_template,
    scroll_job_list,
    click_job_item,
    capture_screenshot,
    click_chat_button,
    activate_chat_input,
    send_chat_message,
    browser_go_back,
    process_job,
    run_loop,
    log_info,
    log_success,
    log_warning,
    log_error,
    log_step,
)


def get_ocr_script_path(config=None):
    """获取 OCR 脚本路径"""
    cfg = config or get_config()
    skill_path = cfg.get('ocr', {}).get('skill_path', './skills/ocr-local')
    script = cfg.get('ocr', {}).get('script', 'ocr.js')
    return Path(skill_path) / 'scripts' / script


def show_config():
    """显示当前配置信息"""
    cfg = get_config()
    coords = cfg.get('coordinates', {})
    
    print("\n" + "=" * 50)
    print(" 当前配置信息")
    print("=" * 50)
    print(f" 目标分辨率：{coords.get('resolution', [2560, 1440])}")
    print(f" 缩放倍数：   {coords.get('scale_multiplier', 1.0)}x")
    print(f" 基准分辨率：2560x1440")
    print(f" 职位坐标：   {coords.get('job_start', [888, 320])}")
    print(f" 截图区域：   {coords.get('screenshot', [1100, 300, 1800, 1250])}")
    print(f" 沟通按钮：   {coords.get('chat_button', [1765, 335])}")
    print(f" 输入框：     {coords.get('chat_input', [1500, 1300])}")
    print("-" * 50)
    print(f" 目标 URL:    {cfg.get('browser', {}).get('url', '')}")
    print(f" 匹配阈值：   {cfg.get('matching', {}).get('threshold', 60)}%")
    print(f" 核心技能：   {', '.join(cfg.get('matching', {}).get('core_skills', []))}")
    print(f" 话术模板：   {cfg.get('chat', {}).get('template_file', '')}")
    print(f" 截图目录：   {cfg.get('screenshot', {}).get('output_dir', '')}")
    print("=" * 50 + "\n")


def cmd_test():
    """测试配置和坐标缩放"""
    cfg = get_config()
    scale = get_scale(cfg)
    
    # 获取缩放后的坐标
    auto = BossAutomation(cfg)
    
    print("\n" + "=" * 50)
    print(" 坐标缩放测试结果")
    print("=" * 50)
    print(f"基准分辨率：2560x1440")
    print(f"目标分辨率：{cfg.get('coordinates', {}).get('resolution', [2560, 1440])}")
    print(f"用户倍率：   {cfg.get('coordinates', {}).get('scale_multiplier', 1.0)}x")
    print(f"最终缩放：   {scale:.2f}x")
    print("-" * 50)
    
    orig = cfg.get('coordinates', {})
    print(f"职位点击：   {orig.get('job_start', [888, 320])} -> {auto.job_start}")
    print(f"截图区域：   {orig.get('screenshot', [1100, 300, 1800, 1250])} -> {auto.screenshot_region}")
    print(f"沟通按钮：   {orig.get('chat_button', [1765, 335])} -> {auto.chat_button}")
    print(f"输入框：     {orig.get('chat_input', [1500, 1300])} -> {auto.chat_input}")
    print("=" * 50 + "\n")


def cmd_ocr(image_path):
    """执行 OCR 识别"""
    ocr_script = get_ocr_script_path()
    
    if not ocr_script.exists():
        log_error(f"OCR 脚本不存在：{ocr_script}")
        return
    
    if not Path(image_path).exists():
        log_error(f"图像文件不存在：{image_path}")
        return
    
    log_step(f"执行 OCR: {image_path}")
    
    try:
        result = subprocess.run(
            ['node', str(ocr_script), '--image', image_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(result.stdout)
            log_success("OCR 完成")
        else:
            log_error(f"OCR 失败：{result.stderr}")
    except Exception as e:
        log_error(f"执行 OCR 出错：{e}")


def main():
    """CLI 主入口"""
    parser = argparse.ArgumentParser(
        description='Boss 直聘职位沟通自动化 CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  py cli.py start        # 启动自动处理流程
  py cli.py test         # 测试配置和坐标缩放
  py cli.py config       # 显示当前配置
  py cli.py scroll       # 滚动职位列表
  py cli.py click        # 点击职位
  py cli.py screenshot   # 截图
  py cli.py ocr <img>    # OCR 识别
  py cli.py chat         # 执行沟通
  py cli.py back         # 浏览器后退

独立函数调用示例 (Python):
  from main import *

  # 只执行点击和截图
  click_job_item()
  path = capture_screenshot()

  # 自定义流程
  click_chat_button()
  send_chat_message("自定义消息")
"""
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'test', 'config', 'scroll', 'click', 'screenshot', 'ocr', 'chat', 'back'],
        help='要执行的命令'
    )
    parser.add_argument(
        'args',
        nargs='*',
        help='命令参数（如 ocr 命令需要图像路径）'
    )
    
    args = parser.parse_args()
    
    # 命令分发
    if args.command == 'start':
        run_loop()
    
    elif args.command == 'test':
        cmd_test()
    
    elif args.command == 'config':
        show_config()
    
    elif args.command == 'scroll':
        scroll_job_list()
        log_success("滚动完成")
    
    elif args.command == 'click':
        click_job_item()
        log_success("点击完成")
    
    elif args.command == 'screenshot':
        path = capture_screenshot()
        log_success(f"截图已保存：{path}")
    
    elif args.command == 'ocr':
        if not args.args:
            print("错误：ocr 命令需要提供图像路径")
            print("用法：py cli.py ocr <image_path>")
        else:
            cmd_ocr(args.args[0])
    
    elif args.command == 'chat':
        click_chat_button()
        activate_chat_input()
        send_chat_message()
        log_success("沟通完成")
    
    elif args.command == 'back':
        browser_go_back()
        log_success("返回完成")


if __name__ == '__main__':
    main()
