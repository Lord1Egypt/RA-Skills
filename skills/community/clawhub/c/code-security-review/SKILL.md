---
name: code-security-review
description: Report only real risks, not manufactured panic. Covers injection, XSS, path traversal, insecure deserialization, authentication and authorization flaws, key leaks, insecure logging, command execution, and other common vulnerabilities.
---

# Code and System Security Review

Report only real risks, not manufactured panic.

## Use Cases

Triggers when users request a security review, code audit, security check, vulnerability analysis, security assessment, penetration test, code scan, or security review.

## Workflow

1. Identify trust boundaries, user inputs, privileged operations, and sensitive data paths.
2. Focus on checking for injection, path traversal, XSS, insecure deserialization, authentication and authorization flaws, key leaks, insecure logging, and command execution issues.
3. Assess both exploitability and impact scope; do not exaggerate low-confidence issues.
4. Mark risks with clear severity levels: critical, high, medium, low.
5. Provide directly actionable remediation recommendations; prioritize providing code patches when possible.
6. If the risk cannot be fully closed in this round, explain the residual risk and subsequent checkpoints.

## Output Format

For each risk point, output:

- **Risk Point**: Brief description of the issue's location and nature
- **Risk Level**: critical | high | medium | low
- **Impact Description**: Actual consequences if exploited
- **Remediation Plan**: Specific, actionable steps to fix the issue
- **Patch**: A code diff that can be directly applied (prioritize providing this)

When no risks are found, output a brief confirmation and do not fabricate issues.

## Common Vulnerability Checklist

See [references/checklist.md](references/checklist.md) for details, covering the OWASP Top 10 and common attack surfaces.