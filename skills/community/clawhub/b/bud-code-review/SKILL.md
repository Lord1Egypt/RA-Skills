---
name: code-review
description: "AI-powered code review using Gemini. Reviews entire projects, catches bugs, suggests fixes, and helps debug."
metadata:
  {
    "openclaw": {
      "requires": { "bins": [] },
      "install": [
        {
          "id": "gemini-key",
          "kind": "env",
          "var": "GEMINI_API_KEY",
          "label": "Gemini API Key (get from https://aistudio.google.com)",
          "required": false
        }
      ]
    }
  }
---

# Code Review

AI-powered code review using Google's Gemini to analyze Python (and other) codebases.

## Setup

1. Get a Gemini API key from https://aistudio.google.com
2. Add to TOOLS.md: `GEMINI_API_KEY=your_key_here`
3. Or set as environment variable

## Features

**Reviews**: Full project or single files — catches bugs, security issues, performance problems, race conditions

**Fixes**: Generates specific code fixes for critical issues found

**Debug**: Analyzes error descriptions + code to identify likely causes

## Usage

```
review /path/to/project    → Review all Python files in directory
review /path/to/file.py    → Review single file
review <code_snippet>      → Review inline code
```

## How it works

1. Recursively finds all `.py` files in path
2. Sends each file to Gemini with context-appropriate prompts
3. Parallel execution for speed
4. Compiles findings into prioritized report:
   - 🔴 Critical (security, race conditions, potential losses)
   - 🟡 Important (bugs, error handling, API issues)
   - 🟢 Suggestions (best practices, maintainability)

## Focus areas by file type

| File | Focus |
|------|-------|
| Trading bots | Race conditions, risk calculation errors, order logic |
| APIs | Auth handling, retry logic, timeout behavior |
| State/DB | Atomicity, corruption risk, concurrent access |
| ML/AI | Lookahead bias, overfitting, data leakage |

## Example output

```
📊 Code Review: trading-bot/

🔴 CRITICAL
• scanner.py: Race condition in flip logic (close→entry not atomic)
• risk_manager.py: Stale order logic wrong for LIMIT orders

🟡 IMPORTANT  
• oanda_api.py: No retry on 429/5xx errors
• state.py: Non-atomic JSON writes

🟢 SUGGESTIONS
• Centralize API calls to reduce rate limit risk
• Add file locking for concurrent state access
```

## Requirements

- Python 3.8+
- `filelock` package (for state files): `pip install filelock`
- Gemini API key (free tier works)