# AI-Friendly SEO Master Workflow

This file activates when a user says:

```text
AI-friendly SEO
AEO
GEO
AI search optimization
Make my website ready for ChatGPT / Gemini / Perplexity / Google AI
Make my brand appear in AI answers
Answer engine optimization
Generative engine optimization
Entity SEO
Reputation SEO
Conversation SEO
```

The goal is to audit normal SEO plus AI-search readiness and produce a practical report.

---

## 1. Simple Meaning for Agents

When a user asks for AI-friendly SEO, do not treat it as only keywords.

Run this combined system:

```text
Traditional SEO
AEO: become the answer
GEO: become a source AI can mention or cite
Entity SEO: make the brand/person/company clear
Reputation SEO: prove trust with reviews, media, profiles, proof
Conversation SEO: answer the full human decision question
```

---

## 2. Default Apify-First Flow

Use Apify first.

Required default check:

```text
APIFY_API_TOKEN
```

Do not ask for many APIs up front.

Apify should be used for:

```text
Website crawl
Competitor crawl
Google SERP checks
People Also Ask / related queries
Google Trends
Google Maps / Places
Google reviews
PageSpeed / Lighthouse actors
AI Overview / AI Mode checks where supported
Third-party mentions
Social profile checks
Backlink / authority checks
GSC/GA4 connector or export actors where available
```

If Apify cannot collect a metric, label it missing or ask for an export later.

---

## 3. AI-Friendly SEO Audit Steps

### Step 1: Capability Check

```text
Is APIFY_API_TOKEN available?
Can Apify actors run?
What is the website URL?
What is the target country/city?
What is the business goal?
```

### Step 2: Normal SEO Baseline

Check:

```text
Crawlability
Indexability
Sitemap / robots
Metadata
H1/H2
Content depth
Schema
Internal links
Page speed
Conversion path
Keywords
Competitors
Backlinks / authority
Local SEO if relevant
```

### Step 3: AEO Audit

Check if pages:

```text
Answer direct questions early
Use clear headings
Include definitions
Include steps
Include cost/process/risk sections
Include comparison tables
Include FAQs based on real questions
Use proof and expert notes
```

### Step 4: GEO Audit

Check if pages are source-worthy:

```text
Clear claims
Clear entity
Original proof
Fresh information
Author/expert identity
External proof links
Structured data
Balanced comparison
No fake hype
```

### Step 5: Entity SEO Audit

Check if the website clearly explains:

```text
Who the person/brand/company is
What they do
Where they operate
Why they are trusted
Which profiles belong to them
Which reviews/media/certificates prove them
```

### Step 6: Reputation SEO Audit

Check:

```text
Google reviews
Trustpilot
LinkedIn
Facebook
YouTube
Clutch/G2/Capterra if relevant
Media mentions
Third-party articles
Student/customer proof
Case studies
Website review/proof pages
```

### Step 7: Conversation SEO Audit

For every money keyword, convert it into a full human question.

Example:

```text
Keyword: AI course
Conversation: Which AI course is trusted, practical, affordable, and can help me earn?
```

Then check if the website answers that complete question.

---

## 4. AI-Friendly SEO Report Structure

Use this report when the user asks for AI-friendly SEO:

```text
1. Audit Mode and Data Sources
2. Executive Summary
3. Traditional SEO Health
4. AEO Score: Can content become the answer?
5. GEO Score: Can AI cite or mention the brand?
6. Entity SEO Score: Does Google/AI understand who this is?
7. Reputation SEO Score: Is there enough proof?
8. Conversation SEO Score: Does content answer real human questions?
9. Apify Findings
10. Competitor / AI Visibility Gap
11. Pages to Create
12. Pages to Improve
13. Schema and Entity Fixes
14. Review / Reputation / Third-Party Authority Plan
15. 30-Day AI-Friendly SEO Plan
16. 60-Day Authority + Content Plan
17. 90-Day Growth Plan
18. Missing Data
```

---

## 5. Scoring Model

Score out of 100:

```text
Technical SEO: 15
Content / On-page: 15
AEO Readiness: 15
GEO / Source-worthiness: 15
Entity SEO: 15
Reputation Proof: 10
Conversation SEO: 10
Conversion / Tracking: 5
```

If local SEO is critical, include local SEO inside Entity + Reputation + Conversion.

---

## 6. Output Rule

Never say:

```text
This guarantees Google AI will show you.
This guarantees ChatGPT will mention you.
```

Say:

```text
This improves the probability that search engines and AI-answer systems can understand, trust, summarize, mention, or cite the brand.
```

---

## 7. Final Action Plan

Every AI-friendly SEO report must end with exact actions:

```text
Create these entity pages
Create these answer blocks
Create these reputation/proof pages
Create these third-party articles
Add these schema types
Fix these SEO blockers
Improve these conversion paths
Build these backlinks/profiles
Track these AI/search KPIs
```

## Research Anchors

Use these public guidance anchors when explaining or auditing AI-friendly SEO:

- Google Search Central: AI features and your website — https://developers.google.com/search/docs/appearance/ai-features
- Google Search Central: Google Search generative AI optimization guide — https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google Search Central: Creating helpful, reliable, people-first content — https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central: Organization structured data — https://developers.google.com/search/docs/appearance/structured-data/organization
- Google Search Central: ProfilePage structured data — https://developers.google.com/search/docs/appearance/structured-data/profile-page
- Google Search Central: Review snippet structured data — https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Bing Webmaster Tools: AI Performance — https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- Bing Webmaster Blog: AI Performance announcement — https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- Perplexity Hub — https://www.perplexity.ai/hub
