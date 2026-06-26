#!/usr/bin/env python3
"""
启动文件下载服务器的主脚本
"""

import argparse
import os
import sys
import subprocess
import time

def main():
    parser = argparse.ArgumentParser(description="启动文件下载服务器")
    parser.add_argument("directory", help="要分享的文件目录路径")
    parser.add_argument("--port", type=int, default=4000, help="服务器端口（默认: 4000）")
    parser.add_argument("--daemon", action="store_true", help="后台运行")
    parser.add_argument("--bind", default="0.0.0.0", help="绑定地址（默认: 0.0.0.0）")
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"❌ 错误：目录不存在: {args.directory}")
        sys.exit(1)
    
    # 切换到目标目录
    os.chdir(args.directory)
    
    print("="*60)
    print("🚀 启动文件下载服务器...")
    print("="*60)
    print(f"📂 目录: {args.directory}")
    print(f"🌐 端口: {args.port}")
    print(f"🔗 绑定: {args.bind}")
    print("="*60)
    
    # 尝试开放防火墙端口
    try:
        result = subprocess.run(
            ["iptables", "-I", "INPUT", "-p", "tcp", "--dport", str(args.port), "-j", "ACCEPT"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ 防火墙端口 {args.port} 已开放")
        else:
            print(f"⚠️  无法自动开放防火墙端口，请手动配置")
    except Exception as e:
        print(f"⚠️  防火墙配置失败: {e}")
    
    # 显示下载链接
    print("\n📥 下载链接:")
    print(f"   主页: http://{args.bind}:{args.port}/")
    print(f"   （如果从外部访问，请使用服务器公网IP）")
    print("="*60)
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "http.server",
        str(args.port),
        "--bind", args.bind
    ]
    
    if args.daemon:
        print("\n🚀 后台启动服务器...")
        # 后台运行
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        print(f"✅ 服务器已在后台启动 (PID: {process.pid})")
        print("\n💡 管理命令:")
        print(f"   查看进程: ps aux | grep '{args.port}'")
        print(f"   停止服务器: pkill -f 'http.server.*{args.port}'")
    else:
        print("\n🚀 前台启动服务器（按 Ctrl+C 停止）...")
        print("")
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n\n👋 服务器已停止")

if __name__ == "__main__":
    main()
