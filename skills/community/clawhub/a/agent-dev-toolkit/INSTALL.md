# Installation Guide

## Prerequisites

- Node.js 18+
- npm 8+
- OpenClaw CLI

## Installation Steps

### 1. Install ClawHub CLI

```bash
npm install -g clawhub
```

### 2. Authenticate

```bash
clawhub login
```

Follow the prompts to create an account or sign in.

### 3. Install the Toolkit

```bash
clawhub install agent-dev-toolkit
```

### 4. Verify Installation

```bash
clawhub list | grep agent-dev-toolkit
```

## Manual Installation

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/openclaw/agent-dev-toolkit.git

# Copy to your skills directory
cp -r agent-dev-toolkit ~/.openclaw/workspace/skills/
```

## Upgrading

```bash
clawhub update agent-dev-toolkit
```

## Uninstallation

```bash
clawhub uninstall agent-dev-toolkit
```

## Troubleshooting

### Error: "clawhub: command not found"

Make sure npm global bin directory is in your PATH:

```bash
export PATH="$(npm config get prefix)/bin:$PATH"
```

Add to your shell config (~/.bashrc or ~/.zshrc) for persistence.

### Error: "Authentication required"

Run `clawhub login` again to refresh your token.

### Error: "Skill not found"

Make sure you're connected to the internet and the ClawHub registry is accessible.

## Next Steps

- Read the [Quick Start Guide](README.md)
- Check out [Examples](examples/)
- Join the [Community](https://discord.gg/openclaw)
