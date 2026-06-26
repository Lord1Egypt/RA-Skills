# code-reviewer

🔍 **AI-powered code review assistant for OpenClaw agent developers**

Automatically analyze code quality, detect security vulnerabilities, performance issues, and provide actionable improvement suggestions.

## Features

- 🛡️ Security vulnerability detection
- ⚡ Performance bottleneck identification  
- 🧹 Code smell and anti-pattern detection
- ✨ Best practices validation
- 📚 Documentation quality assessment
- 📄 Detailed Markdown reports

## Quick Start

### Installation

```bash
clawhub install code-reviewer
```

### Basic Usage

In your OpenClaw conversation:

> "Review the code quality of `src/agent.js`"

Or analyze an entire directory:

> "Generate a code review report for `./skills/my-skill/`"

## What Gets Checked

### Security 🛡️
- Command/SQL injection vulnerabilities
- Hardcoded secrets and API keys
- Unsafe eval() usage
- Permission issues

### Performance ⚡
- Nested loops (O(n²) complexity)
- Synchronous file operations
- Regex compiled in loops
- Memory leaks

### Code Quality 🧹
- Long functions (>50 lines)
- Magic numbers
- Debug statements in production
- Dead code

### Best Practices ✨
- Missing error handling
- Unhandled promises
- TODO/FIXME comments
- Incomplete implementations

## Example Output

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
```

## Supported Languages

- ✅ JavaScript / TypeScript
- ✅ Python
- ✅ Go  
- ✅ Rust
- ✅ Shell scripts

## Configuration

Create `.codereview.json` in your project:

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
  "languages": ["javascript", "python"]
}
```

## CLI Usage

```bash
# Review a single file
node analyzer.js src/index.js

# Review a directory
node analyzer.js ./src

# Generate detailed report
node analyzer.js ./src --detailed
```

## Advanced Examples

See [EXAMPLES.md](./EXAMPLES.md) for:
- Pre-commit hooks
- CI/CD integration
- Slack notifications
- API server mode
- IDE integration

## Privacy & Security

- ✅ Runs locally - code never leaves your machine
- ✅ No telemetry or data collection
- ✅ Open source - audit the code yourself
- ✅ Safe analysis - never executes your code

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Author

Made with 🌸 by 翠花 for the OpenClaw community.

## Support

- 📖 [Full Documentation](./SKILL.md)
- 📧 Issues: [GitHub Issues](https://github.com/your-username/code-reviewer/issues)
- 💬 Discord: [#code-reviewer](https://discord.gg/clawd)

---

**Part of the ClawHub ecosystem** | [clawhub.ai](https://clawhub.ai)
