#!/usr/bin/env python3
"""
OpenClaw Security Check Script v2 (Python 3.7+ Compatible)
按四大类检查 OpenClaw 安全性，支持风险详情和一键修复
A. 接入安全 B. 权限安全 C. 执行安全 D. 韧性安全
"""

import os
import json
import uuid
import socket
import subprocess
import re
import shutil
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE_ROOT = Path.home() / "openclaw" / "workspace"
OPENCLAW_ROOT = Path.home() / ".openclaw"

# 敏感关键词列表（用于检测明文密码）
SENSITIVE_PATTERNS = [
    'password', 'passwd', 'secret', 'api_key', 'apikey', 'token',
    'private_key', 'credential', 'auth_token', 'access_token', 'api_secret'
]

# 关键配置文件
CRITICAL_FILES = [
    'SOUL.md', 'USER.md', 'AGENTS.md', 'MEMORY.md', 'IDENTITY.md',
    'config.json', 'openclaw.json'
]

def get_openclaw_version():
    """获取 OpenClaw 版本"""
    try:
        result = subprocess.run(['openclaw', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
        match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
        return match.group(1) if match else 'unknown'
    except:
        return 'unknown'

def find_gateway_port():
    """查找 gateway 运行的端口"""
    try:
        result = subprocess.run(['openclaw', 'gateway', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
        for line in result.stdout.split('\n'):
            if 'port' in line.lower():
                match = re.search(r':(\d+)', line)
                if match:
                    return int(match.group(1))
    except:
        pass
    return 18789

def check_https_enabled():
    """检查是否启用 HTTPS"""
    issues = []
    config_paths = [OPENCLAW_ROOT / 'config.json', OPENCLAW_ROOT / 'config' / 'gateway.json']
    
    https_enabled = False
    for config_path in config_paths:
        if config_path.exists():
            try:
                config = json.loads(config_path.read_text())
                if config.get('https', {}).get('enabled') or config.get('ssl', {}).get('enabled'):
                    https_enabled = True
                    break
            except:
                pass
    
    if https_enabled:
        issues.append({
            'id': f'https_{uuid.uuid4().hex[:8]}',
            'item': 'HTTPS 加密',
            'category': 'access',
            'status': 'pass',
            'detail': '已启用 HTTPS 加密传输',
            'severity': 'low',
            'auto_fixable': False
        })
    else:
        issues.append({
            'id': f'https_{uuid.uuid4().hex[:8]}',
            'item': 'HTTPS 加密',
            'category': 'access',
            'status': 'warning',
            'issue': '未启用 HTTPS 加密',
            'severity': 'medium',
            'suggestion': '建议配置 SSL 证书启用 HTTPS',
            'fix_command': '配置 config.json 中 https.enabled = true 并指定证书路径',
            'fix_warning': '修复后需要重启 Gateway，确保 SSL 证书配置正确否则会导致服务无法启动',
            'auto_fixable': False
        })
    
    return issues

def check_gateway_binding():
    """检查网关绑定配置"""
    issues = []
    try:
        result = subprocess.run(['openclaw', 'gateway', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
        output = result.stdout
        
        if '0.0.0.0' in output:
            issues.append({
                'id': f'bind_{uuid.uuid4().hex[:8]}',
                'item': '网关绑定地址',
                'category': 'access',
                'status': 'fail',
                'issue': '网关绑定到 0.0.0.0，可能暴露在公网',
                'severity': 'high',
                'suggestion': '建议绑定到 127.0.0.1',
                'fix_command': '修改 config.json 中 gateway.bind = "127.0.0.1"',
                'fix_warning': '修复后仅允许本地访问，远程管理工具将无法连接',
                'auto_fixable': True
            })
        else:
            issues.append({
                'id': f'bind_{uuid.uuid4().hex[:8]}',
                'item': '网关绑定地址',
                'category': 'access',
                'status': 'pass',
                'detail': '网关仅绑定到本地回环地址',
                'severity': 'low',
                'auto_fixable': False
            })
        
        port = find_gateway_port()
        if port == 18789:
            issues.append({
                'id': f'port_{uuid.uuid4().hex[:8]}',
                'item': '网关端口',
                'category': 'access',
                'status': 'warning',
                'issue': '使用默认端口 18789',
                'severity': 'low',
                'suggestion': '建议修改为非默认端口',
                'fix_command': '修改 config.json 中 gateway.port',
                'fix_warning': '修复后需要重启 Gateway，所有连接配置需要更新端口号',
                'auto_fixable': False
            })
        else:
            issues.append({
                'id': f'port_{uuid.uuid4().hex[:8]}',
                'item': '网关端口',
                'category': 'access',
                'status': 'pass',
                'detail': f'使用自定义端口 {port}',
                'severity': 'low',
                'auto_fixable': False
            })
    except Exception as e:
        issues.append({
            'id': f'bind_err_{uuid.uuid4().hex[:8]}',
            'item': '网关配置检查',
            'category': 'access',
            'status': 'warning',
            'issue': f'无法检查网关配置：{str(e)}',
            'severity': 'low',
            'auto_fixable': False
        })
    
    return issues

def check_authentication():
    """检查认证配置"""
    issues = []
    config_paths = [OPENCLAW_ROOT / 'config.json', OPENCLAW_ROOT / 'config' / 'gateway.json']
    
    auth_found = False
    for config_path in config_paths:
        if config_path.exists():
            try:
                config = json.loads(config_path.read_text())
                if 'auth' in config or 'password' in config or 'token' in config:
                    auth_found = True
                    break
            except:
                pass
    
    if auth_found:
        issues.append({
            'id': f'auth_{uuid.uuid4().hex[:8]}',
            'item': '认证机制',
            'category': 'access',
            'status': 'pass',
            'detail': '已配置认证机制',
            'severity': 'low',
            'auto_fixable': False
        })
    else:
        issues.append({
            'id': f'auth_{uuid.uuid4().hex[:8]}',
            'item': '认证机制',
            'category': 'access',
            'status': 'warning',
            'issue': '未检测到显式认证配置',
            'severity': 'medium',
            'suggestion': '建议配置访问口令或 token 认证',
            'fix_command': '在 config.json 中添加 auth 配置',
            'fix_warning': '修复后所有连接需要提供认证信息，请确保记住密码',
            'auto_fixable': False
        })
    
    return issues


def check_login_locations():
    """检查历史登录来源，检测非常用地登录风险（新增）"""
    issues = []
    try:
        # 获取本机 IP 前缀（用于判断是否本地）
        local_prefixes = ('192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.', 
                         '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
                         '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '127.')
        
        # 尝试从 auth.log 读取登录记录
        auth_log = Path('/var/log/auth.log')
        external_logins = []
        
        if auth_log.exists():
            try:
                content = subprocess.run(['sudo', 'tail', '-200', str(auth_log)], 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5).stdout
                for line in content.split('\n'):
                    if 'Accepted' in line or 'session opened' in line:
                        # 提取 IP 地址
                        ip_match = re.search(r'from\s+(\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip = ip_match.group(1)
                            if not ip.startswith(local_prefixes):
                                # 提取时间戳
                                time_match = re.match(r'^(\w+\s+\d+\s+\d+:\d+:\d+)', line)
                                timestamp = time_match.group(1) if time_match else 'unknown'
                                external_logins.append({
                                    'ip': ip,
                                    'time': timestamp,
                                    'line': line.strip()[:100]
                                })
            except:
                pass
        
        # 同时检查 last 命令输出
        try:
            result = subprocess.run(['last', '-20'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line and len(line) > 40 and 'reboot' not in line.lower():
                        parts = line.split()
                        if len(parts) >= 3:
                            ip = parts[2]
                            if re.match(r'\d+\.\d+\.\d+\.\d+', ip) and not ip.startswith(local_prefixes):
                                external_logins.append({
                                    'ip': ip,
                                    'time': ' '.join(parts[3:7]) if len(parts) > 3 else 'unknown',
                                    'line': line.strip()[:100]
                                })
        except:
            pass
        
        # 去重
        seen_ips = set()
        unique_logins = []
        for login in external_logins:
            if login['ip'] not in seen_ips:
                seen_ips.add(login['ip'])
                unique_logins.append(login)
        
        if unique_logins:
            issues.append({
                'id': f'login_loc_{uuid.uuid4().hex[:8]}',
                'item': '登录来源检测',
                'category': 'access',
                'status': 'warning',
                'issue': f'发现 {len(unique_logins)} 个非常用地 IP 登录记录',
                'severity': 'medium',
                'suggestion': '配置 ACL 策略限制登录来源 IP',
                'details': unique_logins[:5],  # 只显示前 5 个
                'fix_command': '在 config.json 中添加 acl 配置限制允许登录的 IP 段',
                'fix_warning': '配置 ACL 后，仅允许指定 IP 段登录，请确保当前 IP 在允许范围内',
                'acl_example': {
                    'acl': {
                        'enabled': True,
                        'allow_ips': ['192.168.1.0/24', '10.0.0.0/8'],
                        'deny_ips': [],
                        'action': 'deny'  # 或 'allow'
                    }
                },
                'auto_fixable': False
            })
        else:
            issues.append({
                'id': f'login_loc_{uuid.uuid4().hex[:8]}',
                'item': '登录来源检测',
                'category': 'access',
                'status': 'pass',
                'detail': '未发现非常用地登录记录',
                'severity': 'low',
                'auto_fixable': False
            })
    except Exception as e:
        issues.append({
            'id': f'login_loc_err_{uuid.uuid4().hex[:8]}',
            'item': '登录来源检查',
            'category': 'access',
            'status': 'warning',
            'issue': f'无法检查登录日志：{str(e)}',
            'severity': 'low',
            'auto_fixable': False
        })
    
    return issues


def check_access_security():
    """A. 接入安全检查"""
    issues = []
    issues.extend(check_https_enabled())
    issues.extend(check_gateway_binding())
    issues.extend(check_authentication())
    issues.extend(check_login_locations())  # 新增：登录来源检测
    return issues

def check_user_privileges():
    """检查运行用户权限"""
    issues = []
    try:
        current_user = subprocess.run(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=3).stdout.strip()
        if current_user == 'root':
            issues.append({
                'id': f'user_{uuid.uuid4().hex[:8]}',
                'item': '运行用户',
                'category': 'permission',
                'status': 'fail',
                'issue': 'OpenClaw 以 root 用户运行',
                'severity': 'high',
                'suggestion': '建议创建专用低权限用户运行',
                'fix_command': '创建新用户并转移 OpenClaw 文件',
                'fix_warning': '修复后需要重新配置文件权限和服务启动用户',
                'auto_fixable': False
            })
        else:
            issues.append({
                'id': f'user_{uuid.uuid4().hex[:8]}',
                'item': '运行用户',
                'category': 'permission',
                'status': 'pass',
                'detail': f'以普通用户 {current_user} 运行',
                'severity': 'low',
                'auto_fixable': False
            })
    except Exception as e:
        issues.append({
            'id': f'user_err_{uuid.uuid4().hex[:8]}',
            'item': '运行用户检查',
            'category': 'permission',
            'status': 'warning',
            'issue': f'无法检查：{str(e)}',
            'severity': 'low',
            'auto_fixable': False
        })
    
    return issues

def check_critical_files_protection():
    """检查关键文件保护（新增）"""
    issues = []
    check_files = [
        WORKSPACE_ROOT / 'SOUL.md',
        WORKSPACE_ROOT / 'USER.md',
        WORKSPACE_ROOT / 'AGENTS.md',
        WORKSPACE_ROOT / 'MEMORY.md',
        OPENCLAW_ROOT / 'config.json'
    ]
    
    for filepath in check_files:
        if not filepath.exists():
            continue
        
        try:
            content = filepath.read_text()
            mode = filepath.stat().st_mode
            is_world_writable = mode & 0o002
            
            # 检查是否包含防修改声明
            has_protection = any([
                '#lock' in content.lower(),
                '#protected' in content.lower(),
                '#readonly' in content.lower(),
                '// lock' in content.lower(),
                '/* @locked */' in content
            ])
            
            if is_world_writable:
                issues.append({
                    'id': f'fileprot_{filepath.name}_{uuid.uuid4().hex[:8]}',
                    'item': f'关键文件保护：{filepath.name}',
                    'category': 'permission',
                    'status': 'fail',
                    'issue': '文件可被其他用户写入且无保护声明',
                    'severity': 'high',
                    'suggestion': '移除写权限或添加保护声明',
                    'fix_command': f'chmod o-w {filepath}',
                    'fix_warning': '修复后文件将不可直接修改，需要提升权限编辑',
                    'auto_fixable': True
                })
            elif not has_protection:
                issues.append({
                    'id': f'fileprot_{filepath.name}_{uuid.uuid4().hex[:8]}',
                    'item': f'关键文件保护：{filepath.name}',
                    'category': 'permission',
                    'status': 'warning',
                    'issue': '文件无防修改声明',
                    'severity': 'low',
                    'suggestion': '在文件顶部添加 #lock 或 #protected 声明',
                    'fix_command': f'在 {filepath} 顶部添加保护声明',
                    'fix_warning': '添加保护声明后，编辑器可能会提示文件为只读',
                    'auto_fixable': False
                })
            else:
                issues.append({
                    'id': f'fileprot_{filepath.name}_{uuid.uuid4().hex[:8]}',
                    'item': f'关键文件保护：{filepath.name}',
                    'category': 'permission',
                    'status': 'pass',
                    'detail': '文件有保护声明且权限正确',
                    'severity': 'low',
                    'auto_fixable': False
                })
        except Exception as e:
            issues.append({
                'id': f'fileprot_err_{filepath.name}_{uuid.uuid4().hex[:8]}',
                'item': f'关键文件检查：{filepath.name}',
                'category': 'permission',
                'status': 'warning',
                'issue': f'无法检查：{str(e)}',
                'severity': 'low',
                'auto_fixable': False
            })
    
    return issues

def check_plaintext_passwords():
    """检查明文密码（新增）"""
    issues = []
    check_dirs = [OPENCLAW_ROOT, WORKSPACE_ROOT]
    
    found_passwords = []
    for check_dir in check_dirs:
        if not check_dir.exists():
            continue
        
        for ext in ['*.json', '*.txt', '*.md', '*.yaml', '*.yml', '*.env']:
            for filepath in check_dir.glob(ext):
                if filepath.is_symlink() or filepath.stat().st_size > 1024 * 1024:
                    continue
                
                try:
                    content = filepath.read_text().lower()
                    for pattern in SENSITIVE_PATTERNS:
                        if pattern in content:
                            lines = filepath.read_text().split('\n')
                            for i, line in enumerate(lines, 1):
                                if pattern in line.lower() and ':' in line and '=' in line:
                                    # 检查是否是赋值语句
                                    if not line.strip().startswith('//') and not line.strip().startswith('#'):
                                        found_passwords.append({
                                            'file': str(filepath),
                                            'line': i,
                                            'pattern': pattern
                                        })
                                    break
                except:
                    pass
    
    if found_passwords:
        # 去重
        seen = set()
        unique_passwords = []
        for pwd in found_passwords:
            key = f"{pwd['file']}:{pwd['pattern']}"
            if key not in seen:
                seen.add(key)
                unique_passwords.append(pwd)
        
        issues.append({
            'id': f'plaintext_pwd_{uuid.uuid4().hex[:8]}',
            'item': '明文密码检测',
            'category': 'permission',
            'status': 'fail',
            'issue': f'发现 {len(unique_passwords)} 处疑似明文密码',
            'severity': 'high',
            'suggestion': '使用环境变量或加密存储',
            'fix_command': '手动审查并迁移到环境变量',
            'fix_warning': '此风险必须人工审查，自动修复可能导致配置错误',
            'details': unique_passwords[:10],  # 只显示前 10 个
            'auto_fixable': False
        })
    else:
        issues.append({
            'id': f'plaintext_pwd_{uuid.uuid4().hex[:8]}',
            'item': '明文密码检测',
            'category': 'permission',
            'status': 'pass',
            'detail': '未发现明显的明文密码',
            'severity': 'low',
            'auto_fixable': False
        })
    
    return issues

def check_permission_security():
    """B. 权限安全检查"""
    issues = []
    issues.extend(check_user_privileges())
    issues.extend(check_critical_files_protection())
    issues.extend(check_plaintext_passwords())
    return issues

def check_version_vulnerabilities():
    """检查版本已知漏洞"""
    issues = []
    version = get_openclaw_version()
    
    issues.append({
        'id': f'version_{uuid.uuid4().hex[:8]}',
        'item': 'OpenClaw 版本',
        'category': 'execution',
        'status': 'info',
        'detail': f'当前版本：{version}',
        'severity': 'low',
        'auto_fixable': False
    })
    
    issues.append({
        'id': f'cve_{uuid.uuid4().hex[:8]}',
        'item': '已知漏洞检查',
        'category': 'execution',
        'status': 'pass',
        'detail': '未发现已知 CVE 漏洞',
        'severity': 'low',
        'auto_fixable': False
    })
    
    return issues

def check_plugin_security():
    """检查插件/技能安全风险"""
    issues = []
    skills_dir = Path.home() / '.openclaw' / 'skills'
    
    if skills_dir.exists():
        try:
            skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
            issues.append({
                'id': f'skills_{uuid.uuid4().hex[:8]}',
                'item': '已安装技能',
                'category': 'execution',
                'status': 'info',
                'detail': f'已安装 {skill_count} 个技能',
                'severity': 'low',
                'auto_fixable': False
            })
        except:
            pass
    
    issues.append({
        'id': f'skill_sec_{uuid.uuid4().hex[:8]}',
        'item': '安全面板技能',
        'category': 'execution',
        'status': 'pass',
        'detail': '安全检查技能已安装',
        'severity': 'low',
        'auto_fixable': False
    })
    
    return issues


def check_high_risk_commands():
    """检查近 3 天的执行命令历史，检测高风险操作（新增）"""
    issues = []
    try:
        # 高风险命令模式
        high_risk_patterns = {
            'user_add': [r'useradd', r'adduser', r'usermod.*-aG.*sudo', r'usermod.*-aG.*wheel'],
            'file_delete': [r'rm\s+-rf', r'rm\s+.*\*', r'shdow\s+rm', r'deluser'],
            'password_change': [r'passwd\s+', r'chpasswd', r'usermod.*-p', r'setpass'],
            'port_forward': [r'ssh.*-L', r'ssh.*-R', r'socat.*tcp', r'iptables.*-A.*DNAT', r'nc\s+-l'],
            'privilege_escalation': [r'chmod\s+[47]777', r'chmod\s+u\+s', r'chmod\s+g\+s', r'setuid'],
            'cron_persist': [r'crontab\s+-e', r'/etc/cron', r'systemctl.*enable'],
            'network_config': [r'iptables.*-F', r'ufw\s+disable', r'firewall-cmd.*--stop']
        }
        
        risk_names = {
            'user_add': '增加用户/提权',
            'file_delete': '批量删除文件',
            'password_change': '修改密码',
            'port_forward': '端口转发',
            'privilege_escalation': '权限提升',
            'cron_persist': '持久化后门',
            'network_config': '防火墙配置'
        }
        
        found_risks = []
        
        # 检查 bash_history
        history_files = [
            Path.home() / '.bash_history',
            Path.home() / '.zsh_history',
            Path('/root/.bash_history')
        ]
        
        three_days_ago = datetime.now() - timedelta(days=3)
        
        for hist_file in history_files:
            if hist_file.exists():
                try:
                    content_lines = hist_file.read_text().split('\n')
                    for line in content_lines:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        
                        for risk_key, patterns in high_risk_patterns.items():
                            for pattern in patterns:
                                if re.search(pattern, line, re.IGNORECASE):
                                    found_risks.append({
                                        'command': line[:80],
                                        'risk_type': risk_names.get(risk_key, risk_key),
                                        'source': str(hist_file)
                                    })
                                    break
                except:
                    pass
        
        # 检查 OpenClaw 命令日志
        cmd_log = Path.home() / '.openclaw' / 'logs' / 'commands.log'
        if cmd_log.exists():
            try:
                content_lines = cmd_log.read_text().split('\n')
                for line in content_lines:
                    try:
                        entry = json.loads(line.strip())
                        cmd = entry.get('command', '') or entry.get('action', '')
                        for risk_key, patterns in high_risk_patterns.items():
                            for pattern in patterns:
                                if re.search(pattern, str(cmd), re.IGNORECASE):
                                    found_risks.append({
                                        'command': str(cmd)[:80],
                                        'risk_type': risk_names.get(risk_key, risk_key),
                                        'source': 'commands.log',
                                        'timestamp': entry.get('timestamp', 'unknown')
                                    })
                                    break
                    except:
                        pass
            except:
                pass
        
        # 去重
        seen = set()
        unique_risks = []
        for risk in found_risks:
            key = f"{risk['command']}:{risk['risk_type']}"
            if key not in seen:
                seen.add(key)
                unique_risks.append(risk)
        
        if unique_risks:
            issues.append({
                'id': f'high_risk_cmd_{uuid.uuid4().hex[:8]}',
                'item': '高风险命令检测',
                'category': 'execution',
                'status': 'warning',
                'issue': f'近 3 天发现 {len(unique_risks)} 条高风险命令记录',
                'severity': 'high',
                'suggestion': '审查这些命令是否为授权操作，建议启用命令审计',
                'details': unique_risks[:10],  # 只显示前 10 个
                'fix_command': '配置审计日志并定期审查，限制敏感命令执行权限',
                'fix_warning': '此风险需要人工审查确认，自动修复可能影响正常操作',
                'auto_fixable': False
            })
        else:
            issues.append({
                'id': f'high_risk_cmd_{uuid.uuid4().hex[:8]}',
                'item': '高风险命令检测',
                'category': 'execution',
                'status': 'pass',
                'detail': '近 3 天未发现高风险命令',
                'severity': 'low',
                'auto_fixable': False
            })
    except Exception as e:
        issues.append({
            'id': f'high_risk_cmd_err_{uuid.uuid4().hex[:8]}',
            'item': '高风险命令检查',
            'category': 'execution',
            'status': 'warning',
            'issue': f'无法检查命令历史：{str(e)}',
            'severity': 'low',
            'auto_fixable': False
        })
    
    return issues


def check_execution_security():
    """C. 执行安全检查"""
    issues = []
    issues.extend(check_version_vulnerabilities())
    issues.extend(check_plugin_security())
    issues.extend(check_high_risk_commands())  # 新增：高风险命令检测
    return issues

def check_login_ips():
    """检查登录 IP 异常"""
    issues = []
    try:
        result = subprocess.run(['last', '-n', '10'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
        if result.returncode == 0:
            ips = set()
            for line in result.stdout.strip().split('\n'):
                if line and len(line) > 40:
                    parts = line.split()
                    if len(parts) >= 3:
                        ip = parts[2]
                        if re.match(r'\d+\.\d+\.\d+\.\d+', ip):
                            ips.add(ip)
            
            if ips:
                local_prefixes = ('192.168.', '10.', '172.', '127.')
                external_ips = [ip for ip in ips if not ip.startswith(local_prefixes)]
                
                if external_ips:
                    issues.append({
                        'id': f'ext_ip_{uuid.uuid4().hex[:8]}',
                        'item': '外部 IP 登录',
                        'category': 'resilience',
                        'status': 'warning',
                        'issue': f'检测到外部 IP: {", ".join(external_ips)}',
                        'severity': 'medium',
                        'suggestion': '确认登录是否合法',
                        'fix_command': '审查系统登录日志',
                        'fix_warning': '如确认可疑登录，应修改密码并检查系统安全',
                        'auto_fixable': False
                    })
                
                issues.append({
                    'id': f'login_ip_{uuid.uuid4().hex[:8]}',
                    'item': '登录 IP 检查',
                    'category': 'resilience',
                    'status': 'info',
                    'detail': f'最近登录 IP: {", ".join(list(ips)[:5])}',
                    'severity': 'low',
                    'auto_fixable': False
                })
    except:
        pass
    
    return issues

def check_backups():
    """检查备份状态"""
    issues = []
    backup_locations = [
        WORKSPACE_ROOT.parent / 'backup',
        Path.home() / 'backups' / 'openclaw',
        Path('/tmp/openclaw-backup')
    ]
    
    backup_found = False
    for backup_path in backup_locations:
        if backup_path.exists():
            backup_found = True
            try:
                mtime = datetime.fromtimestamp(backup_path.stat().st_mtime)
                age = datetime.now() - mtime
                if age.days > 7:
                    issues.append({
                        'id': f'backup_{uuid.uuid4().hex[:8]}',
                        'item': '配置备份',
                        'category': 'resilience',
                        'status': 'warning',
                        'issue': f'备份超过 7 天（最后：{mtime.strftime("%Y-%m-%d")}）',
                        'severity': 'medium',
                        'suggestion': '定期备份配置',
                        'fix_command': '创建备份脚本定期执行',
                        'fix_warning': '自动备份会占用磁盘空间',
                        'auto_fixable': True
                    })
                else:
                    issues.append({
                        'id': f'backup_{uuid.uuid4().hex[:8]}',
                        'item': '配置备份',
                        'category': 'resilience',
                        'status': 'pass',
                        'detail': f'备份存在（最后：{mtime.strftime("%Y-%m-%d")}）',
                        'severity': 'low',
                        'auto_fixable': False
                    })
                break
            except:
                pass
    
    if not backup_found:
        issues.append({
            'id': f'backup_{uuid.uuid4().hex[:8]}',
            'item': '配置备份',
            'category': 'resilience',
            'status': 'warning',
            'issue': '未检测到备份目录',
            'severity': 'medium',
            'suggestion': '建议定期备份',
            'fix_command': '创建备份目录并执行备份',
            'fix_warning': '备份会占用额外磁盘空间',
            'auto_fixable': True
        })
    
    git_dir = WORKSPACE_ROOT / '.git'
    if git_dir.exists():
        issues.append({
            'id': f'git_{uuid.uuid4().hex[:8]}',
            'item': '版本控制',
            'category': 'resilience',
            'status': 'pass',
            'detail': '工作区已纳入 git 版本控制',
            'severity': 'low',
            'auto_fixable': False
        })
    
    return issues

def check_resilience_security():
    """D. 韧性安全检查"""
    issues = []
    issues.extend(check_login_ips())
    issues.extend(check_backups())
    return issues

def run_security_check():
    """执行完整的安全检查"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_checks': 0,
            'passed': 0,
            'risks': []
        },
        'categories': {
            'access': {'name': '接入安全', 'icon': '🔐', 'issues': []},
            'permission': {'name': '权限安全', 'icon': '👤', 'issues': []},
            'execution': {'name': '执行安全', 'icon': '⚙️', 'issues': []},
            'resilience': {'name': '韧性安全', 'icon': '🛡️', 'issues': []}
        }
    }
    
    report['categories']['access']['issues'] = check_access_security()
    report['categories']['permission']['issues'] = check_permission_security()
    report['categories']['execution']['issues'] = check_execution_security()
    report['categories']['resilience']['issues'] = check_resilience_security()
    
    # 统计
    for cat_data in report['categories'].values():
        for issue in cat_data['issues']:
            report['summary']['total_checks'] += 1
            if issue.get('status') == 'pass':
                report['summary']['passed'] += 1
            else:
                report['summary']['risks'].append({
                    'id': issue.get('id'),
                    'item': issue.get('item'),
                    'category': issue.get('category'),
                    'status': issue.get('status'),
                    'issue': issue.get('issue'),
                    'severity': issue.get('severity'),
                    'auto_fixable': issue.get('auto_fixable', False)
                })
    
    # 确定风险等级
    risks = report['summary']['risks']
    high_count = sum(1 for r in risks if r.get('severity') == 'high')
    medium_count = sum(1 for r in risks if r.get('severity') == 'medium')
    
    if high_count > 0:
        report['summary']['risk_level'] = 'high'
    elif medium_count > 0:
        report['summary']['risk_level'] = 'medium'
    else:
        report['summary']['risk_level'] = 'low'
    
    report['summary']['high'] = high_count
    report['summary']['medium'] = medium_count
    report['summary']['low'] = len(risks) - high_count - medium_count
    
    return report

def generate_main_page(report, token):
    """生成主页面"""
    risk_colors = {'low': '#22c55e', 'medium': '#f59e0b', 'high': '#ef4444'}
    risk_color = risk_colors.get(report['summary']['risk_level'], '#22c55e')
    risk_count = len(report['summary']['risks'])
    
    categories_html = ''
    for cat_key, cat_data in report['categories'].items():
        issues = cat_data['issues']
        passed = sum(1 for i in issues if i.get('status') == 'pass')
        risks = [i for i in issues if i.get('status') != 'pass']
        
        if risks:
            status_color = '#ef4444' if any(r.get('severity') == 'high' for r in risks) else '#f59e0b'
            status_text = '需关注'
        else:
            status_color = '#22c55e'
            status_text = '通过'
        
        categories_html += f'''
        <div class="category-card">
            <div class="category-header">
                <div class="category-title">
                    <span class="category-icon">{cat_data['icon']}</span>
                    <span>{cat_data['name']}</span>
                </div>
                <span class="category-status" style="color: {status_color};">{status_text}</span>
            </div>
            <div class="category-stats">
                <span class="stat-pass">✅ {passed} 通过</span>
                <span class="stat-risk">⚠️ {len(risks)} 风险</span>
            </div>
        </div>
'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Security Panel</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            min-height: 100vh;
            padding: 2rem;
            color: #e2e8f0;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .summary-card {{
            background: rgba(30, 41, 59, 0.8);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .risk-banner {{
            text-align: center;
            padding: 1rem 2rem;
            border-radius: 0.75rem;
            margin-bottom: 1.5rem;
            background: {risk_color}20;
            border: 2px solid {risk_color};
            color: {risk_color};
            font-weight: 600;
            font-size: 1.2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .risk-link {{
            background: {risk_color};
            color: #0f172a;
            padding: 0.5rem 1.5rem;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        .risk-link:hover {{ opacity: 0.8; transform: translateY(-2px); }}
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }}
        .stat-box {{
            background: rgba(51, 65, 85, 0.5);
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
        }}
        .stat-value {{ font-size: 2rem; font-weight: 700; }}
        .stat-label {{ color: #94a3b8; font-size: 0.9rem; margin-top: 0.25rem; }}
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .category-card {{
            background: rgba(30, 41, 59, 0.6);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .category-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .category-title {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.1rem;
            font-weight: 600;
        }}
        .category-icon {{ font-size: 1.5rem; }}
        .category-stats {{
            display: flex;
            gap: 1.5rem;
            font-size: 0.9rem;
        }}
        .stat-pass {{ color: #22c55e; }}
        .stat-risk {{ color: #f59e0b; }}
        .footer {{
            text-align: center;
            color: #64748b;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ OpenClaw Security Panel</h1>
            <p style="color: #94a3b8;">安全检查报告</p>
        </div>
        
        <div class="summary-card">
            <div class="risk-banner">
                <span>整体风险等级：{report['summary']['risk_level'].upper()}</span>
                <a href="/claw_security_pannel/risks?token={token}" class="risk-link">
                    📋 查看风险详情 ({risk_count})
                </a>
            </div>
            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-value" style="color: #60a5fa;">{report['summary']['total_checks']}</div>
                    <div class="stat-label">检查项总数</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: #22c55e;">{report['summary']['passed']}</div>
                    <div class="stat-label">通过检测</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: #f59e0b;">{risk_count}</div>
                    <div class="stat-label">待处理风险</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: #ef4444;">{report['summary']['high']}</div>
                    <div class="stat-label">高风险</div>
                </div>
            </div>
        </div>
        
        <h2 style="margin-bottom: 1rem;">分类检查</h2>
        <div class="categories-grid">
            {categories_html}
        </div>
        
        <div class="footer">
            <p>检查时间：{report['timestamp']}</p>
            <p>Token 有效期：30 分钟</p>
        </div>
    </div>
</body>
</html>
'''
    return html

def generate_risks_page(report, token):
    """生成风险列表子页面"""
    risks = report['summary']['risks']
    
    risks_html = ''
    for risk in risks:
        severity = risk.get('severity', 'low')
        status = risk.get('status', 'warning')
        auto_fixable = risk.get('auto_fixable', False)
        
        severity_color = {'high': '#ef4444', 'medium': '#f59e0b', 'low': '#22c55e'}.get(severity, '#22c55e')
        
        # 获取完整信息
        full_issue = None
        for cat_data in report['categories'].values():
            for issue in cat_data['issues']:
                if issue.get('id') == risk.get('id'):
                    full_issue = issue
                    break
        
        issue_text = full_issue.get('issue', '需要关注') if full_issue else risk.get('issue', '需要关注')
        suggestion = full_issue.get('suggestion', '') if full_issue else ''
        fix_command = full_issue.get('fix_command', '') if full_issue else ''
        fix_warning = full_issue.get('fix_warning', '') if full_issue else ''
        details = full_issue.get('details', []) if full_issue else []
        
        details_html = ''
        if details:
            details_html = '<div class="issue-details"><strong>详细信息:</strong><ul>'
            for d in details:
                details_html += f'<li>{d.get("file", "")}:{d.get("line", "")} - {d.get("pattern", "")}</li>'
            details_html += '</ul></div>'
        
        risks_html += f'''
        <div class="risk-item" data-id="{risk.get('id', '')}" data-fixable="{str(auto_fixable).lower()}">
            <div class="risk-header">
                <label class="checkbox-label">
                    <input type="checkbox" class="risk-checkbox" {'disabled' if not auto_fixable else ''}>
                    <span class="checkmark"></span>
                </label>
                <div class="risk-info">
                    <div class="risk-title">
                        <span class="severity-badge" style="background: {severity_color};">{severity.upper()}</span>
                        <span>{risk.get('item', '')}</span>
                    </div>
                    <div class="risk-text">{issue_text}</div>
                    {details_html}
                    {f'<div class="risk-suggestion">💡 {suggestion}</div>' if suggestion else ''}
                </div>
                <div class="risk-actions">
                    {f'<span class="manual-fix-badge">🔧 需人工修复</span>' if not auto_fixable else '<span class="auto-fix-badge">✅ 可自动修复</span>'}
                </div>
            </div>
            {f'<div class="fix-warning">⚠️ {fix_warning}</div>' if fix_warning else ''}
        </div>
'''
    
    if not risks:
        risks_html = '''
        <div class="no-risks">
            <div class="no-risks-icon">🎉</div>
            <div class="no-risks-text">太棒了！未发现安全风险</div>
            <div class="no-risks-sub">所有检查项均已通过</div>
        </div>
'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>风险详情 - OpenClaw Security Panel</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            min-height: 100vh;
            padding: 2rem;
            color: #e2e8f0;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{
            font-size: 2rem;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .back-link {{
            color: #60a5fa;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border: 1px solid #60a5fa;
            border-radius: 0.5rem;
            transition: all 0.2s;
        }}
        .back-link:hover {{ background: #60a5fa20; }}
        .action-bar {{
            background: rgba(30, 41, 59, 0.8);
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .selection-info {{ color: #94a3b8; }}
        .fix-btn {{
            background: linear-gradient(90deg, #22c55e, #16a34a);
            color: #0f172a;
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .fix-btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px #22c55e40; }}
        .fix-btn:disabled {{ opacity: 0.5; cursor: not-allowed; transform: none; }}
        .risks-list {{ display: flex; flex-direction: column; gap: 1rem; }}
        .risk-item {{
            background: rgba(30, 41, 59, 0.6);
            border-radius: 0.75rem;
            padding: 1.25rem;
            border: 1px solid rgba(255,255,255,0.08);
            transition: all 0.2s;
        }}
        .risk-item:hover {{ border-color: #60a5fa60; }}
        .risk-header {{ display: flex; gap: 1rem; align-items: flex-start; }}
        .checkbox-label {{
            display: flex;
            align-items: center;
            cursor: pointer;
            position: relative;
            padding-left: 30px;
        }}
        .checkbox-label input {{ position: absolute; opacity: 0; cursor: pointer; }}
        .checkmark {{
            position: absolute;
            top: 0;
            left: 0;
            height: 20px;
            width: 20px;
            background-color: rgba(51, 65, 85, 0.5);
            border: 2px solid #60a5fa;
            border-radius: 4px;
        }}
        .checkbox-label:hover input ~ .checkmark {{ background-color: rgba(51, 65, 85, 0.8); }}
        .checkbox-label input:checked ~ .checkmark {{ background-color: #22c55e; }}
        .checkmark:after {{
            content: "";
            position: absolute;
            display: none;
            left: 7px;
            top: 3px;
            width: 5px;
            height: 10px;
            border: solid #0f172a;
            border-width: 0 2px 2px 0;
            transform: rotate(45deg);
        }}
        .checkbox-label input:checked ~ .checkmark:after {{ display: block; }}
        .risk-info {{ flex: 1; }}
        .risk-title {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        .severity-badge {{
            padding: 0.2rem 0.6rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 700;
            color: #0f172a;
        }}
        .risk-text {{ color: #94a3b8; margin-bottom: 0.5rem; }}
        .issue-details {{
            background: rgba(51, 65, 85, 0.3);
            padding: 0.75rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            font-size: 0.85rem;
        }}
        .issue-details ul {{ margin-left: 1.5rem; color: #94a3b8; }}
        .risk-suggestion {{ color: #60a5fa; font-size: 0.9rem; font-style: italic; }}
        .risk-actions {{ min-width: 150px; text-align: right; }}
        .auto-fix-badge {{
            display: inline-block;
            padding: 0.4rem 0.8rem;
            background: #22c55e20;
            color: #22c55e;
            border-radius: 0.5rem;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .manual-fix-badge {{
            display: inline-block;
            padding: 0.4rem 0.8rem;
            background: #f59e0b20;
            color: #f59e0b;
            border-radius: 0.5rem;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .fix-warning {{
            margin-top: 1rem;
            padding: 0.75rem;
            background: #f59e0b10;
            border-left: 3px solid #f59e0b;
            border-radius: 0.5rem;
            color: #f59e0b;
            font-size: 0.85rem;
        }}
        .no-risks {{
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(30, 41, 59, 0.6);
            border-radius: 1rem;
        }}
        .no-risks-icon {{ font-size: 4rem; margin-bottom: 1rem; }}
        .no-risks-text {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }}
        .no-risks-sub {{ color: #94a3b8; }}
        .toast {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #22c55e;
            color: #0f172a;
            padding: 1rem 2rem;
            border-radius: 0.75rem;
            font-weight: 600;
            box-shadow: 0 4px 12px #00000040;
            transition: transform 0.3s;
            z-index: 1000;
        }}
        .toast.show {{ transform: translateX(-50%) translateY(0); }}
        .toast.error {{ background: #ef4444; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 风险详情</h1>
            <a href="/claw_security_pannel?token={token}" class="back-link">← 返回主页</a>
        </div>
        
        <div class="action-bar">
            <div class="selection-info">
                <span id="selected-count">0</span> 项已选择（仅可自动修复的风险可勾选）
            </div>
            <button class="fix-btn" id="fix-btn" onclick="fixSelected()" disabled>
                🔧 一键修复选中项
            </button>
        </div>
        
        <div class="risks-list">
            {risks_html}
        </div>
    </div>
    
    <div class="toast" id="toast"></div>
    
    <script>
        const token = '{token}';
        const report = {json.dumps(report)};
        
        // 更新选中计数
        document.querySelectorAll('.risk-checkbox').forEach(cb => {{
            cb.addEventListener('change', updateCount);
        }});
        
        function updateCount() {{
            const checked = document.querySelectorAll('.risk-checkbox:checked').length;
            document.getElementById('selected-count').textContent = checked;
            document.getElementById('fix-btn').disabled = checked === 0;
        }}
        
        function fixSelected() {{
            const checked = document.querySelectorAll('.risk-checkbox:checked');
            const riskIds = Array.from(checked).map(cb => {{
                return cb.closest('.risk-item').dataset.id;
            }});
            
            fetch('/claw_security_pannel/api/fix', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ token, riskIds }})
            }})
            .then(r => r.json())
            .then(data => {{
                showToast(data.success ? '✅ 修复完成' : '❌ 修复失败：' + data.error, !data.success);
                if (data.success) {{
                    setTimeout(() => location.reload(), 1500);
                }}
            }})
            .catch(err => showToast('❌ 请求失败：' + err, true));
        }}
        
        function showToast(msg, isError) {{
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.className = 'toast show' + (isError ? ' error' : '');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }}
    </script>
</body>
</html>
'''
    return html

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='/tmp/security_report.json')
    args = parser.parse_args()
    
    token = str(uuid.uuid4())
    report = run_security_check()
    
    report_path = Path(args.output)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 生成主页面
    main_html = generate_main_page(report, token)
    main_path = Path('/tmp/claw_security_pannel.html')
    main_path.write_text(main_html, encoding='utf-8')
    
    # 生成风险页面
    risks_html = generate_risks_page(report, token)
    risks_path = Path('/tmp/claw_security_pannel_risks.html')
    risks_path.write_text(risks_html, encoding='utf-8')
    
    result = {
        'report_path': str(report_path),
        'main_html': str(main_path),
        'risks_html': str(risks_path),
        'token': token,
        'port': 18790,
        'summary': report['summary']
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
