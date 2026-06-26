---
name: buttondown
description: Create, update, inspect, and send test previews of Buttondown newsletter emails through the Buttondown API. Use when Codex needs to post newsletter copy as a Buttondown draft, manage Buttondown email drafts, preview draft emails to specific recipients, or inspect Buttondown email metadata. Defaults to draft-only and requires explicit user approval before sending, scheduling, publishing, deleting, or emailing previews.
metadata:
  openclaw:
    emoji: "✉️"
    homepage: https://forge.rayhollister.com/rayhollister/buttondown
    envVars:
      - name: BUTTONDOWN_API_KEY
        required: true
        description: Buttondown API key. Store it in your shell, launcher, runtime secret store, or OpenClaw SecretRef; never commit it.
      - name: BUTTONDOWN_CONTEXT
        required: false
        description: Optional Buttondown newsletter username for accounts that manage more than one newsletter.
---

# Buttondown

Use Buttondown's API to create and manage newsletter email drafts.

## Safety Defaults

- Draft-first: when creating an email, set `status: draft` unless the user explicitly approves a different status in the current conversation.
- Do not send, schedule, publish, delete, or send draft previews without explicit user approval in the current conversation.
- Do not put API keys in chat, command history, repo files, draft bodies, logs, or screenshots.
- Read the Buttondown API key from `BUTTONDOWN_API_KEY`. Store it in your shell, launcher, runtime secret store, or OpenClaw SecretRef; never ask the user to paste the token into chat.
- If using a platform account for multiple newsletters, pass the Buttondown newsletter username through `--context` or `BUTTONDOWN_CONTEXT`.

## Configuration

The bundled CLI reads the API key from:

```bash
export BUTTONDOWN_API_KEY="..."
```

Prefer setting this through your runtime's secret manager or environment injection rather than typing it into a command. In OpenClaw, configure it through a SecretRef or equivalent managed environment variable.

Optional environment:

- `BUTTONDOWN_CONTEXT` - newsletter username for the `Buttondown-Context` header.
- `BUTTONDOWN_API_BASE` - defaults to `https://api.buttondown.com/v1`.

## CLI

Run commands from the skill directory:

```bash
python3 scripts/buttondown.py create-draft --subject "Subject" --body-file issue.md
python3 scripts/buttondown.py create-draft --subject "Subject" --body-file issue.md --slug "issue-1" --description "SEO/archive summary"
python3 scripts/buttondown.py create-draft --subject "Subject" --body-file issue.md --editor-mode plaintext
python3 scripts/buttondown.py update-draft <email_id> --subject "New subject" --body-file issue.md
python3 scripts/buttondown.py list --status draft
python3 scripts/buttondown.py get <email_id>
python3 scripts/buttondown.py render <email_id>
python3 scripts/buttondown.py send-draft <email_id> --recipient user@example.com
```

Use `--dry-run` on write commands to inspect the request without calling Buttondown:

```bash
python3 scripts/buttondown.py create-draft --subject "Subject" --body-file issue.md --dry-run
```

## Workflow

1. Prepare clean Markdown or HTML body content in a local file.
2. Remove YAML frontmatter from the body before uploading. Buttondown rejects bodies that start with frontmatter.
3. Create the draft with `create-draft`; confirm the response contains `status: draft`.
4. Share the Buttondown email ID and archive/admin URL from the response when available.
5. For a preview email, show the user the target recipient(s) and get explicit approval, then run `send-draft`.

## Body Format

Buttondown detects Markdown versus HTML automatically. To force the editor mode, pass:

- `--editor-mode plaintext` for Markdown.
- `--editor-mode fancy` for rich HTML.

The CLI prepends the official Buttondown editor-mode comment when this option is set.

## API Reference

Read `references/api.md` when you need endpoint details, request fields, status values, error codes, or direct curl equivalents.
