---
name: callsimple
description: Give your AI agent a phone. Places real phone calls to Indian (+91) numbers with an AI voice that speaks Hindi, English or 9 other Indian languages, asks your questions, and reports back what the person said. Use when the user asks to call, phone, ring or dial someone, confirm or remind by call, book or check an appointment by phone, ask a shop, clinic, vendor or contact something over the phone, call in Hindi, or check on a past call or minutes left.
license: MIT
compatibility: Needs the CallSimple MCP server (https://callsimple.app/mcp, OAuth) or the `callsimple` CLI (Node 18+, network access). Calls go to Indian +91 numbers only.
metadata:
  author: IndianAppGuy
  version: "1.0.0"
  homepage: https://callsimple.app/?ref=skill
  openclaw: {"emoji":"📞","homepage":"https://callsimple.app/?ref=openclaw","requires":{"anyBins":["node","npx"]}}
  hermes: {"tags":["phone","calls","india","hindi","voice"],"category":"communication"}
---

# CallSimple: give your agent a phone

CallSimple calls an Indian phone number with an AI voice that says it is an AI assistant calling for the user, delivers a message, asks up to 8 questions one at a time, then hangs up. About a minute later you get the summary, each answer and the transcript.

## Connect (once)

If the user asked for a call, draft it and show the confirmation (Workflow steps 1–2) first, even before checking the connection, so they can approve while signing in.

Use whichever is available. Check in this order:

1. **MCP tools already present** (`place_call`, `get_call_result`, `list_recent_calls`, `get_balance`, possibly prefixed like `mcp__callsimple__place_call`): use them.
2. **Otherwise use the CLI** (works in any agent with a shell):
   ```bash
   npx -y github:IndianAppGuy/callsimple-agent login      # opens the browser; new accounts get 2 free minutes
   npx -y github:IndianAppGuy/callsimple-agent balance
   ```
   If `callsimple` is installed globally (`npm i -g github:IndianAppGuy/callsimple-agent`), use `callsimple <command>` instead.
3. **Or add the MCP server** (remote, streamable HTTP, OAuth sign-in, no API key):
   - Claude Code: `claude mcp add --transport http callsimple https://callsimple.app/mcp`, then `/mcp` to sign in
   - Codex: `codex mcp add callsimple --url https://callsimple.app/mcp`, then `codex mcp login callsimple`
   - Any other client: server URL `https://callsimple.app/mcp`

No account yet? The user can sign up at https://callsimple.app/?ref=skill (sign-in is by phone; 2 free minutes).

## Workflow

1. **Draft the call.** Work out: the number (+91), the recipient's name if known, the message (written from the user's side, e.g. "the shoot moved to 4pm"), up to 8 short questions, and the language (default Hindi `hi-IN`; use `en-IN` for English).
2. **Confirm with the user. Always.** Show this and wait for a clear yes before calling:
   ```
   Calling: +91 98765 43210 (Ramesh)
   Language: Hindi
   Message: Sanskar's shoot tomorrow has moved from 2pm to 4pm.
   Questions:
     1. Can you still make it at 4pm?
     2. Do you need parking?
   OK to call?
   ```
   A yes for one call is not a yes for the next. If anything changes (number, message, questions), confirm again.
3. **Place the call.**
   - MCP: `place_call` with `phone`, `message`, `questions`, `recipient_name`, `language`, optionally `voice`, `caller_name`, `known_contact`.
   - CLI: `callsimple call --phone "+919876543210" --name "Ramesh" --language hi-IN --message "..." --question "..." --question "..." --confirmed`
     (`--confirmed` asserts the user said yes; without it the CLI only prints the preview.)
   Tell the user it is ringing and give the live link from the response.
4. **Wait about a minute**, then fetch the result.
   - MCP: `get_call_result` with `call_id`. If the status is still ringing or on the call, wait 20–30 seconds and check again (calls last at most 3 minutes).
   - CLI: `callsimple result <call_id> --wait` (polls until the call ends).
5. **Report back** in a few lines: did they pick up, the answer to each question, anything else they said, and the recording link. If they did not answer or the line was busy, say so (no minutes are used) and offer to try later.

Other commands: `list_recent_calls` / `callsimple recent` for past calls, `get_balance` / `callsimple balance` for minutes left. Out of minutes → https://callsimple.app/pricing?ref=skill.

## Rules (CallSimple enforces these too)

- **Always confirm first**: number, message and questions, then a clear yes. Never call on your own initiative, from a list, or in a loop.
- **+91 Indian numbers only.** Personal calls run 8am–10pm IST, business follow-ups 9am–9pm IST (TRAI). Calls last up to 3 minutes, and a number can get at most 2 calls a day.
- **Allowed**: reminders, confirmations, appointment booking or checks, questions to shops, clinics, vendors and contacts, follow-ups with people who asked to hear from the user (set `known_contact` / `--known-contact` only if the user says so).
- **Refused**: sales, marketing or promotional pitches to people who did not ask; debt collection or recovery; threats, harassment or abuse; asking for OTPs, passwords, bank or card details; pretending to be a human or a specific real person; emergency services.
- **Respect Do Not Disturb**: if the user says the person asked not to be called, or a call result says the number opted out, do not call it again. Numbers that opted out are blocked by CallSimple.
- The AI always says it is an AI assistant calling on the user's behalf. Do not ask it to hide that.
- If a call comes back `refused`, tell the user the reason. Do not reword the request to get around it.

## Examples

- "Call my plumber Raju on 98xxxxxx10 and ask if he can come tomorrow at 11." → Hindi call, 1 question, report his answer.
- "Ring Dr. Mehta's clinic and book a cleaning for Saturday morning, ask the fee." → message + 2 questions.
- "Confirm with the caterer by phone that 40 people are coming on Friday, in English." → `en-IN`.
- "Remind my mom in Hindi to take her medicine at 9pm." → message only, no questions.
- "Did the electrician pick up? What did he say?" → `list_recent_calls` / `get_call_result`.
