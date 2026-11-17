#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doc-compliance-assistant · document processing with compliance built-in.

Reads a text/markdown file, normalizes encoding/line-endings/whitespace, then
scans for PII, credentials, and sensitive patterns. Cleaning and scanning happen
in one pass — "process means compliant".

Pure stdlib. Exit codes: 0 clean, 1 findings, 2 usage error.
"""
import argparse
import json
import os
import re
import sys

RULES = [
    ("email",            re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "PII"),
    ("cn_mobile",        re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),                     "PII"),
    ("cn_id_card",       re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),                 "PII"),
    ("aws_access_key",   re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                       "secret"),
    ("github_token",     re.compile(r"\bghp_[A-Za-z0-9]{36,}\b"),                   "secret"),
    ("openai_key",       re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),                    "secret"),
    ("private_key_block",re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"), "secret"),
    ("url_with_basic_auth", re.compile(r"https?://[^\s/:@]+:[^\s/@]+@"),            "secret"),
    ("ipv4",             re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),                "info"),
]


def detect_encoding(path):
    with open(path, "rb") as f:
        head = f.read(4)
    if head.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if head.startswith(b"\xff\xfe") or head.startswith(b"\xfe\xff"):
        return "utf-16"
    if head.startswith(b"\x00\x00\xfe\xff"):
        return "utf-32"
    return "utf-8"


def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = text.replace("\t", "    ")
    if not text.endswith("\n"):
        text += "\n"
    return text


def scan(text):
    findings = []
    for name, pat, severity in RULES:
        for m in pat.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = m.group(0)
            masked = snippet[:3] + "***" + snippet[-3:] if len(snippet) > 8 else "***"
            findings.append({
                "rule": name,
                "severity": severity,
                "line": line_no,
                "match_masked": masked,
            })
    return findings


def main():
    ap = argparse.ArgumentParser(
        description="doc-compliance-assistant · 文档清洗+合规扫描一体 / clean + compliance-scan in one pass"
    )
    ap.add_argument("--file", help="input text/markdown file")
    ap.add_argument("--out", help="write cleaned text here (requires --clean)")
    ap.add_argument("--clean", action="store_true", help="also emit normalized/cleaned text")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    ap.add_argument("--list-rules", action="store_true", help="print all scanner rules and exit")
    a = ap.parse_args()

    if a.list_rules:
        for name, _, sev in RULES:
            print("%-22s %s" % (name, sev))
        sys.exit(0)

    if not a.file:
        ap.error("--file is required (unless --list-rules)")
    if a.clean and not a.out:
        ap.error("--clean requires --out <path>")
    if not os.path.isfile(a.file):
        ap.error("file not found: %s" % a.file)

    enc = detect_encoding(a.file)
    with open(a.file, encoding=enc, errors="replace") as f:
        raw = f.read()

    cleaned = clean_text(raw)
    findings = scan(cleaned)

    if a.clean:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(cleaned)

    n_secret = sum(1 for x in findings if x["severity"] == "secret")
    n_pii = sum(1 for x in findings if x["severity"] == "PII")
    n_info = sum(1 for x in findings if x["severity"] == "info")

    result = {
        "file": a.file,
        "encoding_detected": enc,
        "chars": len(cleaned),
        "findings_total": len(findings),
        "findings_secret": n_secret,
        "findings_pii": n_pii,
        "findings_info": n_info,
        "findings": findings,
        "cleaned_written": a.out if a.clean else None,
    }

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("file: %s ｜ encoding: %s ｜ chars: %d" % (a.file, enc, len(cleaned)))
        print("findings: %d (secret=%d pii=%d info=%d)" % (len(findings), n_secret, n_pii, n_info))
        for x in findings:
            print("  - [%s] %s line=%d match=%s" % (x["severity"], x["rule"], x["line"], x["match_masked"]))
        if a.clean:
            print("cleaned -> %s" % a.out)

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
