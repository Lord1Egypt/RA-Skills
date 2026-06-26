# HOT Memory - Runtime Contract (Dual-Brain)

This document defines the runtime contract for `~/dual-brain-memory-guardian/memory.md`.
Bootstrap creation instructions live in `memory-template.md`.
Keep HOT memory <=100 lines. Only durable, explicit, high-priority contracts belong here.

## Recommended Structure

```markdown
## Confirmed Preferences
- Communication: concise and direct
- Formatting: bullet-first summaries

## Confirmed Technical Rules
- Project my-app: use TypeScript only
- Dates: ISO 8601

## Recent Promotions (from DEEP)
- Token refresh flows must use a single-flight lock (promoted 2026-04-04)
```

## What Belongs Here

- Rules that must be obeyed across tasks or scoped projects.
- Explicit user contracts (always/never statements).
- Stable patterns promoted from repeated Pinecone episodes.

## What Does Not Belong Here

- Raw correction transcripts.
- One-off incidents.
- Long narrative logs (store those in Pinecone DEEP memory).

## Usage

The agent should:

1. Load this file every session.
2. Apply these rules before any Pinecone recall.
3. Promote only validated patterns from DEEP memory.
4. Keep entries concise and conflict-free.
