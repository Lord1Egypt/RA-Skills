---
name: bit
description: Explain bit-cli skill purpose, installation, required setup, and troubleshooting.
metadata: {"openclaw": {"requires": {"bins": ["bit", "git", "go", "sudo"], "env": ["BIT_API_KEY"]}, "primaryEnv": "BIT_API_KEY", "install": [{"id": "go-install", "kind": "go", "label": "Install bit via Go", "bins": ["bit"], "module": "github.com/ParinLL/bit-cli"}]}}
---

# Bit CLI Skill (Documentation-Only)

## Skill Purpose And Trigger Scenarios

- Purpose: Provide a usage entry point for the Bit URL Shortener CLI (`bit`) to create, query, update, delete short links, and view click data.
- Trigger scenarios:
- The user mentions needs like "short URL", "bit-cli", or commands such as `bit create/list/get/update/delete/clicks`.
- The user wants to run Bit API operations with OpenClaw.
- The user needs to verify Bit API availability (for example, a health check).

## Installation (GitHub)

- Install source: `https://github.com/ParinLL/bit-cli`
- Install from GitHub:

```bash
git clone https://github.com/ParinLL/bit-cli.git
cd bit-cli
go build -o bit .
sudo mv bit /usr/local/bin/
```

- Review the repository before building from source.

## Required Environment Variables / Permissions

- Required environment variables:
- `BIT_API_KEY` (required): Bit API authentication key.
- `BIT_API_URL` (optional): Bit API base URL, default `http://localhost:4000`.
- Permission requirements:
- The `bit` executable must be callable from PATH.
- Installing to `/usr/local/bin` with `sudo mv` requires administrator privileges.
- If the target API is remote, network connectivity to that API is required.

## Using The `bit` Binary

- Verify installation:

```bash
which bit
bit ping
```

- Configure API access before running commands:

```bash
export BIT_API_URL="http://localhost:4000"
export BIT_API_KEY="your-api-key"
```

- Command format:
- `bit <command> [arguments] [flags]`

- Main commands and when to use them:
- `bit ping`
- Use for a quick API health check before other operations.
- `bit create <url>`
- Creates a short link for the target URL.
- `bit list [--limit N] [--cursor X]`
- Lists links with optional pagination for large datasets.
- `bit get <id>`
- Retrieves one link and recent click details.
- `bit update <id> <new-url>`
- Replaces the destination URL for an existing short link.
- `bit delete <id>`
- Removes the short link by ID.
- `bit clicks <id> [--limit N] [--cursor X]`
- Shows click history for a link, with optional pagination.

- Typical workflow:

```bash
# 1) Confirm service is reachable
bit ping

# 2) Create a short link
bit create https://example.com/docs

# 3) List links to find the new ID
bit list --limit 20

# 4) Inspect one link
bit get 1

# 5) Check click records
bit clicks 1 --limit 50

# 6) Update destination if needed
bit update 1 https://example.com/new-docs

# 7) Delete when no longer needed
bit delete 1
```

- Practical tips:
- Start with `bit ping` whenever requests fail unexpectedly.
- Use `list`/`get` to confirm IDs before `update` or `delete`.
- Keep `BIT_API_KEY` in environment variables, not in command history or shared scripts.

## Common Troubleshooting

- `bit: command not found`
- Cause: The CLI is not installed or not in PATH.
- Fix: Rebuild with `go build` and verify `which bit` returns a valid path.
- `401 Unauthorized` / `403 Forbidden`
- Cause: `BIT_API_KEY` is missing or invalid.
- Fix: Reset `BIT_API_KEY` and confirm the key is still valid on the server.
- `connection refused` / timeout
- Cause: `BIT_API_URL` is incorrect, the Bit service is not running, or the network is unreachable.
- Fix: Run `bit ping` first, then verify API service status and URL.
- Command succeeds but data is unexpected
- Cause: The target ID does not exist, data was deleted, or the update payload format is incorrect.
- Fix: Validate current state with `bit list` or `bit get <id>`, then retry.
