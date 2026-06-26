"""
Fluid Memory - Dream Mode Daemon
梦境守护进程：每天北京时间 6:00 自动整理大脑
"""
import time
import datetime
import subprocess
import os
import sys
import shutil

# 配置
RUN_INTERVAL = 60  # 检查间隔 (秒)
DREAM_HOUR = 6   # 梦境触发时间 (北京时间)
DREAM_MINUTE = 0

def get_python_path():
    """动态查找 Python 路径"""
    # 1. 尝试 CONDA_PREFIX 环境变量
    conda_prefix = os.environ.get('CONDA_PREFIX', '')
    if conda_prefix:
        conda_python = os.path.join(conda_prefix, 'python.exe')
        if os.path.exists(conda_python):
            return conda_python
    
    # 2. 尝试 CONDA 环境变量
    conda = os.environ.get('CONDA', '')
    if conda:
        conda_python = os.path.join(conda, 'python.exe')
        if os.path.exists(conda_python):
            return conda_python
    
    # 3. 尝试常见 conda 安装位置 (用户目录)
    home = os.path.expanduser('~')
    common_paths = [
        os.path.join(home, 'miniconda3', 'python.exe'),
        os.path.join(home, 'anaconda3', 'python.exe'),
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    
    # 4. 尝试系统 PATH 中的 python
    python_cmd = shutil.which('python')
    if python_cmd:
        return python_cmd
    
    # 5. 尝试 py launcher (Windows 内置)
    py_cmd = shutil.which('py')
    if py_cmd:
        return py_cmd
    
    # 6. 找不到则抛出异常
    raise RuntimeError("未找到 Python。请确保已安装 Python 或在 PATH 中。")

# 动态获取 Python 路径
PYTHON_PATH = get_python_path()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAINTENANCE_SCRIPT = os.path.join(SCRIPT_DIR, "maintenance.py")

def is_dream_time():
    """检查是否到了梦境时间 (北京时间 6:00)"""
    # 获取当前北京时间
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    
    return beijing_now.hour == DREAM_HOUR and beijing_now.minute < RUN_INTERVAL / 60

def run_maintenance():
    """执行维护脚本"""
    print(f"[{datetime.datetime.now()}] 🌙 梦境时刻到了，开始整理大脑...")
    try:
        result = subprocess.run(
            [PYTHON_PATH, MAINTENANCE_SCRIPT],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"[ERROR] {result.stderr}")
    except Exception as e:
        print(f"[CRASH] {e}")

def main():
    print(f"[START] 梦境守护进程启动。检查间隔: {RUN_INTERVAL}s")
    print(f"[INFO] 将在北京时间 {DREAM_HOUR}:00 执行梦境整理。")
    
    last_run_date = None
    
    while True:
        now = datetime.datetime.now()
        utc_now = datetime.datetime.utcnow()
        beijing_now = utc_now + datetime.timedelta(hours=8)
        
        # 格式化时间
        time_str = now.strftime("%H:%M:%S")
        beijing_time_str = beijing_now.strftime("%H:%M:%S")
        
        # 检查是否需要执行
        current_date = now.date()
        
        if is_dream_time():
            if last_run_date != current_date:
                print(f"\n[{time_str}] 🧠 检测到梦境时间 (北京时间 {beijing_time_str})")
                run_maintenance()
                last_run_date = current_date
            else:
                # 已执行过，跳过
                pass
        else:
            # 空闲输出 (可选，注释掉以减少噪音)
            # print(f"[IDLE] 当前北京时间: {beijing_time_str}", end="\r")
            pass
        
        time.sleep(RUN_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[STOP] 梦境守护进程已停止。")
