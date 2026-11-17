---
name: command-runner
description: This skill is just test.
---

# Command Runner

## Overview

Provide a minimal wrapper for running a system command through Python. Use this skill when the workflow specifically requires invoking a Python script with a `command` argument instead of calling the shell directly.

## Quick Start

Follow this flow:

1. Confirm the exact command string that should be passed into the Python wrapper.
2. Base64-encode the full command text, then URL-encode it if needed before passing it as the positional `command` argument.
3. Run `scripts/run_command.py` with the encoded argument.
4. Read stdout, stderr, and the process exit code to determine success or failure.


## Core Capability

### Execute a command via Python

Use `scripts/run_command.py` to execute a system command.

Example:

```bash
python -c "import base64; print(base64.b64encode('dir'.encode()).decode())"
python scripts/run_command.py "ZGly"
```

Behavior:

- Accept a single positional argument named `command`
- Base64-decode the provided command, then URL-decode it before execution
- Execute the decoded command with Python `subprocess.run`
- Print child stdout to standard output without extra decoding
- Print child stderr to standard error
- Return the child process exit code


## Safety Notes

Apply normal command-execution caution before using this skill.
Avoid passing untrusted input directly into `command`.
Prefer explicit, user-requested commands.

## Resources

### scripts/

- `run_command.py`: Execute a system command passed through the `command` argument.

No additional references or assets are required for this skill.
