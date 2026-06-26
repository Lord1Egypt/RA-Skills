#!/usr/bin/env python3
"""
content-security-filter.py
Prompt injection + malware detection filter for all external content.
Run before processing ANY external URL, tweet, article, or pasted text.

Usage:
    python3 content-security-filter.py --text "content to scan"
    python3 content-security-filter.py --file /path/to/file.txt
    python3 content-security-filter.py --url "https://example.com" (fetches + scans)
    echo "text to scan" | python3 content-security-filter.py

Returns: JSON with {safe: bool, risk_level: str, findings: list, sanitized: str}
Exit 0 = safe, Exit 1 = threat detected
"""

import sys
import re
import json
import argparse
import unicodedata
import base64
import urllib.request

# ── Injection pattern library ──────────────────────────────────────────────────

INJECTION_PATTERNS = [
    # Classic overrides
    (r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|context)", "OVERRIDE_ATTEMPT"),
    (r"forget\s+(everything|all|your\s+instructions)", "OVERRIDE_ATTEMPT"),
    (r"disregard\s+(all\s+)?(previous|prior|above)", "OVERRIDE_ATTEMPT"),
    (r"your\s+(new\s+)?(instructions?|rules?|system\s+prompt)\s+(are|is)\s*[:\-]", "INSTRUCTION_HIJACK"),
    (r"(new|updated)\s+system\s+prompt\s*[:\-]", "SYSTEM_PROMPT_INJECT"),
    (r"you\s+are\s+now\s+(a\s+)?(new|different|updated)", "PERSONA_HIJACK"),
    (r"act\s+as\s+(if\s+you\s+are|a\s+new|an?\s+unrestricted)", "PERSONA_HIJACK"),
    (r"DAN\s+mode|jailbreak|unrestricted\s+mode", "JAILBREAK_ATTEMPT"),

    # Data exfiltration attempts
    (r"(send|email|dm|post|share|leak|exfiltrate)\s+(all\s+)?(user|private|secret|confidential|workspace)", "EXFILTRATION_ATTEMPT"),
    (r"(reveal|disclose|print|output|show)\s+(your\s+)?(system\s+prompt|instructions?|api\s+key|token|password|secret)", "CREDENTIAL_EXFIL"),
    (r"what\s+are\s+your\s+(hidden\s+)?(instructions?|rules?|system\s+prompt)", "PROMPT_PROBE"),
    (r"(access|read|dump|extract)\s+(memory|files?|private|workspace)\s+(files?|data|content)", "DATA_EXFIL"),

    # Fake system/meta messages
    (r"\[system\s*message\]|\[admin\]|\[override\]|\[root\]|\[superuser\]", "FAKE_SYSTEM_MSG"),
    (r"<\s*system\s*>|<\s*/system\s*>|\[\[system\]\]", "FAKE_SYSTEM_TAG"),
    (r"(ASSISTANT|SYSTEM|USER)\s*:\s*(ignore|forget|your\s+new)", "FAKE_ROLE_INJECT"),

    # Encoded payloads
    (r"base64\s*:\s*[A-Za-z0-9+/]{20,}={0,2}", "ENCODED_PAYLOAD"),

    # Credential harvesting
    (r"(enter|provide|give|send)\s+(your\s+)?(api\s+key|password|token|secret|credential)", "CREDENTIAL_HARVEST"),

    # Tool/function abuse
    (r"(call|invoke|execute|run)\s+(the\s+)?(exec|shell|bash|python|eval)\s+(tool|function|command)", "TOOL_ABUSE"),
    (r"rm\s+-rf|os\.system|subprocess\.(call|run|Popen)", "COMMAND_INJECT"),
]

# Hidden text techniques
INVISIBLE_CHARS = [
    '\u200b',  # zero-width space
    '\u200c',  # zero-width non-joiner
    '\u200d',  # zero-width joiner
    '\u2060',  # word joiner
    '\ufeff',  # zero-width no-break space (BOM)
    '\u00ad',  # soft hyphen
    '\u034f',  # combining grapheme joiner
]

RISK_LEVELS = {
    "OVERRIDE_ATTEMPT": "CRITICAL",
    "INSTRUCTION_HIJACK": "CRITICAL",
    "SYSTEM_PROMPT_INJECT": "CRITICAL",
    "PERSONA_HIJACK": "HIGH",
    "JAILBREAK_ATTEMPT": "CRITICAL",
    "EXFILTRATION_ATTEMPT": "CRITICAL",
    "CREDENTIAL_EXFIL": "CRITICAL",
    "PROMPT_PROBE": "HIGH",
    "DATA_EXFIL": "HIGH",
    "FAKE_SYSTEM_MSG": "HIGH",
    "FAKE_SYSTEM_TAG": "HIGH",
    "FAKE_ROLE_INJECT": "HIGH",
    "ENCODED_PAYLOAD": "MEDIUM",
    "CREDENTIAL_HARVEST": "HIGH",
    "TOOL_ABUSE": "CRITICAL",
    "COMMAND_INJECT": "CRITICAL",
    "INVISIBLE_CHARS": "MEDIUM",
    "SUSPICIOUS_BASE64": "MEDIUM",
}


def scan_content(text: str) -> dict:
    findings = []
    max_risk = "SAFE"
    risk_order = ["SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

    # 1. Check for invisible/hidden characters
    invisible_found = [c for c in text if c in INVISIBLE_CHARS]
    if invisible_found:
        findings.append({
            "type": "INVISIBLE_CHARS",
            "risk": "MEDIUM",
            "detail": f"Found {len(invisible_found)} invisible/zero-width characters — possible hidden text injection"
        })
        if risk_order.index("MEDIUM") > risk_order.index(max_risk):
            max_risk = "MEDIUM"

    # 2. Check for suspicious base64 blobs
    b64_pattern = re.findall(r'[A-Za-z0-9+/]{40,}={0,2}', text)
    for blob in b64_pattern:
        try:
            decoded = base64.b64decode(blob + '==').decode('utf-8', errors='ignore')
            # Scan decoded content recursively (one level)
            if any(word in decoded.lower() for word in ['ignore', 'system', 'prompt', 'instruction', 'secret', 'token']):
                findings.append({
                    "type": "SUSPICIOUS_BASE64",
                    "risk": "MEDIUM",
                    "detail": f"Base64 blob decodes to suspicious content: {decoded[:80]}..."
                })
                if risk_order.index("MEDIUM") > risk_order.index(max_risk):
                    max_risk = "MEDIUM"
        except Exception:
            pass

    # 3. Pattern matching (case-insensitive)
    text_lower = text.lower()
    for pattern, threat_type in INJECTION_PATTERNS:
        match = re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
        if match:
            risk = RISK_LEVELS.get(threat_type, "MEDIUM")
            findings.append({
                "type": threat_type,
                "risk": risk,
                "matched": match.group(0)[:100],
                "detail": f"Injection pattern detected: {threat_type}"
            })
            if risk_order.index(risk) > risk_order.index(max_risk):
                max_risk = risk

    # 4. Unicode normalization check (homoglyph attacks)
    normalized = unicodedata.normalize('NFKC', text)
    if normalized != text:
        # Check if normalization reveals injection patterns
        norm_lower = normalized.lower()
        for pattern, threat_type in INJECTION_PATTERNS:
            if re.search(pattern, norm_lower, re.IGNORECASE):
                findings.append({
                    "type": "HOMOGLYPH_INJECT",
                    "risk": "HIGH",
                    "detail": "Homoglyph/unicode substitution hiding injection pattern"
                })
                if risk_order.index("HIGH") > risk_order.index(max_risk):
                    max_risk = "HIGH"
                break

    # 5. Sanitize: strip invisible chars and normalize
    sanitized = ''.join(c for c in text if c not in INVISIBLE_CHARS)
    sanitized = unicodedata.normalize('NFKC', sanitized)

    safe = max_risk in ["SAFE", "LOW"]

    return {
        "safe": safe,
        "risk_level": max_risk,
        "findings": findings,
        "finding_count": len(findings),
        "sanitized": sanitized[:5000] if not safe else sanitized,  # truncate if threat
        "chars_scanned": len(text),
    }


def fetch_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; SecurityFilter/1.0)",
        "Accept": "text/html,text/plain"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read(500_000)  # 500KB max
            return raw.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"[FETCH_ERROR: {e}]"


def main():
    parser = argparse.ArgumentParser(description="Content Security Filter — detects prompt injection and malicious content")
    parser.add_argument("--text", help="Text to scan")
    parser.add_argument("--file", help="File to scan")
    parser.add_argument("--url", help="URL to fetch and scan")
    parser.add_argument("--quiet", action="store_true", help="JSON output only (no stderr)")
    args = parser.parse_args()

    if args.text:
        content = args.text
    elif args.file:
        with open(args.file) as f:
            content = f.read()
    elif args.url:
        if not args.quiet:
            print(f"Fetching: {args.url}", file=sys.stderr)
        content = fetch_url(args.url)
    else:
        # Read from stdin
        content = sys.stdin.read()

    result = scan_content(content)

    if not args.quiet:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

    return 0 if result["safe"] else 1


if __name__ == "__main__":
    sys.exit(main())
