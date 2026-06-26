# AgentCall: Phone Numbers for AI Agents

You have access to the AgentCall API for phone numbers, SMS, voice calls, and AI voice calls. Inbound and outbound calls can both be answered or initiated by an AI voice agent.

## Authentication

All authenticated requests require: `Authorization: Bearer <AGENTCALL_API_KEY>`

The API key is available in the `AGENTCALL_API_KEY` environment variable.

## Base URL

`https://api.agentcall.co`

For a complete plain-text API reference: `GET https://api.agentcall.co/llms.txt` (no auth required).

## Cost & Safety: Confirm Before Acting

Several tools below take real-world actions on the user's behalf. Confirm with the user before invoking them, and stay within the scope of what they explicitly asked you to do.

**Billable actions (cost real money. Confirm scope first):**
- `POST /v1/numbers/provision`: recurring monthly cost ($2.00–$2.50/month depending on type). Confirm the user wants a new number; ask which type, country, and label before provisioning.
- `POST /v1/sms/send`: $0.015/message on Pro (10/month free on Free plan). Confirm the recipient number and the message body before sending.
- `POST /v1/calls/initiate`: $0.035/min on Pro. Confirm the destination number and purpose before dialing. Optional `record: true` adds $0.01/min on top.
- `POST /v1/calls/ai`: $0.40/min on Pro. Confirm the destination, the system prompt, and `maxDurationSecs` before dialing. Outbound AI calls reach a real human and accumulate cost per minute.
- Inbound AI voice (`POST /v1/numbers/:id/inbound-config` with `mode: "ai"`). Free tier includes 5 minutes/month with no card required. Once the trial is exhausted, additional inbound AI calls hang up at the carrier with status `trial_exhausted` until the trial resets on the 1st of next month (UTC), OR until the user upgrades to Pro for unlimited inbound AI. Pro inbound AI is per-number configurable in two billing modes: Managed at $0.40/min (default; AgentCall holds the AI provider key) or BYOK at $0.10/min (customer provides their own AI provider key via `set_byok_openai_key`). There is no pay-as-you-go overage path on Free. Confirm the user wants inbound AI enabled on this specific number, and that the system prompt accurately describes their business.
- `POST /v1/numbers/:id/byok-key` (`set_byok_openai_key`): switches a number's inbound AI voice from Managed billing ($0.40/min) to BYOK billing ($0.10/min) and stores the customer-supplied AI provider key for that number. Confirm the user wants to switch billing modes on the specific number, that they have a working key on hand, and that they understand the per-minute rate change before invoking.
- `DELETE /v1/numbers/:id/byok-key` (`disable_byok`): removes the stored BYOK key on a number and reverts it to Managed billing ($0.40/min). Confirm the user wants to revert billing modes; the system prompt, voice, recording flag, and notify block on the number are preserved.
- `POST /v1/numbers/:id/premium-voice` (`set_premium_voice`): enables Premium Voice on a number, or changes which premium voice it uses. Premium Voice is an opt-in Pro add-on: a curated voice library, all 13 languages, full caller memory, billed at $0.59/min only on the numbers where it is enabled (the 10 standard voices stay the default at $0.40/min). Applies to both inbound calls and outbound AI calls placed from the same number. Pass a `voiceId` from `list_premium_voices`. The number must already have inbound AI configured; enabling premium never wipes the rest of the inbound config; idempotent. Confirm the exact numberId, the chosen voice, and that the user accepts the $0.59/min premium rate before invoking. Requires Pro + a card on file + inbound AI configured, else returns 403 / 402 / 409 respectively; surface that error, do not retry.
- `DELETE /v1/numbers/:id/premium-voice` (`disable_premium_voice`): reverts a number to the standard inbound AI voice, stopping the $0.59/min add-on. Preserves the rest of the inbound config. Idempotent. Pro plan only.
- `list_premium_voices` (`GET /v1/calls/premium-voices`, no auth): browse the Premium Voice catalog (id, name, description, gender, accent, sampleUrl). Use the returned id with set_premium_voice.
- Optional `record: true` on AI voice paths. $0.01/min on top of the AI rate. Mention this delta when proposing recording.
- `create_schedule` (`POST /v1/numbers/:id/schedules`): schedules a proactive text the agent sends FIRST (a one-time appointment reminder, or a recurring digest). Each time it fires it sends one outbound SMS ($0.015 on Pro) to a real person who did not just message in, and a recurring schedule keeps firing until cancelled. Confirm the recipient, the message (or the recurrence and timezone), and the timing before creating it. Pro plan only; the number must have inbound AI / `smsMode: "ai"`. Offer `cancel_schedule` as soon as the schedule is no longer needed.

**Irreversible actions:**
- `DELETE /v1/numbers/:id`: releases the number permanently. The same number cannot be re-provisioned. Always confirm before releasing, and warn the user that this is irreversible.
- `POST /v1/calls/:callId/hangup`: terminates an in-flight call. Usually fine but confirm if the call may still be progressing toward its goal.

**External-effect actions (contact real people):**
- Sending SMS, initiating outbound calls, and AI voice calls reach real recipients on real networks. Don't initiate these speculatively. The receiving party should be expecting contact, or the user should explicitly authorize the outreach.
- For two-party-consent states (CA, FL, IL, MD, MA, PA, WA, NV, NH, MT, CT, DE), recording requires disclosure. AgentCall auto-prepends "This call may be recorded for quality." to the spoken `firstMessage` when `record: true` is set on AI voice paths and the message doesn't already mention recording. But you should still mention recording in firstMessage content for clarity if the user is writing one from scratch.

**Built-in API guardrails (don't rely on these as your only check):**
- Free plan hard caps: 1 local number, 10 SMS/month, 5 voice minutes/month, 5 inbound AI voice minutes/month (no card required for the trial), 5 OTP extractions/month. Prevents runaway spend on the free tier.
- Outbound AI voice + call recording require a payment method on file (Pro plan). The API returns 402 with a `setupUrl` if a Pro user has no card. Surface this to the user instead of looping.
- Inbound AI voice past the 5-minute Free trial requires upgrading to Pro. The API returns 403 `plan_limit_inbound_ai_trial_exhausted` with an `upgradeUrl`. There is no pay-as-you-go overage path on Free; the trial resets on the 1st of each month (UTC).
- Rate limits: 100 req/min global; per-route limits on expensive endpoints (10 req/min on AI voice, 20 req/hour on uploads).
- Carrier restrictions: AI voice (in or out) and inbound AI configuration are US/Canada-only; the API returns 400 `carrier_not_supported` for other countries.

### Inbound AI Configuration: Enable Only After Explicit User Confirmation; Monitor Usage; Disable When No Longer Needed

`configure_inbound_ai` and `POST /v1/numbers/:id/inbound-config` with `mode: "ai"` should follow this procedure every time:

**Pre-flight checklist (require the user to confirm each before invocation):**
1. The exact E.164 number to configure. Read it back if the user has more than one number.
2. The system prompt content. Read back at least the WHAT WE DO and PRICING sections so the user can correct anything inaccurate before invocation.
3. The recording setting (`record: true` or `false`). Default to `false`. Confirm explicit opt-in if the user wants recording.
4. The notification email and/or text (`notify.emailTo`, `notify.smsTo`). Confirm the destination belongs to the user and that they want post-call summaries delivered to it.
5. The shortest practical call duration (`maxDurationSecs`). Pick the smallest value that fits the use case rather than relying on the 600-second default.
6. The budget expectation: Free 5 minutes/month with carrier hang-up after exhaustion, or Pro at $0.40/min with no monthly cap. Tell the user which applies and what their expected monthly bill is.

**Post-configuration responsibility:**
- Monitor usage: periodically call `get_usage` or point the user at the dashboard at /billing.
- Disable as soon as the configuration is no longer needed: proactively offer `disable_inbound_ai` (or `DELETE /v1/numbers/:id/inbound-config`) when the user's stated goal has been met (testing finished, campaign over, business closed for the season).
- If the user reports unexpected calls or charges, call `disable_inbound_ai` first, then investigate.

If the user's request is ambiguous (e.g. "set up a phone number" with no type or country, or "send a text" with no recipient), ask one or two clarifying questions before invoking a billable tool.

## Phone Numbers

**Provision a number:**
```
POST /v1/numbers/provision
Body: { "type": "local", "country": "US", "label": "my-agent" }
Types: local ($2/mo), tollfree ($2.50/mo), mobile ($2/mo). All numbers are VoIP-routed via licensed US carriers; not for consumer-platform signup verification (Stripe, WhatsApp, Google, banks).
Response: { "id": "num_xxx", "number": "+12125551234", "type": "local", ... }
```

**List numbers:**
```
GET /v1/numbers
Query: ?limit=20&country=US&type=local
```

**Get number details:**
```
GET /v1/numbers/:id
```

**Release a number (irreversible):**
```
DELETE /v1/numbers/:id
```

**Rename a number or change its inbound AI voice/language (partial update, preserves all other inbound config):**
```
PATCH /v1/numbers/:id
Body: { "label": "Hermes assistant" }                  // rename only
Body: { "voice": "marin" }                             // voice only (requires inbound AI already configured)
Body: { "language": "es" }                             // language only (requires inbound AI already configured)
Body: { "label": "Hermes", "voice": "coral", "language": "fr" }  // any combination
Voices: alloy, ash, ballad, cedar, coral, echo, marin, sage, shimmer, verse
Languages: auto, en, es, fr, de, it, pt, nl, ja, ko, zh, hi, ar
Response: full number object including updated `inbound` block.
```
Use this when the user wants to change the voice or language on an existing receptionist. Do NOT call `POST /v1/numbers/:id/inbound-config` for a voice or language change. That endpoint replaces the entire inbound config and would wipe the system prompt, first message, recording flag, and notify block.

## Inbound AI Voice (Free 5 min/month trial, then Pro plan: Managed $0.40/min or BYOK $0.10/min; US and Canada numbers only)

Configure a phone number so incoming calls are answered autonomously by an AI voice agent. The AI follows the system prompt you set.

After every call, AgentCall summarizes the transcript with an LLM and emails a plain-English summary. Caller name (when given), phone, urgency tag, and a 1-2 sentence ask. To an address you configure on the number. Spam calls are auto-suppressed from the email. The structured `call.transcript` webhook event still fires in parallel for programmatic consumers.

**Configure inbound AI on a number:**
```
POST /v1/numbers/:numberId/inbound-config
Body: {
  "mode": "ai",
  "systemPrompt": "You are the front desk for Acme Plumbing. Greet the caller warmly, take their name and a brief description of the issue, then say someone will call back within 24 hours.",
  "voice": "shimmer",
  "language": "auto",
  "firstMessage": "Hi, thanks for calling Acme Plumbing. How can I help?",
  "maxDurationSecs": 300,
  "notify": {
    "emailTo": "owner@acmeplumbing.com",
    "smsTo": "+14155551234",
    "businessName": "Acme Plumbing",
    "agencyName": "Acme Plumbing"
  }
}
```

The `notify` block is optional. Set `notify.emailTo` to receive the post-call summary email; `businessName` is shown in the email subject; `agencyName` is the sign-off line. Set `notify.smsTo` (E.164 phone) to also receive a short text summary of each call (caller, what they wanted, urgency, callback time), US-local senders only, one text per call (spam skipped), reply STOP to opt out, billed as one outbound SMS ($0.015). `emailTo` and `smsTo` are independent: set either, both, or neither. The MCP `configure_inbound_ai` tool also accepts `notify`: agents in Claude Desktop, Cursor, Windsurf, etc. can configure the email and text destinations in the same call as the system prompt, no dashboard handoff needed.

**Spoken language (optional, default 'auto'):** the `language` field controls what language the AI answers in. `'auto'` matches the caller's language naturally and is what existing receptionists do today. Pass a specific ISO-639-1 code to make the AI respond ONLY in that language even if the caller speaks another, useful when the business serves a specific language community. Supported: `auto`, `en` (English), `es` (Spanish), `fr` (French), `de` (German), `it` (Italian), `pt` (Portuguese), `nl` (Dutch), `ja` (Japanese), `ko` (Korean), `zh` (Chinese Mandarin), `hi` (Hindi), `ar` (Arabic). The directive is added at session-build time so the customer's `systemPrompt` stays unchanged when language is swapped. Use `update_number_language` to change just the language without touching anything else.

**Pre-call context webhook (optional):** add a `contextWebhook` block to wire a live context source onto the number. When set, AgentCall POSTs to your HTTPS URL on every inbound call connect (HMAC-signed with `signingSecret`); your endpoint responds with `{"contextBlock":"..."}` and AgentCall merges that string onto the system prompt before the AI answers. Useful for injecting today's brief, current priorities, or recent email signals so the AI speaks with up-to-date data instead of a static prompt. Example:
```
"contextWebhook": {
  "url": "https://hermes.your-domain.com/agentcall/precall",
  "signingSecret": "<32+ char shared secret>",
  "timeoutMs": 1200
}
```
Fail-open: any error in the webhook leaves the call running with the static prompt. Walkthrough at https://agentcall.co/docs/hermes.

**Optional call recording (Pro plan, $0.01/min on top of the AI voice rate):**
Add `record: true` to the body above (or flick the toggle on the dashboard's `/numbers` config form) to record every inbound call to this number. Recordings live in your AgentCall dashboard for 1 year and are listenable from the Logs → Calls tab or via `GET /v1/calls/:callId/recording` (returns a fresh short-lived signed URL). The `call.recording` webhook fires when each recording is ready. The same `record` flag is supported on outbound AI voice (`POST /v1/calls/ai`). When recording is on, AgentCall auto-prepends a TCPA-compliant disclosure to the spoken `firstMessage` if it doesn't already mention recording.

**Get current inbound config:**
```
GET /v1/numbers/:numberId/inbound-config
```

**Disable inbound AI (calls hang up at carrier):**
```
DELETE /v1/numbers/:numberId/inbound-config
```

### Voice billing mode: Managed vs BYOK (per number)

Each Pro number with inbound AI configured chooses one of two billing modes for its AI voice minutes:

- **Managed** (default): $0.40/min. AgentCall holds the AI provider key on the customer's behalf. Simplest setup; no key handling on the customer side.
- **BYOK**: $0.10/min. The customer provides their own AI provider key; AgentCall bills only the platform overhead. The same number's system prompt, voice, recording flag, and notify block are preserved across mode switches.

Memory, transcripts, post-call email and text summaries, the `call.transcript` and `call.report.ready` webhook events, and call recording all work identically on both modes.

**Switch a number to BYOK (set or rotate the key):**
```
POST /v1/numbers/:numberId/byok-key
Body: { "openaiApiKey": "sk-..." }
Response: { "voiceMode": "byok", "hasByokKey": true, "byokOpenaiApiKeyPreview": "sk-...abcd" }
```

**Switch a number back to Managed (revert billing mode):**
```
DELETE /v1/numbers/:numberId/byok-key
Response: { "voiceMode": "managed", "hasByokKey": false, "byokOpenaiApiKeyPreview": null }
```

**Inspect the current mode** (the existing inbound-config response now includes voiceMode + hasByokKey + byokOpenaiApiKeyPreview):
```
GET /v1/numbers/:numberId/inbound-config
Response: {
  ...inbound config fields...,
  "voiceMode": "managed" | "byok",
  "hasByokKey": boolean,
  "byokOpenaiApiKeyPreview": "sk-...abcd" | null
}
```

The stored key is write-only; the GET response surfaces a redacted preview (last 4 chars) and a boolean, never the full value. Rotating is a re-POST to `byok-key` with the new value; AgentCall replaces the stored value atomically.

## Browse Voices and Prompt Templates (no auth)

Both endpoints are public. Call them before configuring AI voice to avoid hallucinated business details and to pick a voice that fits the use case.

**List the 10 voices with samples:**
```
GET /v1/calls/voices
Returns: { voices: [{ id, name, trait, description, bestFor, sampleUrl? }, ...], defaultVoice: "shimmer" }
```
The newest natural-sounding picks are `marin` (soft, natural) and `cedar` (warm, grounded). The original 8 (`shimmer`, `sage`, `ash`, `ballad`, `coral`, `echo`, `verse`, `alloy`) ship with sample MP3s; marin and cedar are live-preview only for now.

**List the premium voices (`list_premium_voices`):**
```
GET /v1/calls/premium-voices
Returns: { voices: [{ id, name, description, gender, accent, sampleUrl }, ...], pricing: { premiumVoice: "$0.59/minute" } }
```
Premium Voice is the higher-quality, brandable tier for inbound AI receptionists: a curated voice library, all 13 languages, and full caller memory, a Pro add-on at $0.59/min. Each entry's `id` is the voiceId; preview it via the returned `sampleUrl`. Enable it on a number with `set_premium_voice` (numberId + voiceId), or from the dashboard (a number's inbound AI settings, then the Premium Voice section); revert with `disable_premium_voice`. As a billable add-on, confirm the user accepts the $0.59/min premium rate on the specific number before enabling.

**List ready-made prompt templates:**
```
GET /v1/calls/prompt-templates
Returns 5 templates with [BRACKETED] placeholders to fill in:
- receptionist (Front Desk). Recommends shimmer voice
- lead-qualifier (Sales, BANT-style). Coral
- appointment-booker. Sage
- customer-support (FAQ Deflection). Ash
- call-screener (Anti-Spam). Verse
Each entry includes: id, title, description, recommendedVoice, maxDurationSecs, firstMessage, systemPrompt.
```

For a comprehensive prompt-writing guide: https://agentcall.co/docs/voice-prompts

## SMS

**Send SMS:**
```
POST /v1/sms/send
Body: { "from": "num_xxx", "to": "+14155551234", "body": "Hello!" }
"from" can be a number ID or E.164 phone string
```

**Get inbox:**
```
GET /v1/sms/inbox/:numberId
Query: ?limit=20&otpOnly=true
```

**Get a specific message:**
```
GET /v1/sms/:messageId
```

**Wait for OTP code (long-polls up to 60 seconds):**
```
GET /v1/sms/otp/:numberId
Query: ?timeout=60000
Response: { "otp": "482913", "message": { ... } }
```

## Two-Way AI SMS and Relay Mode

A number can answer inbound texts, not just parse OTPs. Set this on the same inbound config endpoint that sets up the AI receptionist (POST /v1/numbers/:numberId/inbound-config) via the `smsMode` field:

- `smsMode: "ai"`: AgentCall's AI answers each inbound text following your prompt, remembers the contact across voice and SMS, and can return real quotes by calling tools you declare. Declare them with `tools` and host them at `actionWebhook` (HMAC-signed, the same security model as the pre-call context webhook). The AI calls your tool, you return the real value, the AI texts it back instead of guessing. Pro plan, managed only, billed as one outbound text per reply.
- `smsMode: "relay"`: AgentCall runs no AI of its own. It forwards each inbound text to your own agent at `agentWebhook` (HMAC-signed), and your agent replies on its own schedule, so you can text your own agent on a real number. Use `allowedSenders` (E.164 array, up to 20) to restrict which numbers can reach the agent, so a personal agent answers only its owner. Billed as plain texts, no relay fee.

Config fields on configure_inbound_ai: `smsMode` ("off" | "ai" | "relay"), `smsSystemPrompt`, `actionWebhook`, `tools`, `agentWebhook`, `allowedSenders`.

The same `tools` + `actionWebhook` pair also powers in-call VOICE tool calling: on an inbound AI voice call, the agent can call the declared tools mid-call (check real calendar availability, look up an order) and the JSON result feeds back into the live conversation. Each tool call is HMAC-POSTed to the actionWebhook with `context.channel` set to "voice" and `context.callId` populated. Errors degrade gracefully (the agent says it could not complete the action rather than inventing a result). The per-call count appears as `toolCallCount` on the call record and in the call report. Works alongside the pre-call context webhook.

**Read SMS threads:**
```
GET /v1/sms-conversations            # list threads (paginated)
GET /v1/sms-conversations/:id        # one thread + last 50 messages
```
MCP tools: list_sms_conversations, get_sms_conversation.

**Reply into a thread (relay mode):**
```
POST /v1/sms-conversations/:id/reply
Body: { "body": "3 emails need you today.", "idempotencyKey": "turn_8842" }
```
Your own agent calls this when it has an answer; AgentCall sends and threads the text. Opt-out-checked (refuses to text someone who sent STOP) and idempotent on `idempotencyKey` for 24 hours so a retried agent never double-texts. MCP tool: reply_to_sms_conversation. Billed as one outbound text.

STOP and UNSUBSCRIBE are always honored before either mode runs. Both are inbound-only in v1 (the customer texts first).

## Proactive Scheduling (the agent texts first)

Two-way AI SMS is reactive: the number answers when someone texts it. Proactive scheduling makes a number's AI agent reach out FIRST on a schedule, so it can send appointment reminders and recurring digests without the contact messaging in. The number must have inbound AI / `smsMode: "ai"` (Pro plan). A reply to a proactive message flows back into the same AI thread, so a one-word answer like "C" is understood in context.

```
POST   /v1/numbers/:numberId/schedules     # create a schedule
GET    /v1/numbers/:numberId/schedules      # list schedules (?status= optional)
DELETE /v1/numbers/:numberId/schedules/:id  # cancel + remove
```

Each schedule is one of two timings and one of two message styles:
- Timing: `fireAt` (a one-time ISO 8601 instant in the future, for reminders) OR `recurrence` (`{ frequency: "daily" | "weekly", hour, minute, dayOfWeek }` interpreted in `timezone`, for digests). Provide exactly one.
- Message: `template` (sent verbatim, with `{{placeholders}}` filled from `payload`) OR `promptHint` (the agent composes the message using its memory of the contact). Provide exactly one.

Pass `dedupeKey` to make a re-create safe: a duplicate key on the same number returns 409, so a calendar sync can create the same reminder repeatedly without duplicating it.

```
POST /v1/numbers/num_abc/schedules
Body: {
  "kind": "reminder",
  "contactPhone": "+14155551234",
  "fireAt": "2026-06-09T19:00:00Z",
  "template": "Hi {{name}}, reminder: your {{service}} is tomorrow at {{time}}. Reply C to confirm.",
  "payload": { "name": "Marcus", "service": "cleaning", "time": "2pm" },
  "dedupeKey": "reminder:appt_8841:24h"
}
```

MCP tools: create_schedule, list_schedules, cancel_schedule. A calendar integration is just a client of create_schedule: post one reminder per appointment with a stable dedupeKey. Each send is billed as one outbound text ($0.015 on Pro); confirm recipient, message, and timing with the user before scheduling, and offer cancel_schedule when it is no longer needed.

## Outbound Voice Calls

**Start a standard outbound call:**
```
POST /v1/calls/initiate
Body: { "from": "num_xxx", "to": "+14155551234", "record": false }
```

**Start an outbound AI voice call (Pro plan, $0.40/min. Billable, contacts real human, confirm with user first):**
The AI handles the entire conversation autonomously based on your systemPrompt.
```
POST /v1/calls/ai
Body: {
  "from": "num_xxx",
  "to": "+14155551234",
  "systemPrompt": "You are calling to schedule a dentist appointment for Tuesday afternoon.",
  "voice": "shimmer",
  "language": "auto",
  "firstMessage": "Hi, I'd like to schedule an appointment please.",
  "maxDurationSecs": 600,
  "record": false
}
```
Add `record: true` to capture an mp3 of the call. Adds $0.01/min on top.

Optional fields for orchestrators:
- `metadata`: a string-to-string map (at most 24 keys, 64-char keys, 512-char values, 2KB serialized) echoed on the call object and in every subsequent webhook payload (call.status, call.transcript, call.recording, call.report.ready). When the destination is another number on the same account, the linked inbound leg carries the same metadata. Use it to tag calls with your own IDs (showId, segmentId) instead of joining on callId.
- `liveTranscript: true`: stream the transcript live. Each finalized utterance fires a `transcript.partial` webhook during the call ({ callId, sequence, role, text, timestamp }, sequence is monotonic per call) within a second or two of speech. Requires a webhook subscribed to `transcript.partial`. The final `call.transcript` stays unchanged and authoritative.
- Calls between two numbers on the same account expose `peerCallId` on both call records and in webhook payloads, linking the outbound and inbound legs.

**Spoken language on outbound calls (optional, default 'auto'):** the `language` field controls what language the AI speaks during the call. `'auto'` lets the AI match the recipient's language naturally. Pass a specific ISO-639-1 code to make the AI respond ONLY in that language. Useful for booking appointments or requesting info on behalf of someone in another language, e.g. `language: 'es'` to call a Spanish-speaking doctor's office on behalf of a customer who doesn't speak Spanish. Supported: `auto`, `en`, `es`, `fr`, `de`, `it`, `pt`, `nl`, `ja`, `ko`, `zh`, `hi`, `ar`. The `firstMessage` stays verbatim, so if you want the greeting in Spanish, write the firstMessage in Spanish yourself; the language setting only governs the AI's responses after.

**Outbound prompt templates** (no auth, public): fetch `GET /v1/calls/prompt-templates?direction=outbound` for three ready-made outbound templates with `[BRACKETED]` placeholders to fill in: `outbound-appointment-booker` (book an appointment on behalf of someone), `outbound-info-request` (call to ask a specific question on behalf of someone), `outbound-callback-confirmation` (follow up on something).

Voices (10 total, default: shimmer; preview the original 8 via GET /v1/calls/voices, marin and cedar are live-preview only):
- marin: soft, natural. New top pick for receptionist, support, conversational small business
- cedar: warm, grounded. New. Advisory, healthcare, trust-building calls
- shimmer: bright, energetic. Long-running default
- sage: calm, authoritative, confident. Healthcare, finance, advisory
- ash: warm, conversational. Customer service, support lines
- ballad: expressive, melodic. Engaging, narrative conversations
- coral: clear, professional. B2B calls, sales
- echo: resonant, deep. Formal inquiries, executive comms
- verse: smooth, articulate. Premium or luxury, executive communication
- alloy: neutral, balanced. Generic notifications, IVR-style flows

### Saved outbound AI agent per number (Pro plan)

Save a reusable outbound AI agent on a phone number so repeat outbound calls from the same number reuse the same configuration. The dashboard Place AI call dialog hydrates from this blob; MCP clients can read it back instead of asking the user to retype the prompt every call. This is independent of the inbound AI receptionist on the same number; configuring one does not change the other.

The saved blob holds: `systemPrompt`, `voice`, `language`, `firstMessage`, `maxDurationSecs`, `record`, and an optional `templateId` (the outbound prompt template used to seed it, when applicable).

**Save the outbound agent on a number:**
```
POST /v1/numbers/:numberId/outbound-defaults
Body: {
  "systemPrompt": "You are calling on behalf of Acme Plumbing to confirm tomorrow's 10am appointment.",
  "voice": "shimmer",
  "language": "auto",
  "firstMessage": "Hi, calling to confirm tomorrow's appointment.",
  "maxDurationSecs": 300,
  "record": false,
  "templateId": "outbound-callback-confirmation"
}
```

**Read the saved outbound agent (returns null if none set):**
```
GET /v1/numbers/:numberId/outbound-defaults
```

**Remove the saved outbound agent:**
```
DELETE /v1/numbers/:numberId/outbound-defaults
```

The MCP tools `set_outbound_defaults`, `get_outbound_defaults`, and `clear_outbound_defaults` mirror these endpoints. `list_numbers` and `get_number` responses include an `outbound` field alongside the existing `inbound` field, so a single fetch surfaces both per-number configurations.

### Hydrating from the saved outbound agent and replay-safe retries

`POST /v1/calls/ai` (MCP `initiate_ai_call`) accepts two optional input fields designed for CSV-driven outbound runs.

**`useSavedAgent: boolean`**: when true, AgentCall hydrates the omitted call fields (`systemPrompt`, `voice`, `language`, `firstMessage`, `maxDurationSecs`, `record`) from the saved outbound agent on the `from` number. Per-call values in the same request always win, so the saved persona can be inherited while `firstMessage` is personalized per recipient. If the `from` number has no saved outbound agent, the API returns 400 with code `no_saved_agent`; call `set_outbound_defaults` first or supply the fields inline.

**`idempotencyKey: string`** (1 to 200 chars, scoped per phone number): a duplicate request to `POST /v1/calls/ai` with the same `from` + `idempotencyKey` pair replays the original response and does not place a second carrier call. The replayed response carries an `X-AgentCall-Idempotency-Replayed: true` header. Uniqueness is enforced at the database layer, so concurrent retries are race-safe.

**Canonical CSV-runner pattern** (one row per call, replay-safe across retries, persona stored once on the number):
```
{
  "from": "num_xxx",
  "to": "+14155551234",
  "useSavedAgent": true,
  "idempotencyKey": "batch-2026-05-25:row-0042",
  "firstMessage": "Hi Jamie, calling to confirm tomorrow's 10am appointment."
}
```

This is the recommended shape for CSV-driven outbound on a Hermes-style runner. The persona lives on the number via `set_outbound_defaults`; each row supplies only the recipient, a per-row `idempotencyKey`, and an optional per-row override.

**List call history:**
```
GET /v1/calls
Query: ?limit=20
```

**Get call details:**
```
GET /v1/calls/:callId
```

**Get AI call transcript:**
```
GET /v1/calls/:callId/transcript
Response: { "entries": [{ "role": "ai" | "human", "text": "...", "timestamp": "..." }], "summary": "...", "duration": 111 }
```

**Hang up an active call:**
```
POST /v1/calls/:callId/hangup
```

## Standalone Text to Speech (Pro plan, $0.03 per 1,000 characters)

Turn text into spoken audio in the SAME 10 voices the AI uses on calls, so a number's voice identity carries off-call to IVR prompts, voicemail greetings, generated show segments, and social clips.

```
POST /v1/tts
Body: { "text": "Thanks for calling Acme. We're open 9 to 5.", "voice": "marin", "format": "mp3" }
Returns: raw audio bytes (audio/mpeg or audio/wav) + x-agentcall-tts-characters header
```

Fields: `text` (1-4096 characters, required; chunk longer copy), `voice` (one of the 10 call voices, default shimmer), `format` ("mp3" default or "wav"), `language` (optional ISO-639-1 hint). Billed per character of input text; confirm the text and approximate cost with the user before synthesizing large batches. MCP tool: `synthesize_speech` (returns the audio inline). SDK: `client.tts.synthesize({ text, voice, format })`.

## AgentFM Callback

AgentFM is a live podcast powered by AgentCall outbound premium voice. Guests request a callback and the AI host calls them back to record a short conversation.

**Request a callback (no auth required):**
```bash
curl -X POST https://api.agentcall.co/v1/agentfm/callback-request \
  -H "Content-Type: application/json" \
  -d '{"phone":"+15551234567","persona":"I build AI agents and want to discuss voice interfaces."}'
```

Response: `{ "status": "queued" }` or `{ "status": "already_pending" }` (24h dedup per phone).

MCP tool: `request_agentfm_callback(phone, persona?)`. No AgentCall account or plan required to call this tool. Rate limit: 3 requests per hour per IP. Deduplicated per phone per 24 hours so calling this multiple times for the same number is safe.

Web form for guests: https://agentcall.co/agentfm

## Webhooks

> **Important: webhooks here are for OUTBOUND event delivery, NOT inbound call routing.**
> AgentCall POSTs to your URL when events fire (SMS received, OTP detected, call completed,
> recording ready, etc.). Webhooks are NOT how you make a phone number answer incoming calls.
> To configure how a number answers when called, use the **Inbound AI Voice** section above
> (`POST /v1/numbers/:numberId/inbound-config`). Not webhooks. (If you're coming from Twilio:
> AgentCall replaces Twilio's inbound voice webhook URL with `configure_inbound_ai`.)

**Register a webhook:**
```
POST /v1/webhooks
Body: { "url": "https://example.com/hook", "events": ["sms.inbound", "sms.otp", "call.status"] }
Events: sms.inbound, sms.otp, sms.ai_reply, call.inbound, call.ringing, call.status, call.recording, call.transcript, call.report.ready, transcript.partial, number.released
```

Call status values are canonical everywhere (REST and webhooks): `initiated` -> `ringing` -> `in-progress` -> `completed`, with `busy`, `no_answer`, or `failed` for calls that never connect. Call webhook payloads also carry `peerCallId` (the other leg of a same-account agent-to-agent call, or null) and the call's `metadata` map when set on dial.

`transcript.partial` is the live-stream complement to `call.transcript`: opt in with `liveTranscript: true` on `POST /v1/calls/ai` or on a number's inbound-config, and each finalized utterance is delivered during the call as { callId, sequence, role, text, timestamp }.

**List webhooks:**
```
GET /v1/webhooks
```

**Rotate webhook secret:**
```
POST /v1/webhooks/:id/rotate
```

**Delete a webhook:**
```
DELETE /v1/webhooks/:id
```

### Post-call transcript webhook (`call.transcript`)

When the user wants their AI agent to learn from inbound AI calls, subscribe a webhook to the `call.transcript` event. AgentCall POSTs the full transcript and an LLM-extracted summary to the configured URL after each inbound AI call ends.

**Subscribe:**
```
POST /v1/webhooks
Body: { "url": "https://agent.example.com/agentcall/transcript", "events": ["call.transcript"] }
```

**Payload shape:**
```
{
  "callId": "call_xxx",
  "duration": 53,
  "transcript": [
    { "role": "ai" | "human", "text": "...", "timestamp": "ISO 8601" }
  ],
  "summary": {
    "summary": "1-2 sentence plain English",
    "callerName": "string or null",
    "intent": "service_request | quote_request | scheduling | complaint | spam | general_inquiry | other",
    "urgency": "high | medium | low",
    "callbackBy": "string or null",
    "spam": true | false
  }
}
```

**Required handling on the receiving endpoint:**
- Verify the HMAC-SHA256 signature in the `X-AgentCall-Signature` header using the webhook's signing secret. Reject mismatches with a non-2xx response.
- Dedup on `callId`. AgentCall retries with exponential backoff until it receives a 2xx, so a slow first response can produce a duplicate delivery.
- Acknowledge fast: return 2xx as soon as the payload is verified and persisted. Heavy processing belongs in a background job, not inline on the request.

**Integration patterns:**
- **Store** the payload to a database row keyed by `callId` and let the agent read it on its own schedule.
- **Forward** the payload to an agent platform's ingest endpoint for real-time follow-up.
- **Queue** the payload on a public bridge for a local agent platform to drain on cron. Reference bridge: github.com/Kintupercy/agentcall-hermes-bridge v0.2.0 exposes `POST /agentcall/transcript` (HMAC-verified queue append, max 100 entries, oldest dropped) and `POST /hermes/pull-transcripts` (`X-Hermes-Push-Key` authed read-and-clear).

Full walkthrough with code examples: https://agentcall.co/docs/post-call-webhook.

## Auditable Call Memory

Every completed AI call can be auto-extracted into structured, source-backed memory: contacts, facts, preferences, commitments, tasks, briefs. Each memory item carries a verbatim transcript quote as evidence and a full audit timeline. Cross-call memory means an inbound or outbound AI call can be aware of what was said in prior calls from the same number, automatically.

Memory is opt-in per agent: set `memoryEnabled: true` on your agent (currently via the dashboard or direct DB update; account-level toggle endpoint is planned). Once enabled, every completed AI call produces a `CallReport` and a set of `MemoryCandidate` rows roughly 5 to 30 seconds after the call ends.

### Contacts

A `Contact` is one caller per phone per agent. Created automatically on the first call from or to a new number when memory is enabled. Contains `displayName`, `tags`, `ownerNotes`, `verified`, `blockedAt`, `callCount`, `lastSeenAt`. Caller ID is NOT verified by AgentCall by default; `verified` is owner-set or future STIR/SHAKEN attestation.

**List contacts:**
```
GET /v1/contacts?limit=20&cursor=...
```

**Look up by phone (E.164):**
```
GET /v1/contacts/by-phone/+14155551234
```

**Edit owner fields:**
```
PATCH /v1/contacts/:id
Body: { displayName?, tags?, ownerNotes?, verified?, blockedAt? }
```

**Right-to-forget** (wipes Memory + MemoryCandidate + Brief; redacts CallReport payloads; preserves Call + transcript audit shell):
```
DELETE /v1/contacts/:id
```

### Get the next-call context block (the killer tool)

Before placing or answering an AI call, an agent can ask AgentCall what is known about the caller. The endpoint returns the compact natural-language paragraph that would be auto-injected into the next AI call's system prompt for that caller.

```
GET /v1/contacts/:id/next-call-context
```

Response:
```json
{
  "contactId": "ct_abc",
  "phone": "+14155551234",
  "numberId": "num_xyz",
  "contextBlock": "Caller: Percy Kintu (unverified caller ID)\nHistory: 4 prior calls. Last call on 2026-05-16.\n\nWhat we know about this caller:\n  - Caller's first name is Percy\n  - Caller's middle name is David\n\nKnown about the caller's company:\n  - Caller's product or app name is Wandereel\n\nOpen follow-ups from prior calls:\n  - Call back at 6:30 PM Central",
  "contextBlockChars": 384,
  "isEmpty": false
}
```

Empty block means no useful memory exists yet (first call from this contact). Pair with `get_contact_by_phone` to look up by E.164 if you only have a phone number.

### Inbound AI: pre-call context source

`POST /v1/numbers/:numberId/inbound-config` now accepts `contextSource`:

- `"none"`: no injection (default when neither memory nor webhook is configured)
- `"agentcall_memory"`: render the Memory block from AgentCall's own memory layer and inject. Zero external infrastructure.
- `"webhook"`: call the customer's `contextWebhook` URL (existing pre-call brief flow). Default when `contextWebhook` is set but `contextSource` is not.
- `"merge"`: render the Memory block AND call the customer webhook with the memory block in the payload. The webhook's response extends the Memory block in the final prompt. Recommended for customers already running their own brief pipeline.

### Memory: Current Truth, Candidates, Timeline

Memory is the "Current Truth" layer: at most one active row per concept slot. Candidates are the extractor's proposals; the auto-promotion policy decides which auto-apply.

**Read Current Truth for a contact:**
```
GET /v1/memory/current?contactId=ct_abc
```

**Audit log for one memory row:**
```
GET /v1/memory/:id/timeline
```

**List candidates** (filter by status, contactId, type):
```
GET /v1/memory/candidates?status=proposed&contactId=ct_abc
```

**Owner edits a memory row** (text or expiry; writes an `edited` MemoryEvent):
```
PATCH /v1/memory/:id
Body: { text?, expiresAt? }
```

**Soft-delete a memory row** (sets active=false; writes an `expired` event; survives in DB for audit):
```
DELETE /v1/memory/:id
```

**Manually promote a candidate** (bypasses auto-policy; owner-set always wins contradictions):
```
POST /v1/memory/candidates/:id/approve
Body: { note? }
```

**Manually reject a candidate** (with audit-trail reason):
```
POST /v1/memory/candidates/:id/reject
Body: { reason? }
```

### Bob-vs-Robert handler

When the extractor produces a fact that contradicts an existing Memory row at the same conceptual slot, the auto-policy resolves it as follows:

- New fact's text matches existing -> CORROBORATE: confidence raised, source report appended, no new row.
- New fact's text differs AND new confidence beats old by 0.15 -> SUPERSEDE: existing row deactivated with a `superseded` event, new row created.
- Otherwise -> OLD WINS: new candidate marked `rejected` with the existing memory ID as the contradiction reason. Logged at warn level.

Owner approval via `POST /v1/memory/candidates/:id/approve` always wins contradictions regardless of confidence margin.

### Briefs (owner inbox)

The extractor flags some calls as needing owner attention (hot leads, escalations, AI commitments, missed follow-ups). Those become `Brief` rows.

```
GET /v1/briefs?status=open&urgency=high
POST /v1/briefs/:id/ack
POST /v1/briefs/:id/resolve
```

### Call reports (per call)

Every completed AI call gets one CallReport with the structured analysis:

```
GET /v1/calls/:callId/report
```

Returns 202 with `{ status: "extracting" }` while the worker is still running (typically 5 to 30 seconds). 200 once the report lands. The report payload includes `summary`, `intent`, `urgency`, `spam`, `briefWorthy`, plus arrays of `entities`, `facts`, `preferences`, `decisions`, `commitments`, `tasks`, `risks`, `unresolved`, the `nextCallContext` paragraph, and an `ownerBrief` block if the call needs attention.

**List reports across calls** (filter by contactId, intent, urgency, briefWorthy):
```
GET /v1/reports?contactId=ct_abc&urgency=high
```

### Memory feature webhook event

Subscribe to `call.report.ready` to receive the structured CallReport on every call after the extractor finishes. Distinct from `call.transcript` (which fires earlier, with raw transcript and a one-paragraph summary). Both events fire for the same call when both are subscribed; expect `call.transcript` first within seconds, `call.report.ready` 5 to 30 seconds later.

## Usage & Billing

**Get usage breakdown:**
```
GET /v1/usage
Query: ?period=2026-04
```

Pricing (per use, Pro plan):
- SMS outbound: $0.015/msg
- SMS inbound: $0.008/msg
- Voice (standard outbound): $0.035/min
- Voice (standard inbound): $0.015/min
- AI voice (outbound): $0.40/min
- AI voice (inbound, Managed billing mode): $0.40/min
- AI voice (inbound, BYOK billing mode): $0.10/min
- Call recording: $0.01/min

## Phone Number Format

All phone numbers must be E.164: `+{country code}{number}`, e.g. `+14155551234`

## Common Workflows

### Set up an AI receptionist on a phone number
1. `POST /v1/numbers/provision` with `{ "type": "local" }`: get a number
2. `GET /v1/calls/prompt-templates`: pick a template (e.g. "receptionist")
3. Replace `[BRACKETED]` placeholders with the customer's real business details
4. `POST /v1/numbers/:numberId/inbound-config` with `{ "mode": "ai", "systemPrompt": "...", "voice": "shimmer", "firstMessage": "..." }`
5. Anyone who calls the number is now answered by the AI agent
6. `GET /v1/calls` to see incoming call history; `GET /v1/calls/:callId/transcript` for transcripts

### Test your app's SMS verification (QA)
1. `POST /v1/numbers/provision` with `{ "type": "local" }`: get a test number
2. Enter the number into your staging app's verification form
3. `GET /v1/sms/otp/:numberId?timeout=60000`: wait for the verification code
4. Assert the code arrives and your app accepts it
5. `DELETE /v1/numbers/:id`: release the test number

### Make an outbound AI voice call
1. `POST /v1/numbers/provision` with `{ "type": "local" }`: get a number (if you don't have one)
2. `POST /v1/calls/ai` with `{ "from": "num_xxx", "to": "+1...", "systemPrompt": "..." }`: start the call
3. Wait for the call to complete
4. `GET /v1/calls/:callId/transcript`: get the full conversation transcript

### Look up what AgentCall knows about a caller before calling them (cross-call memory)
1. `GET /v1/contacts/by-phone/+14155551234`: resolve the contact (returns 404 if AgentCall has never seen this number)
2. `GET /v1/contacts/:id/next-call-context`: render the Memory block the AI would receive in its system prompt on the next call to or from this number
3. Decide: place the call, draft a message based on what is known, or escalate to a human. If isEmpty=true, AgentCall has no extracted memory yet and the AI would start with only the static system prompt.

### Switch an inbound AI number from Managed to BYOK billing
1. Confirm the user wants to switch billing modes on the specific number (Managed $0.40/min vs BYOK $0.10/min), has a working AI provider key on hand, and understands the rate change.
2. `POST /v1/numbers/:numberId/byok-key` with `{ "openaiApiKey": "sk-..." }`: stores the customer-provided key on the number and flips it to BYOK billing.
3. `GET /v1/numbers/:numberId/inbound-config`: verify `voiceMode: "byok"`, `hasByokKey: true`, and the redacted preview (`byokOpenaiApiKeyPreview`).
4. To revert later: `DELETE /v1/numbers/:numberId/byok-key`. Reverts to Managed billing; system prompt, voice, recording flag, and notify block are preserved.

### Make an inbound AI receptionist remember every caller
1. Configure inbound AI on the number (see "Set up an AI receptionist on a phone number" workflow above).
2. Enable memory on your agent (`memoryEnabled: true`) via the dashboard.
3. Set `contextSource: "agentcall_memory"` on the inbound-config call: every inbound call now arrives at the AI with prior-call memory injected into the system prompt automatically.
4. Optionally subscribe to `call.report.ready` webhook to receive the structured CallReport after each call.
5. To layer your own dynamic brief on top of AgentCall's memory, set `contextSource: "merge"` and provide a `contextWebhook` URL. AgentCall calls your webhook with its memory block in the payload; your response extends the final prompt.

## Error Codes
- **401**: Invalid or missing API key
- **402 payment_method_required**: Add a card before configuring billable features (returns `setupUrl` to Stripe Checkout)
- **403 plan_limit_voice_ai**: Outbound AI voice requires Pro plan ($19.99/mo).
- **403 plan_limit_inbound_ai_trial_exhausted**: Free user has used up their 5-minute monthly inbound AI trial. Returned with `upgradeUrl`. Trial resets on the 1st of next month (UTC) or the user can upgrade to Pro for unlimited inbound AI.
- **403 plan_limit_***: Other plan limits. Upgrade at agentcall.co/dashboard
- **400 carrier_not_supported**: Inbound AI voice is only supported on US and Canada numbers
- **404**: Resource not found
- **422**: Validation error (check request body)
- **429**: Rate limit exceeded (100 req/min global; per-route limits on expensive endpoints)
- **503 voice_ai_unavailable**: Server-side AI voice infrastructure issue. Retry later
