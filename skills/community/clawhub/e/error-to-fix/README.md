# Error To Fix

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Explains programming errors in plain language — root cause, fix, and how to prevent it

## What Problem This Solves

An error message is cryptic and the user is stuck. This skill parses the error/stack trace, identifies the error type, explains what happened in plain language, and gives a minimal targeted fix — not a rewrite, just the right solution.

**When triggered:** Error message, stack trace, or exception + explain/fix/resolve intent.

## Features

- **Error type classification** — SyntaxError, TypeError, ImportError, ConnectionError, and 8+ more error types with specific diagnostic strategies
- **Root cause identification** — goes beyond the surface symptom to explain the actual failure mechanism
- **Minimal targeted fixes** — provides the smallest change needed, doesn't rewrite entire files
- **Prevention tips** — one actionable practice per error type to avoid recurrence

## Quick Start

```bash
# Via ClawHub
clawhub install error-to-fix

# Or manually
cp -r error-to-fix ~/.openclaw/skills/
```

### Usage

```
/error-to-fix
```

Paste error message or stack trace, ask what went wrong and how to fix it.

```
/error-to-fix/root-cause
```

Deeper analysis — system-level cause, not just surface symptom.

```
/error-to-fix/prevent
```

Focus on patterns and practices to avoid this error long-term.

## Modes

| Mode | Description |
|------|-------------|
| `/error-to-fix` | Explains error + provides fix |
| `/error-to-fix/root-cause` | System-level root cause analysis |
| `/error-to-fix/prevent` | Prevention patterns and practices |

## Examples

| Error | Explanation |
|-------|-------------|
| Python TypeError | "TypeError: list.append expects str, got int — add `str()` cast around the input" |
| Node ModuleNotFoundError | "ModuleNotFoundError: 'requests' not in requirements.txt — run `pip install requests`" |
| React "undefined is not an object" | "`props.user.address` is accessed before `user` is set. Add guard: `props.user?.address`" |
| Connection refused | "ECONNREFUSED: server at localhost:5432 is not accepting connections. Is PostgreSQL running?" |

## Directory Structure

```
error-to-fix/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Error taxonomy, stack trace patterns, fix cheat sheet
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).