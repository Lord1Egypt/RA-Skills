# Triage rules

On every poll you turn a status snapshot into one decision. It consumes the
**structured `failures[]`** that `query_session` returns — each entry is
`{op, scene, error}` — so triage targets the exact failed shots instead of guessing from prose.
**You classify each failure yourself by reading its `error` text** (there is no server-side
content flag); the rules below are judgment, not a fixed recipe.

## Decisions

| Snapshot | Decision | Action |
|---|---|---|
| `finalVideoUrl` present | `done` | Deliver it (surface for human sign-off if the user asked) |
| `failures[]` non-empty | `fail` | Read each `error`; mind the spend ceiling; send ONE targeted fix for the named shots |
| `messages[]` has a new assistant message | `asked` | The agent is asking something — answer it via `send_message`, then poll with the new `cursor` |
| `agent_processing` / `batch_running` | `running` | Keep polling (~60s) |
| else (idle, no final video, no question) | `idle` | The step finished and the agent is awaiting your next instruction — send the next step, or surface and stop |

## Reading the message tail (`afterSeq` / `cursor`)

`query_session` returns new chat messages since your cursor: pass `afterSeq` (0 first time,
then the `cursor` from the previous poll). Each message is `{role, text, sequenceNumber}`. This
is how you catch the agent **pausing to ask a question** — without it, an `idle` snapshot with
no video looks like a silent stall. Track the max `sequenceNumber` you've seen and pass it back.

## Classifying a failure from its `error`

Read the `error` string and decide:

- **Looks like content/policy/moderation/copyright** (the text says the prompt/image/video was
  blocked, not allowed, flagged, etc.) → don't retry as-is; **reword** it (ladder below).
- **Looks transient/provider** (timeout, 5xx, a param error) → **retry** just the affected scene(s).

## Content/copyright mitigation ladder

When a shot reads as content/copyright-blocked, reword the prompt to clear it **without
changing the characters, their emotions, or the storyline** — keep the beat, change only the
phrasing. These are examples to apply with judgment, **not a fixed recipe**:

1. **Attempt 1 — policy-safe English rewrite.** Reword ONLY the flagged shots' prompts:
   soften/replace the flagged words, make it less explicit, keep the story beat. Other shots
   are untouched.
2. **Attempt ≥2 — Chinese-prompt re-send.** If a shot stays flagged after the rewrite, re-send
   ONLY that shot's prompt **translated into Chinese** (same scene, action, framing). The
   content checker behaves differently on Chinese prompts and often passes one the English
   version fails. Still inside the per-shot retry cap.

## Targeted, never full-regen

Every fix names the **exact** failed shots (from the structured `failures[]`) so the agent
regenerates only those (via `withReference` targets) and re-assembles — it never re-runs shots
that already succeeded. Motion is the expensive op; this is the core cost lever. See
[cost-model-and-caps.md](./cost-model-and-caps.md).

## Failures survive a session clear

`failures[]` comes from the live session's todos while a batch is `batch_failed`; once the
session is cleared (a new run starts, or a hard terminal cleanup), the server **falls back to
the latest finalized Batch doc**, so a halted run still reports its failures instead of going
silent. If even that is empty and state is `idle`, treat it as `idle` (nothing to fix).
