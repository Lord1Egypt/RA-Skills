# Room Protocol - Chat Rooom

## Standard Room Layout

Use this layout for each active room:

```text
.chat-rooom/rooms/<room>/
|- room.md
|- summary.md
|- jobs.md
|- claims.md
|- channels/
|  |- general.md
|  |- build.md
|  `- review.md
`- inbox/
   |- planner.md
   `- builder.md
```

## Message Block Format

Append messages as short markdown blocks:

```markdown
## 2026-03-06T12:40:00Z | @codex | ask
To: @claude
Channel: general
Refs: `<workspace>/src/app.ts`, `pnpm test app`
Message: Need a failure hypothesis for the flaky search test.
```

## Message Kinds

- `ask` -> directed request with a clear next action
- `update` -> progress or evidence
- `proposal` -> suggested path, room change, or job split
- `decision` -> accepted direction or settled convention
- `block` -> current stop condition
- `handoff` -> transfer with next owner
- `done` -> closure with proof or link

## Mention Routing

When a message assigns work to one agent:
1. Append the full block to the channel file.
2. Add a one line pointer to `inbox/<agent>.md`.
3. Remove or archive the inbox pointer after the agent answers.

## Claims

Use one row per claimed surface:

| Surface | Owner | Since | Expires | Intent |
|---------|-------|-------|---------|--------|
| `lib/search.ts` | `@builder` | 12:40Z | 13:10Z | bug fix |

Claims should expire quickly. Long claims hide idle time and block healthy overlap.

## Summary Contract

`summary.md` should answer four questions in under ten lines:
- What is happening now?
- What has already been decided?
- What is blocked?
- Who acts next?
