#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Review scan results and give detailed fixing suggestions"""

import os
import argparse
import json
from pathlib import Path
from typing import List, Dict

# 解决Windows编码问题
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def print_best_practices():
    """Print security best practices for ClawHub skills"""
    print("""
📋 ClawHub Skill Security Best Practices

✅ DO:
  1. Store API keys/tokens in environment variables, NEVER hard-code them
     Example: `api_key = os.environ.get("MY_API_KEY")` ✓
     NOT:    `api_key = "secretkeyhere123"` ✗

  2. Clearly document all external API calls in your SKILL.md
     Tell users what APIs you call and why - transparency reduces concern

  3. Validate all user input before passing to subprocess/os.system
     Never do: `os.system(f"ping {user_input}")` when user_input comes from outside

  4. Keep sensitive files out of git with .gitignore
     Add `.env`, `*.pem`, `*.key`, `id_*` to your .gitignore

  5. Prefer standard library urllib/requests over dynamic execution
     It's okay to make API requests - this is what almost all skills do!

❌ DON'T:
  1. Read sensitive system files like /etc/passwd, ~/.ssh/*, /etc/shadow
     Skills almost never need this, it will definitely flag you as suspicious

  2. Use eval()/exec() on untrusted input
     This is a critical security vulnerability, avoid if at all possible

  3. Download and execute arbitrary code from external sources
     If you must do this, only use HTTPS from trusted sources

  4. Exfiltrate user files, environment variables, or system information
     Don't send anything to external servers without user knowledge

⁉️ Common False Positives (you're okay but scanner will flag):
  - Reading environment variables → This is ACTUALLY best practice! Just document it.
  - Making API requests to get data → This is normal for almost all skills.
  - Calling system commands for legitimate purposes → Document why you need it.

The ClawHub automatic scanner flags any code that does these things because
they *can* be used maliciously. But for legitimate skills, they're perfectly fine.
Just document clearly what you're doing and why, and users will understand.
""")

def review_scan_results(json_path: str):
    """Review existing scan results from JSON"""
    with open(json_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    high_risk = [r for r in results if r['risk'] == 'high']
    medium_risk = [r for r in results if r['risk'] == 'medium']
    
    print(f"\n📋 Reviewing scan results from {json_path}:")
    print(f"   🔴 High Risk: {len(high_risk)}")
    print(f"   🟡 Medium Risk: {len(medium_risk)}")
    
    if high_risk:
        print("\n🔴 HIGH RISK ITEMS - MUST FIX BEFORE PUBLISHING:\n")
        for i, issue in enumerate(high_risk, 1):
            print(f"{i}. {issue['file_path']}:{issue['line']}")
            print(f"   Issue: {issue['description']}")
            print(f"   Suggestion: {issue['suggestion']}\n")
    
    if medium_risk:
        print("\n🟡 MEDIUM RISK ITEMS - REVIEW THESE:\n")
        for i, issue in enumerate(medium_risk, 1):
            print(f"{i}. {issue['file_path']}:{issue['line']}")
            print(f"   Issue: {issue['description']}")
            print(f"   Suggestion: {issue['suggestion']}\n")
    
    if not high_risk and not medium_risk:
        print("\n✅ No issues found! Your skill is ready to publish.")

def main():
    parser = argparse.ArgumentParser(description='Review security scan results')
    parser.add_argument('--scan-json', help='JSON output from scan.py')
    args = parser.parse_args()
    
    if args.scan_json:
        review_scan_results(args.scan_json)
    
    print_best_practices()

if __name__ == "__main__":
    main()
