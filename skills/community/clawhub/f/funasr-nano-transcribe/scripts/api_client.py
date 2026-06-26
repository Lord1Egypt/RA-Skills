#!/usr/bin/env python3
"""
Fun-ASR-Nano-2512 API 客户端
用于调用 FastAPI 服务进行转写
"""

import argparse
import requests
import sys
from pathlib import Path

def transcribe_file(api_url, audio_path):
    """调用 API 转写单个文件"""
    
    audio_path = Path(audio_path)
    if not audio_path.exists():
        print(f"❌ 文件不存在: {audio_path}")
        sys.exit(1)
    
    print(f"🎵 正在转写: {audio_path.name}")
    print(f"🌐 API 地址: {api_url}")
    
    try:
        with open(audio_path, 'rb') as f:
            files = {'audio': (audio_path.name, f, 'audio/mpeg')}
            response = requests.post(f"{api_url}/transcribe", files=files, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                text = result['text']
                duration = result.get('duration', 'N/A')
                
                print(f"✅ 转写完成！耗时: {duration}s")
                print("=" * 50)
                print(text)
                print("=" * 50)
                
                return text
            else:
                print(f"❌ 转写失败: {result.get('error', '未知错误')}")
                sys.exit(1)
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务: {api_url}")
        print("请确保服务已启动: ./start_server.sh")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

def start_server_if_needed(skill_dir):
    """自动启动服务"""
    import subprocess
    import time
    
    print("🚀 服务未运行，正在自动启动...")
    
    # 使用 nohup 启动服务
    log_file = "/tmp/funasr_api.log"
    pid_file = "/tmp/funasr_api.pid"
    
    # 激活虚拟环境并启动服务
    cmd = f"""
cd {skill_dir}
source .venv/bin/activate
nohup python scripts/api_server.py > {log_file} 2>&1 &
echo $! > {pid_file}
"""
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    
    print("⏳ 等待服务启动（约 30 秒）...")
    time.sleep(30)
    
    # 检查服务是否启动成功
    if check_health("http://127.0.0.1:11890", silent=True):
        print("✅ 服务启动成功！")
        return True
    else:
        print("❌ 服务启动失败，请查看日志:", log_file)
        return False

def check_health(api_url, silent=False):
    """检查服务健康状态"""
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            if not silent:
                print(f"✅ 服务健康: {response.json()}")
            return True
        else:
            if not silent:
                print(f"⚠️ 服务异常: HTTP {response.status_code}")
            return False
    except:
        if not silent:
            print(f"❌ 无法连接到服务: {api_url}")
        return False

def main():
    parser = argparse.ArgumentParser(description='FunASR API 客户端')
    parser.add_argument('audio_file', nargs='?', help='音频文件路径')
    parser.add_argument('-u', '--url', default='http://127.0.0.1:11890', help='API 地址')
    parser.add_argument('--health', action='store_true', help='检查服务健康状态')
    parser.add_argument('--start-server', action='store_true', help='自动启动服务（如未运行）')
    
    args = parser.parse_args()
    
    if args.health:
        check_health(args.url)
    elif args.audio_file:
        # 转写前检查服务可用性
        if not check_health(args.url, silent=True):
            # 服务不可用
            skill_dir = Path(__file__).parent.parent
            
            if args.start_server:
                # 自动启动服务
                if not start_server_if_needed(skill_dir):
                    sys.exit(1)
            else:
                print(f"❌ 无法连接到服务: {args.url}")
                print("💡 提示: 使用 --start-server 参数自动启动服务")
                print(f"   或手动运行: {skill_dir}/start_server.sh")
                sys.exit(1)
        
        # 服务可用，执行转写
        transcribe_file(args.url, args.audio_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
