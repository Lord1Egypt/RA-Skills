---
name: claw-mem2db
description: Standalone OpenClaw skill that automatically (and on demand) captures the agent's chat conversations and tool-call chains into a local SQLite + FTS5 database, then replays them as token-budgeted context on the next prompt — so the agent doesn't forget across restarts, compaction, or new sessions. Captures `message_received` / `message_sent` (chat, with explicit cues like "remember this" / "note this" promoted to `decision` observations; bilingual EN + zh-CN cue dictionaries built in) and `after_tool_call` (tool); reads on `before_prompt_build` via hybrid recall (FTS5 search on the latest user message merged with the recent tail). Use when the user wants long-lived agent memory, wants to search past chats and tool-call observations, wants explicit "remember this" cues to stick, wants memory to survive restarts / compaction, or wants to export / import memory across machines. Zero-config — `openclaw plugins install @chainofclaw/claw-mem` is sufficient; works fully on its own with no chain interaction and no external services. Exposes agent-callable tools (`mem-search`, `mem-status`, `mem-forget`) and a CLI namespace (`openclaw mem ...`). Session summaries default to the OpenClaw inference surface (`openclaw infer model run`) so no extra API key is needed. Optional companion: install `coc-soul` alongside to upload memory snapshots on-chain, register a DID identity, mirror to P2P decentralized storage, and recover from a different device after corruption — together they enable "digital immortality" / "silicon-based persistence" for an AI agent.
version: 2.3.1
metadata:
  openclaw:
    homepage: https://www.npmjs.com/package/@chainofclaw/claw-mem
    primaryEnv: CLAW_MEM_DATA_DIR
    requires:
      bins:
        - node
      anyBins:
        - claw-mem
        - openclaw
    install:
      - kind: node
        package: "@chainofclaw/claw-mem"
        version: "2.3.1"
        bins:
          - claw-mem
---

# claw-mem2db — persistent semantic memory for agents

A standalone, plug-in memory layer for OpenClaw agents. claw-mem2db turns every conversation and every tool call into a queryable history — automatic capture, local SQLite + FTS5 storage, hybrid recall on the next prompt. **Use it on its own** for long-lived agent memory; **pair it with `coc-soul`** for on-chain backup, DID identity, P2P storage, and cross-device recovery — i.e. digital / silicon-based persistence.

> **Naming note.** This ClawHub skill is published as **`claw-mem2db`** because the bare `claw-mem` slug was taken. The underlying artifacts keep the original names:
>
> - **npm package:** [`@chainofclaw/claw-mem`](https://www.npmjs.com/package/@chainofclaw/claw-mem)
> - **OpenClaw plugin id:** `claw-mem` (auto-loaded after `openclaw plugins install`)
> - **Standalone CLI binary:** `claw-mem` — *only present if you separately ran `npm i -g @chainofclaw/claw-mem`*. `openclaw plugins install` does **not** put it on your PATH.
>
> Inside OpenClaw, you don't need the standalone bin. Use the agent tools or `openclaw mem …` (covered below).

## Install

The plugin ships on npm as `@chainofclaw/claw-mem`. The full real-world install command is:

```bash
openclaw plugins install @chainofclaw/claw-mem --dangerously-force-unsafe-install --force
```

Two flags are needed in practice — neither is "skip safety checks for fun":

- **`--dangerously-force-unsafe-install`** — claw-mem legitimately uses `child_process` (the `openclaw` summarizer mode spawns `openclaw infer model run`; bootstrap helpers shell out). OpenClaw's static scan flags any plugin that imports `child_process`, so this flag is required to whitelist a known-safe consumer. It is **not** disabling sandboxing of the running plugin.
- **`--force`** — allows reinstalling/upgrading over an existing extension directory without the "already installed" abort.

If `openclaw plugins install` itself errors out (npm cache `EACCES`, registry timeout, etc.), fall back to the in-place tarball install — see the appendix in `references/cli.md`.

### After install: writable data dir

claw-mem opens its SQLite DB on first activation. The data dir auto-resolves (1.1.17+):

  1. `config.dataDir` (per-instance plugin config — set this when the defaults below don't work)
  2. `$CLAW_MEM_DATA_DIR` (operator env override)
  3. `$OPENCLAW_STATE_DIR/claw-mem` (OpenClaw's standard sandboxed state-dir)
  4. `~/.claw-mem` (standalone default)

The first writable candidate wins. If every candidate fails, the plugin throws an actionable error — it does **not** silently fall back to `/tmp`.

**Sandboxed hosts (Docker, restricted-uid runners) commonly hit `EACCES` on `~/.claw-mem`** because `$HOME` is read-only or owned by a different uid. The fix is to point claw-mem at an explicitly-writable directory in `~/.openclaw/openclaw.json`:

```jsonc
{
  "plugins": {
    "entries": {
      "claw-mem": {
        "config": {
          "dataDir": "/home/node/.openclaw/state/claw-mem"
        }
      }
    }
  }
}
```

Use whatever absolute path is writable in your environment (`~/.openclaw/state/claw-mem` is a good default since OpenClaw already owns that tree). Restart the gateway after editing. Verify with `openclaw mem status` — if it returns counts (even 0/0/0), the DB opened successfully.

## Zero-config (after the install + dataDir step)

**No further setup needed.** No chain interaction, no external services, no required env vars beyond the dataDir override above (and only when the default isn't writable).

- **Session hooks auto-register**: every tool call becomes a candidate observation; sessions are summarized on close.
- **Reads work immediately** once any observations have been captured.
- **`CLAW_MEM_DATA_DIR`** is the only env knob and it has a sensible default.

**Memory-only mode is expected, not a degradation.** The gateway log line `[claw-mem] Loaded (memory layer only)` is intentional — claw-mem deliberately owns *only* the memory layer. If you've also installed `coc-node` and/or `coc-soul`, each registers its own commands/tools under its own root, so the three plugins cleanly compose without stepping on each other.

**Session summaries** default to `openclaw` mode when loaded inside OpenClaw (1.1.16+). Each session-end summary is generated by spawning `openclaw infer model run --json` — the summarizer reuses whatever inference provider the host's OpenClaw agent is already authenticated for. **No claw-mem-specific API key, no extra env var, no model picker.** If the spawn fails (openclaw not on PATH, no provider auth) the summarizer falls back to a heuristic stringifier so observations still get summaries. Override with `summarizer.mode: "heuristic"` to skip LLM calls entirely, or `summarizer.mode: "llm"` + `summarizer.llm.apiKey` (or `ANTHROPIC_API_KEY` env) to talk to Anthropic directly via the bundled SDK.

## Mental model

Two streams feed the same store:

- **Chat** — every user message (and optionally every assistant message) is run through a lightweight extractor that flags explicit cues (e.g. "remember this", "note this", "for the record" — full bilingual EN + zh-CN dictionary in the cue config) as `decision` observations and preference cues (e.g. "I prefer", "from now on", "always use") as `learning`. Plain chat lands as a low-signal `discovery`.
- **Tool calls** — every tool the agent runs becomes a typed observation (discovery / decision / pattern / learning / issue / change / explanation), capturing what was read, edited, searched, or executed.

Both streams write into a single local SQLite database with FTS5 full-text search. On each new prompt, claw-mem assembles a token-budgeted **memory context** via hybrid recall — an FTS5 search on the latest user message merged with the recent tail — and injects it into the next prompt. Sessions are summarized on close (the host's OpenClaw inference provider does the summarization, no extra API key needed).

What the agent gets in return:
- No more "I forgot what we were doing" between sessions or after compaction
- Searchable history of decisions, preferences, and the rationale behind them
- Explicit "remember this" cues in chat reliably stick as `decision` observations (bilingual EN + zh-CN cue dictionaries built in)
- All memory stays local by default — no network, no chain, no external service

## Optional companions: from local memory to digital immortality

claw-mem2db is **complete on its own**. It needs nothing else to capture, search, or inject memory. But two adjacent skills extend the agent in directions claw-mem deliberately doesn't:

| Skill | What it adds on top of claw-mem | When to install |
|---|---|---|
| [coc-soul](https://clawhub.ai/ngplateform/coc-soul) | On-chain memory snapshots, DID identity, P2P / IPFS-backed storage, cross-device recovery & resurrection | When you want the agent to survive a host dying, a disk failing, or a move to a different machine — i.e. **digital / silicon-based persistence** |
| [coc-node](https://clawhub.ai/ngplateform/coc-node) | Running a COC blockchain node so the agent participates in the network instead of just consuming it | When you want the agent to be a first-class peer rather than a guest |

The plugins are fully decoupled: claw-mem doesn't know whether coc-soul is installed, and works the same way either way. Installing coc-soul alongside claw-mem creates the immortality story (memory captured locally → snapshotted to chain + IPFS → recoverable from a fresh host using the agent's DID), but you can adopt it later without changing anything in claw-mem.

## How to use it

### From inside an agent loop (preferred)

The plugin registers three agent-callable tools. **Use these — not shell commands — when you're an agent answering the user.** No PATH lookup, no plugin discovery, no shell context required.

| Tool | Parameters | Returns |
|---|---|---|
| `mem-search` | `query` (required), `limit?`, `type?` (`discovery` \| `decision` \| `pattern` \| `learning` \| `issue` \| `change` \| `explanation`) | Matching observations from FTS5 index |
| `mem-status` | none | Stats: observation/summary/session counts, agents, DB path, tokenBudget |
| `mem-forget` | `sessionId` (required) | Confirms deletion of that session's observations |

Typical agent-side patterns:
- Before deciding how to approach a familiar-feeling task, call `mem-search` with the topic — past decisions and their rationale will surface.
- Before claiming "I'm not sure about X," call `mem-search` for X.
- When the user says "forget that whole session" or you notice a session is polluting search results, call `mem-forget` with the session id from `mem-status`.

### From a human shell (CLI)

When operating from a terminal — install/upgrade scripts, ops checks, manual cleanup — use the OpenClaw CLI namespace. Every memory operation is reachable as `openclaw mem <subcommand>`.

```bash
openclaw mem search "checkpoint"        # FTS5 keyword/phrase search
openclaw mem search "..." --type decision --limit 20 --json
openclaw mem status                     # DB stats; --json for machine output
openclaw mem peek                       # preview the context that would be injected
openclaw mem forget <sessionId>         # delete one session's observations
openclaw mem prune --older-than 90      # drop observations older than 90 days
openclaw mem prune --before 2025-01-01  # explicit cutoff
openclaw mem export memory.json         # dump observations to JSON
openclaw mem import memory.json         # restore from JSON
```

Sibling subtrees:
```bash
openclaw mem config get|set|list|path       # plugin config (persisted to ~/.claw-mem/config.json)
openclaw mem db vacuum|migrate-status|size  # SQLite maintenance
openclaw mem version                        # plugin version
```

## Configuration knobs worth knowing

- `tokenBudget` (default 8000) — how much of the next prompt goes to memory context
- `maxObservations` / `maxSummaries` (50 / 10) — hard caps on what's considered for injection
- `skipTools` — tools the observer skips entirely (defaults exclude `TodoWrite`, `AskUserQuestion`, `Skill` because they're usually noisy meta-tools)
- `dedupWindowMs` (30000) — de-duplicate observations with the same content hash within this window
- `summarizer.mode` — `openclaw` (default inside OpenClaw — spawns `openclaw infer model run`), `heuristic` (no LLM), or `llm` (direct Anthropic SDK with own apiKey)
- `summarizer.openclaw.model` — pin a specific provider/model for summary calls (default: let OpenClaw pick); `summarizer.openclaw.timeoutMs` defaults to 60000ms

### Chat compaction (2.3.0+) — automatic summarization & space reclamation

By default, chat capture writes one observation per message. Over time the chat tail grows and the agent's tokenBudget gets eaten by raw chitchat. v2.3.0 adds a compactor that rolls batches of chat observations into a single `chat_compaction` summary, and (optionally) hard-deletes low-importance originals to reclaim space.

**Pipeline:**

1. **Capture-time denoising** — emoji-only / pictograph-only turns are dropped entirely (don't even reach the DB). Each captured row gets a heuristic `importance` score (0.0–1.0) computed from cue match, presence of dates / URLs / code / numbers, length, role, and chitchat-token detection.
2. **Trigger** — every `chatMemory.compaction.triggerEvery` chat captures (default 10) the compactor runs in the background. It also fires opportunistically on `agent_end`.
3. **Roll-up** — the compactor pulls uncompacted chat rows (skipping the most-recent `keepRecentRaw`, default 20), passes the batch through the configured summarizer (`openclaw` mode by default — same auth path as session summaries), writes a single `chat_compaction` observation tagged `tool_name="chat_compaction"` with `importance=0.9`, then marks the originals `compacted=1, compacted_into=<id>`.
4. **Prune** — when `deleteCompactedLowValue=true` (default), compacted rows whose `importance < minImportanceToKeep` (default 0.7) are hard-deleted. The most-recent `keepRecentRaw` are always retained regardless of importance.
5. **Recall** — `before_prompt_build` and `mem-search` exclude `compacted=1` rows by default, so the agent reads the compaction summary + the recent tail instead of seeing the same content twice.

**Schema (migration v3, additive — safe on existing DBs):**

| Column | Type | Default | Meaning |
|---|---|---|---|
| `compacted` | INTEGER | `0` | `1` = rolled into a chat_compaction; hidden from default recall / search |
| `importance` | REAL | `0.5` | heuristic score; higher = more worth keeping |
| `compacted_into` | INTEGER | NULL | id of the chat_compaction observation that this row was rolled into (audit trail) |

**Config (under `chatMemory.compaction`):**

- `enabled` (default `true`)
- `triggerEvery` (default `10`) — run a pass every N captures
- `keepRecentRaw` (default `20`) — never compact the most-recent N
- `deleteCompactedLowValue` (default `true`) — hard-delete after compaction
- `minImportanceToKeep` (default `0.7`) — prune threshold
- `idleMs` (default `120000`) — reserved for future idle-based trigger

Set `chatMemory.compaction.enabled = false` to keep raw chat rows forever (audit-heavy use). Set `deleteCompactedLowValue = false` to keep all originals on disk but still benefit from cleaner recall (the compaction summary stays small).

### Chat memory (2.1.0+ / renamed knobs in 2.2.0)

Pure chat sessions used to slip past the observer because capture only fired on `after_tool_call`. v2.1.0 added `message_received` / `message_sent` capture so spoken-only conversations build up memory too. v2.2.0 also exposes the schema in `openclaw.plugin.json` so `openclaw plugins inspect claw-mem` shows both hooks and config keys, and renames the knobs to match the OpenClaw operator-side conventions (breaking — see migration table below). Defaults are conservative: user messages are captured, assistant messages are not.

- `chatMemory.enabled` (default `true`) — master switch for chat capture
- `chatMemory.explicitOnly` (default `false`) — only capture when the message contains an explicit cue ("remember this", "note this", "for the record", "save this", and the equivalent zh-CN tokens shipped in the default cue dictionary); silences everything else
- `chatMemory.minChars` (default `8`) — drop shorter messages as chitchat
- `chatMemory.maxNarrativeChars` (default `500`) — truncate the captured narrative body at this many characters
- `chatMemory.cues.explicit` / `chatMemory.cues.preference` — override the cue dictionaries (defaults ship bilingual EN + zh-CN); preference cues ("I prefer", "from now on", "always use" + zh-CN equivalents) become `learning` observations. To inspect or override the actual default tokens, run `openclaw mem config get chatMemory.cues`
- `chatMemory.captureAssistant` (default `false`) — also capture assistant messages via `message_sent` (use sparingly — high noise)

Chat observations now carry `toolName: "message_received"` (user) or `toolName: "message_sent"` (assistant) — a 1:1 mapping with the originating hook so downstream filters can write `tool_name IN ('message_received','message_sent')` for "all chat" or pull just one direction. Still no schema migration; the existing `tool_name` column carries the value.

**2.1.0 → 2.2.0 migration (config keys):**

| Old (2.1.0) | New (2.2.0) |
|---|---|
| `chatMemory.minLen` | `chatMemory.minChars` |
| `chatMemory.captureAssistantPromises` | `chatMemory.captureAssistant` |
| (hard-coded 500) | `chatMemory.maxNarrativeChars` |
| chat observations had `tool_name: "chat"` | now `"message_received"` / `"message_sent"` |

### Context recall

How `before_prompt_build` picks observations to inject:

- `contextRecall.mode` (default `hybrid`) — `recent` keeps the chronological tail; `hybrid` runs an FTS5 search on the latest user message and merges the hits with the recent tail (deduped by id). Hybrid surfaces topical past memories instead of always showing the last N regardless of relevance.
- `contextRecall.searchLimitRatio` (default `0.5`) — fraction of `maxObservations` reserved for search hits in hybrid mode; the rest is filled with recent.

Hybrid mode falls back transparently to recent-only if the search throws or no user-message text is available.

Edit any knob with `openclaw mem config set <path> <value>`.

## Hardening (opt-outs)

Default behavior: claw-mem auto-injects a memory context block into every prompt (via `before_prompt_build`) and exposes `mem-search` / `mem-status` / `mem-forget` to the agent. That's the right default for "give the agent persistent memory and let it use it."

If your deployment wants memory to be **query-only** — captured in the background, but never auto-injected and never callable from inside the agent loop — the gateway provides two host-side switches in `~/.openclaw/openclaw.json`:

```jsonc
{
  "plugins": {
    "entries": {
      "claw-mem": {
        "hooks": {
          // Block claw-mem's before_prompt_build hook from stuffing context
          // into the next prompt. Observation capture (after_tool_call) and
          // session summarization (session_end) still fire — only the
          // prompt-side injection is suppressed.
          "allowPromptInjection": false
        }
      }
    }
  },
  // Host-level filter: hide these tools from the agent's tool list entirely.
  // Useful for tightening the agent's surface (e.g. blocking exec/process)
  // and/or making memory access human-only via the CLI.
  "skipTools": ["exec", "process", "mem-search"]
}
```

Pick what fits your threat model:

- **Capture but don't inject** — set `allowPromptInjection: false`. Observations still accumulate; you read them via `openclaw mem search` when needed.
- **CLI-only memory** — also add `mem-search` (and optionally `mem-status` / `mem-forget`) to the host's `skipTools`. The agent can no longer query memory; only humans can via `openclaw mem …`.
- **Default ("memory just works")** — leave both unset.

Note: the plugin-config knob `skipTools` (under `plugins.entries.claw-mem.config.skipTools`, listed above) is a **different** filter. It controls which **observed** tool calls the *observer* records, not which tools the *agent* can see. The host-level `skipTools` at the top of `openclaw.json` is what gates agent visibility.

## Verification (post-install smoke test)

After `openclaw plugins install @chainofclaw/claw-mem` (or an in-place upgrade), restart the gateway and run:

```bash
openclaw mem status              # proves the plugin is loaded; shows 0/0/0 on a fresh DB
openclaw mem peek                # context that would inject on the next prompt
openclaw mem db migrate-status       # confirms schema is current; 0 pending migrations
```

All three should succeed without errors. Common failure modes:

- **`unknown command 'mem'`** — the plugin failed to load. Check `plugins.allow` in `~/.openclaw/openclaw.json` and the gateway startup logs for `[claw-mem] Loaded` (or a `[claw-mem] Bootstrap failed:` line).
- **`Bootstrap failed: ... EACCES ... /home/.../.claw-mem`** — the default `~/.claw-mem` isn't writable on this host. Apply the explicit `dataDir` override from the [Install](#after-install-writable-data-dir) section.
- **`mem search` / `mem-search` agent tool returns "tool not found"** — check whether the host has `mem-search` in `skipTools` (see [Hardening](#hardening-opt-outs)). If yes, that's intentional; query via the CLI or remove the entry.

## When NOT to use this skill

- You want ephemeral agent sessions with no persistent history — don't install claw-mem; OpenClaw's in-session context is enough.
- You want memory-like search *only for code* — tools like grep / ripgrep / `codebase_search` serve that need without the persistence overhead.
- You want on-chain / cross-device backup — add [coc-soul](https://clawhub.ai/ngplateform/coc-soul) on top; claw-mem only persists locally.

## Reference

- `references/cli.md` — every `openclaw mem|config|db` subcommand, plus the standalone-bin appendix
- `references/config.md` — complete config schema
- `references/observer.md` — how observations are extracted, when hooks fire
- `references/programmatic-api.md` — using `Database` / `ObservationStore` / `SearchEngine` as a library

Source and issue tracker: <https://github.com/NGPlateform/claw-mem>.
