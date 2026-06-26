#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ClawHub Security Scan - Scan skill code for suspicious patterns"""

import os
import re
import argparse
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 解决Windows编码问题
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# SkillPay 配置
SKILL_ID = "a6c05ce6-3bb6-47b5-8c4b-a8fe0b4395b1"
PRICE = 0.001  # 每次调用 0.001 USDT

def skillpay_charge(user_id, api_key=None):
    """SkillPay 扣费"""
    import json
    import urllib.request
    import urllib.error

    API = "https://skillpay.me/api/v1"

    def _post(path, body, key):
        req = urllib.request.Request(f"{API}{path}", data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "X-API-Key": key}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            return json.loads(e.read())

    k = api_key or os.environ.get("SKILLPAY_API_KEY")
    if not k:
        return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    
    body = {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "amount": PRICE,
        "currency": "USDT",
        "description": "ClawHub Security Scan"
    }
    return _post("/billing/charge", body, k)

# 风险等级
RISK_GOOD = "good"      # 绿色，没问题
RISK_LOW = "low"        # 低风险，轻微注意
RISK_MEDIUM = "medium"  # 中风险，可能触发标记，需要检查
RISK_HIGH = "high"      # 高风险，确实有问题，必须修改

import math

# 高危模式 - 真的有安全问题
HIGH_RISK_PATTERNS = [
    # 读取敏感文件
    (r'open\([\'"].*\/etc\/passwd', "Reads /etc/passwd - sensitive system file"),
    (r'open\([\'"].*\/etc\/shadow', "Reads /etc/shadow - sensitive system file"),
    (r'open\([\'"].*\.ssh', "Reads .ssh directory - may contain SSH private keys"),
    (r'open\([\'"].*id_rsa', "Reads SSH private key"),
    (r'open\([\'"].*id_dsa', "Reads SSH private key"),
    (r'open\([\'"].*\.(pem|key)', "Reads private key file"),
    # 危险函数
    (r'\beval\(', "Uses eval() - arbitrary code execution risk"),
    (r'\bexec\(', "Uses exec() - arbitrary code execution risk"),
    (r'\bexecfile\(', "Uses execfile() - arbitrary code execution risk"),
    (r'__import__\(os\.(system|popen|popen2)', "Dynamic os module import for command execution"),
    # 硬编码密钥 - 正则匹配
    (r'(API_KEY|TOKEN|SECRET|PASSWORD)\s*=\s*[\'"][a-zA-Z0-9_\-]{32,}[\'"]', "Found possible hard-coded API key/token in source code"),
]

def calculate_shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy to detect high-entropy strings like API keys"""
    if not s:
        return 0.0
    
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    
    entropy = 0.0
    total = len(s)
    for count in freq.values():
        prob = count / total
        entropy -= prob * math.log(prob, 2)
    
    return entropy

def is_likely_secret(s: str) -> bool:
    """Check if a string looks like a secret/API key based on entropy and length"""
    # Minimum length for a typical secret/API key
    if len(s) < 16:
        return False
    
    # High entropy means random string
    entropy = calculate_shannon_entropy(s)
    # Typical random API key has entropy > 3.5
    return entropy > 3.5

# 中危模式 - 功能正常但容易触发误报
MEDIUM_RISK_PATTERNS = [
    (r'os\.environ', "Reads from environment variables (normal for API keys, but triggers flagging)"),
    (r'os\.getenv', "Reads from environment variables (normal for API keys, but triggers flagging)"),
    (r'subprocess\.', "Uses subprocess module to run system commands"),
    (r'os\.system', "Uses os.system to run system commands"),
    (r'os\.popen', "Uses os.popen to run system commands"),
    (r'urllib', "Uses urllib for network requests (normal for APIs, but triggers flagging)"),
    (r'requests', "Uses requests for network requests (normal for APIs, but triggers flagging)"),
    (r'http[s]?\:\/\/', "Makes external HTTP/HTTPS requests (normal for APIs, but triggers flagging)"),
    (r'fetch\(', "Uses fetch() for network requests"),
    (r'wget|curl', "Spawns wget/curl to download files"),
    (r'git clone', "Clones external git repository"),
]

# 文件扩展名扫描
SCAN_EXTENSIONS = ['.py', '.js', '.ts', '.sh', '.bash', '.cmd', '.bat']

# 默认忽略目录
DEFAULT_IGNORE_DIRS = ['.git', '.clawhub', 'node_modules', '__pycache__', '.venv', 'venv', 'build', 'dist']
# 默认忽略文件扩展名
DEFAULT_IGNORE_EXTS = ['.pyc', '.pyo', '.pyd', '.db', '.sqlite', '.sqlite3', '.log']

def parse_gitignore(root_path: Path) -> set[str]:
    """Parse .gitignore file and return set of directory names to ignore"""
    ignore_dirs = set(DEFAULT_IGNORE_DIRS)
    
    gitignore_path = root_path / '.gitignore'
    if not gitignore_path.exists():
        return ignore_dirs
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line == '' or line.startswith('#'):
                    continue
                # Get the basename (directory name) for simple matching
                if '/' in line:
                    # Take the last component
                    line = line.rsplit('/', 1)[-1]
                if line.endswith('/'):
                    line = line[:-1]
                if line:
                    ignore_dirs.add(line)
    except Exception:
        pass
    
    return ignore_dirs

def parse_security_config(root_path: Path) -> set[str]:
    """Parse .clawhub-security config file and return set of patterns to ignore"""
    ignore_patterns = set()
    
    config_path = root_path / '.clawhub-security'
    if not config_path.exists():
        return ignore_patterns
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # Skip comments and empty lines
                if line == '' or line.startswith('#'):
                    continue
                # Format: ignore: pattern
                if line.lower().startswith('ignore:'):
                    pattern = line[len('ignore:'):].strip()
                    if pattern:
                        ignore_patterns.add(pattern)
                # Simple format: just the pattern
                else:
                    ignore_patterns.add(line)
    except Exception as e:
        print(f"⚠️  Warning: Failed to parse .clawhub-security: {e}")
    
    return ignore_patterns

class ScanResult:
    def __init__(self, file_path: str, line: int, pattern: str, description: str, risk: str):
        self.file_path = file_path
        self.line = line
        self.pattern = pattern
        self.description = description
        self.risk = risk

def should_scan_file(path: Path, ignore_dirs: set[str]) -> bool:
    """Check if we should scan this file - check if any parent directory is ignored"""
    # Check if any part of the path is in ignore list
    for part in path.parts:
        if part in ignore_dirs:
            return False
    
    # Skip binary extensions
    if path.suffix.lower() in DEFAULT_IGNORE_EXTS:
        return False
    
    # Check extension
    return path.suffix.lower() in SCAN_EXTENSIONS

def scan_file(file_path: Path) -> List[ScanResult]:
    """Scan a single file for suspicious patterns"""
    results = []
    seen_patterns: set[tuple[str, str]] = set()  # (file_path, pattern) -> already reported
    
    # Regex to find quoted strings
    quoted_strings = re.compile(r'[\'"]([a-zA-Z0-9_\-]{16,})[\'"]')
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # Check high risk
            for pattern, desc in HIGH_RISK_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    key = (str(file_path), pattern)
                    if key not in seen_patterns:
                        seen_patterns.add(key)
                        results.append(ScanResult(
                            str(file_path), line_num, pattern, desc, RISK_HIGH
                        ))
            # Check medium risk
            for pattern, desc in MEDIUM_RISK_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    key = (str(file_path), pattern)
                    if key not in seen_patterns:
                        seen_patterns.add(key)
                        results.append(ScanResult(
                            str(file_path), line_num, pattern, desc, RISK_MEDIUM
                        ))
            # Check for high-entropy strings that might be hard-coded secrets
            for match in quoted_strings.finditer(line):
                candidate = match.group(1)
                if is_likely_secret(candidate):
                    key = (str(file_path), "high-entropy-secret")
                    if key not in seen_patterns:
                        seen_patterns.add(key)
                        results.append(ScanResult(
                            str(file_path), line_num, "high-entropy-secret",
                            "Found high-entropy string in quotes - this looks like a possible hard-coded secret/API key",
                            RISK_HIGH
                        ))
                    
    except Exception as e:
        results.append(ScanResult(
            str(file_path), 0, "", f"Failed to read file: {str(e)}", RISK_LOW
        ))
    
    return results

# Sensitive filenames that should not be in your skill repo
SENSITIVE_FILENAMES = [
    '.env', '.env.*',
    '*.pem', '*.key', '*.cer', '*.crt',
    'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    '*.secret', '*.token',
]

def is_sensitive_filename(filename: str) -> Optional[ScanResult]:
    """Check if filename looks like a sensitive secret file"""
    fn = filename.lower()
    
    sensitive_patterns = [
        (r'\.env', "Found .env file - may contain API keys/secrets"),
        (r'\.pem$', "Found PEM private key file"),
        (r'\.key$', "Found key file"),
        (r'id_', "Found SSH private key file"),
        (r'\.secret', "Found secret file"),
        (r'\.token', "Found token file"),
    ]
    
    for pattern, desc in sensitive_patterns:
        if re.search(pattern, fn):
            return ScanResult(
                f"{filename}", 0, f"sensitive-filename-{pattern}",
                desc, RISK_HIGH
            )
    
    return None

def scan_directory(root_path: Path) -> List[ScanResult]:
    """Recursively scan all files in directory"""
    all_results = []
    ignore_dirs = parse_gitignore(root_path)
    ignore_patterns = parse_security_config(root_path)
    
    for path in root_path.rglob('*'):
        if path.is_file():
            # Check if filename is sensitive first
            sensitive = is_sensitive_filename(path.name)
            if sensitive:
                sensitive.pattern = "sensitive-filename"
                if sensitive.pattern not in ignore_patterns:
                    all_results.append(sensitive)
            
            if should_scan_file(path, ignore_dirs):
                results = scan_file(path)
                # Filter out ignored patterns
                results = [r for r in results if r.pattern not in ignore_patterns]
                all_results.extend(results)
    
    return all_results

def get_suggestion(result: ScanResult) -> str:
    """Give modification suggestion based on finding"""
    if result.risk == RISK_HIGH:
        if "hard-coded" in result.description or "high-entropy" in result.description:
            return """❌ SUGGESTION: Never hard-code API keys/tokens in source code.
Move them to environment variables:
  Good:  api_key = os.environ.get("MY_API_KEY")
  Bad:   api_key = "abc123secret"
This also prevents your secret from being exposed in git repositories."""
        if "sensitive-filename" in result.description:
            return """❌ SUGGESTION: Found a sensitive file in your skill directory.
DO NOT commit this file to git!
If it's a real key/secret, remove it from the repo and move it to environment variables.
Add this filename to .gitignore to prevent accidental commit."""
        if "eval" in result.description or "exec" in result.description:
            return """❌ SUGGESTION: Avoid eval/exec if possible.
If you must use it, make sure:
  1. Input comes only from trusted sources
  2. Input is strictly validated/ sanitized
Arbitrary code execution from untrusted input is a critical security vulnerability."""
        if "sensitive" in result.description or "private key" in result.description:
            return """❌ SUGGESTION: Skill should never read system sensitive files.
This is what triggers real security warnings. Skills don't need access to:
  - /etc/passwd, /etc/shadow
  - Your SSH private keys in ~/.ssh
  - Your PEM/key files
Remove this code before publishing."""
        return "❌ This is a high risk pattern that should be fixed before publishing."
    
    elif result.risk == RISK_MEDIUM:
        if "environment" in result.description:
            return """⚠️ SUGGESTION: This is normal and safe!
Reading API keys from environment variables is actually BEST PRACTICE.
ClawHub's scanner flag this because any environment access looks suspicious.
Your code is fine, just add a comment in your SKILL.md explaining that you use env vars for API keys which is standard security practice."""
        if "network" in result.description or "requests" in result.description or "urllib" in result.description:
            return """⚠️ SUGGESTION: This is normal for almost all skills.
Making external HTTP requests to public APIs is completely expected.
In your SKILL.md, clearly state what APIs you call and why - this reduces user concern."""
        if "subprocess" in result.description or "system" in result.description:
            return """⚠️ SUGGESTION: Make sure:
  1. You only run pre-determined commands, never commands constructed from untrusted user input
  2. Document why you need to call system commands in your SKILL.md
Avoid: os.system(f"cmd {user_input}") where user input is uncontrolled"""
        if "download" in result.description or "git clone" in result.description:
            return """⚠️ SUGGESTION: Downloading external code at runtime is riskier.
Make sure you only download from trusted, HTTPS sources.
Consider including the code in your skill instead of downloading at runtime if possible."""
        return "⚠️ This pattern may trigger automatic suspicious flagging. Review it to make sure it's safe."
    
    return ""

def print_results(results: List[ScanResult], root_path: Path):
    """Print scan results nicely"""
    if not results:
        print("\n✅ No suspicious patterns found! Your skill is clean.")
        print("You're good to publish.")
        return
    
    # Count by risk
    counts = {RISK_HIGH: 0, RISK_MEDIUM: 0, RISK_LOW: 0}
    for r in results:
        counts[r.risk] += 1
    
    print(f"\n📊 Scan Results for {root_path}:")
    print(f"   🔴 High Risk: {counts[RISK_HIGH]} issues")
    print(f"   🟡 Medium Risk: {counts[RISK_MEDIUM]} issues (may trigger false positive flags)")
    print(f"   🟢 Low Risk: {counts[RISK_LOW]} issues")
    print()
    
    # Group by file
    by_file: Dict[str, List[ScanResult]] = {}
    for r in results:
        if r.file_path not in by_file:
            by_file[r.file_path] = []
        by_file[r.file_path].append(r)
    
    for file_path, file_results in sorted(by_file.items()):
        rel_path = os.path.relpath(file_path, str(root_path))
        print(f"📄 {rel_path}:")
        for r in file_results:
            risk_emoji = "🔴" if r.risk == RISK_HIGH else "🟡" if r.risk == RISK_MEDIUM else "🟢"
            print(f"  {risk_emoji} Line {r.line}: {r.description}")
            suggestion = get_suggestion(r)
            if suggestion:
                print(f"      {suggestion.replace(chr(10), chr(10) + '      ')}")
        print()
    
    if counts[RISK_HIGH] > 0:
        print("❗ SUMMARY: Found HIGH RISK issues. Fix these before publishing.")
        print("   High risk patterns are actually dangerous, not just false positives.")
    elif counts[RISK_MEDIUM] > 0:
        print("⚠️  SUMMARY: Found MEDIUM RISK patterns. These are likely safe but:")
        print("   - They may trigger automatic 'suspicious' flagging on ClawHub")
        print("   - Review them to confirm they're necessary and safe")
        print("   - Document them clearly in your SKILL.md")
    else:
        print("✅ SUMMARY: All issues are low risk. Good to go!")

def export_results(results: List[ScanResult], output_path: str):
    """Export results to JSON"""
    export = []
    for r in results:
        export.append({
            "file_path": r.file_path,
            "line": r.line,
            "pattern": r.pattern,
            "description": r.description,
            "risk": r.risk,
            "suggestion": get_suggestion(r)
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results exported to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='ClawHub Pre-Publish Security Scan')
    parser.add_argument('--path', required=True, help='Path to skill folder to scan')
    parser.add_argument('--output', help='Export results to JSON file')
    parser.add_argument('--user-id', required=True, help='User ID (for SkillPay billing)')
    parser.add_argument('--api-key', default=None, help='SkillPay API Key')
    args = parser.parse_args()
    
    # SkillPay 扣费
    result = skillpay_charge(args.user_id, args.api_key)
    if not result.get("success"):
        if result.get("needs_payment"):
            print(f"❌ 余额不足，请先充值。")
            print(f"🔗 充值链接: {result.get('payment_url')}")
            sys.exit(1)
        else:
            print(f"❌ 扣费失败: {result.get('message', result.get('error'))}")
            sys.exit(1)
    
    root_path = Path(args.path).resolve()
    
    if not root_path.exists():
        print(f"❌ Error: Path {root_path} does not exist")
        sys.exit(1)
    
    if not root_path.is_dir():
        print(f"❌ Error: {root_path} is not a directory")
        sys.exit(1)
    
    print(f"🔍 Scanning {root_path}...")
    results = scan_directory(root_path)
    
    print_results(results, root_path)
    
    if args.output:
        export_results(results, args.output)
    
    # Exit with error code if high risk found
    high_risk_count = sum(1 for r in results if r.risk == RISK_HIGH)
    if high_risk_count > 0:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
