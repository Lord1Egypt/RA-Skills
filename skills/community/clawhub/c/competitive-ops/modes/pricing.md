# Mode: pricing -- Pricing Research

Research and track competitor pricing.

## Usage

```
/comp pricing <company-name>
```

## Pricing Deep Dive

For comprehensive pricing analysis with value scoring, use:

```
/comp pricing-deep-dive <company-name>
```

This generates a detailed report including:
- Value score computation (Feature Count / Price * Market Normalization)
- Plan-by-plan breakdown with all attributes
- Pricing history and change detection
- Alert log for any detected changes

### Storage Format

Pricing snapshots are stored as JSON in `data/pricing-snapshots/{company}.json`:

```json
{
  "company": "CompanyName",
  "last_updated": "2026-04-07",
  "plans": [
    {
      "name": "Plan Name",
      "type": "subscription",
      "price": 20.0,
      "period": "monthly",
      "users": 10,
      "api_access": true,
      "price_per_1m_input": 1.0,
      "price_per_1m_output": 3.0,
      "features": ["Feature 1", "Feature 2"]
    }
  ],
  "enterprise": true,
  "free_tier": true,
  "sources": ["https://example.com/pricing"]
}
```

### Alert Logic

**ANY pricing change triggers an alert** -- no threshold-based filtering:
- Price changes (any +/-)
- New plan added
- Plan removed
- Feature changes
- Free tier status change
- Enterprise option change

## Process

### 1. Input
- Company name (normalized)

### 2. Collect Pricing Data

#### Sources
- [ ] **TODO: Playwright Integration**
  ```javascript
  await Playwright.browser_navigate(pricingPage)
  await Playwright.browser_snapshot()
  ```
- WebSearch for:
  - Official pricing pages
  - Third-party reviews mentioning pricing
  - Comparison sites
  - Reddit/forum mentions

#### Pricing Elements to Capture
- **Plans:** Names, tiers, limits
- **Per-user pricing:** Monthly/annual
- **Enterprise pricing:** Custom/contact sales
- **Free tier:** Available/limits
- **Trial:** Duration, limitations
- **Add-ons:** Prices, bundles
- **Contract terms:** Annual, monthly, usage-based

### 3. Pricing Detection

#### Change Detection
Compare against `data/pricing-snapshots/{company}.json` using `scripts/pricing_analyzer.py`:

```python
from pricing_analyzer import PricingChangeDetector, load_snapshot

detector = PricingChangeDetector(any_change=True)  # Alert on ANY change
old = load_snapshot(f"data/pricing-snapshots/{company}.json")
new = load_snapshot("new_snapshot.json")

changes = detector.detect_change(old, new)
for change in changes:
    print(f"ALERT: {change.description}")
```

#### Alert Logic
- **Any pricing change:** Always alert (no threshold)
- **New tier added:** Always alert
- **Plan removed:** Always alert
- **Free tier change:** Always alert
- **Enterprise option change:** Always alert

### 4. Output

#### Pricing Table

```markdown
# Pricing: [Company]

**Researched:** YYYY-MM-DD
**Source:** [URL]

## Current Pricing

| Plan | Price | Users | Key Features |
|------|-------|-------|--------------|
| Free | $0 | 1 | [Features] |
| Basic | $X/mo | up to Y | [Features] |
| Pro | $X/mo | up to Y | [Features] |
| Enterprise | Custom | Unlimited | [Features] |

## Pricing Comparison (vs Market)

| Metric | [Company] | Market Avg |
|--------|-----------|------------|
| Entry price | $X | $X |
| Pro price | $X | $X |
| Value score | X/5 | X/5 |

## Changes Since Last Snapshot

### [Date]
- [Change 1]
- [Change 2]

## Confidence

- **Data freshness:** [date]
- **Source reliability:** [High/Medium/Low]
- **Coverage:** [Complete/Partial/Estimate]
```

### 5. Save Results
- Save snapshot to `data/pricing-snapshots/{company}.json` (JSON format)
- Update `data/profiles/{company}/profile.md` with latest pricing
- Add changelog entry if changed

**JSON Storage** (required for pricing_analyzer.py compatibility):
```python
from pricing_analyzer import save_snapshot, PricingSnapshot

snapshot = PricingSnapshot(
    company="CompanyName",
    last_updated="2026-04-07",
    plans=[...],
    enterprise=True,
    free_tier=True,
    sources=["https://example.com/pricing"]
)
save_snapshot(snapshot, f"data/pricing-snapshots/{company}.json")
```

## Example

```
/comp pricing Anthropic
/comp pricing "OpenAI"
/comp pricing-deep-dive Anthropic
/comp pricing-deep-dive "OpenAI"
```

## TODO Checklist

- [ ] Implement Playwright for dynamic pricing page scraping
- [ ] Add pricing extraction from pricing pages
- [x] Track pricing history over time (JSON snapshots in `data/pricing-snapshots/`)
- [x] Generate pricing alerts (any-change detection via pricing_analyzer.py)
- [x] Add value scoring algorithm (PricingAnalyzer.compute_value_score)

## Common Pricing Patterns

| Pattern | Detection | Action |
|---------|-----------|--------|
| Freemium | Free tier exists | Flag as competitive |
| Per-seat | Per-user pricing | Calculate market rate |
| Usage-based | Meters, tokens | Note as emerging |
| Enterprise | Contact sales | Flag for discovery |
| Bundle | Multiple products | Note cross-sell |
