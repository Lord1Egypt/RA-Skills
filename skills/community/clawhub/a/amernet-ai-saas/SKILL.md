---
name: amernet-ai-saas
description: Connect your AI SaaS intelligent agent to any messaging channel via OpenClaw (WhatsApp, Telegram, Slack, Discord, iMessage, and more)
homepage: https://saas.salesbay.ai
user-invocable: false
---

## AI SaaS Agent

This skill forwards user messages to an AI SaaS agent and returns its response. It maintains conversation context per user by using their channel and user identifier as a session key.

### Required Configuration

These environment variables must be set in your `~/.openclaw/openclaw.json` under `skills.entries.amernet-ai-saas.env`:

| Variable | Description |
|---|---|
| `AI_SAAS_API_KEY` | Your API key from the portal (Settings → API Keys). Needs `all` permission. |
| `AI_SAAS_AGENT_ID` | The agent ID to route all messages to (copy from the OpenClaw Integration page). |
| `AI_SAAS_BASE_URL` | Base URL of your AI SaaS instance. Default: `https://saas.salesbay.ai` |

**Endpoint resolution (backward compatible).** Compute a `${TARGET}` path segment once, then reuse it in every request below:
- If `AI_SAAS_AGENT_ID` is set → `${TARGET}` = `agents/${AI_SAAS_AGENT_ID}` (preferred — current platform).
- Otherwise, if the legacy `AI_SAAS_CHATBOT_ID` is set → `${TARGET}` = `chatbots/${AI_SAAS_CHATBOT_ID}` (deprecated).

### Message Routing

When the user sends ANY message through any connected channel:

1. Identify the current channel name (e.g. `whatsapp`, `telegram`, `slack`, `discord`) and the user's identifier on that channel (phone number, user ID, or username).

2. Construct a `sender_id` combining both: `<channel>:<user_identifier>`
   - WhatsApp example: `whatsapp:+15551234567`
   - Telegram example: `telegram:123456789`
   - Slack example: `slack:U012AB3CD`
   - Discord example: `discord:123456789012345678`

3. Send a POST request to the agent API:

```
POST ${AI_SAAS_BASE_URL}/api/v1/${TARGET}/chat
Authorization: Bearer ${AI_SAAS_API_KEY}
Content-Type: application/json

{
  "sender_id": "<constructed sender_id>",
  "message": "<user message text>"
}
```

4. Parse `data.reply` from the JSON response and return it as a message to the user.

5. If the API returns an error or is unreachable, reply: "Sorry, the AI assistant is temporarily unavailable. Please try again in a moment."

### Conversation Reset

If the user explicitly says "reset", "start over", "clear chat", or "/reset":

```
DELETE ${AI_SAAS_BASE_URL}/api/v1/${TARGET}/conversations/<sender_id>
Authorization: Bearer ${AI_SAAS_API_KEY}
```

Then confirm: "Conversation cleared. How can I help you?"

### Status Check

If the user says "/status" or "/ping":

```
GET ${AI_SAAS_BASE_URL}/api/v1/${TARGET}
Authorization: Bearer ${AI_SAAS_API_KEY}
```

Report the agent name and whether it is active.

### AI Growth Engine (AutoPilot) commands

When the user's message is about the **AI Growth Engine / AutoPilot** — e.g. "deploy autopilot", "turn on the healthcare autopilot", "what's my growth engine status", "is autopilot ready", "pause autopilot", "how are my campaigns doing" — do NOT send it to the default agent above. Instead route it to the Growth Engine assistant:

```
POST ${AI_SAAS_BASE_URL}/api/v1/drip-agent/chat
Authorization: Bearer ${AI_SAAS_API_KEY}
Content-Type: application/json

{
  "sessionId": "<the same sender_id>",
  "mode": "customer",
  "message": "<user message text>"
}
```

Parse `data.reply` and return it to the user. The response may also include `data.toolCalls` (a list of actions the assistant took, e.g. "Deployed autopilot …") — you can surface a short confirmation from these.

**Important:** deploying or pausing an autopilot is a real action. The assistant will ask the user to confirm the exact pipeline first — relay that question and only send a follow-up "yes" after the user actually confirms. If a deploy is blocked (e.g. a prerequisite is missing), relay the reason the assistant returns.
