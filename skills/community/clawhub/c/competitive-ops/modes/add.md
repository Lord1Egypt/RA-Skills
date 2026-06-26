# Mode: add -- Add Competitor

Add a new competitor to the tracking system.

## Usage

```
/comp add <company-name-or-url>
```

## Process

### 1. Input Validation
- Parse company name or URL
- If URL: extract company name
- Normalize company name (lowercase, hyphenate)

### 2. Initialize Research
- Create company directory in `data/profiles/{company-slug}/`
- Initialize profile file
- Run initial WebSearch for basic info:
  - Company description
  - Product overview
  - Target market
  - Pricing (if available)

### 3. Create Entry
- Add entry to `data/competitors.md`
- Assign initial tier based on research:
  - **Tier 1:** Direct competitors, score 4.0+
  - **Tier 2:** Indirect competitors, score 3.0-3.9
  - **Tier 3:** Emerging/watchlist, score below 3.0

### 4. Output
```
✓ Added [Company] to competitors
  Tier: [X]
  Archetype: [Detected]
  Next: Run /comp analyze [Company] for full analysis
```

## Example

```
/comp add Anthropic
/comp add https://www.anthropic.com
```

## Files Created

- `data/profiles/{company-slug}/profile.md`
- `data/pricing-snapshots/{company-slug}.md`
- `data/swot-analysis/{company-slug}.md`

## Files Updated

- `data/competitors.md` (new entry added)

## TODO: Tavily Integration

- [ ] Use TavilySearch for comprehensive initial research
- [ ] Fallback to WebSearch if Tavily unavailable

## Error Handling

| Error | Response |
|-------|----------|
| Company already exists | Show existing entry, offer to update |
| Cannot find company | Ask for more specific name or URL |
| Network error | Retry with WebSearch fallback |
