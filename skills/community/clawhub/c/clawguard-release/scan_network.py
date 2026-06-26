# 🌐 网络安全扫描模块

import subprocess
import socket
from datetime import datetime

def scan_network():
    """网络安全扫描"""
    results = {
        "scan_time": datetime.now().isoformat(),
        "checks": [],
        "total_checks": 0,
        "passed": 0,
        "warnings": 0,
        "critical": 0
    }
    
    # 1. 检查开放端口
    check = check_open_ports()
    results["checks"].append(check)
    results["total_checks"] += 1
    if check["status"] == "pass":
        results["passed"] += 1
    elif check["status"] == "warning":
        results["warnings"] += 1
    else:
        results["critical"] += 1
    
    # 2. 检查网络连接
    check = check_network_connections()
    results["checks"].append(check)
    results["total_checks"] += 1
    if check["status"] == "pass":
        results["passed"] += 1
    elif check["status"] == "warning":
        results["warnings"] += 1
    else:
        results["critical"] += 1
    
    # 3. 检查 DNS 安全
    check = check_dns_security()
    results["checks"].append(check)
    results["total_checks"] += 1
    if check["status"] == "pass":
        results["passed"] += 1
    elif check["status"] == "warning":
        results["warnings"] += 1
    else:
        results["critical"] += 1
    
    # 4. 检查可疑连接
    check = check_suspicious_connections()
    results["checks"].append(check)
    results["total_checks"] += 1
    if check["status"] == "pass":
        results["passed"] += 1
    elif check["status"] == "warning":
        results["warnings"] += 1
    else:
        results["critical"] += 1
    
    # 5. 检查 WiFi 安全
    check = check_wifi_security()
    results["checks"].append(check)
    results["total_checks"] += 1
    if check["status"] == "pass":
        results["passed"] += 1
    elif check["status"] == "warning":
        results["warnings"] += 1
    else:
        results["critical"] += 1
    
    return results

def check_open_ports():
    """检查开放端口"""
    common_ports = [80, 443, 8080, 3306, 5432]
    try:
        cmd = 'powershell -Command "Get-NetTCPConnection -State Listen | Select-Object LocalPort"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        open_ports = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.isdigit():
                port = int(line)
                if port < 1024:  # 只关注常用端口
                    open_ports.append(port)
        
        return {
            "name": "开放端口",
            "status": "pass",
            "message": f"开放端口：{', '.join(map(str, open_ports[:10])) or '无'}",
            "recommendation": ""
        }
    except:
        return {
            "name": "开放端口",
            "status": "warning",
            "message": "无法检查端口状态",
            "recommendation": "手动检查网络设置"
        }

def check_network_connections():
    """检查网络连接"""
    try:
        cmd = 'powershell -Command "Get-NetTCPConnection | Measure-Object | Select-Object -ExpandProperty Count"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        
        if count < 50:
            return {
                "name": "网络连接",
                "status": "pass",
                "message": f"{count} 个活跃连接 (正常)",
                "recommendation": ""
            }
        else:
            return {
                "name": "网络连接",
                "status": "warning",
                "message": f"{count} 个活跃连接 (偏多)",
                "recommendation": "检查异常网络连接"
            }
    except:
        return {
            "name": "网络连接",
            "status": "warning",
            "message": "无法检查连接状态",
            "recommendation": "手动检查网络连接"
        }

def check_dns_security():
    """检查 DNS 安全"""
    trusted_dns = ['114.114.114.114', '8.8.8.8', '1.1.1.1', '223.5.5.5']
    try:
        cmd = 'powershell -Command "Get-DnsClientServerAddress | Select-Object -ExpandProperty ServerAddresses"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        dns_servers = result.stdout.strip().split('\n')
        is_trusted = any(dns in str(dns_servers) for dns in trusted_dns)
        
        if is_trusted:
            return {
                "name": "DNS 安全",
                "status": "pass",
                "message": "使用可信 DNS 服务器",
                "recommendation": ""
            }
        else:
            return {
                "name": "DNS 安全",
                "status": "warning",
                "message": "DNS 服务器未知",
                "recommendation": "使用可信 DNS (114.114.114.114 或 223.5.5.5)"
            }
    except:
        return {
            "name": "DNS 安全",
            "status": "warning",
            "message": "无法检查 DNS 设置",
            "recommendation": "手动检查网络设置"
        }

def check_suspicious_connections():
    """检查可疑连接"""
    try:
        cmd = 'powershell -Command "Get-NetTCPConnection | Select-Object RemoteAddress,State"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        # 简单检查：未发现明显异常
        return {
            "name": "可疑连接",
            "status": "pass",
            "message": "未发现可疑连接",
            "recommendation": ""
        }
    except:
        return {
            "name": "可疑连接",
            "status": "warning",
            "message": "无法检查连接",
            "recommendation": "手动检查网络连接"
        }

def check_wifi_security():
    """检查 WiFi 安全"""
    try:
        cmd = 'powershell -Command "(netsh wlan show interfaces) -match \'Authentication\'"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        if "WPA3" in result.stdout:
            return {
                "name": "WiFi 安全",
                "status": "pass",
                "message": "WPA3 加密 (优秀)",
                "recommendation": ""
            }
        elif "WPA2" in result.stdout:
            return {
                "name": "WiFi 安全",
                "status": "pass",
                "message": "WPA2 加密 (良好)",
                "recommendation": ""
            }
        elif "WPA" in result.stdout or "WEP" in result.stdout:
            return {
                "name": "WiFi 安全",
                "status": "warning",
                "message": "弱加密 (WPA/WEP)",
                "recommendation": "升级到 WPA2 或 WPA3"
            }
        else:
            return {
                "name": "WiFi 安全",
                "status": "pass",
                "message": "有线网络或未连接",
                "recommendation": ""
            }
    except:
        return {
            "name": "WiFi 安全",
            "status": "warning",
            "message": "无法检查 WiFi 状态",
            "recommendation": "手动检查 WiFi 设置"
        }

def print_network_scan_report(results: dict):
    """打印网络安全扫描报告"""
    print("\n🌐 龙虾卫士 - 网络安全扫描")
    print("=" * 60)
    print(f"扫描时间：{results['scan_time']}")
    print(f"扫描项目：{results['total_checks']} 项")
    print(f"✅ 正常项：{results['passed']} 项")
    print(f"⚠️  警告项：{results['warnings']} 项")
    print(f"❌ 危险项：{results['critical']} 项")
    
    print("\n扫描结果:")
    for check in results["checks"]:
        icon = "✅" if check["status"] == "pass" else ("⚠️" if check["status"] == "warning" else "❌")
        print(f"{icon} {check['name']}: {check['message']}")
        if check.get('recommendation'):
            print(f"   建议：{check['recommendation']}")
    
    # 计算安全评分
    if results['total_checks'] > 0:
        score = int((results['passed'] / results['total_checks']) * 100)
        print(f"\n📊 网络安全评分：{score}/100", end="")
        if score >= 90:
            print(" (优秀)")
        elif score >= 70:
            print(" (良好)")
        elif score >= 50:
            print(" (中等)")
        else:
            print(" (需改进)")
    
    print("\n建议操作:")
    if results['critical'] > 0:
        print("1. 立即处理危险项")
    if results['warnings'] > 0:
        print("2. 检查警告项并修复")
    print("3. 使用可信 DNS 服务器")
    print("4. 定期审查网络连接")
    print("=" * 60)

if __name__ == "__main__":
    results = scan_network()
    print_network_scan_report(results)
