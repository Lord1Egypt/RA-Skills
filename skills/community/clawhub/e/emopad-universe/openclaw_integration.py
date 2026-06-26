#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 集成模块
用于 OpenClaw 与 emoPAD Universe 服务的集成
"""

import subprocess
import sys
import os

def install_dependencies():
    """安装依赖"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    install_script = os.path.join(script_dir, 'install.py')
    
    if os.path.exists(install_script):
        subprocess.check_call([sys.executable, install_script])
        return True
    return False

def start_emopad():
    """启动 emoPAD 服务"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cli_script = os.path.join(script_dir, 'emopad_cli.py')
    
    if os.path.exists(cli_script):
        subprocess.check_call([sys.executable, cli_script, 'start'])
        return True
    return False

def stop_emopad():
    """停止 emoPAD 服务"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cli_script = os.path.join(script_dir, 'emopad_cli.py')
    
    if os.path.exists(cli_script):
        subprocess.check_call([sys.executable, cli_script, 'stop'])
        return True
    return False

def get_status():
    """获取 emoPAD 状态"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cli_script = os.path.join(script_dir, 'emopad_cli.py')
    
    if os.path.exists(cli_script):
        subprocess.check_call([sys.executable, cli_script, 'status'])
        return True
    return False
