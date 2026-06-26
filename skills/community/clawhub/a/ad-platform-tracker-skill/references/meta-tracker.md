# Meta Algorithm & Policy Tracker

## Andromeda — The 2025 Paradigm Shift

**What it is:** Meta's new AI-powered ads retrieval engine, built on NVIDIA Grace Hopper Superchip + Meta MTIA hardware. Achieved a 10,000x increase in model complexity vs. predecessor. Replaces the legacy heuristic-based auction model.

**Timeline:** Rolled out late 2024 → early 2025 → global completion October 2025.

**Core change:** Creative is now the primary targeting mechanism. The system reads the *semantic and visual signals* of your creative to decide who sees it — not your audience settings.

### Andromeda Impact by Area

**Creative Strategy (CRITICAL CHANGE)**
- Old model: 3–6 ads per ad set, audience segmentation was the lever
- New model: 10–20 unique creative *concepts* per campaign (not just variations)
- Creative similarity detection: Visually/semantically similar ads are clustered and suppressed together
- Format variety required: static images, short videos, UGC, carousels, reels, founder-led, memes
- Conceptual diversity needed: value, aspiration, social proof, comparison, education, emotion — all different
- Refresh cycle: Every 21–28 days proactively (don't wait for fatigue to show)
- Early data: 17% more conversions at 16% lower cost (1 ad set, 25 diverse creatives vs. 5 ad sets × 5 creatives)
- Advantage+ Creative users: 22% higher ROAS average

**Campaign Structure**
- Old model: Complex segmentation, many ad sets, tightly defined audiences
- New model: 1–3 ad sets max per campaign, broad targeting, let AI find the audience
- Consolidated budget at campaign level
- Enable Advantage+ placements + automated optimization
- Lookalike audiences = signal inputs now, not hard boundaries

**New Metrics to Monitor**
- Creative Fatigue score (rising CPMs = primary red flag before score appears)
- Creative Similarity score (high = algorithm penalizes with CPM increases)
- Top Creative Themes (which angles resonate: humor, nostalgia, social proof, etc.)

**Recommended Andromeda Checklist**
1. ☐ Audit creative library for conceptual diversity (not just visual tweaks)
2. ☐ Consolidate ad sets — aim for 1 per campaign per objective
3. ☐ Switch to broad targeting (expand age to 18-65+, remove interest stacks)
4. ☐ Enable Advantage+ placements
5. ☐ Set up 21-28 day creative refresh schedule
6. ☐ Upload offline conversions / high-quality lead data back to Meta
7. ☐ Test Advantage+ Shopping Campaigns (ASC) for e-commerce
8. ☐ Enable AI creative enhancements (with review for compliance verticals)

---

## Meta Features & Policy Updates (2025–2026)

### Attribution Windows
- **Engaged-view attribution:** Changed from 10s → 5s (2025)
- Action: Adjust ROAS assumptions and attribution models; recalibrate benchmarks

### Placements
- **Threads Feed** added as placement → test for incremental reach and scaling
- **Advantage+ placements** now strongly recommended (algorithm performs better)
- Note: Limited spend on excluded placements (~5% budget can still go there) — removing placements may not fully block them

### Audience & Targeting
- **Lookalike restrictions** on health/finance data (Sept 2025) → audiences may shrink
- **Value Rules** expanded to Leads objective → can fine-tune lead quality scoring
- **Sensitive data blocking**: Custom audiences with health/finance attributes blocked Sept 2025
- **Incremental attribution + value optimization** → new ROAS calculation method available

### AI & Creative Enhancements
- AI-generated text variations available in Ads Manager — READ BEFORE LAUNCHING, especially in health/finance (can violate compliance)
- AI image cropping, animation available
- AI chatbot personalization for ad delivery rolled out Dec 16, 2025 (ex: EU/UK/South Korea)
- Creative Fatigue and Similarity metrics now in dashboard

### Sensitive Category Restrictions (2025)
- **Health & Wellness (Jan 2025):** Add to Cart, Purchase events blocked for optimization; must use Landing Page Views or Engagement instead
- **Financial Services (Jan 14, 2025):** New mandatory "Financial Products and Services" Special Ad Category in US; regulatory authorization proof (SEC etc.) required
- **Healthcare/Finance (Sept 2025):** CAPI and server-side APIs unable to share restricted events
- **Political ads:** Stricter targeting; "Paid for by" disclaimer required
- **Housing, Employment, Credit:** Special ad category with restricted targeting (ongoing)

### CAPI & Measurement
- Pixel + Conversions API (CAPI) dual setup now essential for measurement accuracy
- CAPI fires only when user gives consent (GDPR compliance)
- Offline conversion upload critical for training algorithm on lead quality (especially for lead gen)
- AEM (Aggregated Event Measurement) for privacy-preserving measurement in restricted verticals

### Meta Ads Library API
**Competitor research endpoint:**
```
GET https://graph.facebook.com/v21.0/ads_archive
?access_token=YOUR_TOKEN
&ad_reached_countries=US
&search_terms=YOUR_COMPETITOR
&ad_type=ALL
&fields=id,ad_creation_time,ad_creative_body,ad_snapshot_url
```
- Free to use with a Meta developer account
- Returns: ad copy, creative preview, run dates, page name, country targeting
- Rate limits apply; paginate with `after` cursor

---

## Jon Loomer / Industry Expert Signals to Monitor
- Jon Loomer Digital: Campaign structure under Andromeda
- Social Media Examiner: Creative strategy updates
- Foxwell Digital: Policy and sensitive category compliance
- Vaizle / Five Nine Strategy: Performance data and case studies

---

## Recommended Action Matrix

| Metric Getting Worse | Likely Cause | Action |
|---|---|---|
| Rising CPMs | Creative similarity/fatigue | Add conceptually new creatives |
| Declining ROAS | Andromeda can't diversify | Consolidate ad sets, broaden audience |
| Learning phase restarts | Over-segmentation | Merge ad sets, reduce campaigns |
| Health/finance events blocked | Sensitive category flag | Switch to TOF events, use CAPI carefully |
| Custom audience shrinking | Lookalike restrictions, opt-outs | Build first-party data, CAPI uploads |
| Attribution gap | Engaged-view window change | Recalibrate to 5s window, use 1-day metrics |
