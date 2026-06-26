---
name: code-reviewer
description: |
  AI-powered code review assistant for OpenClaw agent developers. Automatically analyzes code quality, 
  detects security vulnerabilities, performance issues, and provides actionable improvement suggestions.
  
  Built specifically for AI agent code with a focus on safety, best practices, and maintainability.

metadata:
  openclaw:
    requires:
      bins:
        - git
      env: []
    primaryEnv: null
  
  version: "1.0.0"
  author: "翠花 (ClawHub Pioneer)"
  license: "MIT"
  tags:
    - code-quality
    - security
    - development
    - ai-agents
    - best-practices
  
  capabilities:
    - Multi-language support (JavaScript, TypeScript, Python, Go, Rust)
    - Security vulnerability detection
    - Performance issue identification
    - Code smell detection
    - Best practices validation
    - Markdown report generation
---

# code-reviewer - AI Code Review Assistant 🔍

> **Built for AI agent developers who care about code quality.**

An intelligent code review assistant that analyzes your codebase and provides detailed, actionable feedback on:
- 🛡️ **Security vulnerabilities**
- ⚡ **Performance bottlenecks**
- 🧹 **Code smells and anti-patterns**
- ✨ **Best practices adherence**
- 📚 **Documentation quality**

## 🎯 Why code-reviewer?

When building AI agents with OpenClaw, code quality matters more than ever:
- Agents often run with elevated permissions
- Security vulnerabilities can be exploited by malicious prompts
- Performance issues compound when agents loop
- Maintainability is critical for evolving agent behavior

**code-reviewer** understands these unique challenges and provides tailored advice.

---

## 🚀 Quick Start

### Review a single file

Tell your agent:
> "Review the code quality of `src/agent.js`"

### Review an entire directory

> "Analyze all Python files in `./skills/my-skill/`"

### Get a detailed report

> "Generate a full code review report for the current project"

---

## 📋 What Gets Checked

### Security 🛡️

- **Injection vulnerabilities** - Command injection, path traversal, eval usage
- **Sensitive data exposure** - Hardcoded secrets, API keys in code
- **Unsafe dependencies** - Known CVEs in package.json/requirements.txt
- **Permission issues** - Overly broad file access, unnecessary privileges

### Performance ⚡

- **Inefficient algorithms** - O(n²) when O(n) exists, unnecessary loops
- **Memory leaks** - Unreleased resources, closure traps
- **Blocking operations** - Sync file I/O in async contexts
- **Redundant computations** - Repeated calculations, unnecessary allocations

### Code Quality 🧹

- **Code smells** - Long functions, deep nesting, duplicated code
- **Naming conventions** - Inconsistent or unclear variable names
- **Dead code** - Unused imports, unreachable statements
- **Magic numbers** - Hardcoded values without explanation

### Best Practices ✨

- **Error handling** - Unhandled promises, swallowed exceptions
- **Testing** - Missing tests, low coverage areas
- **Documentation** - Missing docstrings, unclear comments
- **Type safety** - Missing type annotations (TypeScript/Python)

---

## 🎨 Output Format

### Terminal Summary

```
🔍 Code Review Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Files analyzed: 12
⚠️  Issues found: 8

Severity Breakdown:
  🔴 Critical: 1
  🟠 High:     2
  🟡 Medium:   3
  🟢 Low:      2

Top Issues:
  1. [CRITICAL] SQL injection vulnerability in query.js:45
  2. [HIGH] Hardcoded API key in config.js:12
  3. [HIGH] Memory leak in worker.js:78

💡 Run with --detailed for full report
```

### Detailed Markdown Report

Saved to `code-review-report.md`:

```markdown
# Code Review Report

**Generated**: 2026-03-24 20:30 PDT
**Project**: my-agent-project
**Files Reviewed**: 12
**Total Issues**: 8

## 🔴 Critical Issues (1)

### 1. SQL Injection Vulnerability
**File**: `src/query.js:45`
**Severity**: CRITICAL

**Issue**:
Unsanitized user input directly interpolated into SQL query.

**Code**:
\`\`\`javascript
const query = `SELECT * FROM users WHERE id = ${userId}`;
\`\`\`

**Impact**:
Allows arbitrary SQL execution. Attacker could read/modify database.

**Fix**:
Use parameterized queries:
\`\`\`javascript
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
\`\`\`

---

## 🟠 High Priority Issues (2)

### 2. Hardcoded API Key
**File**: `config.js:12`
...
```

---

## ⚙️ Configuration

Create `.codereview.json` in your project root for custom rules:

```json
{
  "severity": {
    "min": "medium",
    "failOnCritical": true
  },
  "ignore": {
    "files": ["*.test.js", "dist/*"],
    "rules": ["magic-numbers"]
  },
  "languages": ["javascript", "python"],
  "output": {
    "format": "markdown",
    "path": "./reports/code-review.md"
  }
}
```

---

## 🧠 How It Works

1. **Parse** - Reads your code files using OpenClaw's `read` tool
2. **Analyze** - Uses AI to understand code structure and intent
3. **Detect** - Applies security, performance, and quality rules
4. **Report** - Generates actionable findings with fix suggestions
5. **Learn** - Adapts to your codebase patterns over time

---

## 🌟 Features

### Multi-Language Support

- ✅ JavaScript / TypeScript
- ✅ Python
- ✅ Go
- ✅ Rust
- ✅ Shell scripts
- 🔄 More languages coming soon

### Smart Context Awareness

Understands your project type:
- OpenClaw skills and plugins
- Express/Fastify APIs
- React/Vue frontends
- CLI tools
- Lambda functions

### Incremental Reviews

Reviews only changed files in Git:
> "Review my latest changes"

### Team Integration

Share review reports with your team:
- Export to GitHub PR comments
- Slack/Discord notifications
- Email summaries

---

## 💡 Usage Examples

### Example 1: Pre-commit Review

```
Agent: Review all staged files before I commit
```

**Output**:
```
✅ All clear! No critical issues found.
💡 3 minor suggestions:
  - Consider adding error handling in auth.js:23
  - Variable 'temp' could use a better name in utils.js:56
  - Add JSDoc for function processData() in api.js:12
```

### Example 2: Security Audit

```
Agent: Run a security audit on ./src/
```

**Output**:
```
🛡️ Security Audit Results
━━━━━━━━━━━━━━━━━━━━━━━

🔴 1 critical vulnerability found
🟠 2 high-risk issues detected

Details:
1. [CRITICAL] Command injection in exec.js
2. [HIGH] Sensitive data in logs
3. [HIGH] Missing input validation

📄 Full report: security-audit-2026-03-24.md
```

### Example 3: Performance Check

```
Agent: Find performance bottlenecks in worker.js
```

**Output**:
```
⚡ Performance Analysis
━━━━━━━━━━━━━━━━━━━━━

Found 3 optimization opportunities:

1. Line 45: O(n²) loop - use Map for O(n)
2. Line 67: Sync file read blocks event loop
3. Line 89: Regex compiled in hot path

Estimated improvement: 85% faster
```

---

## 🔒 Privacy & Security

- ✅ **Runs locally** - Your code never leaves your machine
- ✅ **No telemetry** - Zero data collection
- ✅ **Open source** - Audit the code yourself
- ✅ **Safe analysis** - Never executes your code

---

## 📦 Installation

### Via ClawHub (Recommended)

```bash
clawhub install code-reviewer
```

### Manual Installation

```bash
git clone https://github.com/your-username/code-reviewer
cd code-reviewer
clawhub publish .
```

---

## 🤝 Contributing

Found a bug? Have a feature idea?

- 🐛 Report issues: [GitHub Issues](https://github.com/your-username/code-reviewer/issues)
- 💡 Suggest features: [Discussions](https://github.com/your-username/code-reviewer/discussions)
- 🔧 Submit PRs: [Contributing Guide](./CONTRIBUTING.md)

---

## 📜 License

MIT License - see [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

Built with ❤️ by 翠花 for the OpenClaw community.

Special thanks to:
- OpenClaw team for the amazing framework
- ClawHub for making skill distribution easy
- Early adopters for feedback and bug reports

---

## 📞 Support

- 📖 Documentation: [Full docs](./docs/README.md)
- 💬 Discord: [Join #code-reviewer](https://discord.gg/clawd)
- 📧 Email: support@your-domain.com

---

**Made with 🌸 by 翠花 | ClawHub Pioneer**
