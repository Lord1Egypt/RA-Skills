# OpenShell Sandbox Skill

Secure execution environment for specialist agents using NVIDIA OpenShell.

## Overview
OpenShell provides sandboxed containers with Landlock LSM + seccomp + network namespaces + L7 policy engine. Each specialist agent gets an isolated sandbox for safe code execution.

## Sandboxes Available

| Sandbox | Agent | Purpose | Status |
|---------|-------|---------|--------|
| `coder-sandbox` | coder | Code execution, builds, tests | Ready |
| `security-sandbox` | security | Pentesting, security scans | Ready |
| `debug-sandbox` | debug | Bug reproduction, diagnosis | Ready |
| `test-sandbox` | qa-tester | Test execution | Ready |

## CLI Reference

```bash
# List all sandboxes
openshell sandbox list

# Execute command in sandbox
openshell sandbox exec -n <sandbox-name> -- <command> [args...]

# Interactive shell
openshell sandbox connect -n <sandbox-name>

# Create new sandbox
openshell sandbox create --name <name>

# Delete sandbox
openshell sandbox delete <name>

# View logs
openshell logs -n <sandbox-name>

# Gateway status
openshell status

# Diagnose issues
openshell doctor check
```

## Agent Integration

### For Coder Agent
When executing code that could affect the host system:
```bash
# Instead of running locally:
python3 script.py

# Run in sandbox:
openshell sandbox exec -n coder-sandbox -- python3 /workspace/script.py
```

### For Security Agent
When running security tools or scans:
```bash
# Run nmap, nikto, etc. in isolated sandbox
openshell sandbox exec -n security-sandbox -- nmap -sV target
```

### For Debug Agent
When reproducing bugs or testing fixes:
```bash
openshell sandbox exec -n debug-sandbox -- node test.js
```

### For QA-Tester
When running test suites:
```bash
openshell sandbox exec -n test-sandbox -- pytest tests/
```

## File Transfer

To copy files between host and sandbox:
```bash
# Copy file INTO sandbox (via exec cat)
cat local_file.py | openshell sandbox exec -n coder-sandbox -- tee /workspace/local_file.py

# Copy file FROM sandbox
openshell sandbox exec -n coder-sandbox -- cat /workspace/result.txt > local_result.txt
```

## Policies

Default policies apply L7 network restrictions. To view/modify:
```bash
openshell policy list
```

## Resource Limits

- **CPU:** Shared with host (24GB RAM server)
- **Network:** Restricted by L7 policy (no outbound by default)
- **Disk:** Ephemeral (deleted with sandbox)
- **Timeout:** 30 min default per exec command

## Troubleshooting

- **Sandbox not found:** Run `openshell sandbox list` to check status
- **Gateway down:** Run `openshell status` and `openshell doctor check`
- **Permission denied:** Sandboxes run as unprivileged user
- **Network blocked:** Default policy denies outbound; use `openshell policy` to modify

## Architecture

```
Host (Ubuntu ARM64)
  └── OpenShell Gateway (Docker + k3s)
       ├── coder-sandbox (aarch64, Python 3.13, Node 22)
       ├── security-sandbox (aarch64)
       ├── debug-sandbox (aarch64)
       └── test-sandbox (aarch64)
```

## Version
- OpenShell CLI: 0.0.35
- Base image: ghcr.io/nvidia/openshell-community/sandboxes/base:latest
- Platform: aarch64 (ARM64)
