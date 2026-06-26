---
name: context-window-tracker
description: >
  Track and report OpenClaw context window usage with a detailed breakdown of what's
  consuming tokens. Use when: user asks about context usage, token usage,
  "how much context am I using", "how full is my context window", "tokens remaining",
  "am I close to the limit", thinking/reasoning token costs, what's eating context
  (session setup vs conversation vs overhead), or how many turns are left.
  NOT for: estimating tokens for arbitrary text, managing context (compact/prune),
  or cross-session cost aggregation.
homepage: https://github.com/99rebels/context-window-tracker
---

# Context Window Tracker

Shows how much context window is left — without opening the terminal.

## When to Use

- "Check my context"
- "How much context am I using?"
- "How full is my context window?"
- "Tokens remaining"
- "Am I close to the limit?"
- Any question about context usage

## Two Modes

### Compact (default)
One line. Glanceable. Use for quick checks.

```bash
python3 scripts/context_report.py
```

### Detailed
Full breakdown with per-file system prompt, conversation split, trends, and thinking status. Use when the user asks for specifics.

```bash
python3 scripts/context_report.py --detailed
```

Both modes auto-detect the most recently updated session. Options:

```
--session <key>    Target a specific session
--agent <name>     Target a specific agent (default: main)
--detailed         Full breakdown instead of compact one-liner
```

## Output Format

### Default (quick check)
When the user asks "check context", "how much context", "context window", or similar casual phrases.

Show the unicode bar, percentage, estimated turns remaining, and average tokens per turn:

```
🟢 [███░░░░░░░░░░░░░░░░░] 15% | ~736 turns left | 427 tokens/turn
```

Run the compact script (`python3 scripts/context_report.py`) and extract the bar/percentage. Get avg tokens/turn and turns remaining from the detailed script or session_status. Strip all `*` characters before sending to Slack (see Slack rendering fix below).

Add a contextual one-liner when context is 75%+ used (see Guidance section). Otherwise, just show the line.

### Detailed
When the user explicitly asks "detailed context", "full context check", "context breakdown", or "show me everything":

```
🟢 [███████████░░░░░░░░░] Context Usage: 113.7K / 202.8K (56%)
────────────────────
Token Breakdown
System Prompt: ~10.2K tokens (5%)
AGENTS.md: ~2.0K tokens
SOUL.md: ~416 tokens
TOOLS.md: ~717 tokens
IDENTITY.md: ~65 tokens
USER.md: ~83 tokens
HEARTBEAT.md: ~48 tokens
BOOTSTRAP.md: ~18 tokens
MEMORY.md: ~2.3K tokens
📦 Framework overhead: ~5.3K (tool schemas, skill list, runtime)
• Conversation: ~103.5K tokens (51%)
• 📊 Total Used: 113.7K (56%)
• Remaining: 89.1K (44%)
────────────────────
Trends
• Avg tokens per turn: ~316 tokens
• ⏳ Estimated turns remaining: ~281
────────────────────
Session Stats
• 📥 Total input: 2.1K | 📤 Total output: 318 | Cache hit rate: 100%
• Thinking: active (35/200 responses)
```

Run the detailed script and strip all `*` characters for Slack compatibility.

The bar uses `█` (filled) and `░` (empty) across 20 segments (each = 5%). The bar colour shifts: green under 60%, yellow 60-80%, red over 80%.

### Health Indicator

- 🟢 Under 60% used — plenty of room
- 🟡 60–80% used — getting tight
- 🔴 Over 80% used — consider wrapping up

## Auto-Check (Opt-In)

The compact report can run automatically every 10 messages. This is **disabled by default** — the user must explicitly enable it.

To enable, the user must say something like "auto-check my context" or "enable context auto-check". Once enabled:

1. Maintain a message counter in `.msg-counter.json` (same directory as SKILL.md)
2. On every user message, increment the counter
3. If the count is a multiple of 10, run the compact script and append the output to your reply
4. If not, reply normally

The counter survives compaction. If the file is missing, create it starting at 0:

```json
{"count": 0}
```

To disable, the user can say "disable context auto-check" — delete the counter file and stop checking.

**Important:** Never enable this automatically. Only enable when the user explicitly asks.

## Guidance

The script outputs raw data. The LLM adds a contextual one-liner based on the conversation.

**When to add guidance:**
- Only when context is **75%+ used**
- Skip for fresh sessions — no need for advice when there's plenty of room
- Skip if the user just asked for a raw number — give them the number
- Applies to **both** compact and detailed modes

**Slack rendering fix:**
The script uses `*text*` for emphasis, which Slack interprets as italics and can break rendering of the detailed output (long messages with many italics markers fail to display). When the channel is Slack:
- Strip all `*` characters from the script output before displaying
- Alternatively, use the compact mode (one-liner) which doesn't have this issue

**How to write it:**
One line, specific to the current task. For compact mode, append after the one-liner. For detailed mode, append after the final divider.

Examples:
- "Room to finish testing the skill and push to ClawHub, but not start a new one from scratch."
- "Tight — let's wrap up the config changes and commit. Anything else should go in /new."
- "Plenty of room. Keep going."
- Compact: append as `| Tight — wrap up and commit, start fresh for anything new.`

**Rules:**
- One line max. No paragraphs.
- Reference the actual task, not generic categories.
- Don't prescribe what the user should do — describe what fits.
- If you're not sure what the task is, fall back to a generic note or skip it.

## What's Exact vs Estimated

```
✅ Exact (from provider):
  • Total tokens used (from transcript)
  • Context window limit (from session store)
  • Cache hit rate

⚠ Estimated:
  • Per-file system prompt breakdown (chars ÷ 4)
  • Turns remaining (extrapolated from recent growth rate)
  • Thinking token count (bundled by provider, not separately reported)
```

## Notes

- Script reads the transcript (`.jsonl`) as source of truth — the session store can lag behind by thousands of tokens
- If the session store doesn't provide a context window limit (some thread sessions), it shows tokens used without a percentage
- See [references/data-sources.md](references/data-sources.md) for file paths
- See [references/thinking-tokens.md](references/thinking-tokens.md) for how reasoning tokens affect counts
