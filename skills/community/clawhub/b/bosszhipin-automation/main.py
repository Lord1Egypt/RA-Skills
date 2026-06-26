#!/usr/bin/env python3
"""
Boss 直聘职位沟通自动化 - 函数式接口
所有函数独立可用，通过参数接收配置，松耦合设计
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path

from boss_automation import BossAutomation, load_config


# ==================== 配置管理 ====================

def get_config():
    """获取配置字典"""
    return load_config()


def get_scale(config=None):
    """获取当前缩放倍数"""
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    return auto.scale


# ==================== 日志工具 ====================

def log_info(msg):
    """信息日志"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [INFO] {msg}")


def log_success(msg):
    """成功日志"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [OK] {msg}")


def log_warning(msg):
    """警告日志"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [WARN] {msg}")


def log_error(msg):
    """错误日志"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] {msg}")


def log_step(name):
    """步骤日志"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [STEP] {name}")


# ==================== 目录操作 ====================

def setup_directories(config=None):
    """
    创建必要的目录
    
    参数:
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    dirs = [
        cfg.get('screenshot', {}).get('output_dir', './screenshots'),
        cfg.get('ocr', {}).get('output_dir', './ocr_output'),
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


# ==================== 截图路径生成 ====================

def get_screenshot_path(config=None):
    """
    生成截图保存路径
    
    参数:
        config: 配置字典，不传则自动加载
    
    返回:
        str: 截图完整路径
    """
    cfg = config or get_config()
    sc = cfg.get('screenshot', {})
    timestamp = datetime.now().strftime(sc.get('timestamp_format', '%Y%m%d_%H%M%S'))
    filename = f"{sc.get('filename_prefix', 'job')}_{timestamp}.png"
    
    # 基于脚本所在目录构建路径
    script_dir = Path(__file__).parent
    output_dir = sc.get('output_dir', './screenshots')
    
    # 如果是相对路径，则相对于脚本目录
    output_path = Path(output_dir)
    if not output_path.is_absolute():
        output_path = script_dir / output_dir
    
    return str(output_path / filename)


# ==================== 话术模板 ====================

def load_chat_template(config=None):
    """
    加载话术模板
    
    参数:
        config: 配置字典，不传则自动加载
    
    返回:
        str: 话术内容，文件不存在返回 None
    """
    cfg = config or get_config()
    template_file = cfg.get('chat', {}).get('template_file', 'chat_template.txt')
    template_path = Path(template_file)
    
    if not template_path.exists():
        log_warning(f"话术模板不存在：{template_path}")
        return None
    
    return template_path.read_text(encoding='utf-8')


# ==================== 自动化操作函数 ====================

def create_automation(config=None):
    """
    创建自动化实例
    
    参数:
        config: 配置字典，不传则自动加载
    
    返回:
        BossAutomation: 自动化实例
    """
    cfg = config or get_config()
    return BossAutomation(cfg)


def scroll_job_list(scroll_amount=None, scroll_times=None, config=None):
    """
    滚动职位列表
    
    参数:
        scroll_amount: 滚动像素量，负数为向下，默认取配置
        scroll_times: 滚动次数，默认取配置
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    scroll_config = cfg.get('scroll', {})
    
    # 传参优先，否则从配置读取
    amount = scroll_amount if scroll_amount is not None else scroll_config.get('amount')
    times = scroll_times if scroll_times is not None else scroll_config.get('times')
    
    auto = BossAutomation(cfg)
    log_step("滚动职位列表")
    auto.scroll_job_list(amount, times)


def click_job_item(config=None):
    """
    点击职位
    
    参数:
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    log_step("点击职位")
    auto.click_job_item()


def capture_screenshot(save_path=None, config=None):
    """
    截取职位描述
    
    参数:
        save_path: 保存路径，默认自动生成
        config: 配置字典，不传则自动加载
    
    返回:
        str: 截图保存路径
    """
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    
    path = save_path or get_screenshot_path(cfg)
    
    # 确保目录存在
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    log_step(f"截取职位描述 -> {path}")
    auto.capture_job_description(path)
    log_success(f"截图已保存")
    return path


def click_chat_button(config=None):
    """
    点击立即沟通按钮
    
    参数:
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    log_step("点击立即沟通")
    auto.click_chat_button()


def activate_chat_input(config=None):
    """
    激活聊天输入框
    
    参数:
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    log_step("激活输入框")
    auto.activate_chat_input()


def send_chat_message(text=None, config=None):
    """
    发送聊天消息
    
    参数:
        text: 要发送的文本，不传则加载模板
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    
    message = text or load_chat_template(cfg)
    
    if message:
        log_step(f"发送话术 ({len(message)} 字符)")
        auto.paste_and_send(message)
        log_success("消息已发送")
    else:
        log_warning("无可用话术，请手动输入")


def browser_go_back(config=None):
    """
    浏览器后退
    
    参数:
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    auto = BossAutomation(cfg)
    log_step("返回职位列表")
    auto.browser_go_back()


# ==================== 流程控制函数 ====================

def process_job(config=None):
    """
    处理单个职位的完整流程（串行版本，用于快速启动）
    
    参数:
        config: 配置字典，不传则自动加载
    
    返回:
        bool: 是否成功处理
    """
    cfg = config or get_config()
    
    log_step("开始处理新职位")
    
    # 1. 滚动
    scroll_job_list(config=cfg)
    
    # 2. 点击
    click_job_item(config=cfg)
    
    # 3. 截图
    capture_screenshot(config=cfg)
    
    # 4. 沟通流程（自动执行，无需手动确认）
    log_step("执行沟通流程")
    click_chat_button(config=cfg)
    activate_chat_input(config=cfg)
    send_chat_message(config=cfg)
    browser_go_back(config=cfg)
    
    return True


def run_loop(config=None):
    """
    运行主循环，持续处理职位
    
    参数:
        config: 配置字典，不传则自动加载
    """
    cfg = config or get_config()
    
    print()
    print("=" * 50)
    print("  Boss 直聘职位沟通自动化")
    print(f"  版本：{cfg.get('version', '1.0.0')}")
    print("=" * 50)
    
    coords = cfg.get('coordinates', {})
    log_info(f"目标分辨率：{coords.get('resolution', [2560, 1440])}")
    log_info(f"缩放倍数：{get_scale(cfg):.2f}x")
    log_info(f"目标 URL: {cfg.get('browser', {}).get('url', '')}")
    log_info("按 Ctrl+C 可随时中断")
    
    setup_directories(cfg)
    
    try:
        while True:
            process_job(cfg)
            time.sleep(1)
    except KeyboardInterrupt:
        log_info("流程已中断")


# ==================== 主入口 ====================

if __name__ == '__main__':
    run_loop()
