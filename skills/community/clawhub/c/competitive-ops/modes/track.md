# Mode: track -- Competitor Tracker View

Display current status of all tracked competitors.

## Usage

```
/comp track
/comp track <company-name>
/comp track --tier 1
/comp track --archetype "Direct Competitor"
```

## Process

### 1. Load Data
- Read `data/competitors.md`
- Load profiles for each company
- Calculate summary statistics

### 2. Filter (if provided)
- By company name (partial match)
- By tier (1, 2, 3)
- By archetype
- By score range

### 3. Format Output

#### Dashboard View

```
┌─────────────────────────────────────────────────────────────┐
│  COMPETITOR TRACKER                              [Date]   │
├─────────────────────────────────────────────────────────────┤
│  Total: N    Tier 1: X    Tier 2: Y    Tier 3: Z           │
│  Avg Score: X.X    High: X.X    Low: X.X                  │
├─────────────────────────────────────────────────────────────┤
│  TIER 1 - HIGH THREAT                                       │
├─────────────────────────────────────────────────────────────┤
│  ⬤ [Company 1]         Score: X.X    Archetype: Direct     │
│    Last analyzed: X days ago    Trend: ↑ +0.X              │
│    Key: [differentiator 1], [differentiator 2]            │
├─────────────────────────────────────────────────────────────┤
│  ⬤ [Company 2]         Score: X.X    Archetype: Direct     │
│    Last analyzed: X days ago    Trend: ↓ -0.X              │
│    Key: [differentiator 1], [differentiator 2]             │
├─────────────────────────────────────────────────────────────┤
│  TIER 2 - MODERATE THREAT                                  │
├─────────────────────────────────────────────────────────────┤
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

#### Markdown Table View

```markdown
# Competitor Tracker

**Last Updated:** YYYY-MM-DD
**Total Competitors:** N

## Summary

| Tier | Count | Avg Score |
|------|-------|-----------|
| 1 (High) | X | X.X |
| 2 (Medium) | X | X.X |
| 3 (Low) | X | X.X |

## All Competitors

| # | Company | Tier | Score | Archetype | Last Updated |
|---|---------|------|-------|-----------|--------------|
| 1 | [Company] | 1 | X.X | Direct | YYYY-MM-DD |
| 2 | [Company] | 2 | X.X | Indirect | YYYY-MM-DD |
| ... | ... | ... | ... | ... | ... |

## Recent Changes

### Score Changes
- **[Company]:** X.X → Y.Y (±Z)

### New Entries
- **[Company]:** Added [date]

### Stale Data (>30 days)
- **[Company]:** Last updated [date] ⚠️
```

### 4. Alert Flags

Display warnings:
- ⚠️ **Stale data:** Not updated in >30 days
- 🔴 **Score change:** Significant shift detected
- 📈 **Rising threat:** Score increased >0.3
- 💰 **Pricing change:** Recent pricing update
- 📰 **New news:** Major announcement detected

## Options

| Option | Description |
|--------|-------------|
| `--tier N` | Filter by tier (1, 2, or 3) |
| `--archetype` | Filter by archetype |
| `--score` | Filter by score range |
| `--format` | Output format: dashboard, table, markdown |
| `--alerts` | Show only companies with alerts |

## Example

```
/comp track
/comp track Anthropic
/comp track --tier 1
/comp track --archetype "Direct Competitor" --alerts
```

## Data Source

Reads from:
- `data/competitors.md` - Master list
- `data/profiles/*/profile.md` - Detailed profiles
- `data/pricing-snapshots/*.md` - Pricing data

## Stale Data Detection

Flag companies where:
- `last_analyzed` > 30 days ago
- `last_pricing_update` > 60 days ago

## Quick Actions

Display suggested next actions:
- `/comp analyze [Company]` - Full analysis
- `/comp update [Company]` - Check for changes
- `/comp pricing [Company]` - Update pricing
- `/comp compare [A] vs [B]` - Compare two
