---
name: test
description: Automated browser testing - test web page functionality, verify UI elements, run end-to-end test flows, check links, validate forms, and perform QA testing. 自动化测试、网页测试、QA测试、端到端测试、验证功能、检查链接、表单验证。
disable-model-invocation: true
allowed-tools: Bash, Read, Write
argument-hint: <url> [test-description]
---

# Test

Run automated browser tests and validate web page functionality.

## Usage

```
/test https://example.com
/test https://example.com Check login flow works correctly
```

## Instructions

### General Health Check (no test description)
1. **Navigation**: Navigate to URL, verify page loads
2. **Visual**: Screenshot, check for layout issues
3. **Links**: Read DOM, count links, identify broken ones
4. **Responsive**: Screenshot at 375×667 and 1920×1080
5. **Network**: Flag any 4xx/5xx errors
6. **Console**: Flag any JavaScript errors

### Specific Flow Test (with description)
For each step in the described flow:
1. Screenshot BEFORE the action
2. Perform the action
3. Screenshot AFTER the action
4. Verify the expected result

### Report Format

```markdown
## 🧪 Test Report: {URL}
**Date**: {timestamp}

| Check | Status | Details |
|-------|--------|---------|
| Page Load | ✅ PASS | ... |
| Visual | ⚠️ WARN | ... |
| Network | ❌ FAIL | ... |
| Console | ✅ PASS | ... |
```

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
