---
name: dependency-scanner
description: Scan project dependencies for security vulnerabilities using npm audit. Use when checking for vulnerable packages, security audits, or dependency health.
---

# Dependency Scanner Skill

Scans Node.js project dependencies for known security vulnerabilities using `npm audit`.

## Usage

```bash
# Scan current directory
node skills/dependency-scanner/index.js

# Scan specific project
node skills/dependency-scanner/index.js /path/to/project
```

## Features

- Runs `npm audit` and parses JSON results
- Categorizes vulnerabilities by severity (critical, high, moderate, low)
- Provides actionable recommendations
- Returns structured data for programmatic use

## Output

```
=== Dependency Security Scan ===
Target: /path/to/project
Time: 2026-06-07T09:12:38.339Z

Summary:
  Total vulnerabilities: 3
  Critical: 1
  High: 1
  Moderate: 1

Vulnerabilities:
  [CRITICAL] lodash@4.17.15
    Via: Prototype Pollution
    Fix available: Yes
  [HIGH] axios@0.19.0
    Via: SSRF
    Fix available: Yes

Recommendations:
  - CRITICAL: Update vulnerable packages immediately
  - Run: npm audit fix --force (review changes first)
```

## API

### scanDependencies(targetDir, options)

Returns scan results object:
```javascript
{
  timestamp: '2026-06-07T09:12:38.339Z',
  target: '/path/to/project',
  summary: {
    total: 3,
    critical: 1,
    high: 1,
    moderate: 1,
    low: 0
  },
  vulnerabilities: [...],
  recommendations: [...]
}
```

## When to Use

- During security audits
- Before deploying to production
- In CI/CD pipelines
- When updating dependencies
- Periodic security checks