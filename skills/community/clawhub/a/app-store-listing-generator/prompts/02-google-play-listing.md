# Prompt 2: Google Play Listing

Copy and paste this prompt into Claude. Replace all [BRACKETED] fields with your app's details.

---

```
You are an ASO expert specializing in Google Play Store optimization. Generate a complete Google Play listing for the following app. Strictly enforce all character limits and include keyword density analysis.

App Details:
- Name: [APP_NAME]
- Category: [CATEGORY]
- What it does: [ONE_SENTENCE]
- Core features: [FEATURE_1], [FEATURE_2], [FEATURE_3]
- Target user: [WHO]
- Problem solved: [SPECIFIC PROBLEM]
- Competitors: [COMPETITOR_1], [COMPETITOR_2], [COMPETITOR_3]
- Tone: [TONE]
- Primary keyword to rank for: [PRIMARY_KEYWORD]
- Secondary keywords: [KEYWORD_2], [KEYWORD_3]

---

Generate the complete Google Play listing:

**TITLE** (max 50 characters — Google Play indexes the title heavily; include primary keyword)
[title]
Character count: X/50

**SHORT DESCRIPTION** (max 80 characters — appears in search results before tap; no ellipsis cutoff; make every word earn its place)
[short description]
Character count: X/80

**FULL DESCRIPTION** (max 4,000 characters)

Google Play indexes ALL text in the description for keyword search — unlike iOS where only title/subtitle/keywords matter. Structure:

Opening paragraph (first 167 characters = what shows in search results snippets):
- Include primary keyword naturally in first sentence
- Lead with the strongest benefit, not a feature
- End with a proof point or number if possible

Feature sections (keyword-rich but human-first):
- Use natural language that includes target keywords
- Each feature section: 3-4 sentences
- Place secondary keywords in first 500 characters of full description

Benefits section:
- Concrete outcomes ("Wake up 30 minutes earlier" not "alarm features")
- Address the specific pain point of target user

Closing:
- CTA, download prompt
- Optional: support email or website
- Optional: "What users are saying:" + 2-3 short testimonial-style lines if available

[full description — 4,000 chars max]
Character count: X/4,000

**FEATURE GRAPHIC CONCEPT** (1024x500 pixels — the banner at the top of your Play Store listing)
- Headline text (8 words max): [headline]
- Subtext (4 words max): [subtext]
- Background concept: [describe — screenshot montage / lifestyle photo / abstract gradient / flat design]
- Color direction: [match to app's primary brand colors or specify]
- Key visual element: [what should be the focal point]

**A/B SHORT DESCRIPTION VARIANTS** (3 alternatives to test)
1. [short description variant A] (X/80) — angle: [benefit / action / question]
2. [short description variant B] (X/80) — angle: [benefit / action / question]
3. [short description variant C] (X/80) — angle: [benefit / action / question]

**KEYWORD DENSITY REPORT**
Primary keyword "[PRIMARY_KEYWORD]" appears in:
- Title: [yes/no]
- Short description: [yes/no]
- Full description: [X times] — recommendation: [optimal is 3-5x]

Secondary keyword "[KEYWORD_2]" appears:
- Full description: [X times] — [on target / add 1-2 more / reduce]

Secondary keyword "[KEYWORD_3]" appears:
- Full description: [X times] — [on target / add 1-2 more / reduce]

**CONTENT RATING NOTES**
Based on the app description, suggested IARC content rating: [Everyone / Teen / Mature 17+]
Reasons: [brief explanation]
```

---

## Key Differences: Google Play vs iOS

| Factor | iOS App Store | Google Play |
|--------|--------------|-------------|
| Title limit | 30 chars | 50 chars |
| Subtitle | 30 chars | None |
| Keyword field | 100 chars (separate) | Indexes all description text |
| Description | 4,000 chars | 4,000 chars |
| What gets indexed | Title + Subtitle + Keywords only | Title + Short Desc + Full Desc |
| Strategy | Keyword field is precious real estate | Put keywords in the description naturally |

**The most important Google Play rule:** Every keyword you want to rank for must appear in your description text. There is no separate keyword field. Google indexes the full description.
