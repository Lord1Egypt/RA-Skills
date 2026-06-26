---
slug: "code-review-sr"
name: "CodeReview Automated Code Review Assistant"
description: "AI-powered code review that combines fast local static analysis with deep AI reasoning. Catches bugs, security vulnerabilities, performance issues, and style problems. Supports Anthropic, OpenAI, and Ollama models. Falls back to local regex analysis when offline."
author: "@TheShadowRose"
version: "1.0.4"
tags: ["code-review", "ai", "static-analysis", "security"]
license: "MIT"
env:
  ANTHROPIC_API_KEY: "Optional - for Anthropic/Claude models (or set CLAUDE_API_KEY)"
  OPENAI_API_KEY: "Optional - for OpenAI/GPT models"
  OLLAMA_HOST: "Optional - Ollama base URL, default http://localhost:11434"
  OLLAMA_PORT: "Optional - Ollama port, default 11434"
---

# CodeReview — AI-Powered Code Review Assistant

Combines **fast local regex pattern matching** with **deep AI-powered analysis** to deliver thorough, actionable code reviews. Runs a local static analysis pre-pass first, then sends code and initial findings to an AI model for comprehensive review including bug detection, security analysis, performance suggestions, and style feedback.

---

## How It Works

1. **Local Pre-Pass** — Regex-based pattern matching runs instantly, catching hardcoded secrets, eval usage, SQL injection patterns, empty catch blocks, long functions, and more.
2. **AI Deep Review** — The full source code and local findings are sent to your chosen AI model (Anthropic, OpenAI, or Ollama) for deep reasoning about bugs, logic errors, performance, and architecture.
3. **Graceful Fallback** — If no API key is set or the AI call fails, you still get local static analysis results. Never blocks your workflow.

## Usage

```javascript
const { CodeReview } = require('./src/code-review');

// AI-powered review (default: anthropic/claude-haiku-4-5)
const reviewer = new CodeReview({ model: 'anthropic/claude-haiku-4-5' });
const result = await reviewer.review('./src/auth.js');

console.log(result.score);        // 1-10
console.log(result.issues);       // Array of issues with severity, line, type, message
console.log(result.suggestions);  // Actionable improvement suggestions
console.log(result.summary);      // Concise quality summary
console.log(result.aiPowered);    // true

// Review an entire directory
const dirResult = await reviewer.reviewDir('./src', {
  include: ['*.js', '*.ts'],
  exclude: ['node_modules', '.git', 'dist'],
  concurrency: 3
});
console.log(dirResult.averageScore);
console.log(dirResult.totalIssues);
```

### Model Options

| Provider | Example | API Key Env Var |
|----------|---------|-----------------|
| **Anthropic** | `anthropic/claude-haiku-4-5` | `ANTHROPIC_API_KEY` |
| **OpenAI** | `openai/gpt-4o-mini` | `OPENAI_API_KEY` |
| **Ollama** (local) | `ollama/llama3` | None required |

```javascript
// OpenAI
const reviewer = new CodeReview({ model: 'openai/gpt-4o-mini' });

// Local Ollama
const reviewer = new CodeReview({ model: 'ollama/codellama' });

// Local-only (no AI, regex patterns only)
const reviewer = new CodeReview();
const result = await reviewer.review('./src/app.js');
// result.aiPowered === false
```

## What It Catches

| Category | Examples |
|----------|---------|
| **Bugs** | Null references, off-by-one errors, race conditions, empty catch blocks |
| **Security** | SQL injection, XSS, hardcoded secrets, eval usage |
| **Performance** | N+1 queries, unnecessary loops, memory leaks |
| **Style** | Inconsistent naming, long functions, dead code, console.log in production |
| **Logic** | Unreachable code, redundant conditions |
| **Maintainability** | Deeply nested callbacks, magic numbers, TODO/FIXME markers |

## Output Format

```json
{
  "file": "./src/auth.js",
  "score": 5,
  "issues": [
    {
      "severity": "high",
      "line": 42,
      "type": "security",
      "message": "User input passed directly to SQL query without parameterization"
    },
    {
      "severity": "medium",
      "line": 87,
      "type": "bugs",
      "message": "Empty catch block silently swallows database connection errors"
    }
  ],
  "suggestions": [
    "Use parameterized queries or an ORM to prevent SQL injection on line 42",
    "Add error logging in the catch block on line 87",
    "Extract the authentication logic into a separate middleware module"
  ],
  "summary": "The auth module has a critical SQL injection vulnerability and several error handling gaps. Core logic is sound but needs security hardening.",
  "totalIssues": 2,
  "lines": 142,
  "aiPowered": true,
  "model": "anthropic/claude-haiku-4-5"
}
```

## Language Support

Works with any language your AI model understands. The local pre-pass targets common patterns across languages. AI review tested with:

JavaScript, TypeScript, Python, Go, Rust, Java, C#, Ruby, PHP, Swift, Kotlin

## Technical Details

- **Zero npm dependencies** — Pure Node.js using only built-in `https`, `http`, `fs`, and `path` modules
- **File truncation** — Files are truncated at 8,000 characters before sending to AI to stay within token limits
- **Concurrency control** — Directory reviews process files in configurable parallel batches (default: 3)
- **Graceful degradation** — AI failures never crash; local results are always available

---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from
  the use or misuse of this software — including but not limited to financial loss,
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** When an AI model is configured, this software sends your source code and static analysis findings to the configured provider (Anthropic, OpenAI, or a local Ollama instance). Do not run it over code containing secrets or sensitive data unless you understand where data is sent. Without an API key, all analysis is local-only.
The author(s) are not responsible for data loss, corruption, or unauthorized access
resulting from software bugs, system failures, or user error. Always maintain
independent backups of important data. When AI models are configured, file contents
are sent to the respective AI provider's API (Anthropic, OpenAI, or your local Ollama
instance). No data is transmitted externally when running in local-only mode (no model configured).

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)