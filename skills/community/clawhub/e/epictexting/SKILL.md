---
name: epictexting
description: Send SMS text messages from the user's own Twilio number with EpicTexting. Use when the user asks to text someone, send an SMS, send a text message reminder or follow-up, send the same message to a list of people (bulk / mass text, personalised with {name}), check whether a text was delivered, or see recent texts and replies. Works with any country number in international (+countrycode) format.
license: MIT
compatibility: Needs the EpicTexting MCP server (https://www.epictexting.app/api/mcp/mcp) connected in the agent, with a one-time sign-in (OAuth).
metadata:
  author: IndianAppGuy
  version: "1.0.0"
  homepage: https://www.epictexting.app
  repository: https://github.com/IndianAppGuy/epictexting-agent
  openclaw:
    homepage: https://www.epictexting.app/?ref=openclaw
  hermes:
    tags: [sms, twilio, text-message, bulk-sms, messaging]
    category: communication
---

# EpicTexting

Your agent sends the text. EpicTexting sends SMS from your own Twilio number: one message or a personalised bulk text, with delivery status and replies.

## 1. Connect (once)

EpicTexting runs as a hosted MCP server: `https://www.epictexting.app/api/mcp/mcp` (Streamable HTTP, OAuth sign-in, no API key).
If you already see EpicTexting tools (`get_account_status`, `get_message_status` …, possibly prefixed like `mcp__epictexting__…`), skip this.
Otherwise tell the user the one command for their agent, then ask them to sign in when the browser opens:

| Agent | Connect |
|---|---|
| Claude Code | `claude mcp add --transport http epictexting https://www.epictexting.app/api/mcp/mcp` then `/mcp` → epictexting → Authenticate |
| Codex | `codex mcp add epictexting --url https://www.epictexting.app/api/mcp/mcp` then `codex mcp login epictexting` |
| Gemini CLI | `gemini mcp add -t http epictexting https://www.epictexting.app/api/mcp/mcp` then `/mcp auth epictexting` |
| OpenClaw | `openclaw mcp add epictexting --url https://www.epictexting.app/api/mcp/mcp --transport streamable-http` then `openclaw mcp login epictexting` |
| Hermes | `hermes mcp add epictexting --url https://www.epictexting.app/api/mcp/mcp --auth oauth` then `hermes mcp login epictexting` |
| Cursor / Claude.ai / ChatGPT | add a custom MCP connector with the URL above |

A free account works to start: https://www.epictexting.app/?ref=agent-skill

## 2. Tools

| Tool | What it does | Kind |
|---|---|---|
| `get_account_status` | Twilio connected?, default sender, plan, SMS left this month | read-only |
| `list_sender_numbers` | Twilio numbers you can send from | read-only |
| `send_sms` | Send one SMS | **sends / acts** |
| `send_bulk_sms` | Send the same SMS to up to 50 people, personalised with {name} | **sends / acts** |
| `list_recent_messages` | Recent sent and received SMS | read-only |
| `get_message_status` | Delivery status of one message by SID | read-only |

## 3. Rules (non-negotiable)

- **Always confirm before sending.** Show the user exactly who gets what text (every number and the final message, with `{name}` filled in for one example), and for bulk sends the count of SMS. Wait for a clear yes. One send per yes.
- Numbers must be international format (`+15551234567`, `+919876543210`).
- Only text people who expect to hear from the user. No spam, no purchased lists, no marketing to people who haven't opted in. Respect STOP replies.
- If a result has `connect_url`, Twilio isn't connected: give the user that link and stop. If it has `upgrade_url`, the monthly limit is reached: share it.

## 4. Workflow

1. `get_account_status` first. If it returns `connect_url`, share it and stop.
2. Draft the message (and the recipient list for bulk). Use `{name}` for personalisation in `send_bulk_sms`.
3. Show the draft and get a yes. Then `send_sms` (one) or `send_bulk_sms` (≤50).
4. Report what was sent. If asked, check `get_message_status` with the returned SID, or `list_recent_messages` for replies.

## 5. Examples

1. *"Text +1 415 555 0134: running 10 minutes late, see you at 6:10."*
   → Show number + text → yes → send_sms → "Sent from your default number."
2. *"Send this to my 12 workshop attendees: Hi {name}, tomorrow's session starts at 10am in Room B."*
   → Show list + one filled example + "12 SMS" → yes → send_bulk_sms.
3. *"Did my last text to Priya get delivered?"*
   → list_recent_messages to her number → get_message_status → delivered / failed with reason.
4. *"Which numbers can I send from?"*
   → list_sender_numbers.
5. *"Any replies today?"*
   → list_recent_messages → summarise inbound texts.

## 6. Errors

| Result | Do this |
|---|---|
| 401 / "sign in" / auth error | The MCP isn't authorised: run the connect step for the user's agent again. |
| `connect_url` / `upgrade_url` in a result | Give the user that link; don't retry. |
| Tool refuses the request | Explain the reason it gave; don't rephrase to get around it. |
