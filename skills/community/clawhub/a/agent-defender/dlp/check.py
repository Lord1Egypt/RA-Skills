#!/usr/bin/env python3
"""
DLP脱敏拦截模块
"""
import os
import re
import json

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

# 敏感数据规则
DLP_RULES = {
    # 中国身份
    "china_idcard": {
        "pattern": r"[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
        "risk": "CRITICAL",
        "action": "BLOCK"
    },
    "china_phone": {
        "pattern": r"1[3-9]\d{9}",
        "risk": "HIGH",
        "action": "SANITIZE"
    },
    
    # 通用密钥
    "api_key": {
        "pattern": r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})",
        "risk": "CRITICAL",
        "action": "BLOCK"
    },
    "aws_key": {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "risk": "CRITICAL",
        "action": "BLOCK"
    },
    "private_key": {
        "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
        "risk": "CRITICAL",
        "action": "BLOCK"
    },
    
    # 通用
    "email": {
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "risk": "MEDIUM",
        "action": "SANITIZE"
    },
    "ip_address": {
        "pattern": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        "risk": "LOW",
        "action": "LOG"
    },
    
    # 银行卡
    "credit_card": {
        "pattern": r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}",
        "risk": "CRITICAL",
        "action": "BLOCK"
    },
    
    # 密码
    "password": {
        "pattern": r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?([^\s'\"]{8,})",
        "risk": "HIGH",
        "action": "SANITIZE"
    }
}

def sanitize_phone(phone):
    """手机号脱敏"""
    if len(phone) == 11:
        return phone[:3] + "****" + phone[7:]
    return "***"

def sanitize_idcard(idcard):
    """身份证脱敏"""
    if len(idcard) >= 8:
        return idcard[:3] + "**********" + idcard[-4:]
    return "************"

def sanitize_key(key):
    """密钥脱敏"""
    if len(key) > 8:
        return key[:4] + "****" + key[-4:]
    return "****"

def sanitize_email(email):
    """邮箱脱敏"""
    parts = email.split("@")
    if len(parts) == 2:
        name = parts[0]
        if len(name) > 2:
            name = name[:2] + "***"
        return f"{name}@{parts[1]}"
    return "***@***"

def sanitize(text):
    """脱敏处理"""
    findings = []
    sanitized = text
    
    for name, rule in DLP_RULES.items():
        pattern = rule["pattern"]
        
        if rule["action"] == "SANITIZE":
            if name == "china_phone":
                sanitized = re.sub(pattern, lambda m: sanitize_phone(m.group()), sanitized)
            elif name == "china_idcard":
                sanitized = re.sub(pattern, lambda m: sanitize_idcard(m.group()), sanitized)
            elif name in ["api_key", "aws_key", "private_key"]:
                sanitized = re.sub(pattern, lambda m: sanitize_key(m.group()), sanitized)
            elif name == "email":
                sanitized = re.sub(pattern, lambda m: sanitize_email(m.group()), sanitized)
        
        # 记录发现
        matches = re.findall(pattern, text)
        if matches:
            findings.append({
                "type": name,
                "count": len(matches),
                "risk": rule["risk"],
                "action": rule["action"]
            })
    
    return sanitized, findings

def detect(text):
    """检测敏感数据"""
    findings = []
    
    for name, rule in DLP_RULES.items():
        matches = re.findall(rule["pattern"], text)
        if matches:
            findings.append({
                "type": name,
                "count": len(matches),
                "risk": rule["risk"],
                "action": rule["action"],
                "matches": matches[:3]  # 最多显示3个
            })
    
    return findings

def check(data):
    """检查数据"""
    if isinstance(data, str):
        findings = detect(data)
    else:
        findings = []
        for key, value in data.items():
            if isinstance(value, str):
                findings.extend(detect(f"{key}: {value}"))
    
    return {
        "findings": findings,
        "has_critical": any(f["risk"] == "CRITICAL" for f in findings),
        "has_block": any(f["action"] == "BLOCK" for f in findings)
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="DLP检测")
    parser.add_argument("data", help="待检测数据")
    parser.add_argument("--sanitize", action="store_true", help="脱敏处理")
    
    args = parser.parse_args()
    
    findings = detect(args.data)
    
    if not findings:
        print("✅ 未检测到敏感数据")
        return
    
    print(f"⚠️ 检测到 {len(findings)} 类敏感数据:\n")
    
    for f in findings:
        print(f"[{f['risk']}] {f['type']}: {f['count']}处 ({f['action']})")
    
    if args.sanitize:
        sanitized, _ = sanitize(args.data)
        print(f"\n脱敏后:\n{sanitized[:200]}...")

if __name__ == "__main__":
    main()
