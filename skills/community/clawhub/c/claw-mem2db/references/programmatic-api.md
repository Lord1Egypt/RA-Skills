# Programmatic API (library usage)

Every memory primitive is exported from `@chainofclaw/claw-mem`. Use these when embedding claw-mem in your own agent framework, not as an OpenClaw plugin.

## Open the database

```ts
import { Database } from "@chainofclaw/claw-mem";

const db = new Database("/home/you/.claw-mem/claw-mem.db");
db.open();
// ... use db.connection (the underlying node:sqlite handle)
db.close();
```

`db.open()` runs pending migrations on first call.

## Write an observation

```ts
import { ObservationStore } from "@chainofclaw/claw-mem";

const obs = new ObservationStore(db);
obs.insert({
  sessionId: "session-1",
  agentId: "my-agent",
  type: "discovery",
  title: "FTS index rebuilt on launch",
  facts: ["FTS5 table rebuilt on every schema migration"],
  narrative: null,
  concepts: ["sqlite", "fts"],
  filesRead: [],
  filesModified: [],
  toolName: "Read",
  promptNumber: 1,
});
```

## Search

```ts
import { SearchEngine } from "@chainofclaw/claw-mem";

const search = new SearchEngine(db);
const { results, totalCount, source } = search.search({ query: "fts", limit: 5 });
// source is "fts" or "like" (fallback when FTS5 query parsing fails)
```

## Build injection context

```ts
import { buildContext } from "@chainofclaw/claw-mem";

const ctx = buildContext(db, {
  sessionId: "session-1",
  agentId: "my-agent",
  tokenBudget: 8000,
  maxObservations: 50,
  maxSummaries: 10,
});
console.log(ctx.markdown);
console.log("tokens used:", ctx.tokensUsed);
```

The returned `markdown` is literally what would be prepended to the next prompt.

## Extract an observation from a tool call

```ts
import { extractObservation } from "@chainofclaw/claw-mem";

const observation = extractObservation({
  toolName: "Read",
  toolInput: { file_path: "/src/foo.ts" },
  toolResult: "... file content ...",
  sessionId: "session-1",
  agentId: "my-agent",
  promptNumber: 3,
});
if (observation) obs.insert(observation);
```

## Summarize a session

```ts
import { summarizeSession } from "@chainofclaw/claw-mem";

const summary = summarizeSession(db, {
  sessionId: "session-1",
  agentId: "my-agent",
});
// persisted to session_summaries
```

## Re-exported from sub-packages

For convenience the umbrella also re-exports the `node` and `soul` public APIs — you don't need to import `@chainofclaw/node` separately:

```ts
import { NodeManager, BackupManager } from "@chainofclaw/claw-mem";
```
