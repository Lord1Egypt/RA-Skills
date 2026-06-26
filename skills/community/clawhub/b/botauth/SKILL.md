---
name: botauth
description: Use the botauth CLI to list, search, and retrieve secrets from the user's unlocked botauth vault with per-request approval in the desktop app. Use when a task needs API keys, tokens, or passwords from an existing botauth vault.
---

# botauth

Use `botauth` to securely retrieve API keys, tokens, and credentials from the
user's botauth vault. The desktop app must be running, the vault must be
unlocked, and every `list`, `search`, and `get` request can trigger an approval
prompt.

## When to use

- You need an API key, token, or password to complete a task
- The user asks you to use credentials that already exist in botauth
- You need to fill a `.env` file or config from the user's vault

Do not save new secrets unless the user explicitly asks. `botauth add` opens a
desktop flow for the user to fill in the credential.

## Prerequisites

- `botauth` must be installed and available on `PATH`
- The botauth desktop app must be running
- The vault must be unlocked
- Run `botauth status` first

## Core commands

### Check connection

```bash
botauth status
```

### Search or list secrets

```bash
botauth search "openai"
botauth search "github" --provider github
botauth list
botauth list --provider github
botauth list --tags dev,production
```

### Retrieve a secret in two steps

First get metadata:

```bash
botauth get "OpenAI API Key"
botauth get --id <secret-id>
```

Then fetch the sensitive fields:

```bash
botauth get --id <secret-id> --fields api_key
botauth get --id <secret-id> --fields api_key,client_secret --access-key <key>
```

Reuse `--access-key` inside the same workflow when possible to avoid redundant
approval prompts.

### Ask the user to create a secret

```bash
botauth add
botauth add --app openai --secret-name "Production Key"
```

## Typical workflow

```bash
botauth status
botauth search "openai"
botauth get "OpenAI API Key"
botauth get --id <id> --fields api_key --access-key <access-key>
export OPENAI_API_KEY="<value>"
```

## JSON output

Use `--json` for machine-readable output:

```bash
botauth search "github" --json
botauth get --id <id> --fields token --json
```

## Important notes

- `list`, `search`, `get`, and `add` may show approval prompts in the desktop app
- Sensitive values only come back from `get --fields`
- Access keys are short-lived; reuse them during a single task, then discard them
- If `botauth status` fails, ask the user to launch or unlock the desktop app
