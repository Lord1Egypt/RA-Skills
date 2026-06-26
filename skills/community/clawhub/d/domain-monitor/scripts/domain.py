#!/usr/bin/env python3
"""
Domain Monitor - 域名监控工具
"""
import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from urllib.parse import urlparse

DATA_FILE = os.path.expanduser("~/.domain_monitor.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"domains": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_whois(domain):
    """获取 WHOIS 信息（简化版）"""
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        info = {}
        for line in result.stdout.split("\n"):
            if "Expiry Date" in line or "Expiration" in line:
                info["expiry"] = line.split(":")[-1].strip()
            elif "Registrar" in line:
                info["registrar"] = line.split(":")[-1].strip()
            elif "Creation Date" in line:
                info["created"] = line.split(":")[-1].strip()
        
        return info
    except:
        return {"error": "无法获取 WHOIS 信息"}

def check_ssl(domain):
    """检查 SSL 证书"""
    try:
        result = subprocess.run(
            ["openssl", "s_client", "-connect", f"{domain}:443", "-servername", domain],
            input="",
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # 提取证书信息
        output = result.stdout
        if "Verify return code" in output:
            return {"status": "valid", "info": "证书有效"}
        
        return {"status": "unknown"}
    except Exception as e:
        return {"status": "error", "info": str(e)}

def cmd_add(args):
    data = load_data()
    domain = args.domain.strip().lower()
    
    # 去除 http:// 和 www.
    domain = domain.replace("https://", "").replace("http://", "").replace("www.", "")
    domain = domain.split("/")[0]
    
    data["domains"][domain] = {
        "added_at": datetime.now().isoformat(),
        "last_check": None,
    }
    
    save_data(data)
    print(f"✅ 已添加域名: {domain}")

def cmd_status(args):
    domain = args.domain.strip().lower()
    
    print(f"🔍 查询: {domain}")
    print("=" * 50)
    
    # WHOIS
    print("\n📋 WHOIS 信息:")
    whois = get_whois(domain)
    for k, v in whois.items():
        if k != "error":
            print(f"   {k}: {v}")
    
    if "error" in whois:
        print(f"   {whois['error']}")
    
    # SSL
    print("\n🔒 SSL 证书:")
    ssl = check_ssl(domain)
    print(f"   状态: {ssl.get('status', 'unknown')}")

def cmd_list(args):
    data = load_data()
    
    if not data["domains"]:
        print("📭 暂无监控域名")
        return
    
    print("📋 监控列表:")
    print("=" * 50)
    
    for domain in data["domains"]:
        info = data["domains"][domain]
        added = info.get("added_at", "")[:10]
        print(f"  • {domain} (添加于 {added})")

def cmd_check(args):
    data = load_data()
    
    if not data["domains"]:
        print("📭 暂无监控域名")
        return
    
    print("🔄 检查所有域名...")
    print("=" * 50)
    
    for domain in list(data["domains"].keys()):
        print(f"\n📌 {domain}:")
        
        whois = get_whois(domain)
        if "error" not in whois and whois.get("expiry"):
            print(f"   到期: {whois['expiry']}")
        
        ssl = check_ssl(domain)
        print(f"   SSL: {ssl.get('status', 'unknown')}")
        
        data["domains"][domain]["last_check"] = datetime.now().isoformat()
    
    save_data(data)
    print("\n✅ 检查完成")

def main():
    parser = argparse.ArgumentParser(description="Domain Monitor")
    subparsers = parser.add_subparsers()
    
    p_add = subparsers.add_parser("add", help="添加域名")
    p_add.add_argument("domain", help="域名")
    p_add.set_defaults(func=cmd_add)
    
    p_status = subparsers.add_parser("status", help="查看状态")
    p_status.add_argument("domain", help="域名")
    p_status.set_defaults(func=cmd_status)
    
    subparsers.add_parser("list", help="列出监控").set_defaults(func=cmd_list)
    subparsers.add_parser("check", help="检查所有").set_defaults(func=cmd_check)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
