# Token Math Reference

## Why Sessions Bloat

Every message in a session accumulates in the context window. OpenClaw loads:
- System prompt + workspace files (~18K tokens baseline for a typical setup)
- All prior assistant turns
- All prior user turns
- Tool call inputs and outputs

Each query adds ~1K–5K tokens depending on message length and tool use. After 10 queries, a lean session (~18K baseline) can reach 50K–80K tokens. After 20+, it can exceed 400K.

## Cost Impact (Claude Sonnet 4.x pricing reference)

| Tokens | Est. cost per query | Notes |
|---|---|---|
| 18K (new session) | ~$0.054 | Baseline — fresh /new |
| 50K (10 queries) | ~$0.150 | 2.8x baseline |
| 100K (20+ queries) | ~$0.300 | 5.5x baseline |
| 400K (bloated) | ~$1.200 | 22x baseline |

*Costs are estimates. Cached tokens billed at lower rates where applicable.*

## The Compounding Problem

Each new message pays for ALL prior context — every assistant turn, every tool call.
Session cost is O(n²) in message count without resets.

## Reset Saves

Resetting at 10 queries vs. continuing to 20 saves approximately:
- 50% of input tokens for the second 10 queries
- Compounds across the full day if multiple sessions run

## Session Baseline by Setup Size

| Workspace size | Typical baseline |
|---|---|
| Minimal (no project files) | ~5K–8K |
| Standard (SOUL + USER + MEMORY) | ~12K–20K |
| Heavy (large MEMORY + daily logs) | ~25K–40K |

## Signals That a Session Is Bloated

- Responses feel slower than usual
- The agent references stale context from early in the session
- Cost per query visibly increasing
- Tool call outputs are large and repeated (e.g., file reads cached in context)
