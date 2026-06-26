# botauth

Use the `botauth` CLI to retrieve secrets from a local botauth vault with
desktop approval prompts.

## What this skill does

- Searches and lists existing secrets in botauth
- Retrieves secret metadata first, then sensitive fields in a second step
- Encourages minimal secret access and reuse of short-lived access keys
- Defers secret creation to the user through `botauth add`

## Best for

- Codex or Claude workflows that need API keys already stored in botauth
- Agent tasks that must keep humans in the loop for secret access
- Local-first secret retrieval instead of long-lived `.env` files

## Requirements

- `botauth` CLI installed
- botauth desktop app running
- Vault unlocked

## Install the CLI

```bash
npm install -g @botauth/cli
```

## Example workflow

```bash
botauth status
botauth search "openai"
botauth get "OpenAI API Key"
botauth get --id <id> --fields api_key --access-key <access-key>
```

## Files

- `SKILL.md`: agent instructions
- `manifest.yaml`: registry metadata for ClawHub-style publishing
