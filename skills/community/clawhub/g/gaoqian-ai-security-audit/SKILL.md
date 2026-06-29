---
name: AI Agent Security Audit
slug: ai-security-audit
description: Comprehensive AI agent security auditing skill covering prompt injection detection, permission boundary analysis, malicious skill scanning, credential leak detection, and runtime behavior monitoring. Produces audit reports with risk scoring and remediation recommendations.
version: 1.0.0
author: ai-gaoqian
tags:
  - security
  - audit
  - compliance
  - agent-safety
  - vulnerability-scanning
metadata:
  openclaw:
    requires: "python>=3.10, openclaw>=0.9.0"
---

# AI Agent Security Audit

Comprehensive security auditing for AI agent deployments. Detects vulnerabilities across prompt handling, tool permissions, skill behavior, credential management, and runtime operations.

## Usage

Invoke with a target agent configuration path or skill directory to scan:

```
audit: scan /path/to/agent/config
audit: review installed skills
audit: monitor runtime behavior for 30 minutes
```

## Execution Flow

1. **Configuration Audit** — Parse agent config YAML, enumerate permissions, identify over-privileged tool access
2. **Prompt Injection Test** — Run 12 injection patterns (DAN, encoding bypass, role confusion, token smuggling) and score resilience
3. **Skill Scan** — Analyze each installed skill's SKILL.md for suspicious patterns (eval(), shell_exec, credential references, network requests)
4. **Credential Hygiene** — Scan workspace for hardcoded tokens, API keys, private keys in plaintext files
5. **Runtime Monitor** — Observe agent behavior for N minutes, flag any unexpected tool calls, network connections, or file access patterns
6. **Generate Report** — Risk score 0-100, criticality matrix, prioritized remediation steps

## Output Format

```markdown
# Security Audit Report
- **Audit Date**: YYYY-MM-DD HH:MM
- **Audit Scope**: [target]
- **Overall Risk Score**: 67/100 (MEDIUM)

## Critical Findings (2)
- [CRITICAL] Unrestricted shell_executor access allows arbitrary command execution
- [CRITICAL] Skill "data-export" sends data to external endpoint without user consent

## High Findings (3)
- ...

## Recommendations
1. Add allowlist for shell_executor commands
2. Sandbox "data-export" skill network calls
3. ...
```

## Notes

- Requires read access to agent config directory and installed skills path
- Runtime monitoring requires agent process access
- All findings include file paths and line numbers for traceability
- Recommended for any production agent deployment, especially those handling user data or financial operations
