# Mode: update -- Update Competitor Tracking

Check for changes and update competitor data.

## Usage

```
/comp update <company-name>
/comp update all
```

## Process

### 1. Input
- Company name or "all"
- Normalize company name

### 2. Load Current State
- Read existing profile from `data/profiles/{company-slug}/profile.md`
- Read current scores from `data/competitors.md`
- Load previous analysis date

### 3. Check for Changes

#### Research Phase
- [ ] **TODO: TavilySearch Integration**
  ```javascript
  tavilyResults = await TavilySearch({
    query: `${company} news updates ${currentYear}`,
    maxResults: 5
  })
  ```
- WebSearch for:
  - Recent news
  - Product updates
  - Pricing changes
  - Funding announcements
  - Leadership changes

#### Change Detection
Compare against previous data:

| Category | Previous | Current | Change |
|----------|----------|---------|--------|
| Pricing | $X | $Y | ±Z% |
| Score | X.X | X.X | ±X.X |
| News | [count] | [count] | new |

### 4. Significant Changes

Alert if:
- **Score change > 0.3:** Significant competitive shift
- **Pricing change > 10%:** Market positioning change
- **New major feature:** Product capability gap
- **Funding > $10M:** Threat level increase
- **Leadership change:** Potential strategy shift

### 5. Update Files

#### Update Profile
- Update scores in `data/profiles/{company-slug}/profile.md`
- Add changelog entry
- Update timestamp

#### Update SWOT
- Revise SWOT in `data/swot-analysis/{company-slug}.md`
- Mark changes with `[CHANGED]`

#### Update Competitors.md
- Update scores
- Update last_analyzed date
- Add changelog summary

### 6. Output

```markdown
# Update: [Company]

**Checked:** YYYY-MM-DD
**Last Analysis:** YYYY-MM-DD

## Changes Detected

### Score Changes
| Dimension | Previous | Current | Change |
|-----------|----------|---------|--------|
| Product Maturity | X | X | ±0 |
| ... | ... | ... | ... |
| **Overall** | **X.X** | **X.X** | **±X.X** |

### Significant Events
- [ ] Pricing change detected: [details]
- [ ] New feature: [details]
- [ ] News: [headline]

## Alerts

⚠️ **[Alert message]**

## Next Steps

- [ ] Run full analysis: `/comp analyze [Company]`
- [ ] Update pricing: `/comp pricing [Company]`
```

## Batch Update (all)

```
/comp update all
```

Process:
1. Load all competitors from `data/competitors.md`
2. Check each for updates (parallel where possible)
3. Generate consolidated changelog
4. Alert on significant changes

## Example

```
/comp update Anthropic
/comp update all
```

## Output Files

- Changelog: `data/changelogs/{company-slug}-{date}.md`
- Updated: `data/profiles/{company-slug}/profile.md`
- Updated: `data/competitors.md`

## Alert Configuration

From `_profile.md`:
- Score threshold: >0.3 change
- Pricing threshold: >10% change
- News threshold: Any major announcement
