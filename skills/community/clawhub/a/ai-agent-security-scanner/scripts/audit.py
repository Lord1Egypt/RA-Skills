#!/usr/bin/env python3
"""
AI Agent Security Audit Tool
扫描AI Agent/Skill代码安全问题：敏感信息泄露、API密钥、注入风险、权限问题、数据安全等
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path

# 敏感信息正则模式
SENSITIVE_PATTERNS = {
    "API Key - Generic": re.compile(r'(?i)(api[_-]?key|apikey|api_secret)\s*[=:]\s*["\']?([a-zA-Z0-9_\-]{20,})["\']?'),
    "API Key - OpenAI style": re.compile(r'sk-[a-zA-Z0-9]{20,}'),
    "API Key - Bearer Token": re.compile(r'(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}'),
    "Password": re.compile(r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?([^"\'\s;]{6,})["\']?'),
    "Private Key": re.compile(r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'),
    "AWS Access Key": re.compile(r'AKIA[0-9A-Z]{16}'),
    "AWS Secret Key": re.compile(r'(?i)aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']?([a-zA-Z0-9/+=]{40})["\']?'),
    "GitHub Token": re.compile(r'gh[pousr]_[a-zA-Z0-9]{36,}'),
    "JWT Token": re.compile(r'eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+'),
    "Database Connection String": re.compile(r'(?i)(mysql|postgres|mongodb|redis)://[^\s"\'<>]+'),
    "Email + Password Combo": re.compile(r'(?i)(email|username)\s*[=:]\s*["\']?[^\s@]+@[^\s@]+\.[^\s@]+["\']?.*\n.*(password|passwd)\s*[=:]'),
    "Hardcoded IP Address": re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
    "Hardcoded Phone Number": re.compile(r'1[3-9]\d{9}'),
    "ID Card Number": re.compile(r'\b[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b'),
}

# 危险函数模式
DANGEROUS_PATTERNS = {
    "Command Injection - os.system": re.compile(r'os\.system\s*\([''"]'),
    "Command Injection - subprocess shell": re.compile(r'subprocess\.(call|run|Popen)\s*\(.*shell\s*=\s*True'),
    "Command Injection - exec": re.compile(r'(?<!\w)exec\s*\('),
    "Command Injection - eval": re.compile(r'(?<!\w)eval\s*\('),
    "SQL Injection - string format": re.compile(r'(?i)(execute|query)\s*\(.*f["\']'),
    "Path Traversal - open": re.compile(r'open\s*\(\s*[^\'"]+input'),
    "Unsafe Pickle Load": re.compile(r'pickle\.loads?\s*\('),
    "Unsafe YAML Load": re.compile(r'yaml\.load\s*\(.*Loader=.*FullLoader'),
    "Hardcoded Admin Credentials": re.compile(r'(?i)(admin|root)\s*[=:]\s*["\']?(admin|password|123456)["\']?'),
    "Insecure File Permissions - chmod 777": re.compile(r'chmod\s+777|os\.chmod\s*\(.*0o?777'),
    "Debug Mode Enabled": re.compile(r'(?i)debug\s*=\s*True'),
    "CORS Wildcard": re.compile(r'(?i)Access-Control-Allow-Origin.*\*'),
    "Insecure HTTPS Disable": re.compile(r'(?i)(verify\s*=\s*False|ssl_verify.*false|disable_ssl)'),
    "Weak Hash - MD5": re.compile(r'(?i)hashlib\.md5\('),
    "Weak Hash - SHA1": re.compile(r'(?i)hashlib\.sha1\('),
}

# 需要扫描的文件扩展名
SCAN_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.yaml', '.yml', '.env', '.txt', '.md', '.sh', '.bat', '.ps1', '.java', '.go', '.rs'}

# 跳过的目录
SKIP_DIRS = {'node_modules', '.git', '__pycache__', '.venv', 'venv', 'dist', 'build', '.next', '.nuxt'}

def scan_file(filepath):
    """扫描单个文件，返回发现的问题"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [{"type": "file_error", "severity": "low", "message": f"无法读取文件: {e}", "file": str(filepath)}]
    
    # 扫描敏感信息
    for pattern_name, pattern in SENSITIVE_PATTERNS.items():
        for match in pattern.finditer(content):
            line_num = content[:match.start()].count('\n') + 1
            line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""
            
            # 跳过示例和注释中的假密钥
            if any(skip in line_content.lower() for skip in ['example', 'demo', 'sample', 'test_key', 'your_', 'xxx', '***', 'replace', '占位']):
                continue
                
            severity = "critical" if any(k in pattern_name.lower() for k in ['private key', 'api key', 'password', 'aws', 'github token', 'jwt']) else "high" if any(k in pattern_name.lower() for k in ['database', 'combo']) else "medium"
            
            issues.append({
                "type": "sensitive_info",
                "category": pattern_name,
                "severity": severity,
                "file": str(filepath),
                "line": line_num,
                "content": line_content[:100],
                "description": f"发现可能的{pattern_name}"
            })
    
    # 扫描危险函数
    for pattern_name, pattern in DANGEROUS_PATTERNS.items():
        for match in pattern.finditer(content):
            line_num = content[:match.start()].count('\n') + 1
            line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""
            
            # 跳过注释
            if line_content.strip().startswith('#') or line_content.strip().startswith('//') or line_content.strip().startswith('/*'):
                if '#' in pattern_name or 'comment' in pattern_name.lower():
                    pass
                else:
                    continue
            
            severity = "critical" if any(k in pattern_name.lower() for k in ['command injection', 'pickle', 'admin credentials']) else "high" if any(k in pattern_name.lower() for k in ['sql injection', 'path traversal']) else "medium"
            
            issues.append({
                "type": "dangerous_code",
                "category": pattern_name,
                "severity": severity,
                "file": str(filepath),
                "line": line_num,
                "content": line_content[:100],
                "description": f"发现危险代码模式: {pattern_name}"
            })
    
    return issues

def scan_directory(dirpath):
    """扫描目录下所有文件"""
    all_issues = []
    dir_path = Path(dirpath)
    
    for root, dirs, files in os.walk(dir_path):
        # 跳过不需要的目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for file in files:
            filepath = Path(root) / file
            if filepath.suffix.lower() in SCAN_EXTENSIONS:
                issues = scan_file(filepath)
                all_issues.extend(issues)
    
    return all_issues

def ai_analyze(issues, code_snippet="", api_key=None, base_url=None):
    """用AI进行深度分析并给出修复建议"""
    try:
        from openai import OpenAI
    except ImportError:
        print("警告: 需要安装 openai 库才能使用AI深度分析")
        print("运行: pip install openai")
        return None
    
    if not api_key:
        api_key = os.environ.get('DEEPSEEK_API_KEY', '')
    if not api_key:
        print("警告: 未配置DEEPSEEK_API_KEY，跳过AI深度分析")
        return None
    
    if not base_url:
        base_url = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    issues_json = json.dumps(issues[:20], ensure_ascii=False, indent=2)
    
    prompt = f"""你是一位专业的AI安全审计专家。以下是代码安全扫描发现的问题，请进行深度分析并给出修复建议。

## 发现的安全问题
{issues_json}

## 请输出以下内容：
1. 总体风险评级（严重/高/中/低）
2. 最危急的3个问题及原因
3. 每个问题的具体修复方案（给出代码示例）
4. AI Agent特有的安全风险提示（如提示注入、工具滥用、数据泄露等）
5. 安全加固建议清单

请用中文回复，格式清晰。"""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "你是一位资深的网络安全审计专家，专注于AI Agent和大模型应用的安全审计。你的分析专业、准确、可落地。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI分析失败: {e}")
        return None

def generate_report(issues, ai_analysis=None, output_format='text'):
    """生成审计报告"""
    # 统计
    critical = sum(1 for i in issues if i['severity'] == 'critical')
    high = sum(1 for i in issues if i['severity'] == 'high')
    medium = sum(1 for i in issues if i['severity'] == 'medium')
    low = sum(1 for i in issues if i['severity'] == 'low')
    
    if output_format == 'json':
        report = {
            "summary": {"critical": critical, "high": high, "medium": medium, "low": low, "total": len(issues)},
            "issues": issues,
            "ai_analysis": ai_analysis
        }
        return json.dumps(report, ensure_ascii=False, indent=2)
    
    # 文本格式
    lines = []
    lines.append("=" * 60)
    lines.append("  AI Agent 安全审计报告")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"📊 扫描结果汇总:")
    lines.append(f"   🔴 严重 (Critical): {critical}")
    lines.append(f"   🟠 高危 (High): {high}")
    lines.append(f"   🟡 中危 (Medium): {medium}")
    lines.append(f"   🟢 低危 (Low): {low}")
    lines.append(f"   📋 问题总数: {len(issues)}")
    lines.append("")
    
    # 风险评级
    if critical > 0:
        risk_level = "🔴 严重风险"
    elif high > 0:
        risk_level = "🟠 高风险"
    elif medium > 0:
        risk_level = "🟡 中等风险"
    else:
        risk_level = "🟢 低风险"
    
    lines.append(f"⚠️  总体风险评级: {risk_level}")
    lines.append("")
    
    if issues:
        lines.append("-" * 60)
        lines.append("  问题明细（按严重程度排序）")
        lines.append("-" * 60)
        lines.append("")
        
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.get('severity', 'low'), 4))
        
        for idx, issue in enumerate(sorted_issues, 1):
            sev_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(issue.get('severity', 'low'), '⚪')
            lines.append(f"{idx}. {sev_icon} [{issue.get('category', issue.get('type', 'unknown'))}]")
            lines.append(f"   文件: {issue.get('file', 'N/A')}")
            if 'line' in issue:
                lines.append(f"   行号: 第 {issue['line']} 行")
            lines.append(f"   描述: {issue.get('description', '')}")
            if issue.get('content'):
                lines.append(f"   代码: {issue['content']}")
            lines.append("")
    
    if ai_analysis:
        lines.append("-" * 60)
        lines.append("  🤖 AI 深度分析与修复建议")
        lines.append("-" * 60)
        lines.append("")
        lines.append(ai_analysis)
        lines.append("")
    
    lines.append("=" * 60)
    lines.append("  报告生成时间: " + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    lines.append("  工具: Agent Security Audit v1.0")
    lines.append("=" * 60)
    
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='AI Agent 安全审计工具 - 扫描代码安全漏洞')
    parser.add_argument('target', help='要扫描的文件或目录路径')
    parser.add_argument('--no-ai', action='store_true', help='跳过AI深度分析')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式 (默认: text)')
    parser.add_argument('-o', '--output', help='输出报告文件路径')
    parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low', 'all'], default='all', help='只显示指定级别及以上的问题')
    parser.add_argument('--api-key', help='DeepSeek API Key (也可通过环境变量DEEPSEEK_API_KEY设置)')
    parser.add_argument('--base-url', help='DeepSeek API Base URL')
    
    args = parser.parse_args()
    
    target = args.target
    
    if not os.path.exists(target):
        print(f"错误: 路径不存在 - {target}")
        sys.exit(1)
    
    print(f"🔍 开始扫描: {target}")
    print()
    
    # 扫描
    if os.path.isfile(target):
        issues = scan_file(target)
    else:
        issues = scan_directory(target)
    
    # 按严重程度过滤
    if args.severity != 'all':
        severity_levels = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        min_level = severity_levels.get(args.severity, 0)
        issues = [i for i in issues if severity_levels.get(i.get('severity', 'low'), 99) <= min_level]
    
    print(f"✅ 扫描完成，发现 {len(issues)} 个问题")
    print()
    
    # AI分析
    ai_result = None
    if not args.no_ai and issues:
        print("🤖 正在进行AI深度分析...")
        ai_result = ai_analyze(issues, api_key=args.api_key, base_url=args.base_url)
        print()
    
    # 生成报告
    report = generate_report(issues, ai_result, args.format)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 报告已保存到: {args.output}")
    else:
        print(report)
    
    # 退出码：有严重问题返回非零
    critical_count = sum(1 for i in issues if i['severity'] == 'critical')
    sys.exit(1 if critical_count > 0 else 0)

if __name__ == '__main__':
    main()
