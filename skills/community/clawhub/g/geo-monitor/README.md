# geo-monitor

Re-audit a website and track GEO score changes over time against a previous baseline.

## What it does

1. **Re-audits** the site using the same geo-audit scoring methodology
2. **Compares** every dimension and sub-dimension against the baseline
3. **Tracks** which issues were resolved, which are new, and which remain
4. **Calculates** improvement velocity (points per day)
5. **Projects** future score if remaining issues are fixed

## Usage

```bash
# Compare against a previous report
"Re-audit https://mysite.com against GEO-AUDIT-mysite-2026-03-01.md"

# Auto-detect baseline (finds most recent report in current directory)
"Monitor progress for https://mysite.com"

# Claude Code slash command
/geo-monitor https://mysite.com --baseline GEO-AUDIT-mysite-2026-03-01.md
```

## Output

| File | Purpose |
|------|---------|
| `GEO-MONITOR-{domain}-{date}.md` | Before/after comparison with issue tracking and projections |

## Installation

```bash
npx skills add Cognitic-Labs/geoskills --skill geo-monitor
```
