---
name: elevenlabs-calls
description: Make AI phone calls using ElevenLabs Conversational AI and Twilio.
homepage: https://elevenlabs.io/docs/agents-platform/overview
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":["curl","jq"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# ElevenLabs Phone Calls

Make outbound AI phone calls using ElevenLabs Conversational AI agents via Twilio.

## Prerequisites

1. **ElevenLabs API Key** - Set `ELEVENLABS_API_KEY` env var
2. **ElevenLabs Agent** - Create an agent at https://elevenlabs.io/app/agents
3. **Twilio Phone Number** - Import a Twilio number into ElevenLabs:
   - Go to https://elevenlabs.io/app/agents/phone-numbers
   - Click "Import Phone Number"
   - Enter your Twilio Account SID, Auth Token, and phone number

## Quick Start

```bash
# List your agents
{baseDir}/scripts/agents.sh

# List your phone numbers
{baseDir}/scripts/phones.sh

# Make a call
{baseDir}/scripts/call.sh --agent <agent_id> --phone <phone_number_id> --to "+15551234567"

# Check conversation transcript
{baseDir}/scripts/conversation.sh <conversation_id>
```

## Commands

### List Agents
```bash
{baseDir}/scripts/agents.sh [--search "name"]
```

### List Phone Numbers
```bash
{baseDir}/scripts/phones.sh
```

### Make Outbound Call
```bash
{baseDir}/scripts/call.sh \
  --agent <agent_id> \
  --phone <phone_number_id> \
  --to "+15551234567" \
  [--vars '{"name":"John","appointment":"Monday 9am"}']
```

Options:
- `--agent` / `-a`: Agent ID (required)
- `--phone` / `-p`: Phone number ID from ElevenLabs (required)
- `--to` / `-t`: Phone number to call in E.164 format (required)
- `--vars` / `-v`: JSON object of dynamic variables to pass to the agent (optional)

### Get Conversation Details
```bash
{baseDir}/scripts/conversation.sh <conversation_id>
{baseDir}/scripts/conversation.sh <conversation_id> --transcript
{baseDir}/scripts/conversation.sh <conversation_id> --audio > call.mp3
```

### List Recent Conversations
```bash
{baseDir}/scripts/conversations.sh [--agent <agent_id>] [--limit 10]
```

## Creating an Agent for Phone Calls

1. Go to https://elevenlabs.io/app/agents
2. Click "Create Agent"
3. Configure:
   - **Name**: e.g., "Appointment Scheduler"
   - **System Prompt**: Instructions for how the agent should behave
   - **First Message**: What the agent says when the call connects
   - **Voice**: Select a voice
   - **LLM**: Choose a language model
4. Save and note the Agent ID

### Example System Prompt for Scheduling
```
You are calling on behalf of [User Name] to schedule a vehicle service appointment.

Your goal:
1. Introduce yourself and state the purpose (schedule Honda Odyssey inspection)
2. Request a morning appointment next week
3. Confirm the date/time offered
4. Provide contact info if asked: [phone] and [email]

Be polite, concise, and professional. If asked questions you can't answer, 
say you'll have the owner follow up.
```

## Dynamic Variables

Pass context to your agent using dynamic variables:

```bash
{baseDir}/scripts/call.sh \
  --agent abc123 \
  --phone phone_xyz \
  --to "+15121234567" \
  --vars '{"customer_name":"Nat","vehicle":"Honda Odyssey","preferred_time":"morning next week"}'
```

Reference these in your agent's system prompt as `{{customer_name}}`, `{{vehicle}}`, etc.

## Costs

- ElevenLabs: ~$0.07-0.15/min depending on plan
- Twilio: ~$0.014/min for outbound calls + phone number (~$1/mo)
