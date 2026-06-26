#!/usr/bin/env python3
"""
OpenClaw 自动化安全扫描 v2 — nmap + nuclei + 系统审计
"""

import subprocess
import datetime
import re
import os

TARGET = "127.0.0.1"
REPORT_DIR = os.path.expanduser("~/.openclaw/workspace/reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def run(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERROR] {e}"

def get_external_ip():
    out = run("curl -s ifconfig.me", timeout=10).strip()
    return out if re.match(r'^\d+\.\d+\.\d+\.\d+$', out) else "unknown"

def scan_ports(target):
    return run(f"nmap -sS -sV -T4 --top-ports 1000 -oN /dev/stdout {target}", timeout=300)

def scan_vuln(target):
    return run(f"nmap --script vuln -T4 --top-ports 100 -oN /dev/stdout {target}", timeout=300)

def scan_nuclei(target):
    return run(f"nuclei -u http://{target} -severity critical,high,medium -rate-limit 50 -silent 2>&1", timeout=600)

def scan_nuclei_external(ip):
    if ip == "unknown":
        return "跳过（无法获取外网IP）"
    return run(f"nuclei -u http://{ip} -severity critical,high,medium -rate-limit 50 -silent 2>&1", timeout=600)

def scan_ssl(target, port=443):
    return run(f"sslscan --no-colour {target}:{port}", timeout=60)

def check_ssh_config():
    return run("sshd -T 2>/dev/null | grep -iE 'permitrootlogin|passwordauth|pubkeyauth|port|maxauthtries'")

def check_firewall():
    return run("ufw status verbose 2>/dev/null") + "\n" + run("iptables -L -n --line-numbers 2>/dev/null | head -40")

def check_listening_services():
    return run("ss -tlnp")

def check_updates():
    return run("apt list --upgradable 2>/dev/null | head -20")

def check_fail2ban():
    return run("fail2ban-client status 2>/dev/null || echo 'fail2ban not installed'")

def check_users():
    return run("lastlog --time 7 2>/dev/null | head -20")

def assess_severity(port_scan, vuln_scan, nuclei_result):
    issues = []
    dangerous_ports = {21: "FTP", 23: "Telnet", 3306: "MySQL", 6379: "Redis", 27017: "MongoDB", 9200: "Elasticsearch"}
    for port, svc in dangerous_ports.items():
        if re.search(rf'{port}/tcp\s+open', port_scan):
            issues.append(f"🔴 **CRITICAL**: {svc} (port {port}) 对外开放")
    if "VULNERABLE" in vuln_scan.upper():
        vuln_count = vuln_scan.upper().count("VULNERABLE")
        issues.append(f"🔴 **CRITICAL**: nmap 发现 {vuln_count} 个已知漏洞")
    nuclei_lines = [l for l in nuclei_result.strip().splitlines() if l.strip() and not l.startswith("[INF]") and not l.startswith("[WRN]")]
    if nuclei_lines:
        issues.append(f"🔴 **CRITICAL**: nuclei 发现 {len(nuclei_lines)} 个漏洞")
        for l in nuclei_lines[:10]:
            issues.append(f"  - {l.strip()}")
    ssh_cfg = check_ssh_config()
    if "permitrootlogin yes" in ssh_cfg.lower():
        issues.append("🟡 **WARN**: SSH 允许 root 密码登录")
    if "passwordauthentication yes" in ssh_cfg.lower():
        issues.append("🟡 **WARN**: SSH 允许密码登录")
    fw = run("ufw status 2>/dev/null")
    if "inactive" in fw.lower():
        issues.append("🟡 **WARN**: 防火墙未启用")
    f2b = run("fail2ban-client status 2>/dev/null")
    if "not installed" in f2b.lower() or "not found" in f2b.lower():
        issues.append("🟡 **WARN**: fail2ban 未安装")
    if not issues:
        issues.append("🟢 未发现严重问题")
    return issues

def generate_report():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    ext_ip = get_external_ip()

    print(f"[1/8] 端口扫描...")
    port_scan = scan_ports(TARGET)
    print(f"[2/8] nmap 漏洞扫描...")
    vuln_scan = scan_vuln(TARGET)
    print(f"[3/8] nuclei 内网扫描...")
    nuclei_internal = scan_nuclei(TARGET)
    print(f"[4/8] nuclei 外网扫描...")
    nuclei_external = scan_nuclei_external(ext_ip)
    print(f"[5/8] SSL 检查...")
    ssl_scan = scan_ssl(ext_ip, 443) if ext_ip != "unknown" else "跳过"
    print(f"[6/8] 系统安全检查...")
    ssh_cfg = check_ssh_config()
    firewall = check_firewall()
    listeners = check_listening_services()
    print(f"[7/8] 补丁和服务检查...")
    updates = check_updates()
    f2b = check_fail2ban()
    users = check_users()
    print(f"[8/8] 生成报告...")

    all_nuclei = nuclei_internal + "\n" + nuclei_external
    issues = assess_severity(port_scan, vuln_scan, all_nuclei)
    severity_emoji = "🔴" if any("CRITICAL" in i for i in issues) else "🟡" if any("WARN" in i for i in issues) else "🟢"

    report = f"""# {severity_emoji} 安全扫描报告 — {date_str}

**扫描时间**: {time_str}
**目标**: {TARGET} (外网: {ext_ip})
**扫描工具**: nmap + nuclei v3.7 (12669 templates) + sslscan

---

## 风险摘要

{chr(10).join(issues)}

---

## 1. 开放端口 & 服务

```
{port_scan[:3000]}
```

## 2. nmap 漏洞扫描

```
{vuln_scan[:3000]}
```

## 3. Nuclei 漏洞扫描（内网）

```
{nuclei_internal[:3000] if nuclei_internal.strip() else '未发现 critical/high/medium 级别漏洞 ✅'}
```

## 4. Nuclei 漏洞扫描（外网 {ext_ip}）

```
{nuclei_external[:3000] if nuclei_external.strip() else '未发现 critical/high/medium 级别漏洞 ✅'}
```

## 5. SSL/TLS 状态

```
{ssl_scan[:1500]}
```

## 6. SSH 配置

```
{ssh_cfg[:500]}
```

## 7. 防火墙规则

```
{firewall[:1500]}
```

## 8. 监听服务

```
{listeners[:1000]}
```

## 9. 待更新包

```
{updates[:500]}
```

## 10. Fail2Ban 状态

```
{f2b[:500]}
```

## 11. 近 7 天登录记录

```
{users[:500]}
```

---

_报告由 OpenClaw 龙虾参谋自动生成 🦞 | nmap + nuclei + sslscan_
"""

    report_path = os.path.join(REPORT_DIR, f"security-scan-{date_str}.md")
    with open(report_path, "w") as f:
        f.write(report)

    summary = f"""{severity_emoji} **安全扫描完成** — {date_str}

{chr(10).join(issues)}

完整报告: `{report_path}`"""
    print(summary)

    with open(os.path.join(REPORT_DIR, "latest-scan-summary.txt"), "w") as f:
        f.write(summary)

if __name__ == "__main__":
    generate_report()
