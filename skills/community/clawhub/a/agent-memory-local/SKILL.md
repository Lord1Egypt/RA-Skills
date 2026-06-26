---
name: agent-memory-local
description: Local-first memory retrieval for Agent/OpenClaw workspaces. Use when the user asks about prior work, decisions, dates, preferences, root causes, todo history, or "what changed" questions and you want explainable retrieval from MEMORY.md + memory/*.md instead of a remote memory platform. Best for Markdown-based long-term memory, local audits, postmortems, and continuity across long-running assistant sessions.
---

# Agent Memory Local

## Overview

Search and explain facts from `MEMORY.md` and `memory/*.md` in a local workspace.
`agent-memory-local` gives an agent a transparent, local-first memory layer for questions like **“我们上次怎么定这个规则的？”** or **“昨天为什么飞书断联？”** without depending on a hosted memory service.

Production note: this retrieval style has already been used in real OpenClaw operating workflows behind **jisuapi.com** and **jisuepc.com**. That is a proof point, not a dependency.

## Why install this

Use this skill when you want to:
- find prior decisions, root causes, and preference history from Markdown memory files
- explain why a result matched instead of trusting a black-box memory API
- keep retrieval local and rebuild the index inside the workspace

Best fit:
- local or self-hosted agent setups
- teams that store durable memory in Markdown
- users who want transparent, inspectable memory retrieval instead of a black-box cloud memory service

## Common Use Cases

- **Decision recall** — “我们之前怎么定这个规则的？”
- **Incident review** — “飞书昨天为什么断联了？”
- **Change tracking** — “更新后为什么记忆搜索变了？”
- **Preference recall** — “小红书配图策略现在怎么要求？”
- **Policy / guardrail checks** — “敏感信息能不能写进日志？”

## Quick Start

### 30-second first run
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py build-index
python custom-skills/agent-memory-local/scripts/agent_memory_local.py smart-query "飞书昨天为什么断联了" -k 3
```

### Build the local index
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py build-index
```

### Direct retrieval
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py query "昨天更新后为什么记忆搜索变了" -k 6
```

### Smart natural-language retrieval
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py smart-query "飞书昨天为什么断联了" -k 6
python custom-skills/agent-memory-local/scripts/agent_memory_local.py smart-query "What changed in our memory retrieval route after yesterday's update?" -k 6
```

### Health check / doctor
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py doctor
```

### Explain why a result matched
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py explain "飞书昨天为什么断联了" --smart -k 3
python custom-skills/agent-memory-local/scripts/agent_memory_local.py explain "Why did Feishu disconnect yesterday?" --smart -k 3
```

## Not the best fit

Use a different memory system if you need:
- graph/relationship-heavy enterprise memory
- multi-user hosted memory APIs
- fully managed temporal knowledge graph systems

## Core Capabilities

### 1. Local index build
- Reads from:
  - `MEMORY.md`
  - `memory/learnings.md` (if present)
  - `memory/YYYY-MM-DD.md`
- Splits Markdown into retrieval chunks
- Builds a lightweight hashed vector index into `.memory-index/` under the workspace root
- Stores freshness metadata for auto-rebuild checks

### 2. Explainable retrieval
Returns:
- top matched file + title + snippet
- overlap count
- semantic score
- explain block with overlap terms / anchor hits / recency bonus
- index freshness status
- optional `explain` view for cleaner public-facing reasoning output

This makes it useful when the user asks:
- “我们上次怎么定这个规则的？”
- “昨天为什么飞书断联？”
- “记忆检索主路由是什么时候改的？”
- “关于这个需求之前有没有决定？”

### 3. Chinese-friendly anchors
The retriever is tuned for queries like:
- `飞书 掉线`
- `记忆搜索 变了`
- `主路由 默认入口`
- `截图 宿主`
- `duplicate plugin id`
- `gateway timeout`

It boosts domain phrases, recency, and strong anchors instead of relying only on generic vector similarity.

### 4. Smart query rewriting
`smart-query` rewrites and scores multiple candidate queries automatically.
This helps with fuzzy questions like:
- “昨天更新后为什么记忆搜索变了？”
- “飞书昨天为什么断联？”
- “主路由后来是不是改过？”

### 5. Optional rerank enhancement
If `SILICONFLOW_API_KEY` is available, retrieval can optionally rerank the best candidates via SiliconFlow rerank.
If the key is missing, the skill still works locally.

## Example Output

Example command:
```bash
python custom-skills/agent-memory-local/scripts/agent_memory_local.py explain "飞书昨天为什么断联了" --smart -k 2
```

Example result shape:
```json
{
  "query": "飞书昨天为什么断联了",
  "used_query": "飞书 断联 duplicate plugin id gateway timeout",
  "results": [
    {
      "rank": 1,
      "file": "memory/2026-03-10-request-timed-out-before-a-res.md",
      "score": 0.5084,
      "why_matched": {
        "anchor_hits": ["duplicate plugin id", "gateway timeout", "断联", "飞书"],
        "overlap_terms": ["duplicate", "duplicate plugin id", "gateway", "gateway timeout"]
      }
    }
  ]
}
```

This is the point of the skill: not just “some memory results”, but a query rewrite + top hits + an explanation of why they matched.

## Workflow

### Workflow A — answer a memory question
1. Run `smart-query`
2. Inspect top 3-5 results and explain fields
3. Open the source Markdown file if you need exact wording
4. Answer with the retrieved fact, not with guesswork

### Workflow B — prepare for long-running assistant memory
1. Keep durable facts in `MEMORY.md` / `memory/*.md`
2. Run `build-index`
3. Use `doctor` to confirm index freshness
4. Use `query` / `smart-query` as the workspace memory route

### Workflow C — debug retrieval quality
1. Run `doctor`
2. Confirm workspace detection and index freshness
3. Rebuild with `build-index`
4. Retry with `query`
5. If results are fuzzy, try `smart-query`

## Configuration

### Workspace resolution
The scripts resolve the workspace in this order:
1. `--workspace /path/to/workspace` CLI arg
2. `AGENT_MEMORY_WORKSPACE` env var
3. current working directory or its parents
4. the skill location's parent chain

### Optional env vars
- `AGENT_MEMORY_WORKSPACE` — force the workspace root
- `MEMORY_AUTO_REBUILD=0|1` — disable/enable auto rebuild when stale
- `MEMORY_RERANK=0|1` — disable/enable rerank
- `SILICONFLOW_API_KEY` — enable rerank enhancement

Use `--workspace` when running outside the target repo and you want deterministic workspace selection.

### Index location
The index is stored in `.memory-index/` at the resolved workspace root, not inside the skill folder.
Examples:
- workspace `/repo/project` → index at `/repo/project/.memory-index/`
- workspace `E:/openclaw/.openclaw/workspace` → index at `E:/openclaw/.openclaw/workspace/.memory-index/`

### When to rebuild the index
Rebuild manually when:
1. first run in a new workspace
2. `MEMORY.md` or `memory/*.md` changed and you want immediate freshness
3. `doctor` reports a stale index
4. retrieval results look outdated or obviously off-topic
5. you switched workspaces or restored memory files from backup

If `MEMORY_AUTO_REBUILD=1`, query flows may rebuild automatically when the index is stale.

## Files in this skill

### scripts/
- `agent_memory_local.py` — top-level CLI entrypoint
- `build_index.py` — builds `.memory-index/`
- `retrieve.py` — direct retrieval engine
- `memory_query.py` — smart rewrite + best-query selector
- `doctor.py` — health / freshness checker
- `explain.py` — cleaner explanation view for why results matched
- `benchmark.py` — regression benchmark runner against representative memory queries
- `common.py` — workspace and path resolution helpers

### references/
- `architecture.md` — design notes and tradeoffs
- `publish-plan.md` — packaging / release checklist for ClawHub

## When to prefer this skill over heavier memory platforms
Use `agent-memory-local` when you want:
- local-first memory
- human-readable Markdown memory source of truth
- explainable retrieval
- low dependencies
- easy audits and backups

Prefer heavier systems (Mem0 / Letta / Graphiti / Zep-style approaches) when you need:
- hosted memory APIs
- multi-user context services
- temporal knowledge graphs
- relationship-aware graph retrieval
- enterprise-scale memory orchestration
