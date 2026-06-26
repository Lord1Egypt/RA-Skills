# App Store Listing Generator

**Version:** 1.0.0  
**Category:** Marketing / Mobile Apps  
**Author:** max_0x1  
**License:** MIT-0  
**Price:** $29 one-time | $9.99/month

---

## What This Skill Does

Generates conversion-optimized app store listings for iOS (App Store) and Android (Google Play), plus release notes and an ASO keyword strategy. Every field respects platform character limits — no truncation surprises.

4 prompts covering the full app store presence:
1. **iOS App Store Listing** — Title (30), Subtitle (30), Keywords (100), Description (4,000)
2. **Google Play Listing** — Title (50), Short Description (80), Full Description (4,000), Feature Graphic concepts
3. **App Update Release Notes** — What's New copy (4,000 chars iOS / 500 chars Android), 3 A/B test variants
4. **ASO Keyword Strategy** — Keyword gaps, competitor steal list, metadata optimization checklist

---

## Inputs Required

For the listing prompts (1–2):
- App name
- App category (e.g., Productivity, Health & Fitness, Finance)
- One-sentence description of what the app does
- Top 3 core features
- Primary target user (who is this for?)
- Main problem it solves
- 3–5 competitor apps (optional but improves keyword output)
- Tone (professional / friendly / bold / minimal)

For release notes (3):
- Version number
- List of changes (features added, bugs fixed, improvements)
- Tone

For ASO strategy (4):
- App name, category, 3–5 competitors
- Current keyword field (if updating)

---

## Prompt 1: iOS App Store Listing

```
You are an App Store Optimization (ASO) expert. Generate a complete iOS App Store listing for the following app.

App Details:
- Name: [APP_NAME]
- Category: [CATEGORY]
- What it does: [ONE_SENTENCE_DESCRIPTION]
- Core features: [FEATURE_1], [FEATURE_2], [FEATURE_3]
- Target user: [TARGET_USER]
- Problem solved: [PROBLEM]
- Competitors: [COMPETITOR_1], [COMPETITOR_2], [COMPETITOR_3]
- Tone: [TONE]

Generate the following, strictly respecting all character limits:

**TITLE** (max 30 characters — include primary keyword naturally)
[Your title here]
Character count: X/30

**SUBTITLE** (max 30 characters — secondary benefit or keyword)
[Your subtitle here]
Character count: X/30

**KEYWORD FIELD** (max 100 characters, comma-separated, no spaces after commas, no brand names)
[keyword1,keyword2,keyword3...]
Character count: X/100

**DESCRIPTION** (max 4,000 characters — first 3 lines appear above "more" fold; make them count)

[First 3 lines — hook, primary benefit, proof point]

[Body: expand on top 3 features with concrete benefits, not just feature names. Use short paragraphs and line breaks for readability. Include social proof language if applicable.]

[Closing: CTA + download prompt]

Character count: X/4,000

**A/B TITLE VARIANTS** (3 alternatives to test)
- Variant A: [title] (X/30)
- Variant B: [title] (X/30)
- Variant C: [title] (X/30)

**ABOVE-THE-FOLD PREVIEW** (what users see before tapping "more")
[Paste first 3 lines of description here so client can verify]

**LOCALIZATION NOTES**
- If targeting Spanish-speaking markets: [keyword translation suggestions]
- If targeting UK English: [spelling/phrasing adjustments]
```

---

## Prompt 2: Google Play Listing

```
You are an ASO expert specializing in Google Play. Generate a complete Google Play Store listing for the following app.

App Details:
- Name: [APP_NAME]
- Category: [CATEGORY]
- What it does: [ONE_SENTENCE_DESCRIPTION]
- Core features: [FEATURE_1], [FEATURE_2], [FEATURE_3]
- Target user: [TARGET_USER]
- Problem solved: [PROBLEM]
- Competitors: [COMPETITOR_1], [COMPETITOR_2], [COMPETITOR_3]
- Tone: [TONE]

Generate the following, strictly respecting all character limits:

**TITLE** (max 50 characters — Google indexes this heavily; include primary keyword)
[Your title here]
Character count: X/50

**SHORT DESCRIPTION** (max 80 characters — appears in search results before tap; make every word count)
[Your short description here]
Character count: X/80

**FULL DESCRIPTION** (max 4,000 characters — Google Play indexes all text for search; keyword density matters more here than iOS)

[Opening paragraph: hook + primary benefit + social proof in first 167 characters (what appears in search)]

[Feature section: use natural language that includes target keywords. Avoid keyword stuffing — write for humans, but place keywords in the first 500 characters.]

[Benefits section: concrete outcomes, not feature names. "Wake up earlier" not "alarm features."]

[Closing: CTA, download prompt, support/contact info]

Character count: X/4,000

**FEATURE GRAPHIC CONCEPT** (1024x500 — text overlay suggestions for the banner shown at top of listing)
- Headline text: [8 words max]
- Subtext: [4 words max]
- Visual suggestion: [describe what to show — screenshot, lifestyle, abstract]

**A/B SHORT DESCRIPTION VARIANTS** (3 alternatives to test)
- Variant A: [short desc] (X/80)
- Variant B: [short desc] (X/80)
- Variant C: [short desc] (X/80)

**KEYWORD DENSITY REPORT**
Primary keyword "[KEYWORD]" appears: X times in full description
Secondary keywords: [list each + count]
Recommendation: [add/remove/adjust]
```

---

## Prompt 3: App Update Release Notes

```
You are an ASO expert writing app update release notes. Generate release notes for the following update.

App Details:
- App name: [APP_NAME]
- Version: [VERSION_NUMBER]
- Changes this update:
  [LIST_OF_CHANGES]
- Tone: [TONE]

Generate the following:

**iOS WHAT'S NEW** (max 4,000 characters — but short is better; 100-300 words ideal)

[Version X.X.X]

[Opening line: lead with the most user-impactful change, not technical details. "You asked, we listened." type openers work well.]

[Bulleted changes, user-benefit framing. Not "Fixed null pointer exception" → "App no longer crashes when switching between tabs."]

[Closing: thanks line + support CTA if warranted]

Character count: X/4,000

**ANDROID WHAT'S NEW** (max 500 characters — extremely tight; pick top 3 changes only)
[Condensed version]
Character count: X/500

**A/B VARIANTS** (3 opening line variants to test engagement)
- Variant A: [first line] — [angle: benefit-led]
- Variant B: [first line] — [angle: social proof]
- Variant C: [first line] — [angle: problem solved]

**INTERNAL RELEASE NOTES** (for team/testers — technical detail OK here)
[Full technical changelog with internal language]
```

---

## Prompt 4: ASO Keyword Strategy

```
You are an App Store Optimization (ASO) strategist. Develop a keyword strategy for the following app.

App Details:
- App name: [APP_NAME]
- Category: [CATEGORY]
- What it does: [ONE_SENTENCE_DESCRIPTION]
- Current keywords being targeted (if known): [CURRENT_KEYWORDS]
- Competitors: [COMPETITOR_1], [COMPETITOR_2], [COMPETITOR_3]

Generate the following:

**KEYWORD GAP ANALYSIS**

Primary keywords (high volume, high competition — fight for these):
1. [keyword] — search volume estimate: [high/medium/low] | difficulty: [hard/medium/easy]
2. [keyword] — ...
3. [keyword] — ...

Secondary keywords (medium volume, medium competition — winnable):
1. [keyword]
2. [keyword]
3. [keyword]
4. [keyword]
5. [keyword]

Long-tail keywords (lower volume, lower competition — fast wins):
1. [keyword phrase]
2. [keyword phrase]
3. [keyword phrase]
4. [keyword phrase]
5. [keyword phrase]

**COMPETITOR STEAL LIST**
Keywords your competitors rank for that you don't — sorted by opportunity:
1. [keyword] — used by [competitor], estimated volume: [high/med/low]
2. [keyword] — ...
3. [keyword] — ...
4. [keyword] — ...
5. [keyword] — ...

**iOS KEYWORD FIELD (OPTIMIZED)** (max 100 chars, no spaces after commas)
[keyword1,keyword2,keyword3,...]
Character count: X/100

**METADATA OPTIMIZATION CHECKLIST**
- [ ] Primary keyword appears in Title
- [ ] Secondary keyword appears in Subtitle
- [ ] No keyword appears in both Keyword field AND Title/Subtitle (wasted slot)
- [ ] No competitor brand names in keyword field (policy violation risk)
- [ ] All keywords are singular OR plural — not both (pick higher volume)
- [ ] Google Play description: primary keyword in first 167 characters
- [ ] Google Play description: secondary keyword appears 3-5x naturally

**90-DAY ASO ROADMAP**
Month 1: [focus area + specific actions]
Month 2: [focus area + specific actions]
Month 3: [focus area + specific actions]

**QUICK WINS** (do these in the next 7 days)
1. [specific action]
2. [specific action]
3. [specific action]
```

---

## Output Examples

See `examples/focusflow-habit-tracker/` for a complete worked example:
- iOS listing for a habit tracking app
- Google Play listing
- v2.1.0 release notes
- Full ASO keyword strategy

---

## Pricing

| Tier | Price | What You Get |
|------|-------|--------------|
| Skill access | $29 one-time | All 4 prompts, example, updates |
| Monthly | $9.99/month | Same + priority support |
| Done-For-You | $79/listing | Max runs all 4 prompts, delivers formatted Google Doc |

---

## Who This Is For

- Indie developers launching their first app
- Mobile app studios managing multiple listings
- Growth marketers doing App Store Optimization
- Agencies creating app store assets for clients
- SaaS founders moving to mobile
