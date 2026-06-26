#!/usr/bin/env python3
"""
Bug Bounty Report Template Generator
Generates professional reports for HackerOne, Bugcrowd, etc.
"""

import argparse
import sys
import json
from datetime import datetime

CWE_MAP = {
    "xss": {"cwe": "CWE-79", "name": "Cross-site Scripting", "cvss_base": 6.1,
             "description": "Improper Neutralization of Input During Web Page Generation"},
    "idor": {"cwe": "CWE-639", "name": "Insecure Direct Object Reference", "cvss_base": 7.5,
              "description": "Authorization Bypass Through User-Controlled Key"},
    "sqli": {"cwe": "CWE-89", "name": "SQL Injection", "cvss_base": 9.8,
              "description": "Improper Neutralization of Special Elements used in an SQL Command"},
    "ssrf": {"cwe": "CWE-918", "name": "Server-Side Request Forgery", "cvss_base": 8.6,
              "description": "Server-Side Request Forgery"},
    "rce": {"cwe": "CWE-78", "name": "OS Command Injection", "cvss_base": 9.8,
             "description": "Improper Neutralization of Special Elements used in an OS Command"},
    "auth-bypass": {"cwe": "CWE-287", "name": "Improper Authentication", "cvss_base": 9.8,
                     "description": "Improper Authentication"},
    "info-disclosure": {"cwe": "CWE-200", "name": "Information Exposure", "cvss_base": 5.3,
                         "description": "Exposure of Sensitive Information to an Unauthorized Actor"},
    "csrf": {"cwe": "CWE-352", "name": "Cross-Site Request Forgery", "cvss_base": 6.5,
              "description": "Cross-Site Request Forgery"},
    "redirect": {"cwe": "CWE-601", "name": "Open Redirect", "cvss_base": 6.1,
                  "description": "URL Redirection to Untrusted Site"},
    "path-traversal": {"cwe": "CWE-22", "name": "Path Traversal", "cvss_base": 7.5,
                        "description": "Improper Limitation of a Pathname to a Restricted Directory"},
    "xxe": {"cwe": "CWE-611", "name": "XML External Entity", "cvss_base": 9.1,
             "description": "Improper Restriction of XML External Entity Reference"},
}

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


def generate_report(args):
    vuln = CWE_MAP.get(args.type, {
        "cwe": "CWE-XXX",
        "name": args.type or "Custom Vulnerability",
        "cvss_base": 5.0,
        "description": "See description below"
    })

    severity = args.severity or "medium"
    target = args.target or "target.com"
    title = args.title or f"{vuln['name']} in {target}"
    date = datetime.now().strftime("%Y-%m-%d")

    report = f"""# {title}

**Date:** {date}
**Researcher:** [Your Name / Handle]
**Target:** {target}
**Severity:** {severity.upper()}
**CWE:** {vuln['cwe']} — {vuln['description']}
**CVSS Base Score:** {vuln['cvss_base']}

---

## Summary

A {vuln['name'].lower()} vulnerability was identified in {target} that allows an attacker to [describe impact briefly].

## Steps to Reproduce

1. Navigate to `https://{target}/[vulnerable-endpoint]`
2. [Step 2 — e.g., Intercept the request using Burp Suite]
3. [Step 3 — e.g., Modify the `id` parameter to `../admin`]
4. [Step 4 — e.g., Observe that the response contains admin data]

## Proof of Concept

```
# Request
GET /api/v1/users/[ATTACKER_INPUT] HTTP/1.1
Host: {target}
Authorization: Bearer [TOKEN]

# Response
HTTP/1.1 200 OK
{{
  "sensitive_data": "..."
}}
```

**Screenshots/Video:** [Attach evidence]

## Impact

An attacker can:
- [Impact 1 — e.g., Access other users' private data]
- [Impact 2 — e.g., Perform actions on behalf of other users]
- [Impact 3 — e.g., Escalate privileges to admin]

## Remediation

- [Fix suggestion 1 — e.g., Implement proper authorization checks on all API endpoints]
- [Fix suggestion 2 — e.g., Validate user ownership of requested resources]
- [Fix suggestion 3 — e.g., Add rate limiting to prevent enumeration]

## References

- [{vuln['cwe']} — MITRE](https://cwe.mitre.org/data/definitions/{vuln['cwe'].split('-')[1]}.html)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
"""

    if args.platform == "hackerone":
        report += "\n## HackerOne Submission Checklist\n"
        report += "- [ ] Vulnerability type selected\n"
        report += "- [ ] Asset/scope confirmed\n"
        report += "- [ ] Proof of concept attached\n"
        report += "- [ ] Impact clearly stated\n"
        report += "- [ ] No destructive testing performed\n"
    elif args.platform == "bugcrowd":
        report += "\n## Bugcrowd Submission Checklist\n"
        report += "- [ ] Priority/rating selected\n"
        report += "- [ ] Target confirmed in scope\n"
        report += "- [ ] Evidence attached\n"
        report += "- [ ] Steps to reproduce complete\n"

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


def main():
    parser = argparse.ArgumentParser(description="Bug Bounty Report Generator")
    parser.add_argument("--platform", choices=["hackerone", "bugcrowd", "generic"], default="generic")
    parser.add_argument("--type", choices=list(CWE_MAP.keys()) + ["custom"], default="custom")
    parser.add_argument("--title", help="Report title")
    parser.add_argument("--severity", choices=["critical", "high", "medium", "low", "info"])
    parser.add_argument("--target", help="Target domain")
    parser.add_argument("--output", "-o", help="Output file")
    args = parser.parse_args()
    generate_report(args)


if __name__ == "__main__":
    main()
