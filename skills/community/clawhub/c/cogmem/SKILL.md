---
name: "cogmem-memory-backend"
description: "Install and connect cogmem as a durable memory backend for OpenClaw. Version 2.5.1."
metadata:
  openclaw:
    tags: [memory, cogmem, cognitiveos]
---

# cogmem Memory Backend for OpenClaw

Use this skill when an OpenClaw workspace needs `cogmem` (the `@CognitiveOS/core` successor package) as its durable memory backend.

## Ground Rules

- Use TOML config only: `~/.cogmem/config.toml` or project `.cogmem/config.toml`.
- Do not create .agent-brain.env files.
- Do not pass `--env-path`.
- Do not configure kernel behavior through `AB_*`, `COGMEM_*`, or `AGENT_BRAIN_MODEL_*` environment variables.
- Do not import `AGENTS.md`, `TOOLS.md`, `HEARTBEAT.md`, or `BOOTSTRAP.md`; they are operational instructions, not durable user memory.
- Do not run a separate vector search before calling `memory.recall()`. `KernelAgentMemoryBackend.recall()` is the first-class recall path and already performs pulse activation, temporal traversal, graph traversal, and narrative assembly.

## Install

Run from the OpenClaw workspace root:

```bash
bun add "github:liuqin164/Cogmem#main"
./node_modules/.bin/cogmem-init --agent openclaw --scope project
./node_modules/.bin/cogmem-doctor
```

For a specific version:
```bash
bun add "github:liuqin164/Cogmem#<commit>"
```

This creates project-local kernel config and storage under `.cogmem/`, which is the recommended OpenClaw workspace setup.

```bash
./node_modules/.bin/cogmem-init --agent openclaw --scope project
```

The install creates:

```text
.cogmem/config.toml
.cogmem/memory.db
.cogmem/snapshots/
```

## Configure Embedding Model

To embed imported memories with a local quantized model, run Ollama locally and configure the kernel before importing:

```bash
ollama pull qwen3-embedding:0.6b
```

```toml
[core]
vector_dimension = 1024

[embedding]
provider = "openai_compatible"
base_url = "http://localhost:11434/v1"
model = "qwen3-embedding:0.6b"
```

Use the matching dimension for larger local models: `qwen3-embedding:4b` uses `2560`; `qwen3-embedding:8b` uses `4096`. Run `./node_modules/.bin/cogmem-doctor` after editing. Imported records are embedded through the configured kernel embedder during `cogmem-import-openclaw`.

## Migrate Existing OpenClaw Memory

Always preview first:

```bash
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --dry-run
```

Then migrate:

```bash
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw
```

Use JSON output when another agent is orchestrating the run:

```bash
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --json
```

The importer is idempotent. Re-running it skips records already imported into the same memory database.
Real non-JSON imports print source-level and embedding+ingest progress to stderr. Use `--json --progress` to keep JSON on stdout while streaming progress to stderr, or `--no-progress` when a wrapper needs quiet stderr.

Imported sources:

- `USER.md` as user profile memory.
- `SOUL.md`, `PERSONA.md`, and `IDENTITY.md` as persona/profile memory.
- `MEMORY.md` as imported summary/index memory.
- `memory/YYYY-MM-DD.md` and `memory/YYYY-MM-DD-<slug>.md` as daily episodic memory.
- `sessions/*.md`, `session-logs/*.md`, `session_logs/*.md`, `conversations/*.md`, `exports/sessions/*.md`, and `exports/conversations/*.md` as session memory.

Useful scoped imports:

```bash
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --date 2026-05-07
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --session ./custom-session.md
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --memory ./custom-memory.md
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --session ./one.md --session ./two.md
./node_modules/.bin/cogmem-import-openclaw --workspace . --project openclaw --memory ./one.md --memory ./two.md
```

## Runtime Wiring

Use `KernelAgentMemoryBackend` for turn storage and recall:

```ts
import {
  KernelAgentMemoryBackend,
  createMemoryKernelFromConfig,
} from 'cogmem';

const kernel = createMemoryKernelFromConfig();
const memory = new KernelAgentMemoryBackend(kernel);

await memory.rememberTurn({
  agentId: 'openclaw',
  projectId: 'openclaw',
  sessionId,
  userText,
  assistantText,
});

const recall = memory.recall({
  agentId: 'openclaw',
  projectId: 'openclaw',
  query: userText,
});

const preparedContext = {
  mode: recall.recallMode,
  narrative: recall.narrative,
  pulseTrace: recall.pulseTrace,
  temporalLabels: recall.temporalTraversal?.labels,
  memories: recall.items,
};
```

Use `recall.narrative` as the compact prompt context and `recall.items` as cited memory evidence. If `recall.recallMode === 'universe_navigation'`, the memory kernel has already prepared related context through the pulse/temporal/narrative path.

## OpenClaw Host Integration Notes

`cogmem-connect openclaw` installs this file into `<workspace>/skills/cogmem-memory/SKILL.md`, which is OpenClaw's workspace skill location. That makes the procedure discoverable without changing OpenClaw host config.

Current OpenClaw memory config is OpenClaw-owned. Its documented backend selector is `memory.backend` with values such as `"builtin"` and `"qmd"`, and the built-in memory surface exposes tools such as `memory_search` and `memory_get`. Do not write `plugins.slots.memory` or other unknown OpenClaw config fields for cogmem; OpenClaw uses strict config validation and unknown fields can prevent the Gateway from starting.

To make every future OpenClaw turn automatically use the memory kernel, install the local plugin wrapper:

```bash
./node_modules/.bin/cogmem-connect openclaw --workspace . --auto --force
```

`--auto` writes `<workspace>/extensions/cogmem-auto-memory/`, patches `plugins.load.paths`, and enables `hooks.allowPromptInjection=true` and `hooks.allowConversationAccess=true` for the wrapper. The wrapper registers `before_prompt_build` for governed recall and `agent_end` for turn recording, then calls `KernelAgentMemoryBackend` through `cogmem` public API via a Bun bridge. cogmem does not import OpenClaw.

Queued remember is the default. `agent_end` appends a durable JSONL job under `.cogmem/queue/openclaw-remember.jsonl` and spawns a background drain process, so Telegram or gateway responses are not blocked by embeddings, SQLite writes, or slow local models. If a drain fails, the job is retried and then moved to a dead-letter file instead of being silently discarded.

After package updates or config drift, repair the host wiring:

```bash
./node_modules/.bin/cogmem-doctor --fix --agent openclaw --workspace .
```

The wrapper maps OpenClaw behavior to cogmem like this:

- `memory_search` should call `memory.recall()` and return `recall.narrative` plus cited `recall.items`.
- `memory_get` should read from the cited evidence returned by core or from the original workspace file when a citation includes a file path.
- Prompt injection should use `recall.narrative`, not a raw vector nearest-neighbor dump.
- Turn capture should enqueue `memory.rememberTurnWithResult()` after the agent response. If OpenClaw exposes tool calls, tool results, or task events in the hook payload, the wrapper records them as ledger events with parent/child causality; if a result has no matching call, it is stored as a partial-causality task event instead of inventing a chain.

## Debug Recall

Normal prompt injection stays compact. When a user asks where a memory came from, why it was recalled, or why another candidate was filtered, run:

```bash
./node_modules/.bin/cogmem-explain-recall --query "<user question>" --project openclaw --agent openclaw --json
```

Inspect `sourceAnchor`, `activationPath`, `whyMatched`, `filteredEvidence`, and `governanceReason`. `sourceAnchor` points back to raw ledger events or imported source files. `filteredEvidence` is for audit/debug and must not be injected wholesale into normal prompts.

After runtime wiring changes, run:

```bash
openclaw config schema
openclaw doctor
openclaw plugins inspect <plugin-id> --runtime --json
openclaw gateway restart
```

## Dream Curator (Background Service)

The Dream Curator runs as a systemd user service for background memory consolidation:

```bash
systemctl --user status cogmem-dream-curator
journalctl --user -u cogmem-dream-curator -n 20
```

Run manually:
```bash
./node_modules/.bin/cogmem dream --project openclaw --watch --interval-ms 30000 --promote --json
```

## MCP Bridge Option

If the OpenClaw environment exposes an MCP client, use the core MCP bridge instead of writing a native plugin first:

```bash
./node_modules/.bin/cogmem-mcp
```

Expose these tools to the agent:

- `cogmem_remember_turn`
- `cogmem_recall`
- `cogmem_explain_recall`
