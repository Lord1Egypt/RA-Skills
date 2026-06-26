#!/usr/bin/env python3
"""
开放防火墙端口
"""

import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="开放防火墙端口")
    parser.add_argument("ports", nargs="+", type=int, help="要开放的端口列表")
    
    args = parser.parse_args()
    
    print("="*60)
    print("🔓 开放防火墙端口...")
    print("="*60)
    
    success_count = 0
    for port in args.ports:
        try:
            result = subprocess.run(
                ["iptables", "-I", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "ACCEPT"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ 端口 {port} 已开放")
                success_count += 1
            else:
                print(f"❌ 端口 {port} 开放失败: {result.stderr}")
        except Exception as e:
            print(f"❌ 端口 {port} 开放失败: {e}")
    
    print("="*60)
    print(f"✅ 成功开放 {success_count}/{len(args.ports)} 个端口")
    print("="*60)
    
    if success_count < len(args.ports):
        print("\n💡 提示：如果无法自动开放端口，请手动配置防火墙或云服务器安全组")
        sys.exit(1)

if __name__ == "__main__":
    main()
