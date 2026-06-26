#!/usr/bin/env python3
"""
Node配对助手 - 用于自动配对OpenClaw Node
用法: python node_pair.py
"""
import json
import subprocess
import sys
import time

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def main():
    print("=== OpenClaw Node 配对助手 ===")
    
    # 1. 检查当前状态
    print("\n[1/3] 检查Node状态...")
    stdout, stderr, code = run_cmd("openclaw node status")
    print(stdout)
    
    # 2. 检查是否有pending请求
    print("\n[2/3] 检查配对请求...")
    stdout, stderr, code = run_cmd("openclaw nodes pending")
    print(stdout)
    
    if "No pending" in stdout:
        print("当前没有配对请求，需要先在Gateway上启动配对模式")
        print("\n请运行: openclaw node run --host 127.0.0.1 --port 18789")
        print("然后在另一个终端运行: openclaw nodes pending")
        print("看到pending请求后运行: openclaw nodes approve <requestId>")
    
    # 3. 列出已配对节点
    print("\n[3/3] 已配对节点:")
    stdout, stderr, code = run_cmd("openclaw nodes list")
    print(stdout)

if __name__ == "__main__":
    main()
