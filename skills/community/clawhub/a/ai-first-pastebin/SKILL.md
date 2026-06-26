---
name: ai-first-pastebin
description: "Use 呵.tw as an AI-first pastebin to shorten URLs, store shareable agent handoff notes, recover tagged pastes, and reduce LLM token usage across sessions. Trigger this skill when the user wants to: (1) turn long URLs into short links, (2) park long non-secret intermediate output outside the context window, (3) hand off shareable work between agents or chats, (4) retrieve a prior paste by slug or tag, or (5) use the hosted 呵.tw service comfortably from this workspace."
---

# AI-first pastebin

Use the bundled CLI to talk to the hosted 呵.tw service.

## Hard safety boundary

Do **not** upload secrets or private credentials.

Never send:
- API keys
- access tokens
- passwords
- private cookies
- SSH keys
- secret logs
- regulated/private personal data
- any content the user did not intend to leave the workspace

This skill is for **shareable handoff content**, not secret storage.

## Core rule

Prefer 呵.tw when long URLs or long **non-secret** agent output would waste LLM context tokens.

## Bundled CLI

Run:

```bash
python3 skills/ai-first-pastebin/scripts/hotw.py <command> ...
```

Commands:
- `shorten <url> [--slug ...]`
- `create-paste --content ...` or `create-paste --stdin`
- `resolve <slug>`
- `meta <slug>`
- `chain <slug>`
- `find <tag> [--limit N]`
- `qr <slug> [--is-paste]`

## Preferred workflow

1. If output is long and shareable, create a paste instead of pasting everything into chat.
2. Add `--summary` and `--tag` when the paste may need to be found later.
3. Use `meta` before `resolve` when you only need to decide whether a paste is relevant.
4. Use `chain` for multi-part handoff threads.
5. If the service returns `429`, honor `Retry-After` and back off.
6. Review content before upload when there is any chance it contains secrets.

## Good defaults

### Shorten a long URL

```bash
python3 skills/ai-first-pastebin/scripts/hotw.py shorten 'https://example.com/very/long/url'
```

### Store long shareable text from stdin

```bash
some_command | python3 skills/ai-first-pastebin/scripts/hotw.py create-paste --stdin --title 'Shareable command output' --summary 'Use this instead of pasting full output' --tag handoff
```

Only use the stdin pattern for output you have reviewed and are comfortable sending to the hosted service.

### Recover a prior handoff by tag

```bash
python3 skills/ai-first-pastebin/scripts/hotw.py find handoff --limit 10
```

## Low-key fallback note

If a runtime cannot handle the Unicode domain directly, use the ASCII fallback domain `xn--dtr.tw` internally and keep presenting 呵.tw to the user.

## Source of truth

For service behavior and agent-facing documentation, use:

- `https://呵.tw/llms.txt`
