#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

def scan_text_for_patterns(text):
    patterns = {
        "url_credential_leak": [r"token=", r"gatewayUrl=", r"key=", r"secret=", r"Authorization"],
        "risky_proxy_to_18789": [r"reverse_proxy\s+(127\.0\.0\.1|localhost):18789", r"proxy_pass\s+http://(127\.0\.0\.1|localhost):18789"]
    }
    findings = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for risk_type, ps in patterns.items():
            for p in ps:
                if re.search(p, line, re.IGNORECASE):
                    findings.append(f"[{risk_type}] L{i}: {line.strip()}")
    return findings

def main():
    scan_targets = []
    if Path("/etc/caddy").exists():
        scan_targets.extend(Path("/etc/caddy").rglob("*.conf"))
        scan_targets.append(Path("/etc/caddy/Caddyfile"))
    if Path("/etc/nginx").exists():
        scan_targets.extend(Path("/etc/nginx").rglob("*.conf"))
    
    all_findings = []
    for p in set(scan_targets):
        if p.exists() and p.is_file():
            try:
                txt = p.read_text("utf-8", errors="ignore")
                file_findings = scan_text_for_patterns(txt)
                if file_findings:
                    all_findings.append(f"--- File: {str(p)} ---")
                    all_findings.extend(file_findings)
            except Exception:
                continue
                
    result = {
        "status": "risks_found" if all_findings else "clean",
        "findings": all_findings if all_findings else ["未扫描到明显的凭据泄露或 18789 端口直接转发规则。"]
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()