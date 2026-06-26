# Keyword Research Methodology

## How App Store Keyword Indexing Works

**iOS (App Store)**
- Indexed fields: App Name (30 chars), Subtitle (30 chars), Keyword Field (100 chars), In-App Purchase names, Developer name
- NOT indexed: Description, reviews
- Keywords field: comma-separated, no spaces around commas, no repeated words already in title/subtitle
- Single-word keywords index better than phrases in the keyword field; phrases work better in title/subtitle

**Android (Google Play)**
- Indexed fields: Title (30 chars), Short Description (80 chars), Long Description (4000 chars), Developer name
- Description is fully indexed — keyword density matters (1-3% recommended)
- No separate keyword field; must weave keywords naturally into description copy

## Keyword Research Framework

### Phase 1: Seed Keyword Brainstorm

Start with these four sources:
1. **Core function**: What does the app literally do? (e.g., "track calories", "learn guitar")
2. **User problems**: What pain does it solve? (e.g., "lose weight fast", "guitar for beginners")
3. **Competitors**: What keywords do top competitors appear for?
4. **User language**: How would a first-time user describe what they're looking for?

### Phase 2: Keyword Classification

Classify every keyword candidate into this matrix:

| | High Relevance | Low Relevance |
|---|---|---|
| **High Volume** | Target — primary keywords | Avoid — traffic but wrong users |
| **Low Volume** | Target — long-tail gems | Skip |

**Difficulty tiers:**
- Hard (competition score 70+): Need strong domain authority + ratings to rank
- Medium (40-70): Best ROI for mid-stage apps
- Easy (<40): Quick wins, especially for new apps

### Phase 3: Competitor Keyword Gap Analysis

1. Identify top 3-5 direct competitors by category ranking
2. For each competitor, note which keywords they appear in top 10 for
3. Find keywords where:
   - Competitors rank but you don't (opportunity gap)
   - You rank 11-20 (low-hanging fruit — small push gets top 10)
   - No strong competitor ranks (blue ocean)

### Phase 4: Keyword Prioritization Scoring

Score each keyword 1-5 on three dimensions, then multiply:

```
Priority Score = Relevance (1-5) × Volume (1-5) × (6 - Difficulty) (1-5)
```

Top 20 by priority score = your keyword strategy.

## Keyword Placement Rules

### iOS Keyword Placement Priority
1. **App Name**: Put your single most important keyword here — gets highest weight
2. **Subtitle**: Put your second most important keyword phrase here
3. **Keyword Field**: Fill all 100 characters; no spaces after commas; no words already in title/subtitle; use singular OR plural (not both); include competitor names cautiously (gray area)

### Android Keyword Placement
1. **Title**: Lead with primary keyword, follow with brand or secondary keyword
2. **Short Description**: Hook sentence + primary keyword + one secondary keyword
3. **Long Description**: First 167 characters are shown before "read more" — pack value here. Primary keyword 3-5x naturally, secondary keywords 2-3x each

## Keyword Tracking

Track weekly:
- Current rank for each target keyword
- Impressions change (leading indicator)
- Download conversion per keyword (if available via Apple Search Ads / Google data)

Flag for revision if a keyword has been in top priority list for 8+ weeks with no top-20 ranking — swap it out.

## Output Format for Keyword Deliverable

When presenting keyword recommendations, use this format:

```
## Recommended Keyword Strategy: [App Name]

### Primary Keywords (put in title/subtitle)
| Keyword | Est. Monthly Searches | Competition | Recommended Placement |
|---------|----------------------|-------------|----------------------|
| [kw1]   | ~50K                 | Medium       | App Name             |
| [kw2]   | ~30K                 | Low          | Subtitle             |

### Keyword Field / Description Keywords
[kw3], [kw4], [kw5], [kw6]... (100 chars total for iOS)

### Long-tail Opportunities
| Keyword Phrase | Why It's Valuable |
|---------------|-------------------|
| [phrase 1]    | Low competition, high buyer intent |
| [phrase 2]    | Competitor gap — top 3 don't target this |

### Keywords to Drop / Avoid
- [kw]: Too competitive for current app authority
- [kw]: Low relevance, attracts wrong users
```
