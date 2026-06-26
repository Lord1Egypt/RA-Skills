---
name: debug
description: Debug web pages by inspecting network requests, console logs, DOM structure, and page errors. Use when the user wants to debug a website, check for errors, inspect network traffic, view console output, find broken requests, diagnose page issues, or troubleshoot web applications. 调试网页、检查错误、网络请求分析、控制台日志、排查问题、诊断页面、查看报错。
allowed-tools: Bash, Read, Write
---

# Debug

Debug and diagnose web page issues.

## Diagnostic Tools

| Check | What To Look For |
|-------|-----------------|
| Network requests | Failed requests (4xx/5xx), timeouts |
| Console logs | JS errors, warnings, uncaught exceptions |
| DOM structure | Broken images, empty containers, missing elements |
| Screenshot | Visual rendering issues, layout problems |

## Workflows

### Full Health Check
1. Navigate to URL
2. Screenshot the page
3. List network requests → flag 4xx/5xx errors
4. Capture console logs → flag errors and warnings
5. Read DOM → check for broken images, empty containers
6. Compile summary report

### Network Analysis
1. Navigate to URL
2. List all network requests
3. Report: URL, method, status, response type
4. Highlight failed requests

### Console Investigation
1. Navigate to URL
2. Capture console logs
3. Categorize: ERRORS / WARNINGS / INFO
4. Report findings

### Responsive Check
1. Screenshot at default viewport
2. Resize to mobile (375×667) → screenshot
3. Resize to tablet (768×1024) → screenshot
4. Resize to desktop (1920×1080) → screenshot
5. Compare and note layout issues

## Report Template

```markdown
## 🔍 Debug Report: {URL}

### Network Health
- Total: X | ✅ Success: X | ❌ Failed: X

### Console Output
- 🔴 Errors: X | 🟡 Warnings: X

### Recommendations
1. ...
```

Refer to [browser-context](../browser-context/SKILL.md) for available tools per backend.
