---
name: context-viz
description: Visualize the current context window usage — token estimates per component (system prompt, tools, workspace files, messages, free space). Use when the user asks about context size, token usage, context breakdown, "how full is the context", or wants to see what's consuming their context window.
---

# Context Visualization

Estimate and display a breakdown of the current context window usage.

## How It Works

Run the bundled script to estimate token counts for workspace files:

```bash
python3 scripts/estimate_tokens.py /path/to/workspace
```

The script counts characters in known workspace files and estimates tokens (~4 chars/token).

Then call `session_status` to get the actual context usage from OpenClaw.

## Generating the Visualization

1. Run `session_status` to get: model, context used/total, compactions
2. Run `scripts/estimate_tokens.py <workspace_path>` to estimate file token sizes
3. Estimate message tokens: `context_used - system_overhead - file_tokens`
4. Present the breakdown using the format below

## Output Format

Use a monospace block with bar chart. Adapt the bar lengths proportionally.

```
📊 Context Usage
<model> • <used>k/<total>k tokens (<pct>%)

Component                    Tokens    %     
─────────────────────────────────────────────
⚙️  System prompt + tools    ~Xk      X%    ░░
📋  AGENTS.md                ~Xk      X%    ░
👻  SOUL.md                  ~Xk      X%    
👤  USER.md                  ~Xk      X%    
🔧  TOOLS.md                 ~Xk      X%    ░
💓  HEARTBEAT.md             ~Xk      X%    
🧠  MEMORY.md                ~Xk      X%    ░
🪪  IDENTITY.md              ~Xk      X%    
💬  Messages                 ~Xk      X%    ░░░░░░░░░░░░
📭  Free space               ~Xk      X%    ░░░░░
─────────────────────────────────────────────
```

Use ░ blocks: 1 block per ~2% of total context. Round to nearest block.

## Memory Inventory (not in context)

Below the context chart, add a **Memory on Disk** section showing what's stored in `memory/` — grouped by category. These files are NOT loaded into context but represent the agent's total knowledge base.

```
💾 Memory on Disk (not in context)
Category                     Files  Tokens   Size
──────────────────────────────────────────────────
📰  chinese-ai-digests        12    ~23k     92KB
📁  other                     11    ~12k     46KB
📅  daily-notes                9    ~5k      17KB
🗃️  zettelkasten               8    ~4k      15KB
💼  linkedin                   2    ~1k       5KB
──────────────────────────────────────────────────
     Total:                   42    ~44k    177KB
```

The script auto-categorizes files by directory or filename pattern.

## Notes

- Token estimates use ~4 chars/token (rough average for English/mixed content)
- System prompt + tools overhead is estimated at ~8-10k tokens for a typical OpenClaw setup
- Message tokens are the remainder after subtracting files + system overhead
- Memory files are informational only — they show what the agent has accumulated
- For Discord/WhatsApp: skip markdown tables, use the block format above
