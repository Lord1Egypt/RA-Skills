# geo-compare

Compare GEO scores across 2-3 competing websites side by side.

## What it does

1. **Audits** 2-3 sites in parallel using the geo-audit scoring methodology
2. **Compares** scores across all 4 dimensions and sub-dimensions
3. **Identifies** where you trail competitors and by how much
4. **Recommends** priority fixes ranked by competitive impact
5. **Highlights** quick wins to overtake specific competitors

## Usage

```bash
# Compare your site against competitors
"Compare https://mysite.com with https://competitor-a.com and https://competitor-b.com"

# Claude Code slash command
/geo-compare https://mysite.com https://competitor-a.com https://competitor-b.com
```

## Output

| File | Purpose |
|------|---------|
| `GEO-COMPARE-{domain}-{date}.md` | Full comparison matrix with gap analysis and recommendations |

## Installation

```bash
npx skills add Cognitic-Labs/geoskills --skill geo-compare
```
