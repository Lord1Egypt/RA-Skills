#!/usr/bin/env python3
"""
Domain Monitor - 域名监控工具
监控域名到期时间、WHOIS 信息变化、SSL 证书状态。适合站长和域名投资者。
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from urllib.parse import urlparse

DATA_FILE = os.path.expanduser("~/.domain_monitor.json")


def load_data():
    """加载监控数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"domains": {}}


def save_data(data):
    """保存监控数据"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_whois(domain):
    """获取 WHOIS 信息"""
    try:
        result = subprocess.run(
            ["whois", domain], capture_output=True, text=True, timeout=10
        )

        info = {}
        for line in result.stdout.split("\n"):
            line = line.strip()
            if not line or ":" not in line:
                continue

            # 提取关键信息
            if any(x in line.lower() for x in ["expiry", "expiration", "expire"]):
                info["expiry"] = line.split(":", 1)[-1].strip()
            elif "registrar" in line.lower():
                info["registrar"] = line.split(":", 1)[-1].strip()
            elif any(x in line.lower() for x in ["creation", "registered", "register"]):
                info["created"] = line.split(":", 1)[-1].strip()
            elif "updated" in line.lower():
                info["updated"] = line.split(":", 1)[-1].strip()
            elif "name server" in line.lower() or "nameserver" in line.lower():
                if "dns" not in info:
                    info["dns"] = []
                dns = line.split(":", 1)[-1].strip()
                if dns and dns not in info["dns"]:
                    info["dns"].append(dns)

        return info if info else {"error": "无法获取 WHOIS 信息"}
    except FileNotFoundError:
        return {"error": "未安装 whois 命令，请运行：brew install whois"}
    except subprocess.TimeoutExpired:
        return {"error": "WHOIS 查询超时"}
    except Exception as e:
        return {"error": f"WHOIS 查询失败：{str(e)}"}


def check_ssl(domain):
    """检查 SSL 证书"""
    try:
        result = subprocess.run(
            ["openssl", "s_client", "-connect", f"{domain}:443", "-servername", domain],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = result.stdout
        cert_info = {"status": "unknown"}

        # 提取证书信息
        if "Certificate chain" in output or "subject=" in output:
            cert_info["status"] = "valid"

            # 提取证书主题
            for line in output.split("\n"):
                if "s:" in line or "subject=" in line:
                    cert_info["subject"] = line.strip()
                if "i:" in line or "issuer=" in line:
                    cert_info["issuer"] = line.strip()

            # 检查证书有效期
            verify_result = subprocess.run(
                ["openssl", "x509", "-noout", "-dates"],
                input=output,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if verify_result.stdout:
                for line in verify_result.stdout.split("\n"):
                    if "notAfter=" in line:
                        cert_info["expires"] = line.split("=", 1)[1].strip()
                    elif "notBefore=" in line:
                        cert_info["valid_from"] = line.split("=", 1)[1].strip()
        elif "verify return code" in output:
            cert_info["status"] = "valid"
        else:
            cert_info["status"] = "invalid_or_not_found"

        return cert_info
    except FileNotFoundError:
        return {"status": "error", "info": "未安装 openssl 命令"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "info": "SSL 检查超时"}
    except Exception as e:
        return {"status": "error", "info": str(e)}


def calculate_days_to_expiry(expiry_str):
    """计算距离到期还有多少天"""
    if not expiry_str:
        return None

    # 尝试多种日期格式
    date_formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%SZ",
        "%d-%b-%Y",
        "%d %b %Y",
        "%B %d %Y",
        "%Y/%m/%d",
    ]

    for fmt in date_formats:
        try:
            expiry_date = datetime.strptime(expiry_str, fmt)
            delta = expiry_date - datetime.now()
            return delta.days
        except ValueError:
            continue

    return None


def cmd_add(args):
    """添加域名到监控"""
    data = load_data()
    domain = args.domain.strip().lower()

    # 去除协议和前缀
    domain = domain.replace("https://", "").replace("http://", "").replace("www.", "")
    domain = domain.split("/")[0].split(":")[0]

    if domain in data["domains"]:
        print(f"⚠️  域名已存在：{domain}")
        return

    # 获取初始 WHOIS 信息
    print(f"🔍 正在获取 {domain} 的初始信息...")
    whois = get_whois(domain)

    data["domains"][domain] = {
        "added_at": datetime.now().isoformat(),
        "last_check": None,
        "initial_whois": whois,
        "last_whois": whois,
        "alerts": [],
    }

    save_data(data)

    print(f"✅ 已添加域名：{domain}")
    if "expiry" in whois:
        days = calculate_days_to_expiry(whois["expiry"])
        if days:
            status = "⚠️  " if days < 30 else "✅ "
            print(f"   {status}到期时间：{whois['expiry']} (剩余 {days} 天)")
        else:
            print(f"   到期时间：{whois['expiry']}")


def cmd_status(args):
    """查看域名状态"""
    domain = args.domain.strip().lower()

    print(f"🔍 查询：{domain}")
    print("=" * 60)

    # WHOIS
    print("\n📋 WHOIS 信息:")
    whois = get_whois(domain)
    if "error" in whois:
        print(f"   ❌ {whois['error']}")
    else:
        for key, value in whois.items():
            if key == "dns":
                print(f"   DNS 服务器：{', '.join(value)}")
            elif key != "error":
                label = {
                    "expiry": "到期时间",
                    "registrar": "注册商",
                    "created": "注册日期",
                    "updated": "更新日期",
                }.get(key, key)
                print(f"   {label}: {value}")

        # 计算到期天数
        if "expiry" in whois:
            days = calculate_days_to_expiry(whois["expiry"])
            if days:
                if days < 0:
                    print(f"   ❌ 已过期 {abs(days)} 天")
                elif days < 30:
                    print(f"   ⚠️  即将到期：剩余 {days} 天")
                elif days < 90:
                    print(f"   ⚠️  注意：剩余 {days} 天")
                else:
                    print(f"   ✅ 正常：剩余 {days} 天")

    # SSL
    print("\n🔒 SSL 证书状态:")
    ssl = check_ssl(domain)
    if ssl.get("status") == "valid":
        print(f"   ✅ 证书有效")
        if "subject" in ssl:
            print(f"   主题：{ssl['subject']}")
        if "issuer" in ssl:
            print(f"   颁发者：{ssl['issuer']}")
        if "expires" in ssl:
            print(f"   证书到期：{ssl['expires']}")
    elif ssl.get("status") == "invalid_or_not_found":
        print(f"   ⚠️  未找到有效 SSL 证书")
    else:
        print(f"   ❌ {ssl.get('info', '检查失败')}")

    # 监控状态
    data = load_data()
    if domain in data["domains"]:
        info = data["domains"][domain]
        print(f"\n📊 监控状态:")
        print(f"   添加时间：{info.get('added_at', 'N/A')[:10]}")
        print(
            f"   最后检查：{info.get('last_check', 'N/A')[:10] if info.get('last_check') else '从未'}"
        )
        if info.get("alerts"):
            print(f"   历史告警：{len(info['alerts'])} 条")


def cmd_list(args):
    """列出所有监控域名"""
    data = load_data()

    if not data["domains"]:
        print("📭 暂无监控域名")
        print("\n💡 使用以下命令添加域名:")
        print("   python3 scripts/domain_monitor.py add example.com")
        return

    print("📋 监控列表:")
    print("=" * 60)
    print(f"{'域名':<30} {'添加日期':<12} {'最后检查':<12} {'状态'}")
    print("-" * 60)

    for domain in sorted(data["domains"].keys()):
        info = data["domains"][domain]
        added = info.get("added_at", "")[:10]
        last_check = (
            info.get("last_check", "")[:10] if info.get("last_check") else "从未"
        )

        # 检查状态
        whois = info.get("last_whois", {})
        expiry = whois.get("expiry", "")
        days = calculate_days_to_expiry(expiry) if expiry else None

        if days and days < 0:
            status = "❌ 已过期"
        elif days and days < 30:
            status = f"⚠️  {days}天"
        elif days and days < 90:
            status = f"⚠️  {days}天"
        else:
            status = "✅ 正常"

        print(f"{domain:<30} {added:<12} {last_check:<12} {status}")

    print("-" * 60)
    print(f"共 {len(data['domains'])} 个域名")


def cmd_check(args):
    """检查所有监控域名"""
    data = load_data()

    if not data["domains"]:
        print("📭 暂无监控域名")
        return

    print("🔄 检查所有域名...")
    print("=" * 60)

    alerts = []

    for domain in list(data["domains"].keys()):
        print(f"\n📌 {domain}:")

        # WHOIS 检查
        whois = get_whois(domain)
        if "error" not in whois and whois.get("expiry"):
            print(f"   到期：{whois['expiry']}")
            days = calculate_days_to_expiry(whois["expiry"])
            if days:
                if days < 0:
                    print(f"   ❌ 已过期 {abs(days)} 天")
                    alerts.append(f"{domain} 已过期 {abs(days)} 天")
                elif days < 30:
                    print(f"   ⚠️  剩余 {days} 天")
                    alerts.append(f"{domain} 即将到期 (剩余{days}天)")
                else:
                    print(f"   ✅ 剩余 {days} 天")

        # SSL 检查
        ssl = check_ssl(domain)
        ssl_status = ssl.get("status", "unknown")
        if ssl_status == "valid":
            print(f"   SSL: ✅ 有效")
        elif ssl_status == "invalid_or_not_found":
            print(f"   SSL: ⚠️  无效或未找到")
        else:
            print(f"   SSL: ❌ {ssl.get('info', '检查失败')}")

        # 更新监控数据
        data["domains"][domain]["last_check"] = datetime.now().isoformat()
        data["domains"][domain]["last_whois"] = whois

        # 检查 WHOIS 变化
        initial = data["domains"][domain].get("initial_whois", {})
        if initial.get("registrar") and whois.get("registrar"):
            if initial["registrar"] != whois["registrar"]:
                alert = f"{domain} 注册商变更：{initial['registrar']} → {whois['registrar']}"
                alerts.append(alert)
                print(f"   ⚠️  {alert}")

    save_data(data)

    # 显示告警汇总
    if alerts:
        print("\n" + "=" * 60)
        print("🚨 告警汇总:")
        for alert in alerts:
            print(f"   • {alert}")

    print("\n✅ 检查完成")


def cmd_remove(args):
    """从监控中移除域名"""
    data = load_data()
    domain = args.domain.strip().lower()

    if domain not in data["domains"]:
        print(f"❌ 域名不在监控列表中：{domain}")
        return

    confirm = input(f"确认要移除域名 {domain} 的监控吗？(y/N): ")
    if confirm.lower() != "y":
        print("已取消")
        return

    del data["domains"][domain]
    save_data(data)
    print(f"✅ 已移除域名：{domain}")


def cmd_history(args):
    """查看域名监控历史"""
    data = load_data()
    domain = args.domain.strip().lower()

    if domain not in data["domains"]:
        print(f"❌ 域名不在监控列表中：{domain}")
        return

    info = data["domains"][domain]

    print(f"📊 {domain} 监控历史:")
    print("=" * 60)
    print(f"添加时间：{info.get('added_at', 'N/A')}")
    print(f"最后检查：{info.get('last_check', 'N/A')}")

    if info.get("initial_whois"):
        print("\n初始 WHOIS:")
        for k, v in info["initial_whois"].items():
            if k != "dns":
                print(f"   {k}: {v}")
            else:
                print(f"   DNS: {', '.join(v)}")

    if info.get("last_whois"):
        print("\n最新 WHOIS:")
        for k, v in info["last_whois"].items():
            if k != "dns":
                print(f"   {k}: {v}")
            else:
                print(f"   DNS: {', '.join(v)}")

    if info.get("alerts"):
        print(f"\n历史告警 ({len(info['alerts'])} 条):")
        for alert in info["alerts"][-10:]:  # 显示最近 10 条
            print(f"   • {alert}")


def main():
    parser = argparse.ArgumentParser(
        description="Domain Monitor - 域名监控工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/domain_monitor.py add example.com          添加域名监控
  python3 scripts/domain_monitor.py status example.com       查看域名状态
  python3 scripts/domain_monitor.py list                     列出所有监控
  python3 scripts/domain_monitor.py check                    检查所有域名
  python3 scripts/domain_monitor.py remove example.com       移除域名监控
  python3 scripts/domain_monitor.py history example.com      查看监控历史
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # add 命令
    p_add = subparsers.add_parser("add", help="添加域名到监控")
    p_add.add_argument("domain", help="域名")
    p_add.set_defaults(func=cmd_add)

    # status 命令
    p_status = subparsers.add_parser("status", help="查看域名状态")
    p_status.add_argument("domain", help="域名")
    p_status.set_defaults(func=cmd_status)

    # list 命令
    subparsers.add_parser("list", help="列出所有监控域名")

    # check 命令
    subparsers.add_parser("check", help="检查所有监控域名")

    # remove 命令
    p_remove = subparsers.add_parser("remove", help="移除域名监控")
    p_remove.add_argument("domain", help="域名")
    p_remove.set_defaults(func=cmd_remove)

    # history 命令
    p_history = subparsers.add_parser("history", help="查看域名监控历史")
    p_history.add_argument("domain", help="域名")
    p_history.set_defaults(func=cmd_history)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if hasattr(args, "func"):
        args.func(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "check":
        cmd_check(args)


if __name__ == "__main__":
    main()
