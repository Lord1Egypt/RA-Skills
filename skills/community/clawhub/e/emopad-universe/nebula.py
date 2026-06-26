#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emoNebula 模块 - 情绪星云自动报告
持续实时监测情绪 PAD，每隔 5 分钟弹出窗口显示情绪星云图
"""

import os
import sys
import time
import json
import signal
import requests
import subprocess
from datetime import datetime

# 设置显示环境变量（强制覆盖，不继承父进程）
os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY'] = '/run/user/1000/gdm/Xauthority'

CONFIG_DIR = os.path.expanduser("~/.config/emopad")
SNAPSHOT_FILENAME = "nebula_latest.png"
PID_FILE = os.path.join(CONFIG_DIR, "nebula.pid")
LOG_FILE = os.path.join(CONFIG_DIR, "nebula.log")

viewer_process = None

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')
    print(log_line)

def get_config():
    return {
        'service_host': '127.0.0.1',
        'service_port': 8766,
        'nebula_interval': 300
    }

def show_image(image_path):
    global viewer_process
    
    if not os.path.exists(image_path):
        log_message(f"图片不存在: {image_path}")
        return False
    
    try:
        # 关闭之前的窗口
        if viewer_process and viewer_process.poll() is None:
            viewer_process.terminate()
            try:
                viewer_process.wait(timeout=2)
            except:
                viewer_process.kill()
        
        # 启动 eog
        viewer_process = subprocess.Popen(
            ['eog', '--new-instance', image_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log_message("已使用 eog 窗口显示图片")
        return True
    except Exception as e:
        log_message(f"显示图片失败: {e}")
        return False

def generate_and_show_report(config):
    host = config.get('service_host', '127.0.0.1')
    port = config.get('service_port', 8766)
    
    try:
        pad_response = requests.get(f"http://{host}:{port}/pad", timeout=5)
        if pad_response.status_code != 200:
            log_message(f"获取 PAD 状态失败: {pad_response.status_code}")
            return False
        
        pad_data = pad_response.json()
        eeg_valid = pad_data.get('eeg_valid', False)
        ppg_valid = pad_data.get('ppg_valid', False)
        gsr_valid = pad_data.get('gsr_valid', False)
        valid_count = sum([eeg_valid, ppg_valid, gsr_valid])
        
        if valid_count < 2:
            log_message("数据不足，跳过本次报告")
            return True
        
        log_message("正在生成情绪星云图...")
        snapshot_response = requests.get(f"http://{host}:{port}/snapshot", timeout=10)
        if snapshot_response.status_code != 200:
            log_message(f"获取截图失败: {snapshot_response.status_code}")
            return False
        
        snapshot_dir = os.path.expanduser("~/.config/emopad/snapshots")
        os.makedirs(snapshot_dir, exist_ok=True)
        snapshot_path = os.path.join(snapshot_dir, SNAPSHOT_FILENAME)
        
        with open(snapshot_path, 'wb') as f:
            f.write(snapshot_response.content)
        
        log_message("截图已保存")
        
        if show_image(snapshot_path):
            log_message("emoNebula 报告已显示")
            return True
        return False
            
    except Exception as e:
        log_message(f"生成报告时出错: {e}")
        return False

def main():
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except:
            pass
    
    config = get_config()
    interval = config.get('nebula_interval', 300)
    
    log_message("=" * 60)
    log_message("emoNebula 已启动")
    log_message(f"显示间隔: {interval // 60} 分钟")
    log_message("=" * 60)
    
    running = True
    
    def signal_handler(signum, frame):
        nonlocal running
        running = False
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    log_message("显示首次报告...")
    generate_and_show_report(config)
    
    last_send_time = time.time()
    
    while running:
        try:
            time.sleep(1)
            current_time = time.time()
            
            if current_time - last_send_time >= interval:
                log_message("显示定时报告...")
                generate_and_show_report(config)
                last_send_time = current_time
                log_message(f"下次显示: {interval // 60} 分钟后")
                
        except Exception as e:
            log_message(f"主循环出错: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
