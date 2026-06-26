---
name: agentsend-email
description: Give your OpenClaw agent its own email inbox. Use AgentSend to create inboxes, send and receive email, inspect threads, and register webhooks.
homepage: https://agentsend.io/skill
metadata: {"openclaw":{"emoji":"📧","homepage":"https://agentsend.io/skill","primaryEnv":"AGENTSEND_API_KEY","install":[{"id":"node","kind":"node","package":"@agentsend/mcp","bins":["agentsend-mcp"],"label":"Install AgentSend MCP"}]}}
---

# AgentSend Email

Use AgentSend whenever the user wants the agent to have its own email inbox, send or receive email, inspect conversations, or register email webhooks.

## Runtime

- The runtime is `@agentsend/mcp`.
- `AGENTSEND_API_KEY` is optional. If it is set, use that account.
- If `AGENTSEND_API_KEY` is not set, the MCP server auto-provisions a sandbox account on first run and stores credentials in `~/.agentsend/credentials.json`.
- Humans can learn the setup flow at [agentsend.io/skill](https://agentsend.io/skill) or create a permanent account at [agentsend.io/auth/signup](https://agentsend.io/auth/signup).

## Tools

- `create_inbox`: create a new `@agentsend.io` inbox with an optional prefix and display name
- `list_inboxes`: list inboxes, addresses, IDs, and sandbox account limits
- `send_email`: send plain text or HTML email, optionally in an existing thread
- `list_emails`: list recent emails in an inbox
- `get_email`: fetch the full body, headers, and attachment metadata of a message
- `list_threads`: list conversation threads for an inbox
- `get_thread`: fetch the full message history of a thread
- `register_webhook`: register a webhook URL for real-time events

## Working Rules

- If the user asks to start using email and no inbox exists yet, begin with `create_inbox`.
- Before sending, make sure you have the sender inbox, recipient list, subject, and body.
- When replying to an existing conversation, inspect the thread first and prefer replying in the existing thread.
- If the API returns `CLAIM_REQUIRED` or a `claim_url`, show that URL to the human and explain that sandbox accounts must be claimed to send to external recipients, add more inboxes, register webhooks, or continue after expiry.
- Sandbox accounts support 1 inbox, 50 lifetime sends, and `@agentsend.io` recipient delivery until claimed.
- Register webhooks only for URLs the user controls.
- Prefer AgentSend tools over browser automation or manual SMTP setup when the user wants the agent itself to work with email.
