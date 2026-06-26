#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emoPAD Universe CLI - 情绪宇宙命令行工具
用于控制 emoPAD 服务的启动、停止和状态查询
"""

import argparse
import sys
import os
import subprocess
import time
import signal
import requests

PID_FILE = os.path.expanduser("~/.config/emopad/emopad.pid")
NEBULA_PID_FILE = os.path.expanduser("~/.config/emopad/nebula.pid")

def is_service_running():
    """检查服务是否正在运行"""
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return True
    except (ValueError, OSError, ProcessLookupError):
        return False

def kill_all_nebula():
    """关闭所有 nebula 和 eog 进程"""
    # 杀死所有 nebula.py 进程
    try:
        subprocess.run(['pkill', '-9', '-f', 'python3.*nebula.py'], 
                      capture_output=True, timeout=2)
    except:
        pass
    
    # 杀死所有 eog 进程（显示 nebula 图片的）
    try:
        subprocess.run(['pkill', '-9', '-f', 'eog.*nebula_latest'], 
                      capture_output=True, timeout=2)
    except:
        pass
    
    # 清理 PID 文件
    for pid_file in [NEBULA_PID_FILE]:
        if os.path.exists(pid_file):
            try:
                os.remove(pid_file)
            except:
                pass

def check_and_install_dependencies():
    """检查并安装依赖"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    install_script = os.path.join(script_dir, 'install.py')
    
    if os.path.exists(install_script):
        print("正在检查并安装依赖...")
        result = subprocess.run([sys.executable, install_script])
        return result.returncode == 0
    return False

def start_service():
    """启动 emoPAD 服务"""
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    
    # 先确保关闭所有旧进程
    stop_service(silent=True)
    
    if is_service_running():
        print("emoPAD 服务已经在运行中")
        return 0
    
    # 检查并安装依赖
    check_and_install_dependencies()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    service_script = os.path.join(script_dir, 'emoPAD_service.py')
    
    if not os.path.exists(service_script):
        print(f"❌ 找不到服务脚本: {service_script}")
        return 1
    
    print("🚀 启动 emoPAD Universe 服务...")
    
    process = subprocess.Popen(
        [sys.executable, service_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True
    )
    
    time.sleep(3)
    
    try:
        response = requests.get(f"http://127.0.0.1:8766/pad", timeout=5)
        if response.status_code == 200:
            with open(PID_FILE, 'w') as f:
                f.write(str(process.pid))
            print(f"✅ emoPAD Universe 服务已启动 (PID: {process.pid})")
            print(f"服务地址: http://127.0.0.1:8766")
            return 0
    except Exception:
        pass
    
    print("❌ 服务启动失败，请检查日志")
    return 1

def stop_service(silent=False):
    """停止 emoPAD 服务"""
    if not silent:
        print("🛑 正在停止 emoPAD Universe...")
    
    # 先关闭所有 nebula 进程
    kill_all_nebula()
    
    # 停止 emoPAD 服务
    if not is_service_running():
        if not silent:
            print("emoPAD 服务未运行")
        # 仍然清理 PID 文件
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except:
                pass
        return 0
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGTERM)
        
        # 等待进程结束
        for _ in range(10):
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except OSError:
                break
        
        os.remove(PID_FILE)
        if not silent:
            print("✅ emoPAD Universe 服务已停止")
        return 0
    except Exception as e:
        if not silent:
            print(f"停止服务时出错: {e}")
        # 强制清理
        try:
            os.kill(pid, signal.SIGKILL)
        except:
            pass
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except:
                pass
        return 0

def get_status():
    """获取当前 PAD 状态"""
    if not is_service_running():
        print("emoPAD 服务未运行")
        return 1
    
    try:
        response = requests.get(f"http://127.0.0.1:8766/pad", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("=" * 50)
            print("🌌 emoPAD Universe - 当前情绪状态")
            print("=" * 50)
            print(f"  Pleasure (愉悦度):  {data['P']:+.3f}")
            print(f"  Arousal (唤醒度):   {data['A']:+.3f}")
            print(f"  Dominance (支配度): {data['D']:+.3f}")
            print(f"  最接近的情绪: {data['closest_emotion']} (距离: {data['distance']:.3f})")
            print()
            print("📡 传感器状态:")
            print(f"  EEG (脑电):   {'✅ 正常' if data['eeg_valid'] else '❌ 未连接'}")
            print(f"  PPG (心率):   {'✅ 正常' if data['ppg_valid'] else '❌ 未连接'}")
            print(f"  GSR (皮肤电): {'✅ 正常' if data['gsr_valid'] else '❌ 未连接'}")
            print("=" * 50)
            return 0
        else:
            print(f"获取状态失败: HTTP {response.status_code}")
            return 1
    except Exception as e:
        print(f"获取状态失败: {e}")
        return 1

def generate_snapshot():
    """手动生成情绪星云图"""
    if not is_service_running():
        print("emoPAD 服务未运行，请先启动服务")
        return 1
    
    try:
        response = requests.get(f"http://127.0.0.1:8766/snapshot", timeout=10)
        if response.status_code == 200:
            output_path = os.path.expanduser("~/.config/emopad/emopad_snapshot.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ 情绪星云图已保存: {output_path}")
            # 自动打开图片
            os.system(f"xdg-open {output_path} &")
            return 0
        else:
            print(f"生成截图失败: HTTP {response.status_code}")
            return 1
    except Exception as e:
        print(f"生成截图失败: {e}")
        return 1

def toggle_nebula():
    """切换 emoNebula 状态（已废弃，现在自动启动）"""
    print("emoNebula 现在随服务自动启动，无需手动切换")
    print("使用 'openclaw emopad stop' 停止服务时会同时停止 emoNebula")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description='emoPAD Universe CLI - 情绪宇宙命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s start           # 启动情绪监测服务（自动关闭旧进程）
  %(prog)s stop            # 停止服务
  %(prog)s status          # 查看当前情绪状态
  %(prog)s snapshot        # 手动生成情绪星云图
        """
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'status', 'snapshot', 'nebula'],
        help='要执行的命令'
    )
    
    args = parser.parse_args()
    
    commands = {
        'start': start_service,
        'stop': stop_service,
        'status': get_status,
        'snapshot': generate_snapshot,
        'nebula': toggle_nebula,
    }
    
    return commands[args.command]()

if __name__ == '__main__':
    sys.exit(main())
