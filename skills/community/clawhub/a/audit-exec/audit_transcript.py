# -*- coding: utf-8 -*-
"""
审计 OpenClaw transcript 文件，提取并分析 exec 命令
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

# ========== 风险规则定义 ==========

# 🔴 高风险 (Red Line) - 命中直接标红
HIGH_RISK_PATTERNS = [
    # 级联删除 - Linux
    (r'rm\s+-rf\s+', 'Linux 级联删除'),
    (r'find.*-delete', 'Linux 递归删除'),
    # 级联删除 - Windows
    (r'del\s+/s\s+/q', 'Windows 递归删除'),
    (r'rmdir\s+/s\s+/q', 'Windows 递归删除'),
    (r'Remove-Item\s+.*-Recurse\s+.*-Force', 'Windows 强制递归删除'),
    # 防火墙 - Linux
    (r'iptables', 'Linux 防火墙规则修改'),
    (r'ufw\s+(enable|disable|delete|insert)', 'Linux 防火墙操作'),
    # 防火墙 - Windows
    (r'netsh\s+advfirewall', 'Windows 防火墙规则修改'),
    (r'Set-NetFirewallRule', 'Windows 防火墙规则修改'),
    (r'netsh\s+firewall', 'Windows 防火墙配置'),
    # 注册表 - Windows
    (r'reg\s+add\s+.*HKLM', 'Windows 注册表写入 (系统级)'),
    (r'reg\s+add\s+.*HKCU', 'Windows 注册表写入 (用户级)'),
    (r'reg\s+delete', 'Windows 注册表删除'),
    # 启动项 - Linux
    (r'cron\s+', 'Linux 定时任务'),
    # 启动项 - Windows
    (r'bcdedit', 'Windows 启动项修改'),
    (r'schtasks\s+/create', 'Windows 计划任务创建'),
    # 密钥泄露
    (r'(private.*key|私钥|api.?key|api_key|password|密码|token|token).*\.(pem|key|crt|p12|pfx|env)', '密钥文件访问'),
    # 远程连接
    (r'psexec', 'PsExec 远程执行'),
    (r'wmic\s+/node:', 'WMI 远程查询'),
    (r'Enter-PSSession', 'PowerShell 远程会话'),
]

# 🟡 中风险 (Yellow Line) - 标黄记录
MEDIUM_RISK_PATTERNS = [
    # 提权 - Linux
    (r'\bsudo\s+', 'Linux 提权执行'),
    # 提权 - Windows
    (r'\brunas\s+', 'Windows 提权执行'),
    (r'Start-Process\s+.*-Verb\s+RunAs', 'Windows UAC 提权'),
    # 外部下载 - Linux
    (r'\bcurl\s+', 'Linux 外部网络请求'),
    (r'\bwget\s+', 'Linux 外部网络下载'),
    # 外部下载 - Windows
    (r'Invoke-WebRequest', 'Windows 外部网络请求'),
    (r'\biwr\s+', 'Windows 外部网络请求'),
    (r'bitsadmin', 'Windows BITS 传输'),
    # 安装软件 - 跨平台
    (r'pip\s+install\s+', 'Python 包安装'),
    (r'npm\s+install\s+-g', '全局 npm 包安装'),
    (r'apt-get\s+install', 'APT 包安装'),
    (r'yum\s+install', 'YUM 包安装'),
    # 安装软件 - Windows
    (r'choco\s+install', 'Chocolatey 安装'),
    (r'winget\s+install', 'WinGet 安装'),
    # 远程连接
    (r'\bssh\s+', 'SSH 远程连接'),
    (r'\bnc\s+', 'NetCat 远程连接'),
]

def load_whitelist(whitelist_path):
    """加载白名单"""
    whitelist = []
    if os.path.exists(whitelist_path):
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # 格式: pattern -> 说明
                if '->' in line:
                    pattern = line.split('->')[0].strip()
                    reason = line.split('->')[1].strip()
                else:
                    pattern = line.strip()
                    reason = "白名单"
                if pattern:
                    whitelist.append((pattern, reason))
    return whitelist

def check_risk_level(command):
    """检查命令风险等级"""
    for pattern, reason in HIGH_RISK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return 'HIGH', reason
    
    for pattern, reason in MEDIUM_RISK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return 'MEDIUM', reason
    
    return 'LOW', None

def is_whitelisted(command, whitelist):
    """检查是否在白名单中"""
    for pattern, reason in whitelist:
        if re.search(pattern, command, re.IGNORECASE):
            return True, reason
    return False, None

def audit_transcript(transcript_path, whitelist_path, days=1):
    """审计 transcript 文件"""
    
    # 加载白名单
    whitelist = load_whitelist(whitelist_path)
    
    # 计算时间范围
    now = datetime.now()
    cutoff = now.timestamp() - (days * 86400)
    
    # 解析时间戳正则
    timestamp_pattern = r'"timestamp":"(\d{4}-\d{2}-\d{2}T[\d:]+)'
    
    results = {
        'HIGH': [],
        'MEDIUM': [],
        'LOW_WHITELISTED': [],
        'LOW': []
    }
    
    if not os.path.exists(transcript_path):
        print(f"[ERROR] Transcript file not found: {transcript_path}")
        return results
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                msg = json.loads(line.strip())
                if msg.get('type') != 'message':
                    continue
                
                # 提取时间戳
                ts_str = msg.get('timestamp', '')
                if ts_str:
                    # 处理 ISO 时间格式
                    try:
                        ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                        ts = ts.timestamp()
                    except:
                        continue
                    
                    # 只检查指定天数内的
                    if ts < cutoff:
                        continue
                
                # 检查是否是 toolCall 类型的 exec
                content = msg.get('message', {}).get('content', [])
                if not isinstance(content, list):
                    continue
                
                for item in content:
                    if item.get('type') == 'toolCall':
                        tool_name = item.get('name', '')
                        if tool_name == 'exec':
                            args = item.get('arguments', {})
                            command = args.get('command', '')
                            
                            if not command:
                                continue
                            
                            # 检查风险等级
                            risk_level, risk_reason = check_risk_level(command)
                            
                            # 检查白名单
                            whitelisted, wl_reason = is_whitelisted(command, whitelist)
                            
                            # 格式化时间
                            time_str = ''
                            if ts_str:
                                try:
                                    dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                                    time_str = dt.strftime('%H:%M:%S')
                                except:
                                    time_str = ts_str[11:19] if len(ts_str) > 19 else ts_str
                            
                            entry = {
                                'time': time_str,
                                'command': command[:100] + '...' if len(command) > 100 else command,
                                'full_command': command,
                                'risk_reason': risk_reason
                            }
                            
                            if whitelisted:
                                entry['wl_reason'] = wl_reason
                                results['LOW_WHITELISTED'].append(entry)
                            elif risk_level == 'HIGH':
                                results['HIGH'].append(entry)
                            elif risk_level == 'MEDIUM':
                                results['MEDIUM'].append(entry)
                            else:
                                results['LOW'].append(entry)
            
            except json.JSONDecodeError:
                continue
            except Exception as e:
                continue
    
    return results

def generate_report(results, days=1):
    """生成报告"""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    
    total = (len(results['HIGH']) + len(results['MEDIUM']) + 
              len(results['LOW']) + len(results['LOW_WHITELISTED']))
    
    report = []
    report.append("=" * 50)
    report.append("       [Exec Command Audit Report]")
    report.append("=" * 50)
    report.append(f"日期: {date_str}")
    report.append(f"平台: Windows / Linux")
    report.append(f"审计范围: 最近 {days} 天")
    report.append("")
    report.append(f"Total: {total} exec commands")
    report.append(f"  [HIGH] High Risk: {len(results['HIGH'])}")
    report.append(f"  [MEDIUM] Medium Risk: {len(results['MEDIUM'])}")
    report.append(f"  [LOW] Low Risk: {len(results['LOW'])}")
    report.append(f"  [OK] Whitelisted: {len(results['LOW_WHITELISTED'])}")
    report.append("")
    
    # 高风险
    if results['HIGH']:
        report.append("-" * 50)
        report.append("[HIGH] High Risk Commands - Please verify!")
        report.append("-" * 50)
        for item in results['HIGH']:
            report.append(f"[{item['time']}] {item['command']}")
            report.append(f"    Risk: {item['risk_reason']}")
        report.append("")
    
    # 中风险
    if results['MEDIUM']:
        report.append("-" * 50)
        report.append("[MEDIUM] Medium Risk Commands - Logged")
        report.append("-" * 50)
        for item in results['MEDIUM']:
            report.append(f"[{item['time']}] {item['command']}")
            report.append(f"    Reason: {item['risk_reason']}")
        report.append("")
    
    # 白名单
    if results['LOW_WHITELISTED']:
        report.append("-" * 50)
        report.append(f"[OK] Whitelisted ({len(results['LOW_WHITELISTED'])} commands)")
        report.append("-" * 50)
        for item in results['LOW_WHITELISTED']:
            report.append(f"[{item['time']}] {item['command']}")
            report.append(f"    Whitelist: {item['wl_reason']}")
        report.append("")
    
    # 低风险
    if results['LOW']:
        report.append("-" * 50)
        report.append(f"[LOW] Low Risk Commands ({len(results['LOW'])} commands)")
        report.append("-" * 50)
        for item in results['LOW']:
            report.append(f"[{item['time']}] {item['command']}")
        report.append("")
    
    report.append("=" * 50)
    report.append("审计完成")
    report.append("=" * 50)
    
    return '\n'.join(report)

if __name__ == '__main__':
    import sys
    
    # 默认路径 (Linux)
    transcript_path = r'/root/.openclaw/agents/main/sessions'
    whitelist_path = r'/root/.openclaw/workspace/skills/audit-exec/whitelist.txt'
    
    # 查找最新的 transcript 文件
    if os.path.isdir(transcript_path):
        files = [f for f in os.listdir(transcript_path) if f.endswith('.jsonl')]
        if files:
            # 按修改时间排序，取最新的
            files.sort(key=lambda f: os.path.getmtime(os.path.join(transcript_path, f)), reverse=True)
            transcript_path = os.path.join(transcript_path, files[0])
    
    print(f"使用 transcript: {transcript_path}")
    print(f"使用白名单: {whitelist_path}")
    print()
    
    # 运行审计
    results = audit_transcript(transcript_path, whitelist_path, days=1)
    
    # 生成报告
    report = generate_report(results, days=1)
    print(report)
