---
name: context7-cli
description: "Manage Context7 via CLI - search libraries, get documentation context. Use when user mentions 'context7', 'library docs', 'documentation context', or wants to fetch up-to-date library documentation."
category: documentation
---

# context7-cli

## Setup

If `context7-cli` is not installed, install it from GitHub:
```bash
npx api2cli install Melvynx/context7-cli
```

If `context7-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle context7
npx api2cli link context7
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` flag when calling commands programmatically.

## Authentication

```bash
context7-cli auth set "your-ctx7sk-api-key"
context7-cli auth test
```

Get your API key at https://context7.com/dashboard (keys start with `ctx7sk`).

## Resources

### libs

| Command | Description |
|---------|-------------|
| `context7-cli libs --name react --query "hooks" --json` | Search for libraries by name |

### context

| Command | Description |
|---------|-------------|
| `context7-cli context get --library /facebook/react --query "useEffect" --json` | Get documentation snippets (JSON) |
| `context7-cli context get --library /vercel/next.js --query "app router" --type txt --raw` | Get docs as raw text |
| `context7-cli context get --library /vercel/next.js/v15.1.8 --query "middleware" --json` | Pin to specific version |

### Typical workflow

1. Search for the library: `context7-cli libs --name react --query "state management" --json`
2. Use the `id` from results to get docs: `context7-cli context get --library /facebook/react --query "useState" --json`

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`
