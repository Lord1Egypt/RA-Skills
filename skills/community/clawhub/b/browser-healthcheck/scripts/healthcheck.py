#!/usr/bin/env python3
"""
Browser Health Check Script
诊断 OpenClaw Browser 工具状态，提供修复建议。

用法：
    python healthcheck.py --profile openclaw
    python healthcheck.py --profile user --fix
"""

import argparse
import json
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_ok(msg):
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.RESET}")

def print_fail(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.RESET}")

def check_port_available(port):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            return True
    except OSError:
        return False

def check_port_listening(port):
    """检查端口是否有服务监听"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect(('127.0.0.1', port))
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def check_cdp_http(port):
    """检查 CDP HTTP 端点是否响应"""
    try:
        url = f"http://127.0.0.1:{port}/json/version"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return True, data
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return False, None

def check_config():
    """检查 OpenClaw 配置"""
    config_path = Path.home() / '.openclaw' / 'openclaw.json'
    
    if not config_path.exists():
        print_error(f"Config file not found: {config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            # 使用 json5 解析（如果可用），否则用 json
            try:
                import json5
                config = json5.load(f)
            except ImportError:
                # 手动移除注释和尾随逗号
                content = f.read()
                content = '\n'.join(line for line in content.split('\n') 
                                   if not line.strip().startswith('//'))
                config = json.loads(content)
        
        browser_config = config.get('browser', {})
        print_ok(f"Browser enabled: {browser_config.get('enabled', False)}")
        print_ok(f"Default profile: {browser_config.get('defaultProfile', 'not set')}")
        
        return browser_config
    except Exception as e:
        print_error(f"Failed to parse config: {e}")
        return None

def find_chrome_process(port):
    """查找占用指定端口的 Chrome 进程"""
    try:
        # Windows: netstat -ano | findstr "9223"
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    return int(pid)
    except Exception:
        pass
    
    return None

def healthcheck(profile, fix=False):
    """执行健康检查"""
    print(f"\n{Colors.BOLD}Browser Health Check{Colors.RESET}")
    print(f"Profile: {profile}\n")
    
    issues = []
    
    # 1. 检查配置
    config = check_config()
    if not config:
        issues.append("配置文件问题")
        return False, issues
    
    # 获取端口
    profiles = config.get('profiles', {})
    profile_config = profiles.get(profile, {})
    port = profile_config.get('cdpPort', 9223 if profile == 'openclaw' else 9222)
    
    print_ok(f"CDP port: {port}")
    
    # 2. 检查端口状态
    if check_port_listening(port):
        print_ok(f"Port {port} is listening")
    else:
        print_warn(f"Port {port} is not listening")
        issues.append(f"端口 {port} 未监听")
    
    # 3. 检查 CDP HTTP
    cdp_ok, cdp_data = check_cdp_http(port)
    if cdp_ok:
        print_ok(f"CDP HTTP endpoint responding")
        if cdp_data:
            print_ok(f"Browser: {cdp_data.get('Browser', 'unknown')}")
    else:
        print_error(f"CDP HTTP endpoint not responding")
        issues.append("CDP HTTP 无响应")
    
    # 4. 检查端口冲突
    if not check_port_available(port) and not check_port_listening(port):
        pid = find_chrome_process(port)
        if pid:
            print_warn(f"Port {port} occupied by process {pid}")
            issues.append(f"端口被进程 {pid} 占用")
            
            if fix:
                print(f"Attempting to kill process {pid}...")
                try:
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                                 check=True, capture_output=True)
                    print_ok(f"Process {pid} killed")
                    time.sleep(2)
                except subprocess.CalledProcessError as e:
                    print_error(f"Failed to kill process: {e}")
    
    # 5. 总结
    print()
    if issues:
        print_fail(f"Browser health check failed")
        print("\nIssues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\nSuggested fixes:")
        if "端口未监听" in str(issues):
            print("  • Run: browser(action=start, profile='openclaw')")
        if "端口被进程" in str(issues):
            print("  • Run: taskkill /F /PID <pid>")
            print("  • Or: openclaw gateway restart")
        if "CDP HTTP 无响应" in str(issues):
            print("  • Run: openclaw gateway restart")
            print("  • Wait 5 seconds and try again")
        
        return False, issues
    else:
        print_success("Browser health check passed")
        return True, []

def main():
    parser = argparse.ArgumentParser(description='Browser Health Check')
    parser.add_argument('--profile', default='openclaw', 
                       choices=['openclaw', 'user'],
                       help='Browser profile to check')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix issues automatically')
    
    args = parser.parse_args()
    
    passed, issues = healthcheck(args.profile, args.fix)
    
    sys.exit(0 if passed else 1)

if __name__ == '__main__':
    main()
