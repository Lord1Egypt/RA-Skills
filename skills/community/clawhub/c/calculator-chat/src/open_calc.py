#!/usr/bin/env python3
"""
Open Calculator with Number - 在系统计算器上显示数字
用于"计算器聊天"技能：根据中文谐音显示数字（520=我爱你）
"""

import sys
import os

# 设置显示环境（用于虚拟机环境）
if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

import subprocess
import time


def is_calculator_running():
    """检查计算器是否正在运行"""
    try:
        # 使用 pgrep 检查进程，避免直接杀进程
        result = subprocess.run(
            ['pgrep', '-x', 'gnome-calculator'],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except Exception:
        return False


def close_calculator():
    """关闭已打开的计算器"""
    try:
        subprocess.run(
            ['pkill', '-x', 'gnome-calculator'],
            capture_output=True,
            timeout=2
        )
        time.sleep(0.3)
    except Exception:
        pass  # 忽略错误


def open_calculator_with_number(number):
    """
    用 gnome-calculator 打开计算器并预填数字
    
    Args:
        number: 要显示的数字或表达式
    """
    # 先关闭已打开的计算器（确保只有一个实例）
    if is_calculator_running():
        close_calculator()
    
    # 验证输入只包含安全字符
    # 只允许数字和基本运算符
    safe_chars = set('0123456789+-*/.() ')
    if not all(c in safe_chars for c in str(number)):
        print(f"❌ 输入包含不安全字符: {number}")
        return False
    
    try:
        # 打开计算器并预填表达式
        # 使用 --equation 参数安全地传递输入
        subprocess.Popen(
            ['gnome-calculator', '--equation', str(number)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # 脱离父进程
        )
        time.sleep(0.5)  # 等待计算器启动
        print(f"✅ 已打开计算器，显示: {number}")
        return True
        
    except FileNotFoundError:
        print("❌ 错误: 未找到 gnome-calculator，请安装: sudo apt install gnome-calculator")
        return False
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False


def main():
    """主函数"""
    # 默认显示 520（我爱你）
    number = sys.argv[1] if len(sys.argv) > 1 else '520'
    
    # 基本输入验证
    if len(number) > 100:  # 防止过长的输入
        print("❌ 输入过长")
        sys.exit(1)
    
    success = open_calculator_with_number(number)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
