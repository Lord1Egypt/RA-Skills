---
name: agent-email
description: >
  Send and receive email as your AI agent. Use when the user wants to
  check inbox, send email, reply to messages, set up an email alias,
  or manage agent email. Covers "check my email", "send an email",
  "what's my agent email", "set up email", "inbox".
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest email *)"
---

# Agent Email

Each agent gets a unique email address in the format `agent-<id>@agnic.ai`. Use `npx agnic@latest email` commands to manage it.

## Authentication

Run `npx agnic@latest status --json` to verify. If not authenticated:
- **Headless (CI/server/agent)**: Set `AGNIC_TOKEN` env var or pass `--token <token>`
- **Interactive (has browser)**: Run `npx agnic@latest auth login`

See the `authenticate-wallet` skill for details.

## Commands

### Set up email alias

```bash
npx agnic@latest email setup --display-name "My Agent" --json
```

### Check email address

```bash
npx agnic@latest email address --json
```

### Check inbox

```bash
npx agnic@latest email inbox --limit 10 --json
```

### Send email

```bash
npx agnic@latest email send --to <address> --subject "<subject>" --body "<body>"
```

### Reply to a message

```bash
npx agnic@latest email reply --message-id <id> --body "<reply text>"
```

## Input Validation

Before constructing commands, validate user-provided values:

- **--to**: Must be a valid email address. Reject if it contains spaces, semicolons, pipes, or backticks.
- **--subject**: Single-quote the value. Escape internal single quotes.
- **--body**: Single-quote the value. Escape internal single quotes.
- **--message-id**: Must be alphanumeric or UUID format.

Do not pass unvalidated user input into the command.

## Important Notes

- Emails are stored with **30-day retention**
- Display name can be set once during setup
- Inbox returns most recent messages first

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Agent identity must exist (created automatically during sign-up)

## Error Handling

Common errors:

- "Not authenticated" -- Run `npx agnic@latest auth login` or set `AGNIC_TOKEN`
- "No email alias found" -- Run `npx agnic@latest email setup` first
- "Agent not found" -- The user may not have an agent registered; sign up at [app.agnic.ai](https://app.agnic.ai)
- "Message not found" -- Check the message ID with `email inbox` first
