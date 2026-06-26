---
name: competitive-positioning-research
version: 1.0.0
description: "Strategic competitive analysis skill for positioning research. Defines comparison dimensions, selects structural analogues, researches each comp, scores your approach 1-5, and produces ranked recommendations. Use before writing public-facing pages or when product positioning decisions are being made. Hard limit: 4 web searches per session."
metadata:
  {
    "openclaw": {
      "emoji": "🔭",
      "requires": {
        "bins": [],
        "env": []
      },
      "primaryEnv": null,
      "network": {
        "outbound": true,
        "reason": "Uses web_search to research competitor platforms and industry case studies on behalf of the user."
      },
      "security_notes": "Fetches publicly available content (competitor landing pages, case studies, industry articles) on behalf of the user. No private data is transmitted. Web searches are limited to 4 per research session."
    }
  }
---

# Skill: Competitive Positioning Research
_Owner: Archie | Maintained by: Sara_

---

## When to Use This Skill

**Triggers:**
- "How does our X compare to how [category] leaders do it?"
- "Research how successful [category] platforms handle [specific problem]"
- "What can we learn from [Platform A / Platform B] for our [page/feature/approach]?"
- Pre-ship review Phase 3 (strategic positioning check)
- Before writing any public-facing page that has direct category comps

**Not for:**
- Technical claim accuracy — that's the **technical accuracy review** pattern (fee amounts, hash functions, protocol specs)
- Deep product research — that's a **full Archie research brief**
- Pricing analysis — that's **Becky**

This skill is for *strategic/UX research* — "how did the best examples in this space solve this specific problem, and how do we stack up?" Not "is this claim correct?"

---

## The Research Pattern

### Step 1: Define the comparison dimensions

Before searching, lock down:
- **What specific problem** are we researching? (e.g. "two-sided marketplace landing page hero CTA — which side to prioritise?")
- **What category** are the comps in? (e.g. "developer-facing two-sided marketplace")
- **3–5 dimensions** to score on (e.g. side prioritisation, cold-start handling, social proof, trust signals)
- **Target output:** scored table + ranked recommendations

Don't start searching until you've written these down. Undefined scope = research sprawl.

### Step 2: Select comps

Pick **4–6 platforms**. More is noise. Selection criteria:
- Same audience type (developer, consumer, enterprise)
- Same structural problem (two-sided, subscription, usage-based)
- Mix of early-stage (how they launched) and mature (how they evolved)
- **Prioritise structural analogues over direct competitors** — defensive bias corrupts the analysis

### Step 3: Research each comp

For each platform, find:
- How they handled the *specific problem* (not general company history)
- What they prioritised early vs. mature stage
- What worked and what they changed
- One key lesson that applies to your situation

**Search patterns that work:**
- `"[platform] landing page teardown"`
- `"[platform] early growth strategy"`
- `"[platform] cold start problem"`
- `"two-sided marketplace [specific problem] best practices"`
- `"[platform] how they solved [problem]"`

**Model knowledge vs. web search:** For well-known platforms (Airbnb, Stripe, Uber, Replicate), Archie has sufficient model knowledge for structural patterns. Use web search for specifics — a changed CTA, a pivot, a dated case study.

### Step 4: Score our approach

Build a scoring table against the dimensions from Step 1. Score each **1–5** with a brief, honest note.

A 2/5 with a real explanation is more useful than a 4/5 that flatters the team. Score what exists, not what was intended.

### Step 5: Produce recommendations

Ranked by **impact**, not effort. For each recommendation:
- What to change
- Why (which comp's evidence supports it)
- Approximate effort: one-line fix / section rewrite / new feature

---

## Output Format

```markdown
# [Topic] — Competitive Positioning Research
_Date: YYYY-MM-DD | Analyst: Archie_

## Executive Summary
[3–4 sentences: headline finding + top recommendation]

## Comparison Dimensions
[The 3–5 dimensions being scored, and why they matter]

## Case Studies

### [Platform]
- **What they did:** ...
- **When (early vs mature):** ...
- **Key lesson:** ...

## Scoring Table

| Dimension | Score (1-5) | Notes |
|---|---|---|

## Recommendations (ranked by impact)
1. **[Change]** — [why, which comp supports it] — [effort]

## What We Got Right
[Strengths to preserve]
```

---

## Time Budget and Scope

| Type | Comps | Time |
|---|---|---|
| Quick (known category) | 2–4 | 8–10 min |
| Full (novel category) | 5–6 | 15–20 min |

**Hard limit: 4 web searches.** Synthesise from what you find. If you haven't found enough after 4 searches, scope was too broad — narrow the question, not the search count.

---

## Worked Example

**Date:** 2026-03-24  
**Product:** Reddi Agent Protocol (two-sided agent marketplace)  
**Problem:** Two-sided landing page hero CTA — which side to prioritise?  
**File:** `projects/reddi-agent-protocol/reviews/archie-marketplace-research-2026-03-24.md`

**Comps studied:** Stripe, Uber, Airbnb, Hugging Face, Replicate (5 — right call, stopped before noise)

**Dimensions scored:** Side prioritisation, supply-side hook, demand-side hook, chicken-and-egg acknowledgement, social proof, trust signals

**Headline finding:** Seller-first hero is defensible at pre-supply stage, but the page is missing three things: cold-start acknowledgement, zero-friction demo, and any social proof. The "Browse Agents" CTA risks leading to a near-empty index — an active anti-signal.

**Top recommendation:** Add a dual-path hero split so both sides feel directly spoken to without diluting the primary message.

**Surprise:** Replicate — the closest structural analogue — led with *consumers* from day one, and made a live runnable demo the primary conversion mechanism on the landing page. Not a "coming soon" but an actual working model you could run from the hero. That's the bar for our live demo CTA.

**Score that stung:** Chicken-and-egg handling got 1/5. The page doesn't acknowledge it's early-stage, and "why join a marketplace with no one in it yet?" has no answer anywhere on the page. Honest score, actionable gap.

---

## Common Mistakes

**Too many comps.** Six becomes noise. Pick four or five strong structural analogues, research them properly, and stop.

**Comparing to direct competitors.** Direct comp analysis introduces defensive bias. Structural analogues (same problem, different space) produce better lessons. Airbnb teaches more about marketplace cold starts than any other agent marketplace would.

**Generous scoring.** A scoring table where everything is 3–4/5 is useless. The purpose of the table is to surface gaps. If nothing scores below 3, you're flattering the work, not analysing it.

**Searching too broadly.** `two-sided marketplace` returns 10 years of generic content. `Replicate model provider growth strategy` returns the specific insight you need. Start specific, widen only if necessary.

**Grepping the full repo.** Archie times out on `grep -r` across a full project directory. Always read targeted files by path. Never use recursive search on a large workspace.

---

_This skill was written 2026-03-24 by Sara, based on Archie's marketplace research for Reddi Agent Protocol._
