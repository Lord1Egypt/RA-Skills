# 🌙 dreaming-optimizer

> **Version:** 1.0.0  
> **Skill ID:** `dreaming-optimizer`  
> **Status:** Ready for Development

## Quick Reference

| 项目 | 内容 |
| ---- | ---- |
| 核心原理 | OpenClaw Dreaming REM六步记忆整合（整理→评分→去重→打标→提交→摘要） |
| 主入口 | `bin/optimize.sh` |
| 依赖 | OpenClaw v2026.4.9+, tiktoken, sqlite3 |

## Features (MVP)

1. **Entry scorer** — LLM-based priority scoring (0–100)
2. **Deduplication** — Semantic similarity merge against existing memories
3. **Fact tagger** — Label as fact/opinion/preference/context
4. **Commit writer** — Write optimized entries to persistent memory
5. **Dreaming summary** — Traceable REM consolidation report
6. **Configurable threshold** — Min score threshold (default: 70)

## File Structure

```
dreaming-optimizer/
├── SKILL.md              # This file
├── bin/
│   ├── optimize.sh       # Main entry point
│   ├── score_entries.py  # LLM-based priority scoring
│   ├── deduplicate.py    # Semantic deduplication
│   └── commit.py         # Write to B-layer
├── scripts/
│   └── dreaming_summary.py
├── config/
│   └── default_threshold.yaml
└── README.md
```

## Usage

```bash
# Manual invoke
dreaming-optimizer/bin/optimize.sh

# With custom threshold
dreaming-optimizer/bin/optimize.sh --threshold 80
```

## Integration

- Reads from: `~/.openclaw/workspace/memory/YYYY-MM-DD.md`
- Writes to: `~/.openclaw/memory/<agent>.sqlite` (B-layer)
- Summary output: `~/.openclaw/workspace/memory/dreaming-summaries/`

## Pricing

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 10 cycles/mo, 100 entries/cycle |
| **Pro** | **$9.90/mo** | Unlimited, dedup, backfill queue, Obsidian export |

## Development

See: ``
