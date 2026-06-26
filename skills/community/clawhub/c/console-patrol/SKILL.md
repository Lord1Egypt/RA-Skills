# ConsolePatrol Skill

## Name

`console-patrol`

## Description

AI-First Console Error & Warning Detector for Web Applications. Automatically scans web pages to detect console errors and warnings, with framework-specific rules for Ant Design, React, and Element UI.

## When to Use

Use this skill when the user asks to:
- "Check for console errors"
- "Scan pages for warnings"
- "Audit a web app"
- "Find issues in the application"
- "Debug console output"
- Fixing React/antd/Element UI warnings

## Prerequisites

The skill uses `console-patrol` package:

```bash
pip install console-patrol
playwright install chromium
```

## Core Workflow

### 1. Quick Scan (Recommended)

```python
from console_patrol import ConsolePatrol

patrol = ConsolePatrol()
result = patrol.scan(
    url="http://localhost:3000",
    routes=[
        "http://localhost:3000/",
        "http://localhost:3000/dashboard",
        "http://localhost:3000/settings",
    ],
    wait_time=2.0,
)

print(f"Issues found: {result.report.total_issues}")
for issue in result.issues:
    print(f"[{issue.severity.value}] {issue.rule_id}")
    print(f"  Fix: {issue.suggestion}")
```

### 2. Auto-Discover Routes

```python
from console_patrol import ConsolePatrol

patrol = ConsolePatrol()
result = patrol.scan(
    url="http://localhost:3000",
    router_type="react",
    base_path="/admin",
    auto_discover=True,  # Auto-discover common routes
)
```

### 3. With Framework Auto-Detection

```python
result = patrol.scan(
    url="http://localhost:3000",
    routes=["http://localhost:3000/"],
    detect_framework=True,  # Auto-detect UI framework
)
print(f"Detected: {result.framework_info.ui_framework}")
```

### 4. CLI Usage

```bash
# Scan with auto-discovery
console-patrol scan http://localhost:3000 --router-type react --auto-discover

# Scan specific routes
console-patrol scan http://localhost:3000 --routes "/,/dashboard,/about"

# With screenshots on errors
console-patrol scan http://localhost:3000 --screenshot

# Output formats
console-patrol scan http://localhost:3000 --format markdown
```

## Detection Rules

### Severity Levels

| Level | Meaning | Exit Code |
|-------|---------|-----------|
| P0 | Fatal (crashes, JS exceptions) | 2 |
| P1 | Warning (framework issues) | 1 |
| P2 | Hint (code smell) | 0 |

### Built-in Rules

#### Ant Design
- `antd-useForm-unhooked` (P1): `form.getFieldValue()` called outside Form
- `antd-modal-context` (P1): Static modal in React 18
- `antd-tree-missing-keys` (P1): Tree wildcard keys
- `antd-table-duplicate-key` (P0): Duplicate key in Table

#### React
- `react-uncaught-error` (P0): Uncaught JS exception
- `react-chunk-load-error` (P0): Module load failure
- `react-hooks-rules` (P1): Hooks violation
- `react-list-missing-key` (P2): Missing key prop

## Response Format

When issues are found, respond with:

```
## ConsolePatrol Scan Results

**Pages Scanned:** N
**Total Issues:** N

| Severity | Count |
|----------|-------|
| P0 (Fatal) | N |
| P1 (Warning) | N |
| P2 (Hint) | N |

### Issues

**[P0] react-uncaught-error**
- Message: Error description
- Location: page URL
- Fix: Suggestion

**[P1] antd-useForm-unhooked**
- Message: Error description
- Location: page URL
- Fix: Use state instead of form.getFieldValue() in render
```

## Important Notes

1. **Wait Time**: Default 2s after page load. Increase for SPAs with lazy loading.
2. **Screenshots**: Use `--screenshot` flag to capture error screenshots.
3. **Frameworks**: Pass `--frameworks antd,react` to limit rule scope.
4. **Exit Codes**: Use in CI/CD: `if [ $? -gt 0 ]; then echo "Issues found"; fi`

## Installation for Agent

If `console-patrol` is not installed:

```python
import subprocess
subprocess.run(["pip", "install", "console-patrol"], check=True)
subprocess.run(["playwright", "install", "chromium"], check=True)
```

## Edge Cases

- **Page not loading**: Timeout is 30s by default. Check if dev server is running.
- **No issues found**: Report success, no action needed.
- **P0 issues**: Always highlight as critical, suggest immediate fix.
- **Framework not detected**: Use default rules (antd, react, element).
