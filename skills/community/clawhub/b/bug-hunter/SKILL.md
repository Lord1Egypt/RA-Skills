---
name: bug-hunter
description: >
  Bug analysis, reproduction, and reporting assistant. Analyze logs, stack traces,
  screenshots to identify root cause. Generate structured bug reports with severity,
  priority, reproduction steps, and expected vs actual behavior.
  Use when: (1) analyzing error logs or stack traces, (2) writing bug reports,
  (3) triaging bugs, (4) reproducing issues, (5) root cause analysis,
  (6) "分析这个bug", "写bug报告", "看看这个报错", "帮我定位问题", "崩溃分析".
  NOT for: fixing code (use coding tools), writing test cases (use test-case-gen),
  or project management.
metadata:
  openclaw:
    emoji: "🐛"
---

# Bug Hunter

Analyze, reproduce, and report bugs with precision.

## When to Use

✅ **USE this skill when:**
- Analyzing error logs, stack traces, crash dumps
- Writing structured bug reports
- Triaging and prioritizing bugs
- Root cause analysis from symptoms
- "这个报错是什么原因" / "帮我写个bug单"

❌ **DON'T use this skill when:**
- Fixing the code → use coding tools
- Writing test cases → use `test-case-gen`
- Testing APIs → use `api-tester`

## Bug Report Template

When writing a bug report, use this structure:

```markdown
## 🐛 Bug Report

**Title**: [Module] Brief description of the issue

**Severity**: 🔴 Critical / 🟠 Major / 🟡 Minor / 🟢 Trivial
**Priority**: P0-Blocker / P1-High / P2-Medium / P3-Low
**Environment**: OS / Browser / App Version / API Version
**Reporter**: 虫探 🔍
**Date**: YYYY-MM-DD

### Description
Clear, concise description of what went wrong.

### Steps to Reproduce
1. Step one (be specific: URL, button name, exact input)
2. Step two
3. Step three

### Test Data
- Account: xxx
- Input: xxx

### Expected Result
What should happen.

### Actual Result
What actually happened. Include error messages verbatim.

### Evidence
- Screenshot: [attached]
- Log snippet:
\`\`\`
ERROR 2024-01-01 10:00:00 NullPointerException at UserService.java:42
\`\`\`

### Root Cause Analysis (if identified)
- Location: file:line
- Cause: description
- Impact scope: what else might be affected

### Suggested Fix (if obvious)
Brief suggestion for the developer.
```

## Log Analysis

### Common Error Patterns

| Pattern | Likely Cause | Action |
|---------|-------------|--------|
| `NullPointerException` | Null reference not handled | Check null checks, data flow |
| `ConnectionTimeout` | Network/service issue | Check service health, timeout config |
| `OutOfMemoryError` | Memory leak or insufficient heap | Analyze heap dump, check for leaks |
| `DeadlockException` | Concurrent resource contention | Review lock ordering, transaction scope |
| `401 Unauthorized` | Token expired/invalid | Check auth flow, token refresh |
| `429 Too Many Requests` | Rate limiting | Check request frequency, add throttling |
| `CORS error` | Cross-origin misconfiguration | Check server CORS headers |

### Log Analysis Steps

1. **Identify the error**: Find the first error in the chain (root cause, not symptom)
2. **Check timestamp**: When did it first occur? Is it recurring?
3. **Check context**: What request/operation triggered it?
4. **Check stack trace**: Which module/function? What line?
5. **Check related logs**: What happened before the error?
6. **Reproduce**: Can you trigger the same error consistently?

```bash
# Quick log analysis commands
# Find errors in log file
grep -n -i "error\|exception\|fatal\|failed" app.log | tail -20

# Count error types
grep -oP '\w+Exception' app.log | sort | uniq -c | sort -rn

# Find errors in time range
awk '/2024-01-01 10:0[0-5]/' app.log | grep -i error

# Get context around an error (5 lines before and after)
grep -B5 -A5 "NullPointerException" app.log
```

## Severity Classification

| Severity | Definition | Example |
|----------|-----------|---------|
| 🔴 **Critical** | System crash, data loss, security breach, no workaround | Payment charged but order not created |
| 🟠 **Major** | Core feature broken, has workaround | Login fails on Chrome but works on Firefox |
| 🟡 **Minor** | Non-core feature issue, cosmetic with functional impact | Sort order wrong on list page |
| 🟢 **Trivial** | Cosmetic only, typo, UI alignment | Button color slightly off |

## Triage Decision Matrix

```
                    High Impact          Low Impact
High Frequency   →  P0 Fix Now          P1 Fix Soon
Low Frequency    →  P1 Fix Soon         P2/P3 Backlog
```

## Root Cause Categories

When analyzing root cause, classify into:

- **Code Defect**: Logic error, missing validation, wrong algorithm
- **Config Error**: Wrong environment config, missing feature flag
- **Data Issue**: Corrupt data, migration problem, encoding issue
- **Infrastructure**: Server capacity, network, third-party service
- **Design Flaw**: Architectural issue, race condition by design
- **Requirement Gap**: Ambiguous or missing requirement

## Tips

- Always include the **exact** error message, not a paraphrase
- Screenshots > descriptions for UI bugs
- Include both expected AND actual results — never skip either
- Note if the bug is intermittent (include frequency)
- Check if the bug exists in previous versions (regression?)
- For API bugs, include the full request and response

## Screenshot / UI Bug Analysis

When provided with screenshots:

1. **Describe the visual issue**: Element misaligned? Missing? Wrong state?
2. **Identify affected component**: Which UI component/area?
3. **Check viewport**: Is it responsive-related? Note screen size if visible.
4. **Compare**: Expected design vs actual rendering
5. **Classify**: Layout bug / Style bug / Functional state bug / Data display bug

Use the `image` tool to analyze screenshots, then include findings in the bug report's Evidence section.

## API Error Response Analysis

When analyzing API errors:

```bash
# Save full request + response for bug report
curl -v -X POST "https://api.example.com/endpoint" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' 2>&1 | tee /tmp/api-debug.log

# Key things to capture:
# - Request URL, method, headers, body
# - Response status code, headers, body
# - Timing information
# - Any redirect chain
```

Common API error patterns:

| Status | Check | Likely Root Cause |
|--------|-------|------------------|
| 400 | Request body/params | Validation logic or schema mismatch |
| 401 | Auth header | Token expired, wrong auth scheme |
| 403 | Permissions | RBAC config, resource ownership |
| 404 | URL path | Route not registered, wrong ID |
| 409 | Business logic | Duplicate entry, state conflict |
| 422 | Validation detail | Semantic validation (format, range) |
| 500 | Server logs | Unhandled exception, null ref, DB error |
| 502/503 | Infrastructure | Upstream service down, deployment in progress |
