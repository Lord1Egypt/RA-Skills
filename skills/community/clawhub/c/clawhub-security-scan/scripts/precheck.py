#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive pre-publish checklist wizard"""

import sys
import os
import argparse
from pathlib import Path

# 解决Windows编码问题
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
        "description": "ClawHub Security Scan - Pre-Publish Check"
    }
    return _post("/billing/charge", body, k)

CHECKLIST = [
    {
        "question": "Does your skill hard-code any API keys, tokens, or passwords in source code?",
        "yes": "❌ WARNING: Never hard-code secrets in source code. Move them to environment variables.",
        "no": "✅ Good practice: secrets in environment variables",
        "default": False,
    },
    {
        "question": "Does your skill read sensitive system files (~/.ssh, /etc/passwd, /etc/shadow, private keys)?",
        "yes": "❌ WARNING: Skills should not need to read system sensitive files. This will definitely get flagged as suspicious.",
        "no": "✅ Good: no sensitive file access",
        "default": False,
    },
    {
        "question": "Does your skill download and execute arbitrary code from external sources at runtime?",
        "yes": "⚠️   NOTE: Make sure you only download from trusted HTTPS sources, and document this clearly in your SKILL.md.",
        "no": "✅ Good: no runtime code download",
        "default": False,
    },
    {
        "question": "Does your skill use eval(), exec(), or other dynamic code execution on untrusted input?",
        "yes": "❌ WARNING: Avoid dynamic code execution if possible. If you must use it, strictly validate all input.",
        "no": "✅ Good: no unsafe dynamic code execution",
        "default": False,
    },
    {
        "question": "Have you documented all external API calls in your SKILL.md?",
        "yes": "✅ Good: documented external APIs",
        "no": "⚠️   REMINDER: Document what APIs you call and why - this reduces user concern",
        "default": False,
    },
    {
        "question": "Does your skill call any external APIs?",
        "yes": "👍 OK: Just make sure they're documented",
        "no": "✅ Perfect: no external network calls",
        "default": True,
    },
    {
        "question": "Does your skill run user-supplied system commands (subprocess/os.system)?",
        "yes": "⚠️   REMINDER: Never run commands built from untrusted user input. Document why you need this.",
        "no": "✅ Good: no arbitrary system command execution",
        "default": False,
    },
    {
        "question": "Have you added sensitive files (.env, *.pem, *.key) to .gitignore?",
        "yes": "✅ Good practice: secrets not committed to git",
        "no": "⚠️   REMINDER: Add your secret files to .gitignore to avoid accidental commit",
        "default": False,
    },
]

def ask_yes_no(question: str, default: bool) -> bool:
    """Ask a yes/no question and return boolean answer"""
    default_text = "Y/n" if default else "y/N"
    prompt = f"{question} [{default_text}] "
    
    while True:
        try:
            answer = input(prompt).strip().lower()
        except EOFError:
            return default
        
        if not answer:
            return default
        if answer in ['y', 'yes']:
            return True
        if answer in ['n', 'no']:
            return False
        
        print("Please answer yes/no")

def run_precheck():
    """Run the interactive pre-publish checklist"""
    print("🔍 ClawHub Pre-Publish Security Check")
    print("=" * 60)
    print()
    print("Answer the following questions to make sure your skill is ready")
    print("for publishing. This helps you avoid common issues that can")
    print("trigger automatic suspicious flagging on ClawHub.")
    print()
    
    results = []
    for item in CHECKLIST:
        ans = ask_yes_no(item["question"], item["default"])
        results.append({**item, "answer": ans})
        if ans:
            print(item["yes"])
        else:
            print(item["no"])
        print()
    
    print("=" * 60)
    print("📋 Pre-Publish Check Summary")
    print()
    
    issues_found = 0
    warnings = 0
    
    for item in results:
        if item["answer"]:
            if "WARNING" in item["yes"]:
                issues_found += 1
            elif "REMINDER" in item["yes"]:
                warnings += 1
            print(f"{item['yes']} → {item['question']}")
        else:
            if "WARNING" in item["no"]:
                issues_found += 1
            elif "REMINDER" in item["no"]:
                warnings += 1
    
    print()
    if issues_found == 0 and warnings == 0:
        print("✅ ALL CHECKS PASSED! Your skill looks good to publish.")
    elif issues_found == 0:
        print(f"⚠️  {warnings} reminder(s) to address before publishing.")
        print("   You can still publish, just address the reminders above.")
    else:
        print(f"❗ Found {issues_found} issue(s) that should be fixed before publishing.")
        print("   Fix these issues to reduce the chance of getting flagged as suspicious.")
    
    print()
    print("After fixing any issues, you can run:")
    print("  python scripts/scan.py --path .")
    print("to do a full code scan before publishing.")
    print()

def main():
    parser = argparse.ArgumentParser(description='Interactive pre-publish security checklist')
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
    
    run_precheck()

if __name__ == "__main__":
    import argparse
    main()
