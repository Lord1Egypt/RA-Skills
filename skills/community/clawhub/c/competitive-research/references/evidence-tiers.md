# Evidence Tiers

Every factual claim in a competitive-intel report must carry one of these four confidence tiers.
The tier appears inline with the claim and in the Evidence Log.

---

## Tier Definitions

### HIGH
**Meaning:** Direct, primary source. Accessed today. Specific claim on a public page.
**When to use:** Pricing pulled directly from a pricing page. Feature listed on product page. Quote from official press release. Review text copied verbatim.
**Format:** `[HIGH]`
**Example:** `Four Sigmatic charges $55/month for their subscription plan [HIGH — foursigmatic.com/subscribe, accessed 2026-03-20]`

---

### MEDIUM
**Meaning:** Synthesized from multiple sources, no single definitive citation. Or: single source but indirect (e.g., an analyst summary, a comparison article, a user paraphrase rather than direct quote).
**When to use:** Pricing estimate from a third-party comparison page. Feature claim from a blog review rather than the product's own site. Market structure observation aggregated across several sources.
**Format:** `[MEDIUM]`
**Example:** `Onnit's primary customer appears to be male, 28–45, interested in biohacking [MEDIUM — synthesized from ad creative, About page, and G2 reviewer demographics]`

---

### LOW
**Meaning:** Inferred from indirect signals with limited corroboration. The inference is defensible but not directly sourced.
**When to use:** Estimating revenue from employee count + pricing. Estimating market position from SEO traffic proxies (SimilarWeb, Ahrefs estimates). Drawing conclusions from the absence of data.
**Format:** `[LOW]`
**Example:** `Thesis appears to be growing based on increased LinkedIn hiring activity and expanding SKU range [LOW — LinkedIn jobs page + product catalog, accessed 2026-03-20]`

---

### INFERRED
**Meaning:** Model reasoning from available evidence. No direct source. This is the analyst's judgment call, not an observed data point.
**When to use:** Opportunity mapping. Positioning gap identification. "What the customer really wants." Any section that says "this suggests" or "this implies."
**Format:** `[INFERRED]`
**Example:** `The gap in mid-priced ($30–$50) high-bioavailability formats suggests an opening for a brand that skips the premium positioning but maintains ingredient quality [INFERRED]`

---

## Usage Rules

1. **Every table row in the Evidence Log must have a tier.** No tier = not in the log = not in the report as fact.

2. **Do not upgrade LOW to MEDIUM to make a claim sound stronger.** Tier down if uncertain, never tier up.

3. **INFERRED is not bad.** The Opportunity Map section is entirely INFERRED. That is correct and expected. Label it, don't hide it.

4. **HIGH claims need a URL.** If you cannot provide a URL for a HIGH claim, downgrade to MEDIUM.

5. **Avoid mixing tiers within a single sentence.** If a claim is part-sourced and part-inferred, break it into two sentences with separate tiers.

6. **When a source is paywalled or login-gated, note it.** `[MEDIUM — behind login; claim from paraphrase in [source], accessed DATE]`

---

## Evidence Log Format

Use this table at the end of every report:

```markdown
## Evidence Log

| Claim | Source Name | URL | Date Accessed | Tier |
|-------|-------------|-----|---------------|------|
| Four Sigmatic charges $55/month subscription | Four Sigmatic pricing page | https://foursigmatic.com/subscribe | 2026-03-20 | HIGH |
| Onnit targets male biohackers | Synthesized — ad creative + G2 + About page | multiple | 2026-03-20 | MEDIUM |
| Thesis growing based on hiring activity | LinkedIn jobs + product catalog | multiple | 2026-03-20 | LOW |
```

Minimum rows: one per competitor profile + one per market structure claim.
Opportunity Map claims do not need Evidence Log rows — they are INFERRED by design and labeled in-text.
