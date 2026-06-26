# Prompt 4: ASO Keyword Strategy

Copy and paste this prompt into Claude. Replace all [BRACKETED] fields with your app's details.

---

```
You are an App Store Optimization (ASO) strategist. Develop a comprehensive keyword strategy for the following app. Focus on actionable recommendations, not just theory.

App Details:
- App name: [APP_NAME]
- Category: [CATEGORY]
- What it does: [ONE_SENTENCE]
- Target user: [WHO]
- Problem solved: [SPECIFIC PROBLEM]
- Competitors: [COMPETITOR_1], [COMPETITOR_2], [COMPETITOR_3]
- Current keyword field (if updating): [CURRENT_KEYWORDS or "starting from scratch"]
- Countries targeting: [e.g., "US, UK, Canada" or "US only"]

---

Generate the complete ASO keyword strategy:

**KEYWORD TIER ANALYSIS**

Tier 1 — Primary Keywords (high volume, high competition — fight for these with strong ratings/downloads)
1. [keyword] | Est. volume: High | Competition: Hard | In title? [Yes/No — recommend if not]
2. [keyword] | Est. volume: High | Competition: Hard | In title? [Yes/No]
3. [keyword] | Est. volume: High | Competition: Hard | In title? [Yes/No]

Tier 2 — Secondary Keywords (medium volume, medium competition — winnable in 3-6 months)
1. [keyword] | Est. volume: Medium | Competition: Medium
2. [keyword] | Est. volume: Medium | Competition: Medium
3. [keyword] | Est. volume: Medium | Competition: Medium
4. [keyword] | Est. volume: Medium | Competition: Medium
5. [keyword] | Est. volume: Medium | Competition: Medium

Tier 3 — Long-Tail Keywords (lower volume, low competition — fast rankings, convert well)
1. [keyword phrase] | Est. volume: Low | Competition: Easy | Why it converts: [reason]
2. [keyword phrase] | Est. volume: Low | Competition: Easy | Why it converts: [reason]
3. [keyword phrase] | Est. volume: Low | Competition: Easy | Why it converts: [reason]
4. [keyword phrase] | Est. volume: Low | Competition: Easy | Why it converts: [reason]
5. [keyword phrase] | Est. volume: Low | Competition: Easy | Why it converts: [reason]

**COMPETITOR KEYWORD STEAL LIST**
Keywords your competitors likely rank for that you don't yet — sorted by opportunity score (volume × achievability):

| Keyword | Used by | Est. Volume | Your current position | Action |
|---------|---------|-------------|----------------------|--------|
| [keyword] | [competitor] | High/Med/Low | Not ranking | Add to keyword field |
| [keyword] | [competitor] | High/Med/Low | Not ranking | Add to iOS keyword field |
| [keyword] | [competitor] | High/Med/Low | Not ranking | Add to Google Play description |
| [keyword] | [competitor] | High/Med/Low | Not ranking | Add to title or subtitle |
| [keyword] | [competitor] | High/Med/Low | Not ranking | Add to keyword field |

**OPTIMIZED iOS KEYWORD FIELD** (max 100 characters, comma-separated, no spaces)
[keyword1,keyword2,keyword3,keyword4,keyword5,keyword6,keyword7]
Character count: X/100

Optimization notes:
- Removed from previous field: [keywords removed + why]
- Added: [keywords added + why]
- Avoided: [words already in title/subtitle — would be wasted characters]

**OPTIMIZED GOOGLE PLAY DESCRIPTION KEYWORDS** (since Google Play indexes all text)
Primary keyword placement:
- "[primary_keyword]" should appear in: first sentence, first 167 chars, and 3-5x total in description
- Recommended first sentence: "[SUGGESTED_OPENING_SENTENCE_WITH_KEYWORD]"

Secondary keyword placements:
- "[keyword_2]": first 500 chars + 2-3x in body
- "[keyword_3]": body section + closing

**METADATA OPTIMIZATION CHECKLIST**
iOS App Store:
- [ ] Primary keyword appears in Title
- [ ] Secondary keyword appears in Subtitle  
- [ ] No words from Title appear in Keyword field (wasted slot)
- [ ] No words from Subtitle appear in Keyword field (wasted slot)
- [ ] No competitor brand names in Keyword field (policy violation)
- [ ] All keywords are singular OR plural — not both (pick higher search volume variant)
- [ ] Keyword field uses exactly 100 characters (not 97, not 103)
- [ ] Keywords separated by comma only, no spaces (spaces count against limit)

Google Play:
- [ ] Primary keyword in first 50 characters of Full Description
- [ ] Primary keyword appears 3-5x naturally in Full Description
- [ ] Short Description includes primary or secondary keyword
- [ ] Full Description is at least 2,500 characters (incomplete descriptions hurt rankings)
- [ ] No keyword stuffing (same word more than 5x = penalty risk)

**SEASONAL KEYWORD OPPORTUNITIES**
Based on this app's category, consider adding these time-based keywords during peak seasons:
- [Month/season]: [keyword to add temporarily] — [why it spikes]
- [Month/season]: [keyword] — [why]
- [Month/season]: [keyword] — [why]

**90-DAY ASO ROADMAP**

Month 1 — Foundation:
- Implement optimized Title, Subtitle, Keyword field
- Fix any metadata errors (duplicates, wasted characters)
- Specific actions: [list 3-4 concrete steps]

Month 2 — Build:
- Monitor keyword rankings (use AppFollow or Sensor Tower free tier)
- Swap lowest-performing keywords in field for Tier 3 long-tails
- Run A/B test on Title Variant B
- Specific actions: [list 3-4 concrete steps]

Month 3 — Optimize:
- Analyze which keywords drove installs (check App Store Connect → Analytics → Source → App Store Search)
- Double down on converting keywords, drop non-converting ones
- Consider localized keyword fields for secondary markets
- Specific actions: [list 3-4 concrete steps]

**QUICK WINS** (do these in the next 7 days for immediate impact)
1. [Specific action with estimated impact]
2. [Specific action with estimated impact]
3. [Specific action with estimated impact]

**RED FLAGS TO FIX NOW**
[List any obvious errors in current metadata if provided, or common pitfalls for this category]
```

---

## How to Use This Strategy

1. **Run this prompt first** before writing any listing copy — keywords should drive copy, not the reverse
2. **Implement Tier 3 long-tails first** — fastest path to early rankings while Tier 1 builds
3. **Revisit every 30 days** — keyword performance shifts, especially after algorithm updates
4. **Track before/after** — screenshot your App Store Connect keyword rankings before implementing changes

## Free Tools to Validate These Keywords

- **App Store Connect → Analytics → App Store → Source: App Store Search** — shows exactly what keywords people searched to find your app
- **AppFollow free tier** — basic keyword tracking (3 keywords free)
- **Google Play Console → Store Listing Experiments** — A/B test descriptions directly in the console
