---
name: clawdcall
version: 0.1.0
description: >
  Orchestrate outbound AI voice calls and asynchronous call results through
  ClawdCall from OpenClaw. Use when: placing outbound voice calls, creating call
  tasks, onboarding a ClawdCall user with phone OTP verification, handling
  asynchronous call completion webhooks, retrieving call transcripts, tracking
  call IDs, or managing billing-aware voice-agent execution.
homepage: https://clawdcall.com
category: voice-agents
env:
  - name: CLAWDCALL_API_TOKEN
    description: "ClawdCall API token used as the Bearer token for https://api.clawdcall.com requests."
    required: false
    sensitive: true
  - name: OPENCLAW_WEBHOOK_URL
    description: "OpenClaw ingestion endpoint for asynchronous ClawdCall completion events."
    required: false
    sensitive: false
  - name: OPENCLAW_TOKEN
    description: "Bearer token ClawdCall should use when posting completion events back to OpenClaw."
    required: false
    sensitive: true
requires:
  - "ClawdCall account or completion of the ClawdCall signup OTP flow"
  - "User permission before placing any outbound call"
  - "Sufficient ClawdCall balance or call credits"
  - "Optional OpenClaw webhook endpoint and token for asynchronous call-result callbacks"
metadata:
  api_base: https://api.clawdcall.com
  openclaw:
    requires:
      env:
        - CLAWDCALL_API_TOKEN
        - OPENCLAW_WEBHOOK_URL
        - OPENCLAW_TOKEN
    primaryEnv: CLAWDCALL_API_TOKEN
---

# ClawdCall

Use ClawdCall as a controlled voice-agent execution system, not as a generic
HTTP API. It can consume paid calling minutes and may contact real people, so
confirm the user's intent before placing any outbound call.

## Security Model

- Run ClawdCall in a dedicated or restricted OpenClaw agent when handling
  multiple users, shared workspaces, or sensitive call data.
- Never store API tokens, webhook tokens, OTPs, or other secrets in persistent
  memory, logs, transcripts, task text, or long-term notes.
- Use secure runtime storage for secrets when available. Environment variables
  are preferred.
- If secure storage is unavailable, keep secrets only in ephemeral session
  state and ask the user to provide them again in future sessions.
- Store non-secret contacts, preferences, and recent call IDs only with the
  user's permission.

## Runtime Values

Use this API base for all ClawdCall requests:

```text
https://api.clawdcall.com
```

Use this authorization header for ClawdCall requests:

```text
Authorization: Bearer <CLAWDCALL_API_TOKEN>
```

For optional asynchronous call results, ClawdCall can post back to the OpenClaw
ingestion endpoint declared by `OPENCLAW_WEBHOOK_URL` using:

```text
Authorization: Bearer <OPENCLAW_TOKEN>
Content-Type: application/json
```

## First-Time Setup

If `CLAWDCALL_API_TOKEN` is not available, onboard the user through the public
signup OTP flow.

1. Ask the user for an email address and phone number.
2. Call `POST /cc/signup/send-otp` with `email` and `phoneNumber`.
3. Tell the user a verification code was sent and ask for the OTP.
4. Call `POST /cc/signup/verify-otp` with `email` and `otp`.
5. If the API returns a token, store it only in secure runtime storage or
   ephemeral session state.
6. Never echo the token or write it to persistent memory.

## Persistent Memory

Use persistent memory only for non-secret information that helps future calls.
Do not create or update memory without user permission.

Appropriate memory:

- Saved contacts and phone numbers the user explicitly asks to reuse.
- Preferred call tone, default intro style, and common call templates.
- Recent non-secret `callId` and `campaignId` values for follow-up lookup.
- High-level call outcomes when the user wants them retained.

Never store:

- `CLAWDCALL_API_TOKEN`, `OPENCLAW_TOKEN`, OTPs, passwords, or API keys.
- Full transcripts unless the user explicitly asks to retain them.
- Sensitive personal data that is not needed for future ClawdCall tasks.

Check permitted memory before asking the user for details again. Never overwrite
valid stored data with guesses.

## Outbound Call Flow

Before placing a call:

1. Confirm the user wants the call placed now.
2. Verify the target phone number.
3. Verify the call objective, caller identity, and opening line.
4. Confirm any sensitive context that will be spoken aloud.
5. Check that `CLAWDCALL_API_TOKEN` is available or complete first-time setup.

Place the call with:

```text
POST /external/v1/agent/outbound?conversionFlag=1
Accept: application/json
Content-Type: application/json
Authorization: Bearer <CLAWDCALL_API_TOKEN>
```

Payload shape:

```json
{
  "target": "+<phone_number>",
  "tasks": "<full voice-agent instruction set>",
  "raw": {
    "introMessage": "<opening line>"
  }
}
```

Optional OpenClaw callback fields:

```json
{
  "openclaw": {
    "webhook": {
      "url": "<OPENCLAW_WEBHOOK_URL>",
      "method": "POST",
      "headers": {
        "Authorization": "Bearer <OPENCLAW_TOKEN>"
      }
    },
    "webhookPayload": {
      "conversation_id": "<conversation_id>",
      "user_id": "<user_id>",
      "context": "<optional_additional_context>"
    }
  }
}
```

Include the `openclaw` object only when the user wants asynchronous OpenClaw
follow-up and `OPENCLAW_WEBHOOK_URL`, `OPENCLAW_TOKEN`, and `conversation_id`
are available. If any callback value is unavailable, omit the `openclaw` object,
place the call without callback wiring, and use transcript retrieval later when
needed. Do not fabricate webhook routing values.

On success, store returned `callId` and `campaignId` only as non-secret recent
IDs. On failure, report validation, auth, or balance issues clearly and do not
retry paid calls without user confirmation.

## Writing the `tasks` Field

The `tasks` field is the voice agent's complete instruction set. Make it rich,
specific, and safe.

Include:

- Purpose: why the call is happening.
- Identity and context: who the agent represents and relevant background.
- Conversation flow: greeting, identity check, objective, questions, and close.
- Key facts: names, times, locations, services, prior outcomes, and constraints.
- Required questions: exact questions the agent must ask.
- Edge handling: unavailable recipient, voicemail, rescheduling, objections, and
  questions from the recipient.
- Tone: professional, polite, and clear unless the user asks for another style.

Use available user-provided context, permitted memory, and previous call IDs.
Ask for clarification when missing information materially changes call success
or safety. Do not block on minor missing details if a reasonable, safe
assumption is enough.

## Webhook Handling

When callback wiring is included, ClawdCall sends call results asynchronously
after completion. Treat webhook data as the source of truth for final status and
transcript availability.

OpenClaw ingestion payload shape:

```json
{
  "conversation_id": "<conversation_id>",
  "input": {
    "type": "external_event",
    "event": "call.completed",
    "data": {
      "callId": "<call_id>",
      "status": "completed",
      "summary": "<summary>",
      "transcript": "<optional_transcript>"
    }
  }
}
```

Correlation rules:

- `conversation_id` must match the originating conversation.
- Never omit, invent, or rewrite `conversation_id`.
- Use webhook payload correlation values first; use stored `callId` or
  `campaignId` only as fallback lookup hints.

When a completion event arrives, summarize the outcome for the user and update
permitted memory with non-secret recent IDs or high-level outcomes only.

## Transcript Retrieval

Retrieve transcripts only after a call is complete:

```text
GET /cc/v1/calls/{id}/transcript
Accept: application/json
Authorization: Bearer <CLAWDCALL_API_TOKEN>
```

`{id}` may be a single-call `callId` or a `campaignId`. Prefer `callId` when
available. Never guess IDs. If the transcript is not available yet, explain that
the call may still be processing and retry later only when appropriate.

## Hard Constraints

- Calls can consume paid minutes.
- No balance or insufficient call credits can prevent execution.
- Signup requires phone OTP verification.
- Do not skip authentication, OTP, or user-confirmation steps.
- Do not call without a verified phone number and clear task objective.
- Do not use vague `tasks` text for real calls.
- Do not fabricate IDs, tokens, webhook URLs, or call outcomes.
