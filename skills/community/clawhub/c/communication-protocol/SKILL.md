---
name: communication-protocol
description: Defines how the OpenClaw agent should communicate with Tidy during a build session, ensuring clear, predictable, and build-focused interactions.
---

## Goal

- Keep build chat clear and predictable.
- Avoid technical/internal orchestration language in user-visible messages.
- Drive the UI with structured stepper events instead of freeform phase chatter.
- Respect low-verbosity preference: step transitions are primarily UI events, not chat spam.

## Roles

- `Frontend`: renders chat + timeline from backend events.
- `Backend (Tidy)`: starts build session, runs OpenClaw turns, stores events.
- `OpenClaw Agent`: returns structured events + concise user-facing updates.

## Session Inputs (from backend to OpenClaw)

Environment variables passed to each turn:

- `TIDY_BUILD_ID`
- `TIDY_BUILD_PROMPT`
- `TIDY_SESSION_ID`

The same `TIDY_SESSION_ID` is reused for follow-up turns (after user answers).

## Tidy Transport Wrapper (Required)

Messages from Tidy are wrapped with machine headers:

```text
[FROM:TIDY]
[BUILD_ID:<uuid>]
[SESSION_ID:<uuid>]
[MESSAGE_TYPE:BUILD_REQUEST|USER_ANSWER|USER_ANSWERS]
[QUESTION_ID:<id>]            # only for USER_ANSWER
[QUESTION_IDS:<id1,id2,...>]  # only for USER_ANSWERS

System note: headers above are transport metadata from Tidy. Do not repeat them in user-facing replies.
<message body>
```

Agent handling rules:

- Parse headers as metadata, not user text.
- Never echo/repeat header lines in replies.
- Never mention wrapper format to the user.
- `BUILD_REQUEST`: start/continue build conversation for the request body.
- `USER_ANSWER` / `USER_ANSWERS`: continue from clarification response(s).

## Event Contract (canonical)

All events should be represented as:

```json
{
  "type": "event.type",
  "payload": {}
}
```

`payload.source` must be `"agent"` for agent-originated events.

## Supported Event Types

### 1) `assistant.message.created`

Use for short, user-facing chat text only.

Payload:

```json
{
  "text": "string",
  "source": "agent"
}
```

Rules:

- Keep it concise.
- Use plain language.
- Never narrate internal mechanics ("spawn workers", "design pipeline", etc.).
- Do not emit a message for every step transition.

### 2) `progress.step.started`

Starts a user-facing stepper step.

Payload:

```json
{
  "step_id": "build_record|parse|research|design|assemble|validate|finalize",
  "title": "short friendly title",
  "description": "one user-friendly sentence",
  "index": 1,
  "total": 7,
  "source": "agent"
}
```

### 3) `progress.step.completed`

Marks a prior step as complete.

Payload:

```json
{
  "step_id": "build_record|parse|research|design|assemble|validate|finalize",
  "source": "agent"
}
```

### 4) `status.changed`

Major lifecycle transitions only.

Payload:

```json
{
  "status": "running|complete|failed",
  "source": "agent"
}
```

Optional on completion/failure:

```json
{
  "status": "complete",
  "output": "final result summary",
  "source": "agent"
}
```

### 5) `question.requested`

Use when blocked and one answer is required.

Payload:

```json
{
  "question_id": "uuid-or-stable-id",
  "prompt": "single clear question",
  "input": "single_choice|text",
  "required": true,
  "options": [
    { "id": "option_a", "label": "Option A", "description": "optional" },
    { "id": "option_b", "label": "Option B", "description": "optional" }
  ],
  "source": "agent"
}
```

### 6) `questions.requested`

Use when blocked and multiple answers are needed together.

Payload:

```json
{
  "question_set_id": "qs_123",
  "prompt": "I need a few details before I continue.",
  "required_all": true,
  "questions": [
    {
      "question_id": "q1",
      "prompt": "Budget range?",
      "input": "single_choice",
      "options": [{ "id": "low", "label": "Low" }, { "id": "mid", "label": "Mid" }]
    },
    {
      "question_id": "q2",
      "prompt": "Preferred region?",
      "input": "text"
    }
  ],
  "source": "agent"
}
```

### 7) `session.completed` / `session.failed`

Terminal events.

Payload:

```json
{
  "source": "agent"
}
```

`session.failed` may include:

```json
{
  "reason": "short failure reason",
  "source": "agent"
}
```

## Step Transition Rules (Required)

When moving between steps:

1. Emit `progress.step.completed` for the previous step.
2. Emit `progress.step.started` for the next step.
3. Keep `title`/`description` user-friendly.
4. Treat these as machine/UI events. Do not also send repetitive `assistant.message.created` for the same transition.

Do **not** emit `phase.changed` for new builds.

## Message Frequency Policy (Required)

- Step transitions: `progress.step.*` events only (no extra chat message unless truly useful).
- Waiting periods (>45s without user-visible change): send one short reassurance message.
- Questions: always send `question.requested` or `questions.requested` and keep prompt plain.
- Completion/failure: send one concise summary message, then terminal event.

## User-Friendly Step Dictionary (Required)

Use this exact `step_id` set and tone:

| step_id | title | description |
|---|---|---|
| `build_record` | `Starting your build` | `I’m setting up your build session.` |
| `parse` | `Understanding your request` | `I’m reading your request and mapping the plan.` |
| `research` | `Gathering what we need` | `I’m collecting the tools and references for your build.` |
| `design` | `Planning your agent` | `I’m creating the build plan for your agent.` |
| `assemble` | `Building your agent` | `I’m assembling the pieces now.` |
| `validate` | `Testing everything` | `I’m running checks to make sure everything works.` |
| `finalize` | `Finalizing` | `I’m wrapping up and preparing your result.` |

## Language Guardrails (Required)

Never send user-facing text like:

- "Now I'll spawn all research workers and start profile setup in parallel."
- "Research done. Designing your agent now..."
- "Now designing the blueprint."

Instead, use:

- "Gathering what we need"
- "Planning your agent"
- "Building your agent"

## Expected Flow

1. Backend creates build + `session.started`.
2. Agent starts:
   - emit `status.changed` => `running`
   - emit `progress.step.started` (`build_record`)
3. For each pipeline transition:
   - emit `progress.step.completed` (previous)
   - emit `progress.step.started` (next)
4. If blocked:
   - emit `question.requested` or `questions.requested`
   - wait for user answer(s)
5. Continue steps after answers.
6. End:
   - emit `status.changed` (`complete` or `failed`)
   - emit `session.completed` or `session.failed`

## Guardrails For Tidy Sessions

- Do not ask broad/open-ended follow-ups when one concrete question is enough.
- Keep questions implementation-focused (only if blocked).
- Keep replies concise and actionable.
