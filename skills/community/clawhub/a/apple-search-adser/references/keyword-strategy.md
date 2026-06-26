# Keyword Strategy Framework

## Keyword Intent Tiers

Not all keywords are equal. Segment by intent — different tiers need different bids, budgets, and expectations.

### Tier 1: High Intent (Solution Seekers)

Users know what they want and are ready to install.

Characteristics:
- Action verbs: "track", "plan", "manage", "edit", "learn"
- Category + purpose: "habit tracker", "calorie counter", "budget app"
- High CR (typically 40-60%), moderate to high CPT

Examples:
- "HIIT workout app"
- "AI photo editor"
- "daily expense tracker"
- "language learning app"

**Bid approach**: Pay premium — these convert. Start at Apple's suggested bid midpoint.

---

### Tier 2: Feature Keywords

Users searching for a specific capability, not a whole solution.

Characteristics:
- Feature-specific: "interval timer", "macros calculator", "PDF scanner"
- Often longer, more specific queries

Examples:
- "rest timer between sets"
- "split bill calculator"
- "scan document to PDF"

**Bid approach**: Mid-range bids. CR is good when your app has that feature prominently.

---

### Tier 3: Long-Tail Keywords

More specific intent = lower competition, lower CPI, higher install quality.

Examples:
- "workout planner for beginners no gym"
- "AI habit tracker with streaks"
- "budget tracker for couples"

**Bid approach**: Lower bids — less competition. These often deliver your best-quality users.

**Finding long-tails**: Use your Discovery campaign. Users type exactly what they need — export the search terms and look for specific, unconventional phrases that convert.

---

### Tier 4: Awareness Keywords

Broad, high-volume, low-intent searches.

Examples:
- "fitness"
- "productivity"
- "photo"

**Bid approach**: Very low bids or avoid entirely. Impression volume is high but conversion is poor. Use only in Discovery to see if any related search terms convert.

---

## Keyword Research Process

### Step 1: Seed List from Your App

Start with what your app does:
- Core features (list 5-10)
- User goals ("I want to lose weight" → "weight loss tracker")
- Target scenarios ("after work" → "evening workout")
- Pain points your app solves

### Step 2: Competitor Mining

Search each competitor in the App Store. Look at their:
- App name keywords
- Screenshot callouts (reveal what features they emphasize)
- User reviews (exact phrases users use = high-intent search terms)

### Step 3: Apple Search Ads Keyword Planner

In the ASA dashboard, use the keyword suggestion tool:
- Enter seed keywords
- Filter by relevance and popularity
- Look for keywords with "medium" popularity — high enough to have volume, low enough to not be hypercompetitive

### Step 4: Discovery Campaign Mining (ongoing)

After 2-4 weeks of running a discovery campaign:
- Export search terms report
- Sort by conversion rate (descending)
- Filter: CR > 25%, installs ≥ 5
- Add to exact match campaigns

---

## Keyword Match Types

### Exact Match
- Triggers only when user searches exactly that term (minor variations allowed)
- Highest relevance, lowest impression volume
- Use for proven converting keywords

### Broad Match
- Triggers for related searches, synonyms, word-order variations
- Higher impression volume, lower relevance
- Use in Discovery to find new converting terms

### Search Match (Apple's automated)
- Apple finds related search terms automatically
- Enable in Discovery campaigns only
- Disable in Brand and Generic to maintain control

---

## Negative Keywords — Wasted Spend Prevention

Add these as negatives to all campaigns from day one:

**Universal negatives** (add to every campaign):
- free (unless your app is free)
- crack, hack, cheat, mod, apk
- wallpaper, ringtone, sticker, emoji
- Any category completely unrelated to your app

**Brand campaign negatives**: Add all competitor names as negatives — prevents your brand campaign from showing for competitor searches (that belongs in the Competitor campaign).

**Generic campaign negatives**: After 4 weeks, add any search terms from Discovery that had 0 conversions with ≥ 10 taps. These are burning budget.

**Negative match types**: Use exact match negatives for specific terms, broad match negatives for topic exclusions.

---

## Keyword Scoring Matrix

Use this to prioritize which keywords to bid up vs down:

```
Score = (Conversion Rate × 5) + (Install Volume × 3) - (CPA × 2)
```

Normalize each factor to 1-10 scale within your dataset. Keywords with score ≥ 25 are candidates for bid increases. Keywords with score ≤ 10 for 2+ weeks are candidates for pausing.

---

## Output Format for Keyword Deliverables

When recommending keywords, use this structure:

```
## Keyword Strategy: [App Name]

### Brand Campaign
[App name], [misspelling 1], [brand variation]

### Generic Campaign — Exact Match (Priority)
| Keyword | Intent | Est. Competition | Action |
|---------|--------|-----------------|--------|
| [kw1]   | High   | Medium          | Start at $X bid |
| [kw2]   | High   | Low             | Start at $X bid |

### Generic Campaign — Broad Match (Phase 2)
[Add after 2 weeks of exact match data]

### Long-Tail Opportunities
[kw1] — [why valuable]
[kw2] — [why valuable]

### Competitor Targets
[Competitor 1] — [rationale]
[Competitor 2] — [rationale]

### Negative Keywords (add immediately)
free, [category unrelated terms], [confirmed non-converters]
```
