---
name: brand-butler-local-authority-engine
version: 1.2.0
description: "Brand Butler: Local Authority Engine — the white-glove SEO and AEO system for local service businesses. Use this skill immediately when the user asks about SEO rankings, backlinks, citations, site audits, Google Search Console indexing problems, competitor backlink analysis, directory submissions, schema markup, content placement articles, local map pack visibility, or AI answer engine optimization (Perplexity, ChatGPT, Google AI Overviews). Also triggers for any local business growth, online visibility, or 'why isn't my site ranking?' conversation. Works for agencies managing clients and business owners doing their own SEO. Covers HVAC, plumbing, electrical, law, dental, roofing, and any local service business. Built by Adrian Boysel."
tags: [seo, local-seo, aeo, backlinks, citations, google, schema, content, audit, rankings, local-business, brand-butler, authority, concierge]
author: Adrian Boysel
homepage: https://adrianboysel.com
metadata:
  clawhub:
    emoji: "🎩"
    requires:
      bins: []
      env: []
    stateDirs: []
    persistence: "This skill is instruction-only. It guides the user through SEO workflows conversationally — all directory submissions, GSC access, and credential handling are performed manually by the user or agent in a supervised session. The skill never stores, logs, or transmits credentials. Login tracking is recorded by the user in their own external tracker (e.g. a spreadsheet), not by this skill. No files are written to disk. No network requests are made by the skill itself."
---

# 🎩 Brand Butler: Local Authority Engine

**The SEO & citation system that builds unshakeable local presence.**

*Built by [Adrian Boysel](https://adrianboysel.com) — digital marketing agency founder and creator of [Brand Butler](https://adrianboysel.com) and [Skill Stacker](https://joinskillstacker.com).*

Brand Butler: Local Authority Engine handles the full SEO and AEO lifecycle for local service businesses — from technical audits to citation campaigns to AI answer engine optimization. Whether you're an agency managing clients or a business owner building your own presence, this skill works as your dedicated local search strategist.

---

## ⛔ AGENT RULES — READ BEFORE DOING ANYTHING

> 1. **Always run Phase 0 intake first.** Never skip NAP collection. Every audit, campaign, and content piece depends on it.
> 2. **Foundation before paint.** Fix technical SEO and schema before building backlinks. Advanced tactics don't fix a broken foundation.
> 3. **NAP must be identical everywhere.** Even "St." vs "Street" can suppress rankings. Establish canonical NAP and use it on every submission.
> 4. **Never guess — gather context.** If GCT information is missing, ask. Optimizing without knowing the business's goals, content, and targets produces generic, ineffective output.
> 5. **Track submissions in an external tracker.** Instruct the user to log directory submissions (name, URL, login, status, listing URL, dofollow) in their own spreadsheet or doc. This skill never stores, logs, or requests passwords — always direct the user to record credentials in their own secure tool.
> 6. **Never ask for passwords in chat.** If directory access is needed, instruct the user to log in themselves or use a password manager. Never collect or repeat credentials conversationally.
> 7. **Hand off blockers gracefully.** reCAPTCHA, phone verification, and Cloudflare blocks get handed to the business owner with exact step-by-step instructions — never leave them stranded.
> 8. **All network actions are user-performed.** This skill provides instructions and strategy. Fetching sitemaps, accessing GSC, submitting to directories — all of these are actions the user takes in their own browser or tools, not actions this skill performs autonomously.

---

## When to Use This Skill

Use when the user asks to:
- Audit a website for SEO issues or indexing problems
- Build backlinks or citations for a local business
- Analyze competitor backlinks and find directory opportunities
- Fix Google Search Console indexing issues
- Write SEO-optimized content for link placements (guest posts, sponsored content)
- Submit a business to directories and citation sites
- Create a citation/backlink campaign plan
- Improve local search rankings or map pack visibility
- Optimize for AI answer engines (Perplexity, ChatGPT, Google AI Overviews)
- Answer "why isn't my site ranking?" or "how do I get more leads from Google?"

---

## Phase 0: Client Intake (Always Start Here)

Before any SEO work, gather the business fundamentals. **Never skip this phase.**

### The GCT Framework

**Goals:** What services generate the most revenue? What does the business want more of?
**Content:** What does the business actually offer? What makes them different from competitors?
**Targeting:** Who is the ideal customer? What locations? What search intent are they typing?

### NAP — Canonical Identity

Establish this exact format first. It will be used **identically** on every directory, citation, and schema block:

| Field | Example |
|-------|---------|
| Business Name | Apex Plumbing & Drain (not "Apex Plumbing and Drain") |
| Street Address | 1234 Oak St Ste 200 (pick one format and lock it) |
| City, State ZIP | Sacramento, CA 95814 |
| Phone | (916) 555-0100 |
| Website | https://apexplumbing.com |
| Email | office@apexplumbing.com |

**CRITICAL:** Search for existing listings immediately. Multiple phone numbers, address variations, or name variations actively suppress rankings. Document all inconsistencies and flag for the owner before campaign launch.

### Business Profile to Collect
- Owner name + preferred contact
- Year founded
- Licenses/certifications (state contractor license #, NATE cert, bar number, etc.)
- Full service list
- Service area (every city, neighborhood, ZIP)
- Google Business Profile URL + current rating/review count
- Existing Yelp listing
- Standard description (150-200 words) — used for most directories
- Short description (50 words) — used for character-limited listings

---

## Phase 1: Technical SEO Audit

> Read `references/technical-audit-checklist.md` for the complete audit checklist and scoring rubric.

### Priority Order

1. **Keyword placement** — Target keyword in URL, title tag, H1, meta description, first paragraph on every page
2. **Schema markup** — LocalBusiness, Service, FAQ, Article, BreadcrumbList as appropriate
3. **Core Web Vitals** — LCP < 2.5s, INP < 200ms, CLS < 0.1 (mobile is primary)
4. **Mobile interstitials** — Pop-ups that block content trigger Google ranking penalties
5. **Trust signals** — NAP in footer, about page, contact page; real staff photos; bios
6. **Sitemap audit** — Compare sitemap.xml count vs GSC submitted vs actually indexed
7. **Internal linking** — Map entity relationships, build contextual links with target-keyword anchors

### Google Indexation Diagnostics

If the client reports low indexation (e.g., 29 of 129 pages indexed):

**Step 1:** Compare sitemap.xml page count vs GSC submitted count.
If GSC shows more URLs than the sitemap → Google is discovering junk URLs (parameters, tags, pagination).

**Step 2:** Identify exclusion reason in GSC → Pages → "Why pages aren't indexed":
- *"Discovered – currently not indexed"* = crawl priority/budget issue
- *"Crawled – currently not indexed"* = content quality or duplication issue
- *"Duplicate without user-selected canonical"* = missing or wrong canonical tags

**Step 3:** Apply the right fix:
- Thin city-swap pages → add 600-800 words of genuine local content per page
- Overlapping blog posts → consolidate into one authoritative article with 301 redirects
- Parameter/tag URLs → noindex or robots.txt disallow
- **Goal:** 50 strong pages that all get indexed beats 129 pages where 100 are ignored

---

## Phase 2: Backlink & Citation Campaign

> Read `references/directory-master-list.md` for the complete directory database, exclusion list, and submission notes.

### Campaign Execution Order

**Step 1 — Data Aggregators** *(do first — they feed 100+ downstream sites automatically)*
Data Axle, Foursquare Places, TransUnion/Neustar Localeze

**Step 2 — Tier 1 High-Authority (DA 80+)**
Google Business Profile, Apple Business Connect, Bing Places, Yelp, BBB, Nextdoor, Trustpilot, LinkedIn Company Page, Facebook Business

**Step 3 — Industry-Specific Directories**
Find directories for the client's exact trade (HVAC, plumbing, legal, dental, roofing, etc.), utility/certification directories (SMUD, PG&E, state licensing boards). These deliver maximum topical relevance — prioritize over generic directories.

**Step 4 — General Business Directories (DA 40-75)**
Manta, Brownbook, Storeboard, Hotfrog, Cybo, APSense, Callupcontact, etc.

**Step 5 — Local & Regional Directories**
Chambers of Commerce (paid but high value — dofollow, strong local authority signal), city-specific portals, local news site directories, regional "best of" lists (Expertise.com, etc.)

**Step 6 — Competitor Backlink Gap Analysis**
Export competitor backlinks from Ahrefs/SEMrush/Ubersuggest. Filter: DA ≥ 10, not spam. Cross-reference against client's existing listings. Submit to every qualifying free directory the competitor has that the client doesn't.

### Submission Rules
1. NAP must be **identical** across every submission — verify against canonical NAP before each entry
2. Use the standard business description — do not spin or randomize
3. Always include website URL — that's where link equity flows from
4. Select the most specific category available
5. Add all service area cities wherever the directory allows
6. Track every submission in your own external spreadsheet: directory name, URL, status, listing URL, dofollow/nofollow — never share or paste passwords directly into chat

### Handling Blockers

| Blocker | Action |
|---------|--------|
| reCAPTCHA | Note in tracker; give owner exact URL + pre-filled fields to complete manually |
| Email verification | Flag which inbox to check; provide login credentials |
| Phone verification | Flag for owner — cannot be done remotely |
| Cloudflare/bot blocking | Must be completed from a real browser session |
| Paid only | Exclude unless client explicitly approves the cost |

---

## Phase 3: Content Placement Articles

> Read `references/content-placement-guide.md` for full article templates, anchor text strategy, and platform-specific requirements.

### Article Requirements
- **Minimum 750 words** (aim for 1,000+ for maximum placement value)
- **Maximum 2 links** to client site unless placement explicitly allows more
- **Anchor text:** Use target keyword phrases — "Rocklin AC repair", "Sacramento plumbing services"
- **No images** unless the placement specifically includes them
- **Match host site's tone** — read 3-5 of their existing articles before writing

### AEO Optimization
- Primary keyword in the title (H1)
- Keywords naturally in H2 subheadings
- Question-answering H2s that match conversational/voice queries
- Local geo signals: city names, neighborhoods, landmarks, regional conditions
- Supporting semantic terms for topical depth
- Write for humans. Optimize for machines. Never stuff.

### Meta Block for Placement's Special Requirements Field
```
Meta Title: [Primary Keyword] | [City/Service Area]
Meta Description: [150-160 chars with primary + secondary keywords]
Please keep anchor text links exactly as written in the article.
Do not add additional outbound links.
Category: [Most relevant category on host site]
```

---

## Phase 4: AEO — Answer Engine Optimization

Optimizing for Perplexity, ChatGPT, and Google AI Overviews requires a different playbook than traditional SEO.

### AEO Content Principles
- **Structured answers first.** Each page directly answers "What is [service]?", "How much does [service] cost in [city]?", "How long does [service] take?" — one question, one direct answer, then supporting detail.
- **FAQ schema is mandatory.** Every service page needs FAQ schema with 5-10 Q&A pairs targeting conversational queries.
- **Entity-based writing.** Mention related entities naturally: nearby cities, complementary services, certifications, equipment brands used.
- **Cite credible sources.** Link out to manufacturer specs, city permit offices, state licensing boards. AI engines favor pages that reference authoritative sources.
- **Kill the fluff intro.** AI engines scrape the most direct answer — put it in the first paragraph, not after three sentences of throat-clearing.

### AEO Schema Priority
1. LocalBusiness (name, address, phone, geo coordinates, areaServed, openingHours)
2. Service (for each individual service page)
3. FAQPage (5-10 questions per page minimum)
4. HowTo (for process-based content)
5. Review/AggregateRating (pulled from GBP)

---

## Phase 5: Ongoing Optimization

### Weekly/Monthly Checks
- Google Search Console: indexation rates, crawl errors, coverage changes, new manual actions
- Google Analytics: organic traffic trends, top landing pages, conversion events
- Citation consistency: spot-check NAP across top 10 listings monthly
- Competitor new backlinks: run gap analysis quarterly

### Freshness Strategy
- Update one FAQ answer per page every 6 months with current data
- Refresh blog posts annually with updated statistics and year references
- Add new service area pages as the business expands geographically
- Respond to new reviews across all major platforms within 48 hours

### Content Quality Triage

| Action | When to Apply |
|--------|--------------|
| **Improve** | Page has ranking potential but lacks depth or optimization |
| **Noindex** | Page is needed for users but not worth crawl budget |
| **Delete + 301 Redirect** | Page is redundant or harmful to crawl efficiency |

---

## Key Principles

1. **Context before action.** Never optimize without understanding the business. Generic audits produce generic results.
2. **Absence is the #1 enemy.** A missing ranking factor hurts more than a weak one. Cover all bases before deep-optimizing any single factor.
3. **Relevance over volume.** 10 relevant internal links beat 600 random ones. 50 fully indexed pages beat 129 half-indexed ones.
4. **Human in the loop.** This agent handles 80% of the work. Owner confirms GCT, approves categories, resolves blockers.
5. **Measure everything.** Every change traces: impressions → clicks → calls → revenue.
6. **Foundation before paint.** Schema, Core Web Vitals, trust signals, and keyword placement come before link building.
7. **NAP consistency is non-negotiable.** One inconsistency across 60 directories does more harm than having 30 fewer listings.

---

## Reference Files

| File | When to Read |
|------|-------------|
| `references/technical-audit-checklist.md` | Before running any on-page or technical audit |
| `references/directory-master-list.md` | Before starting any citation or backlink campaign |
| `references/content-placement-guide.md` | Before writing any placement articles |
| `references/seo-strategy-framework.md` | For high-level strategy context and client education |

---

*🎩 Brand Butler: Local Authority Engine — Part of the [Brand Butler](https://adrianboysel.com) suite by [Adrian Boysel](https://adrianboysel.com)*
*[Skill Stacker](https://joinskillstacker.com) | [Brand Hacker](https://brandhacker.com)*
