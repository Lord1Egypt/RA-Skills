---
name: cairn
version: "1.2.2"
description: Local hybrid index for things you intentionally collect — code, docs, web pages, PDFs, raw text. FTS5 + vector embeddings + AST knowledge graph in a single sqlite file. v1.2 ships explicit safety gates for ingestion (path allowlist, size caps, offline mode); v1.2.1 adds startup warning when no allowlist is set + published GGUF SHA256s for pre-cached air-gapped deployment. MCP server exposes search / graph / ask / path / tags so models can both query and maintain a curated local knowledge base.
license: MIT
disable-model-invocation: true
requires:
  env:
    - name: CAIRN_RUNTIME
      required: false
    - name: CAIRN_CHAT_MODEL
      required: false
    - name: CAIRN_CPU_ONLY
      required: false
    - name: CAIRN_DEBUG_DOC
      required: false
    - name: CAIRN_OFFLINE
      required: false
    - name: CAIRN_ALLOWED_ROOTS
      required: false
    - name: CAIRN_MAX_INGEST_FILES
      required: false
    - name: CAIRN_MAX_INGEST_BYTES
      required: false
metadata:
  clawdbot:
    requires:
      env:
        - name: CAIRN_RUNTIME
          required: false
        - name: CAIRN_CHAT_MODEL
          required: false
        - name: CAIRN_CPU_ONLY
          required: false
        - name: CAIRN_DEBUG_DOC
          required: false
        - name: CAIRN_OFFLINE
          required: false
        - name: CAIRN_ALLOWED_ROOTS
          required: false
        - name: CAIRN_MAX_INGEST_FILES
          required: false
        - name: CAIRN_MAX_INGEST_BYTES
          required: false
  openclaw:
    requires:
      env:
        - name: CAIRN_RUNTIME
          required: false
        - name: CAIRN_CHAT_MODEL
          required: false
        - name: CAIRN_CPU_ONLY
          required: false
        - name: CAIRN_DEBUG_DOC
          required: false
        - name: CAIRN_OFFLINE
          required: false
        - name: CAIRN_ALLOWED_ROOTS
          required: false
        - name: CAIRN_MAX_INGEST_FILES
          required: false
        - name: CAIRN_MAX_INGEST_BYTES
          required: false
    install:
      - id: npm-cairn-index
        kind: npm
        package: cairn-index@1.2.1
        flags: []
        label: "Install cairn (npm, optional — bundled in lib/cairn/ on clawhub)"
  author: mrsirg97-rgb
  version: "1.2.2"
  clawhub: https://clawhub.ai/mrsirg97-rgb/cairn
  source: https://github.com/mrsirg97-rgb/cairn
  npm: https://www.npmjs.com/package/cairn-index
compatibility: >-
  Node ≥ 20. Native deps build on install (better-sqlite3, sqlite-vec, three tree-sitter grammars).
  Default runtime requires ollama at http://127.0.0.1:11434 with `nomic-embed-text` pulled.
  Set CAIRN_RUNTIME=embedded to run embed + chat in-process via node-llama-cpp (auto-downloads GGUFs to ~/.cairn/models on first use, ~785 MB; set CAIRN_OFFLINE=1 to block the download path and require pre-cached models).
  Network egress: (a) explicit `cairn add <url>` (user-initiated web ingest), (b) localhost ollama only when CAIRN_RUNTIME=ollama, (c) Hugging Face GGUF download on first use only when CAIRN_RUNTIME=embedded and the model isn't pre-cached. CAIRN_OFFLINE=1 blocks (a) and (c); (b) stays available because it's localhost.
  No API keys, no telemetry, no accounts.
---

# cairn

Local hybrid index for the things *you* intentionally collect — codebases, design docs, audit notes, web pages, PDFs, raw text. Curate, ingest, retrieve. One sqlite file, no daemons (embedded) or one daemon (ollama).

## What cairn is for

Local-first retrieval grounding for an LLM. You curate what's indexed (no automatic crawling), `cairn add` brings it in, and either you or a model running over MCP can query the result. Five query surfaces:

- **Hybrid chunk search** (`search`) — FTS5 + vector embeddings fused via reciprocal rank fusion. Returns ranked text chunks.
- **Knowledge graph** (`graph`) — entities (functions, structs, concepts) and edges (`calls`, `depends_on`, `mitigates`, `references`, `verifies`) extracted from code (tree-sitter, AST-based) and markdown (LLM, hash-gated, optional).
- **Composed retrieval** (`ask`) — hybrid search + per-hit entity context in one call. Replaces a search-then-graph round trip.
- **Shortest path** (`path`) — BFS between two entities through the edge graph. Batched layer fetch — one SQL per BFS layer, not per node.
- **Tag-filtered retrieval** (`tags`, `--tag`) — concept entities carry free-form LLM-emitted tags (`attack`, `invariant`, `mev`, etc). Filter `search` / `ask` / `graph` by tag; discover the in-use tag vocabulary via `tags`.

Cross-source linking (`cairn link sdk program`) resolves names across two related sources — an SDK calling its on-chain program is the canonical case. Soft-delete + FK cascades keep the graph clean across refreshes and removals.

## Quick start

Library:

```ts
import { Cairn } from 'cairn-index'

const cairn = new Cairn() // defaults to ~/.cairn, ollama @ 127.0.0.1:11434
await cairn.ingest.add({ kind: 'code', path: './src', label: 'my-project' })
const hits = await cairn.retrieve.search('how does the chunker handle overlap', { k: 5 })
cairn.close()
```

CLI:

```bash
cairn add ./src --label my-project
cairn search "how does the chunker handle overlap" -k 5
cairn graph "fee invariant" --tag invariant
cairn ask "what mitigates pool squatting" --tag attack
cairn path 1:engine.rs:swap 1:math.rs:calc_swap_fee
cairn tags
```

MCP (stdio):

```bash
cairn-mcp   # exposes search / list / add / graph / ask / path / tags / refresh
```

## Configuration & safety (v1.2+)

Cairn is a curated index — you trust what you put in, and you control the surface around ingestion via env vars. None are required (defaults are sensible for a single-user developer setup), but every one is meaningful in shared, agent-driven, or compliance-sensitive deployments.

### Trust model — read this first

- **Autonomous model invocation is disabled** (`disable-model-invocation: true`). Tool calls require explicit user invocation through the host — the model can't decide on its own to call `CAIRN_ADD` or `CAIRN_SEARCH` without being asked. Matches the conservative default used by other side-effect-bearing skills. User-initiated flows ("index this repo for me", "find related online files") still work because the user's request to the agent IS the explicit invocation context; what's blocked is silent grounding (model autonomously calling cairn before answering, without being asked to).
- **You trust what you index.** Cairn doesn't auto-crawl. Every source enters via an explicit `cairn add` (CLI, library, or MCP) by you or by an agent you've authorized for that call. Indexed content is queryable later, including by future MCP-connected agents — that is the point. Ingesting untrusted web pages or sensitive code into a long-lived shared index is your call to make, and you can isolate sensitive content by running cairn against a different `dbPath`.
- **MCP gives connected agents full read + ingest access when invoked.** That's what MCP *is*. The host (Claude Desktop, OpenCode, etc.) controls which agents connect AND now (with `disable-model-invocation: true`) gates each call behind explicit user approval. Mutating ops `remove` / `link` / `unlink` / `reindex` are CLI-only — destructive or topology-changing actions require a human at the terminal.
- **Network egress is bounded.** See the network-egress note in the frontmatter. Localhost ollama is not blocked under `CAIRN_OFFLINE`; only outbound (web fetch, Hugging Face GGUF download) is.

### Defense-in-depth env vars

| Env var | Default | Purpose |
|---|---|---|
| `CAIRN_OFFLINE` | unset | When `1` or `true`, blocks `fetchWeb` (no `cairn add <url>`) and blocks non-local model resolution (no Hugging Face GGUF auto-download). Pre-cache models and pass `modelPath` for embedded runtime. Localhost ollama still allowed. |
| `CAIRN_ALLOWED_ROOTS` | unset (no restriction) | Comma-separated absolute paths. When set, `cairn add` rejects any local path (`code`, `file`, `pdf` kinds) outside these roots. Trailing slashes normalized. Defense-in-depth for MCP-connected agents that might be prompt-influenced into indexing the wrong place. Real protection is host-side per-call approval — this is the belt. |
| `CAIRN_MAX_INGEST_FILES` | `10000` | Pre-check on `addCode` directory walks. Aborts before any chunking/embedding work if the file count exceeds the limit. Bypassable via CLI `--force` flag (MCP intentionally does not expose `force`). |
| `CAIRN_MAX_INGEST_BYTES` | `524288000` (500 MB) | Pre-check on `addCode` directory walks. Aborts if total bytes exceed the limit. Same bypass model as the file cap. |
| `CAIRN_RUNTIME` | `ollama` | Switch between `ollama` and `embedded`. Embedded runs in-process via node-llama-cpp; first use auto-downloads GGUFs unless `CAIRN_OFFLINE` is set. |
| `CAIRN_CPU_ONLY` | unset | Force CPU-only inference on the embedded runtime. |
| `CAIRN_CHAT_MODEL` | Qwen3-0.6B Q8 | Override the doc-extraction chat model. |
| `CAIRN_DEBUG_DOC` | unset | Log per-doc extraction counts during ingest. |

### Air-gapped / offline-only deployment

```bash
# Pre-cache the embed and chat GGUFs once on a connected machine,
# verify the SHA256s match the published values (docs/setup.md
# "Verifying pre-cached models"), copy ~/.cairn/models/* to the
# air-gapped host, then:
export CAIRN_RUNTIME=embedded
export CAIRN_OFFLINE=1
export CAIRN_ALLOWED_ROOTS=/var/cairn/sources
cairn-mcp
```

Under this configuration, cairn makes zero network calls. Web ingestion is blocked outright; model resolution refuses anything that isn't an absolute path. Published SHA256s for the two cacheable GGUFs are in `docs/setup.md` so you can verify the bytes you ship to the air-gapped host match the bytes cairn was developed against.

### Startup warning

`cairn-mcp` logs a single warning line on boot when `CAIRN_ALLOWED_ROOTS` is unset, surfacing the path-allowlist call to operators who didn't read the docs. Set the env var to silence it (and confine ingestion); leave unset for a single-user developer setup where any-path ingestion is the intended behavior.

### MCP-connected-agent deployment

```bash
# Confine ingestion to a curated tree; everything else rejected at the gate.
export CAIRN_ALLOWED_ROOTS=/var/cairn/repos,/var/cairn/docs
# Lower the size cap if your sources are typically small
export CAIRN_MAX_INGEST_FILES=2000
cairn-mcp
```

The MCP host should still gate `add` / `refresh` calls per-invocation if the connected agent is partially-trusted. The env-var caps are belt-and-suspenders for the case where host gating is misconfigured or bypassed.

## Runtimes

Two interchangeable backends behind one `Cairn` class:

| Runtime | Daemon? | Embeds | Chat | First-run cost |
|---|---|---|---|---|
| `ollama` (default) | yes (localhost) | ollama `nomic-embed-text` | ollama Qwen3-0.6B Q8 (optional) | `ollama pull` once |
| `embedded` (set `CAIRN_RUNTIME=embedded`) | no | in-process via node-llama-cpp | in-process Qwen3-0.6B Q8 (optional) | ~785 MB GGUF download to `~/.cairn/models` (blocked if `CAIRN_OFFLINE=1`; pre-cache and use `modelPath`) |

Switching runtimes is one line — they implement the same `EmbedRuntime` / `ChatRuntime` contracts behind `EmbedProvider` / `ChatProvider`.

## Schema

Single baseline (`SCHEMA_VERSION = 2`, additive in v1.1). Tables: `sources`, `files`, `chunks` (+ `chunks_fts`, `chunks_vec`), `entities` (+ `entities_vec`), `edges`, `entity_tags`, `source_links`, `meta`. FK cascades from `sources` through entities into edges/tags; triggers keep `chunks_vec` and `entities_vec` in sync. v1 to v1.1 upgrade is automatic via `CREATE TABLE IF NOT EXISTS` — no migration runtime. v1.2 added no schema changes (safety gates only).

## MCP tools

Exposed by `cairn-mcp` over stdio. Read + ingest. Mutating ops `remove` / `link` / `unlink` / `reindex` are CLI-only — destructive actions require explicit user intent.

| Tool | Purpose |
|------|---------|
| `search` | Hybrid chunk search. Params: `query`, `k?`, `kind?`, `source?`, `tag?`. |
| `list` | List indexed sources. Params: `kind?`. |
| `graph` | Entity-level retrieval. Params: `query?` xor `entity_id?`, `k?`, `tag?`. |
| `ask` | Search + per-hit entity + 1-hop edges. Params: `query`, `k?`, `kind?`, `source?`, `tag?`, `maxEntitiesPerHit?`, `maxEdgesPerEntity?`. |
| `path` | Shortest path between two entities. Params: `from`, `to`, `maxDepth?`, `directed?`. |
| `tags` | List every tag in use across active entities + count. Discovery surface for the `--tag` filter. |
| `add` | Ingest a new source. Params: `kind?` (auto-detects), `target`, `label?`, `include?`, `exclude?`. Subject to `CAIRN_ALLOWED_ROOTS` and the size caps; `--force` is CLI-only. |
| `refresh` | Re-index existing source. Params: `ref` (id, uri, or `'all'`). |

## Verification

- 17 tests passing locally on the v1.2 baseline (7 pure, 10 live including LLM doc-extraction and embedded-runtime end-to-end). Live tests cover the actual ollama and node-llama-cpp paths, not mocks. New `tests/safety.ts` covers all three v1.2 gates (CAIRN_OFFLINE blocks/allows the right things; ALLOWED_ROOTS multi-root + trailing-slash + per-kind enforcement; size caps fire and force=true bypasses).
- The doc-extraction LLM pass uses ollama's `format` (or llama.cpp's grammar) for JSON-Schema-enforced output — even the sub-1B default chat model emits shape-valid concepts/edges/tags.
- Hash-gated re-extraction. Concepts re-emerge on refresh; doc-derived edges rebuild from scratch per doc; parse edges (AST) rebuild source-wide.

## Links

- [github.com/mrsirg97-rgb/cairn](https://github.com/mrsirg97-rgb/cairn)
- npm: [`cairn-index`](https://www.npmjs.com/package/cairn-index) (bins: `cairn`, `cairn-mcp`)
- SDK bundled in `lib/cairn/`
