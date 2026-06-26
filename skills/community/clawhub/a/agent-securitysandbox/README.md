# Multi-Agent Security Sandbox (MASS)

Multi-Agent Security Sandbox (MASS) is an open-source Dockerized environment designed to securely test and monitor untrusted AI agent skills. This repository is formatted as a **ClawHub/OpenClaw Agent Skill**.

## Features
- **Ubuntu-based Sandbox:** A highly compatible and stable environment.
- **Docker Isolation:** Leverages Docker's security features (seccomp, AppArmor, capabilities dropping).
- **Native Skill Integration:** Ready to be installed via ClawHub or used directly by OpenClaw agents.
- **CLI Script:** Easy-to-use script (`scripts/mass`) for running commands in the sandbox.

## Installation
1. **Prerequisites:** Ensure [Docker](https://docs.docker.com/get-docker/) is installed and running on your system.
2. **Installation via ClawHub:**
   ```bash
   clawhub install assix/multi-ai-agent-security-sandbox
   ```
3. **Manual Installation:**
   ```bash
   git clone https://github.com/assix/multi-ai-agent-security-sandbox.git
   cd multi-ai-agent-security-sandbox
   ```

## Usage
### CLI usage
You can use the `mass` script directly:
```bash
./scripts/mass "<command>"
```
Example:
```bash
./scripts/mass "python3 -c 'print(\"secure execution\")'"
```

### Agent Skill usage
Once installed, agents can use the MASS sandbox automatically when they identify untrusted code execution tasks.

## Security Features
- **Capabilities Dropped:** All Linux capabilities are dropped (`--cap-drop=ALL`).
- **No Network:** Network access is disabled by default (`--network=none`).
- **Non-Root User:** Code runs as `sandboxuser`.
- **Syscall Filtering:** Sensitive system calls are blocked via a custom seccomp profile in `assets/seccomp.json`.

## License
MIT
