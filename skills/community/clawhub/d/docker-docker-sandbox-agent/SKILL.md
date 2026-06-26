---
name: docker-sandbox
description: |
  A generic skill that provides a secure, temporary Docker sandbox for executing generated code (Python, Node.js, bash, etc.). Agents can use this to verify their code works without compromising the host machine.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🐳"
    requires:
      bins: ["docker"]
    platform: ["macos", "linux", "windows"]
---

# Docker Sandbox

> Execute and verify code securely inside isolated temporary containers.

## Problem

Agents frequently generate code (Python, JS, Shell scripts) that they need to test before presenting a final solution. Running this code directly on the host machine poses significant security and stability risks.

## Solution

The `docker-sandbox` skill establishes a pattern for agents to provision a **temporary, isolated container** environment using Docker. Code executes inside the container, captures standard output and error, and cleans up immediately after completion.

## Features

- ✅ **Host Isolation** - Runs code securely away from the host system's file tree and environment variables.
- ✅ **Ephemeral Execution** - Containers are automatically destroyed (`--rm`) after the process exits.
- ✅ **Multi-environment** - Supports Python, Node.js, Go, or any Docker-supported runtime.
- ✅ **Resource Controls** - Hard constraints on memory and CPU avoid runaway processes.

## Usage Guide (For Agents)

When evaluating or testing code, use the following execution abstractions via the host terminal. Prepare your code in a local temporary directory (e.g., `./.sandbox/`), then mount it in the container.

### 1. Python Verification

Run a python script securely with constrained memory and CPU.

```bash
# Create a test script
mkdir -p .sandbox
echo 'print("Hello from Docker Sandbox!")' > .sandbox/main.py

# Execute in python sandbox
docker run --rm \
    --memory="512m" \
    --cpus="1.0" \
    --network none \
    -v "$(pwd)/.sandbox:/app" \
    -w /app \
    python:3.10-slim python main.py
```

### 2. Node.js Verification

Evaluate JavaScript / Node.js safely.

```bash
docker run --rm \
    --memory="512m" \
    --cpus="1.0" \
    --network none \
    -v "$(pwd)/.sandbox:/app" \
    -w /app \
    node:18-alpine node main.js
```

### 3. Bash/Shell Verification

Test shell scripts in a generic Alpine environment.

```bash
docker run --rm -v "$(pwd)/.sandbox:/app" -w /app alpine sh script.sh
```

## Security Guidelines

1. **Mount Minimization**: **Never** mount sensitive host directories (e.g., `/etc`, `~/.ssh`, or `/`) into the sandbox. Mount only the specifically designated `.sandbox` or task-related directory.
2. **Network Isolation**: By default, include `--network none` in the command to prevent the code from exfiltrating data or initiating unwanted network requests, unless network access is functionally necessary for the test.
3. **Privileges**: Never use `--privileged` mode or run containers mapped directly to the root user of the host if preventable.
