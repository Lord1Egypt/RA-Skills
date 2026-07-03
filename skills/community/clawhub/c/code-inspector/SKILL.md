---
name: code-inspector
description: Scan AI-generated code for bugs before deploying — 8 static analysis checks from critical (hardcoded secrets, unsafe eval) to low (unused imports). Production-readiness score 0-100. Because AI code looks fine until it isn't.
version: 1.2.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [Code-Review, Static-Analysis, Security, AI-Code, Quality, CLI, Python]
    homepage: https://github.com/minirr890112-byte/code-inspector
---

# code-inspector

## Problem → Solution

**The problem**: AI generates code that compiles and looks correct. But it silently drops edge case handling, hardcodes secrets, catches exceptions with bare except/pass, and uses mutable defaults. You deploy it. It breaks. Reddit is full of "I let Claude loose and it broke the entire site" stories.

**The solution**: One command scans any Python file for 8 categories of AI-code bugs. Critical → High → Medium → Low severity. Production-readiness score 0-100. Don't deploy AI code blind.

## Quick Start

```bash
pip install git+https://github.com/minirr890112-byte/code-inspector.git

code-inspector app.py           # scan a file
cat app.py | code-inspector     # scan from pipe
```

## What It Checks

| Check | Severity | Example |
|-------|----------|---------|
| Hardcoded secrets | 🔴 critical | `api_key = "sk-abc123"` |
| Unsafe eval/exec | 🔴 critical | `eval(user_input)` |
| Infinite loops | 🔴 critical | append-while-iterating |
| Mutable defaults | 🟠 high | `def fn(items=[])` |
| Shadowed builtins | 🟠 high | `list = [1,2,3]` |
| Bare except/pass | 🔴 critical | `except: pass` |
| Deep nesting | 🟡 medium | 5+ nested loops |
| Unused imports | ⚪ low | AST-based detection |

## Scoring

```
90-100: 🟢 PRODUCTION-READY
70-89:  🟡 NEEDS REVIEW
50-69:  🟠 HIGH RISK
0-49:   🔴 DO NOT DEPLOY
```

---
⭐ **Star this repo if AI code has ever broken your production**: [github.com/minirr890112-byte/code-inspector](https://github.com/minirr890112-byte/code-inspector)
