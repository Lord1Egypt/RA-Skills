# Code Audit & Security Scan

Static code analysis for security vulnerabilities, style violations, and bugs.

## When to Use

Trigger on: "audit code", "scan for bugs", "security check", "code review", "find vulnerabilities"

## What This Does

- Analyzes code for common security issues
- Checks for style violations
- Identifies potential bugs
- Returns structured report with severity levels

## Supported Languages

- Python
- JavaScript/TypeScript

## Workflow

### Step 1: Receive Code
Get code to analyze + language.

### Step 2: Static Analysis
Analyze using pattern matching and heuristics:

**Python checks:**
- Use of eval(), exec(), __import__()
- Hardcoded credentials
- SQL injection risks
- Path traversal
- Insecure random

**JS/TS checks:**
- eval() usage
- innerHTML without sanitization
- Hardcoded API keys
- console.log in production code

### Step 3: Scoring

```
Score = 100 - (issues_found × severity_weight)
Verdict: PASS (>80), WARN (50-80), FAIL (<50)
```

### Step 4: Present Results

```
## Code Audit: [language]

### Summary
| Metric | Value |
|--------|-------|
| Score | [X]/100 |
| Verdict | [PASS/WARN/FAIL] |
| Issues | [N] |

### Issues
1. [SEVERITY] [issue description] (line [N])
2. ...

### Recommendations
- [fix suggestions]
```

## No External Tools Required

This skill uses only:
- Platform exec tool
- Pattern matching
- No external binaries needed

## Example

```
## Code Audit: Python

### Summary
| Metric | Value |
|--------|-------|
| Score | 70/100 |
| Verdict | WARN |
| Issues | 3 |

### Issues
1. HIGH: eval() usage (line 2)
2. MEDIUM: hardcoded 'password' (line 5)
3. LOW: unused import 'os' (line 1)

### Recommendations
- Replace eval() with safer alternatives
- Use environment variables for secrets
- Remove unused imports
```

## Notes

- Works with platform tools only
- No install steps required
- Pattern-based analysis (not full compiler)
- Always note limitations in report