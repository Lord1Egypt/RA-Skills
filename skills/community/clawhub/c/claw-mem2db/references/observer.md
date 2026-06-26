# Observer and session hooks

claw-mem plugs into OpenClaw's session lifecycle with two hooks:

## Observation capture (per tool call)

Every time the agent calls a tool, the observer:

1. Checks `skipTools` — if the tool is in the list, abort
2. Extracts structured fields: `type`, `title`, `facts[]`, `narrative`, `concepts[]`, `filesRead[]`, `filesModified[]`, `toolName`, `promptNumber`
3. Computes a content hash; de-duplicates against recent observations (within `dedupWindowMs`)
4. Estimates tokens for future budgeting
5. Writes to the `observations` table + FTS index

The `type` classification is a closed enum (claw-mem does not mutate it):

- **discovery** — newly found fact about the codebase / environment / world
- **decision** — chose X over Y for a reason
- **pattern** — recurring structure worth noting
- **learning** — new capability or understanding
- **issue** — bug, blocker, unknown
- **change** — mutation to files / state / config
- **explanation** — answer to a user question

## Memory injection (per new prompt)

Before the next user prompt is handed to the model, claw-mem builds a **memory context**:

1. Find recent observations relevant to the current session / agent / question
2. Apply `tokenBudget`, `maxObservations`, `maxSummaries` caps
3. Render as markdown (one section per observation type)
4. Inject as a system-message-level prefix

`claw-mem mem peek` renders exactly this artifact without triggering the injection. Use it to debug "why didn't the agent remember X?"

## Session summarization (on session end)

When a session closes, claw-mem summarizes it into the `session_summaries` table:

- `request` — what the user asked for
- `investigated` — what the agent explored
- `learned` — key takeaways
- `completed` — what shipped
- `nextSteps` — what's still open
- `notes` — loose ends

Summaries have a higher injection priority than raw observations in future memory contexts.

## Opting out

- `config.enabled: false` — disable the whole skill
- `skipTools: [...]` — add more tool names to skip
- `mem forget <sessionId>` — delete observations from a specific session
- `mem prune --before <iso>` — drop everything older than a cutoff
