---
name: at-email-cli
description: Use the AgentTeam Email CLI command `at-email` to operate an agent mailbox. Use when the user wants to check mailbox status, list inbox messages, read safe message content, search mail, mark messages read, archive messages, send email, reply to email, use JSON output for automation, check CLI version/update status, or install/launch the CLI when the skill is available but `at-email` is not installed.
metadata:
  openclaw:
    requires:
      anyBins:
        - at-email
        - npx
        - npm
    primaryEnv: AT_EMAIL_WILDDUCK_ACCESS_TOKEN
    envVars:
      - name: AT_EMAIL_WILDDUCK_API_BASE_URL
        required: false
        description: WildDuck API base URL for mailbox commands.
      - name: AT_EMAIL_WILDDUCK_ACCESS_TOKEN
        required: false
        description: WildDuck API access token for mailbox commands.
      - name: AT_EMAIL_WILDDUCK_USER_ID
        required: false
        description: WildDuck user ID for mailbox commands.
      - name: AT_EMAIL_MAILBOX_ADDRESS
        required: false
        description: Optional default mailbox address for display and replies.
      - name: AT_EMAIL_CONTROL_API_BASE_URL
        required: false
        description: Control API base URL for safe message reads.
      - name: AT_EMAIL_MESSAGE_READ_TOKEN
        required: false
        description: Message-read token for safe message body access.
    homepage: https://github.com/agentteamhq/agentteam-email/tree/main/apps/at-email-cli
---

# at-email CLI

Use `at-email` as the command name. `at-email-cli` is only the app/package folder name.

## First Step

When the user asks you to operate email, first check whether the CLI is available:

```bash
command -v at-email
at-email --version
```

If `at-email` is missing, see **Install Or Run If Missing** at the end of this skill.

## Runtime Configuration

The CLI reads its connection settings from environment variables. Do not invent
credentials or print secret values.

Required for most mailbox commands:

```text
AT_EMAIL_WILDDUCK_API_BASE_URL
AT_EMAIL_WILDDUCK_ACCESS_TOKEN
AT_EMAIL_WILDDUCK_USER_ID
```

Optional but useful:

```text
AT_EMAIL_MAILBOX_ADDRESS
```

Required for safe message reads:

```text
AT_EMAIL_CONTROL_API_BASE_URL
AT_EMAIL_MESSAGE_READ_TOKEN
```

If configuration is missing, run the command and relay the CLI's exact missing
variable message rather than guessing values.

## Output Mode

Use text mode for human-readable summaries:

```bash
at-email inbox --unseen
```

Use `--json` when parsing output, chaining commands, or reporting structured
results:

```bash
at-email inbox --json --limit 10
```

In JSON mode, successful JSON is written to stdout and errors are written to
stderr so stdout stays machine-readable.

## Common Commands

Check configured mailbox status:

```bash
at-email status
```

List inbox messages:

```bash
at-email inbox
at-email inbox --unseen
at-email inbox --limit 50
at-email inbox --folder INBOX --json
```

Read a message through the safe message-read path:

```bash
at-email read 123
at-email read 123 --json
```

Search mail:

```bash
at-email search "invoice"
at-email search "from:alice@example.com" --limit 20 --json
```

Mark or archive a message:

```bash
at-email mark-read 123
at-email archive 123
```

Send a message:

```bash
at-email send --to alice@example.com --subject "Hello" --body "Message body"
```

Reply to a message:

```bash
at-email reply 123 --body "Thanks, received."
at-email reply 123 --all --body "Thanks, everyone."
```

Check version and updates:

```bash
at-email version
at-email self-update
```

When installed through npm, `self-update` is disabled because npm owns the
installed package version. Update notices still tell the user how to update the
npm package.

## Workflow Patterns

For "check my mail", run:

```bash
at-email status
at-email inbox --unseen
```

For "read the latest message", run:

```bash
at-email inbox --json --limit 1
at-email read <message_id>
```

For "reply to this message", inspect the message first unless the user already
provided enough context:

```bash
at-email read <message_id>
at-email reply <message_id> --body "<reply>"
```

For automation, prefer `--json`, parse the returned IDs, then call the
follow-up command with the selected `message_id`.

## Install Or Run If Missing

Prefer the npm package for the easiest bootstrap:

```bash
npx --yes @agentteamhq/email@latest --version
```

For one-off use, prefix the intended command with `npx --yes`:

```bash
npx --yes @agentteamhq/email@latest inbox --unseen
```

For a persistent install, ask before modifying the user's global tools, then run:

```bash
npm install -g @agentteamhq/email
at-email --version
```

If npm is unavailable or a standalone binary is required, download the matching
`at-email_X.Y.Z_<os>_<arch>[.exe]` asset and `checksums.txt` from the
`agentteamhq/agentteam-email` GitHub Release, verify the checksum, place the
binary on `PATH`, and run `at-email --version`.
