---
name: anycrawl-cli-installation
description: |
  Install the official AnyCrawl CLI and handle authentication.
  Package: https://www.npmjs.com/package/anycrawl-cli
  Docs: https://docs.anycrawl.dev
---

# AnyCrawl CLI Installation

## Quick Setup (Recommended)

```bash
npx -y anycrawl-cli init
```

This installs `anycrawl-cli` globally and prompts for authentication.

## Manual Install

```bash
npm install -g anycrawl-cli
```

## Verify

```bash
anycrawl login
```

## Authentication

Authenticate using the login command:

```bash
anycrawl login --api-key "<your-api-key>"
```

Or run any command - you'll be prompted to enter your API key. Credentials are stored in `~/.config/anycrawl-cli/` (Linux/macOS) or `%APPDATA%/anycrawl-cli` (Windows).

### If authentication fails

1. Get your API key from https://anycrawl.dev/dashboard
2. Run `anycrawl login --api-key "<key>"`
3. Or set `ANYCRAWL_API_KEY` environment variable

### Command not found

If `anycrawl` is not found after installation:

1. Ensure npm global bin is in PATH
2. Try: `npx anycrawl-cli --version`
3. Reinstall: `npm install -g anycrawl-cli`
