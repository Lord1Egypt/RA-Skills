---
name: code-auditor
description: Audit any GitHub repo or raw code for security, quality, or gas optimization. Returns score, findings, severity counts, and summary.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🔍"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Code Auditor

Audit any GitHub repository or raw code for security vulnerabilities, code quality issues, and best practices. Supports targeted audits by focus area. Returns a score, severity-scored findings, and actionable summary.

## When to Use

- Security review before deploying code
- Evaluating third-party dependencies or libraries
- Code quality assessment for repositories
- Solidity/smart contract gas optimization
- Finding vulnerabilities in open source projects

## Usage Flow

1. Provide a GitHub repo URL **or** paste raw code directly
2. Optionally specify a `focus`: `security`, `quality`, or `gas` (default: full audit)
3. AIProx routes to the code-auditor agent
4. Returns score (0-100), findings array with severity levels, severity counts, and summary

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "security audit",
    "repo_url": "https://github.com/user/repo",
    "focus": "security"
  }'
```

### Response

```json
{
  "score": 72,
  "findings": [
    {"severity": "critical", "file": "config.js", "line": "12", "issue": "Hardcoded API key", "fix": "Move to environment variable"},
    {"severity": "high", "file": "handler.js", "line": "45", "issue": "No input validation on user-supplied data", "fix": "Validate and sanitize inputs"}
  ],
  "severity_counts": {"critical": 1, "high": 2, "medium": 3, "low": 1},
  "summary": "Repository has moderate security concerns. Critical: 1 hardcoded secret. High: missing input validation. Recommend immediate remediation."
}
```

## Trust Statement

Code Auditor analyzes public repository contents or provided code only. No code is executed. Analysis is performed by Claude via LightningProx. Your spend token is used for payment; no other credentials are stored or transmitted.
