# Error Diagnosis

Analyze error messages, stack traces, and log output to diagnose root causes and suggest fixes. Use when debugging crashes, runtime errors, build failures, or unexpected behavior.

## Usage

```
Diagnose this error: [paste error message or stack trace]
```

Or with context:
```
Diagnose: [error]. Language: [lang]. Framework: [framework]. Recent changes: [what changed].
```

## How It Works

1. **Parse** — extract error type, message, file locations, line numbers from raw output
2. **Classify** — categorize the error (syntax, runtime, dependency, config, permission, network, OOM, etc.)
3. **Trace** — follow the call stack to identify the originating code vs. where the error surfaced
4. **Diagnose** — determine root cause using error patterns, common pitfalls, and framework-specific knowledge
5. **Fix** — provide actionable fix with code snippets

## Supported Error Sources

- **Stack traces**: Python, JavaScript/Node.js, Java, Go, Rust, C/C++, Ruby, PHP
- **Build errors**: npm, pip, cargo, gradle, maven, webpack, vite, tsc
- **Runtime errors**: segfaults, OOM, deadlocks, race conditions, type errors
- **Infrastructure**: Docker, Kubernetes, systemd, nginx, database connection errors
- **CI/CD**: GitHub Actions, GitLab CI, CircleCI failure logs

## Output Format

```markdown
## Error Type
[Classification: e.g., "TypeError — accessing property of undefined"]

## Root Cause
[1-2 sentences explaining WHY this happened]

## Fix
[Code snippet or command to resolve]

## Prevention
[How to avoid this in the future: type check, test, lint rule, etc.]
```

## Advanced Features

### Multi-Error Analysis
Paste multiple errors — the skill identifies whether they share a root cause or are independent issues.

### Regression Detection
```
This error started after [commit/change]. Analyze whether the change could cause this.
```

### Environment Comparison
```
Works in dev, fails in prod. Error: [error]. Dev config: [config]. Prod config: [config].
```

## Scripts

### `scripts/parse_stacktrace.py`

Extracts structured data from raw stack traces:

```bash
python3 scripts/parse_stacktrace.py < error.log
```

Returns JSON with error type, message, frames (file, line, function), and suggested search queries.
