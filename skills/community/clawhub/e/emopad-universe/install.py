#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emoPAD Universe - 安装脚本
自动检测并安装所需的Python依赖，并在安装完成后自动启动服务
支持 Linux 和 Windows
"""

import subprocess
import sys
import os
import time
import platform

SYSTEM = platform.system()

REQUIRED_PACKAGES = [
    'mne', 'heartpy', 'neurokit2', 'bleak', 'pyvista', 'pyserial',
    'scipy', 'numpy', 'PyWavelets', 'fastapi', 'uvicorn', 'pillow',
    'requests', 'pyyaml'
]

PID_FILE = os.path.expanduser("~/.config/emopad/emopad.pid")
NEBULA_PID_FILE = os.path.expanduser("~/.config/emopad/nebula.pid")

def check_package(package):
    try:
        import_name = package
        if package == 'PyWavelets':
            import_name = 'pywt'
        elif package == 'pillow':
            import_name = 'PIL'
        elif package == 'pyserial':
            import_name = 'serial'
        __import__(import_name)
        return True
    except ImportError:
        return False

def install_package(package):
    print(f"正在安装 {package}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
        print(f"✅ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package} 安装失败: {e}")
        return False

def is_service_running():
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        if SYSTEM == 'Windows':
            subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'])
            return True
        else:
            os.kill(pid, 0)
            return True
    except (ValueError, OSError, ProcessLookupError, subprocess.CalledProcessError):
        return False

def kill_all_nebula():
    """关闭所有 nebula 和 eog 进程"""
    print("🧹 清理旧进程...")
    if SYSTEM == 'Linux':
        try:
            subprocess.run(['pkill', '-9', '-f', 'python3.*nebula.py'], 
                          capture_output=True, timeout=2)
            subprocess.run(['pkill', '-9', '-f', 'eog.*nebula_latest'], 
                          capture_output=True, timeout=2)
        except:
            pass
    elif SYSTEM == 'Windows':
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/FI', 'WINDOWTITLE eq nebula.py'],
                          capture_output=True)
        except:
            pass
    
    # 清理 PID 文件
    if os.path.exists(NEBULA_PID_FILE):
        try:
            os.remove(NEBULA_PID_FILE)
        except:
            pass
    print("✅ 旧进程已清理")

def start_service():
    """启动 emoPAD 服务"""
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    
    # 先关闭所有旧进程
    kill_all_nebula()
    
    if is_service_running():
        print("emoPAD 服务已经在运行中")
        return True
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    service_script = os.path.join(script_dir, 'emoPAD_service.py')
    
    if not os.path.exists(service_script):
        print(f"❌ 找不到服务脚本: {service_script}")
        return False
    
    print("🚀 启动 emoPAD Universe 服务...")
    
    if SYSTEM == 'Windows':
        process = subprocess.Popen(
            [sys.executable, service_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        process = subprocess.Popen(
            [sys.executable, service_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
    
    time.sleep(3)
    
    try:
        import requests
        response = requests.get(f"http://127.0.0.1:8766/pad", timeout=5)
        if response.status_code == 200:
            with open(PID_FILE, 'w') as f:
                f.write(str(process.pid))
            print(f"✅ emoPAD Universe 服务已启动 (PID: {process.pid})")
            print(f"服务地址: http://127.0.0.1:8766")
            return True
    except Exception:
        pass
    
    print("❌ 服务启动失败")
    return False

def start_nebula():
    """启动 emoNebula"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nebula_script = os.path.join(script_dir, 'nebula.py')
    
    if not os.path.exists(nebula_script):
        print(f"❌ 找不到 nebula 脚本")
        return False
    
    # 确保关闭所有旧 nebula 进程
    kill_all_nebula()
    
    print("🚀 启动 emoNebula（将每5分钟弹出窗口显示情绪星云图）...")
    print("💡 提示: 弹出的图片窗口可以手动关闭")
    
    if SYSTEM == 'Windows':
        subprocess.Popen(
            [sys.executable, nebula_script],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        env = os.environ.copy()
        env['DISPLAY'] = ':1'
        env['XAUTHORITY'] = '/run/user/1000/gdm/Xauthority'
        
        subprocess.Popen(
            [sys.executable, nebula_script],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
    
    time.sleep(2)
    print(f"✅ emoNebula 已启动")
    print(f"🌌 将每 5 分钟弹出窗口显示情绪星云图")
    print(f"📝 日志: ~/.config/emopad/nebula.log")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print(f"emoPAD Universe - 安装与启动 ({SYSTEM})")
    print("=" * 60)
    print()
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("❌ 错误: pip 未安装或不可用")
        sys.exit(1)
    
    print("正在检查依赖...")
    print()
    
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        if check_package(package):
            print(f"✅ {package} 已安装")
        else:
            print(f"⏳ {package} 未安装")
            missing_packages.append(package)
    
    print()
    
    # 安装缺失的包
    if missing_packages:
        print(f"需要安装 {len(missing_packages)} 个包")
        print()
        
        failed_packages = []
        for package in missing_packages:
            if not install_package(package):
                failed_packages.append(package)
        
        print()
        
        if failed_packages:
            print(f"⚠️ 以下包安装失败:")
            for pkg in failed_packages:
                print(f"   - {pkg}")
            print()
            print("请手动安装:")
            print(f"pip install {' '.join(failed_packages)}")
            return 1
    
    print("=" * 60)
    print("🎉 所有依赖已安装！")
    print("=" * 60)
    print()
    
    # 自动启动服务
    if start_service():
        print()
        # 自动启动 emoNebula
        start_nebula()
        print()
        print("🌌 emoPAD Universe 已就绪！")
        print("   服务地址: http://127.0.0.1:8766")
        print("   每 5 分钟将弹出窗口显示情绪星云图")
        print()
        print("💡 使用说明:")
        print("   openclaw emopad status    # 查看当前情绪状态")
        print("   openclaw emopad snapshot  # 手动生成星云图")
        print("   openclaw emopad stop      # 停止服务")
    else:
        print()
        print("⚠️ 服务启动失败，请检查错误信息")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
