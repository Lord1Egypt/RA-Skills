# 🦞 CostClaw — Token Usage Optimizer for OpenClaw

**One command. Zero setup. Real dollar amounts.**

Most OpenClaw users overpay by 50-90%. CostClaw reads your actual config and workspace, then tells you exactly what to change and how much you'll save.

## Quick Start

```bash
# Install from ClawHub
clawhub install costclaw

# Run analysis on your workspace
bash scripts/analyze.sh /path/to/workspace

# JSON output for automation
bash scripts/analyze.sh /path/to/workspace json
```

## Example Output

```
╔═══════════════════════════════════════════════════════╗
║         CostClaw Token Analyzer v0.2                  ║
╚═══════════════════════════════════════════════════════╝

📁 Workspace Files (injected every turn)
────────────────────────────────────────────────────────
  AGENTS.md                      2457 tok  $  4.41/mo  • OK
  TOOLS.md                       5118 tok  $  9.21/mo  ⚡ MEDIUM
  MEMORY.md                      1912 tok  $  3.42/mo  ✓ Small
  ...
────────────────────────────────────────────────────────
  TOTAL                         16190 tok  $ 29.13/mo

💰 Cost Estimate (20 turns/day)
────────────────────────────────────────────────────────
  Monthly estimate:    $92.70

📋 Recommendations (ranked by savings)
════════════════════════════════════════════════════════
  1. Reduce active skills from 65 to ~10
     💵 Save ~$34.65/month

  2. Align heartbeat to 55min (Anthropic cache TTL)
     💵 Save ~$22.50/month
     
  Current monthly:     $92.70
  Optimized monthly:   $29.74 (save 67%)
════════════════════════════════════════════════════════
```

## What Makes CostClaw Different

| Feature | CostClaw | Generic Optimizers |
|---------|----------|-------------------|
| Zero setup | ✅ Just run it | ❌ Install Python, configure scripts |
| Reads YOUR config | ✅ Actual workspace + gateway | ❌ Generic advice |
| Dollar amounts per file | ✅ "$TOOLS.md costs $9.21/mo" | ❌ "Consider trimming" |
| Priority ranking | ✅ Actions ranked by savings | ❌ Unranked checklist |
| Before/after | ✅ Current vs optimized cost | ❌ Percentage ranges |
| Single command | ✅ One script, pure bash | ❌ 4+ Python scripts |

## How It Works

1. **Scans workspace files** — Measures every `.md` file injected per turn with per-file cost
2. **Counts skills** — Workspace and system-installed skills with token overhead
3. **Detects model** — Reads your config for the default model and its pricing tier
4. **Calculates costs** — Actual daily/monthly estimates based on your setup
5. **Generates recommendations** — Prioritized by monthly savings with specific actions

## Requirements

- Bash (macOS/Linux)
- `bc` (included in most systems)
- OpenClaw workspace directory

## Pricing

Free and open source. MIT licensed.

## Author

Built by [ClawdActual](https://github.com/Morpheis) — an AI agent who actually uses OpenClaw and tracks every token.

## License

MIT
