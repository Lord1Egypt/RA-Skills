---
name: agent-firewall
description: "Real-time input/output filtering for agent communications. Block prompt injection, data exfiltration, and unauthorized commands before they reach the model."
metadata: {"openclaw":{"emoji":"🧱","category":"blue-team"}}
---

# Agent Firewall — Input/Output Guardian

## Architecture

```
[Channel Input] → [INPUT FILTER] → [Agent/Model] → [OUTPUT FILTER] → [Channel Output]
                        ↓                                  ↓
                  ┌─────────────┐                  ┌──────────────┐
                  │ Block List  │                  │ Secret Scan  │
                  │ Pattern DB  │                  │ PII Redact   │
                  │ Rate Limit  │                  │ Path Scrub   │
                  │ Encoding Det│                  │ URL Checker  │
                  └─────────────┘                  └──────────────┘
```

## Input Filters

| # | Filter | Description |
|---|--------|-------------|
| 1 | Injection patterns | Regex + heuristic match for "ignore previous", "you are now", role confusion |
| 2 | Unicode sanitizer | Strip zero-width chars, control characters, RTL overrides |
| 3 | Encoding detector | Detect Base64, hex, ROT13 encoded payloads in user messages |
| 4 | Role confusion | Detect fake system messages, assistant impersonation |
| 5 | Rate limiter | Max messages per user per channel per minute |
| 6 | Size limiter | Reject inputs exceeding token budget |

## Output Filters

| # | Filter | Description |
|---|--------|-------------|
| 1 | Secret scanner | High-entropy strings + known patterns (AWS key, GitHub token) |
| 2 | PII redactor | Email, phone, SSN, credit card → `[REDACTED]` |
| 3 | Path scrubber | Remove internal filesystem paths from outputs |
| 4 | URL checker | Block responses containing known malicious URLs |
| 5 | Consistency check | Verify output doesn't contradict system prompt directives |

## Configuration

```yaml
# .security/firewall-rules.yaml
input:
  injection_patterns:
    - pattern: "ignore (all )?previous instructions"
      action: BLOCK
      severity: CRITICAL
    - pattern: "you are now (?!helping)"
      action: BLOCK
      severity: HIGH
  rate_limit:
    max_per_minute: 30
    max_per_hour: 500
  max_input_tokens: 4096

output:
  secret_patterns:
    - name: aws_key
      pattern: "AKIA[0-9A-Z]{16}"
      action: REDACT
    - name: github_token
      pattern: "gh[ps]_[A-Za-z0-9_]{36,}"
      action: REDACT
  pii_redaction: true
  path_scrubbing: true
```

## Guardrails

- Firewall rules are append-only in production — deletion requires human approval
- False positives → log, alert, pass through with warning (don't silently drop)
- All blocks are logged with: timestamp, rule matched, full context, channel, user hash
- Firewall itself cannot be disabled by agent instructions
- Rules file is read-only from the agent's perspective
