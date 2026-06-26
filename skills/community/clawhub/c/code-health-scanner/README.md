# Code Health Scanner v1.0

One-click Spring Boot code health diagnosis.

## What It Does

Scans your Java/Spring Boot project and generates a structured health report:

- 🔴 **Critical**: SQL injection, hardcoded secrets, resource leaks — potential crashes
- 🟡 **Warning**: N+1 queries, God classes, swallowed exceptions — technical debt
- 🟢 **Info**: Naming conventions, outdated dependencies, TODO accumulation

## Quick Start

```
"Scan my project at /path/to/spring-boot-app"
```

Scanner auto-discovers the project type, scans relevant files, and outputs a health report with a 0-100 score.

## Supported

| Stack | Support |
|-------|---------|
| Java 8-21 | ✅ Full |
| Spring Boot 2.x/3.x | ✅ Full |
| MyBatis / MyBatis Plus | ✅ Full |
| JPA / Hibernate | ✅ Partial |
| Maven | ✅ Full |
| Gradle | 🟡 Partial |

## Scan Modes

| Mode | Scope | Use Case |
|------|-------|----------|
| Quick Scan | `src/main/` only | Daily dev |
| Full Scan | + tests + build config | Pre-release |
| Incremental | git diff only | CI pipeline |

## Health Score

```
Score = 100 - (Critical × 15) - (Warning × 5) - (Info × 1)

≥ 85: ✅ Healthy
70-84: 🟡 Needs Attention
< 70: 🔴 At Risk
```

## Auto-Fix

Low-risk Info issues (naming, annotations, imports) can be auto-fixed on confirmation.

## Install

```bash
# ClawHub
openclaw skills install code-health-scanner

# Manual
cp -r code-health-scanner/ ~/.openclaw/workspace/skills/
```

## Model

- **Quick Scan**: `deepseek-v4-flash` (fast, cheap)
- **Full Scan**: `deepseek-v4-pro` (deep reasoning)
- **Large Projects**: Sub-agents per module (parallel)

## License

MIT — see [LICENSE](LICENSE)
