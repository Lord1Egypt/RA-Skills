# debug

**Debug Assistant** — Analyze error messages, stack traces, and logs. Get instant diagnosis and fix suggestions for common programming errors.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Parse and diagnose an error message or stack trace | `analyze "TypeError: Cannot read property 'foo' of undefined"` |
| `explain` | Explain what an error code or exception type means | `explain ECONNREFUSED` |
| `suggest` | Suggest fixes for a given error pattern | `suggest "ModuleNotFoundError: No module named 'requests'"` |

## Usage

```bash
bash script.sh analyze "your error message or stack trace here"
bash script.sh explain ENOENT
bash script.sh suggest "SyntaxError: Unexpected token }"
```

You can also pipe input:
```bash
cat error.log | bash script.sh analyze -
```

## Features

- Recognizes 40+ common error patterns across Python, Node.js, Go, Bash, and system errors
- Identifies error type, root cause, and severity
- Provides actionable fix suggestions with code examples
- Supports piped input for log file analysis
- Color-coded output for quick scanning

## Requirements

- `bash` >= 4.0
- `python3` >= 3.7
- No external packages required (uses only stdlib)

## Examples

```
$ bash script.sh analyze "ECONNREFUSED 127.0.0.1:5432"

🔍 Error Analysis
─────────────────────────────────────
Type     : System / Network Error
Code     : ECONNREFUSED
Severity : HIGH
Summary  : Connection actively refused by the target host

Root Cause:
  The service at 127.0.0.1:5432 is not running or is not
  accepting connections on that port.

Fix Suggestions:
  1. Check if the service is running:
       sudo systemctl status postgresql
  2. Verify the port is correct and the service is bound to it:
       ss -tlnp | grep 5432
  3. Check firewall rules:
       sudo ufw status
  4. Confirm connection string in your config/env
```

```
$ bash script.sh explain ModuleNotFoundError

📖 Error Explanation
─────────────────────────────────────
Name     : ModuleNotFoundError
Language : Python
Category : ImportError subclass

Description:
  Raised when Python cannot locate the specified module.
  This is a subclass of ImportError introduced in Python 3.6.

Common Causes:
  • Package not installed in the current environment
  • Virtual environment not activated
  • Typo in the module name
  • Module installed for a different Python version
```
