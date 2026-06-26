---
name: mass-sandbox
description: Execute untrusted code or commands in a secure, isolated Docker environment. Use when asked to run unknown scripts, third-party skills, or any code that might pose a security risk to the host system.
metadata:
  openclaw:
    requires:
      bins: [docker]
---

# Multi-Agent Security Sandbox (MASS)

## Overview
This skill provides a secure "clean room" for executing and monitoring untrusted commands and code. It uses Docker with restricted capabilities, no network access, and a custom seccomp profile to isolate the execution from your host system.

## When to Use
- When asked to run a script or command from an untrusted source.
- When testing a new agent skill that requires system access.
- When you need to verify the behavior of code that might be malicious.

## Workflow

### 1. Identify Untrusted Input
Determine if the command or script you are asked to run should be sandboxed.

### 2. Run in Sandbox
Use the `mass` script located in the skill's `scripts/` directory to wrap the command.

**Usage:**
```bash
./scripts/mass "<command>"
```

**Example:**
To run a suspicious Python script:
```bash
./scripts/mass "python3 untrusted_script.py"
```

### 3. Review Output
The `mass` tool will return the stdout and stderr from the sandbox. If the command was blocked by security policies (e.g., trying to access sensitive files or making network calls), the output will reflect the failure.

## Security Features
- **Capabilities Dropped:** All Linux capabilities are dropped (`--cap-drop=ALL`).
- **No Network:** Network access is disabled by default (`--network=none`).
- **Non-Root User:** Code runs as `sandboxuser`.
- **Syscall Filtering:** Sensitive system calls are blocked via `seccomp.json`.

## Limitations
- **No GUI:** The sandbox is CLI-only.
- **Persistence:** Any changes made inside the container are lost after execution (`--rm`).
- **Dependencies:** Only tools installed in the `Dockerfile` are available.
