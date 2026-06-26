# Metadata Optimization Guide

## iOS App Store Metadata

### App Name (30 characters)
- Most heavily weighted field in Apple's algorithm
- Structure: `[Primary Keyword] - [Brand]` or `[Brand]: [Primary Keyword]`
- The keyword in the name gets ~3x the weight of keywords elsewhere
- Avoid: articles (a, the), filler words, punctuation that wastes chars
- Good example: `Calm: Sleep & Meditation` — brand + two high-value keywords in 25 chars
- Bad example: `The Best Meditation App for You` — wastes chars, no specificity

### Subtitle (30 characters)
- Second most weighted field
- Use for secondary keyword phrase you couldn't fit in the name
- Should also make sense as a human-readable tagline
- Structure: `[Secondary Keyword] + [Benefit]` or `[Feature] + [Target Audience]`
- Example: `Focus, Relax & Sleep Better` — three additional indexed terms

### Keyword Field (100 characters)
Rules:
- Comma-separated, NO spaces after commas (saves chars)
- Never repeat words already in title or subtitle
- Use singular — Apple indexes both singular and plural from one form (usually)
- No special characters except commas
- Competitor brand names: technically allowed, ethically gray, low risk legally but against Apple guidelines in spirit
- Numbers: include digit versions (e.g., `5` not `five`)

Character-saving tips:
- Omit stop words (and, for, the, to, of)
- Use short synonyms
- Think what a user types, not what sounds professional

### Description (4000 characters)
- NOT indexed by Apple's search algorithm
- Purely for conversion — written for humans, not search bots
- First 167 characters show before "more" button — make them count

**Description structure:**
```
[Hook — problem/solution in 1-2 sentences]

[Core features as benefit statements, bulleted]
• [Feature]: [What it means for the user]
• [Feature]: [What it means for the user]

[Social proof — ratings, user count, awards]

[Secondary features]

[Call to action]
```

### In-App Purchases (iOS)
- IAP names ARE indexed by App Store search
- Name your subscriptions/IAPs with relevant keywords
- Example: "Premium Meditation Pack" indexes "meditation" without using title/keyword chars

---

## Google Play Metadata

### Title (30 characters)
- Highest weight in Play Store ranking
- Keywords here have biggest impact
- Structure: `[Brand] - [Primary Keyword]` or `[Primary Keyword] by [Brand]`
- Example: `Duolingo - Language Lessons` — brand recognition + primary keyword

### Short Description (80 characters)
- Shown in search results before user opens the listing
- First impression + keyword opportunity
- Structure: Hook + primary benefit + secondary keyword
- Must stand alone — assume user hasn't seen the title
- Example: `Learn Spanish, French & more. Free language learning app.`

### Long Description (4000 characters)
- Fully indexed — this IS your keyword field on Android
- Recommended keyword density: primary keyword 3-5x, secondary 2-3x
- Natural integration — don't stuff
- Structure mirrors iOS description but with deliberate keyword placement
- Bold text using `<b>` tags for key phrases (Play Store renders basic HTML)
- First paragraph indexed most heavily — front-load keywords

### Category
- Choose primary category carefully — affects which "Top Charts" you appear in
- Secondary category available on Android — use it strategically

---

## Conversion Copywriting Principles

### The "Value Before Feature" Rule
Don't list features — explain what they do for the user.
- Bad: "AI-powered sleep tracking"
- Good: "Wake up refreshed — our AI learns your sleep cycle and finds your perfect alarm window"

### The "Show Don't Tell" Principle
- Bad: "The best meditation app"
- Good: "10 million people have used Calm to sleep better, stress less, and live more mindfully"

### Social Proof Hierarchy (most to least powerful)
1. User count ("10M+ downloads")
2. Rating ("4.8 stars, 200K reviews")
3. Awards ("App of the Year, Apple")
4. Media mentions ("As seen in Forbes")
5. Expert endorsements

### Localization Note
When adapting copy for other markets, don't just translate — adapt the social proof, the benefits emphasis, and the CTA to match local user expectations. Japanese users respond to precision and detail; US users respond to outcomes and social proof; German users respond to features and specifications.

---

## Metadata Audit Checklist

Before finalizing, verify:
- [ ] Title uses primary keyword in first 15 characters
- [ ] No character waste (no trailing spaces, unnecessary punctuation)
- [ ] Keyword field has no spaces after commas (iOS)
- [ ] No repeated words across title + subtitle + keyword field (iOS)
- [ ] Description hook addresses user's problem in first sentence
- [ ] Social proof included with specific numbers
- [ ] CTA present and action-oriented
- [ ] Reading level appropriate for target audience
- [ ] Localized versions adapted, not just translated
