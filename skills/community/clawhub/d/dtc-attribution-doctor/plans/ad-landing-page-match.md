# Plan: Ad–Landing Page Match (ad-landing-page-match)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: 广告落地页匹配诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`, `#7 web_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `landing-page-reception`, `site-funnel-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: diagnose message / audience-to-landing-page match by joining ad-side signals (CTR, click intent) from `#4 ad_analysis_list` with on-site signals (landing-page CVR, engagement) from `#7 web_analysis_list`, keyed by campaign / landing page. Detect mismatch where strong CTR meets weak landing-page CVR — i.e., the ad earns the click but the page or offer fails to convert it (wrong page / wrong offer).
- **solution space**: a per-campaign match verdict (aligned / message-mismatch / wrong page) + the matching specialist plan to chain. Recommendations only; human-executed.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "good clicks but no conversions", "is the landing page matching the ad", "ad-to-page mismatch", "are we sending clicks to the right page".
- **Boundary**: this plan localizes the ad-to-page mismatch; it does NOT redesign the landing experience or diagnose the full on-site funnel — it hands off to `landing-page-reception` / `site-funnel-diagnosis`.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope — which campaigns / landing pages?** (if named, scope to it; else top-spend campaigns)
  3. **Join key — campaign-to-page mapping known?** (confirm how ads map to landing pages so the join is valid)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` on either side → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). The join requires a usable ad→landing-page mapping.
- **caliber**: ad-side CVR/intent from true `conversions`; landing-page CVR/engagement from `#7` on-site fields. Both periods equal length, same `model`/`goal`; `ad_net_roas` reference only.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (campaign) | `{start_date,end_date,dimensions:"campaign",model,goal}` | ad-side CTR / clicks / cvr / intent per campaign |
| b | `#7 web_analysis_list` (landing page) | `{start_date,end_date}` | on-site landing-page CVR / engagement: unique_users, product_view_users, atc_users, purchases, purchases_rate, engagement_rate |
| c | join a × b by campaign / landing_page | — | align ad intent against landing-page reception to find mismatch |

- **caliber reminders**: see §1 of functions.md; key here — `#4` (ad caliber) and `#7` (on-site caliber) are different sources joined by mapping, not summed; ad-side conversion uses true `conversions`.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (ad-side) and b (on-site); build the join by campaign / landing page.
2. **Analyze — read the match**:
   - high CTR + healthy landing-page CVR/engagement ⇒ aligned.
   - high CTR + weak landing-page CVR / low engagement ⇒ mismatch: the ad promises something the page does not deliver (wrong page or wrong offer).
   - low CTR ⇒ this is a creative/relevance issue, not an LP-match issue — note and route elsewhere.
3. **Compare**: per campaign, ad-side CTR/intent vs on-site CVR/engagement, current vs prior; tag aligned / mismatch.
4. **Conclude**: name mismatched campaign→page pairs with evidence (e.g., "Campaign A CTR top-quartile but its LP CVR is bottom-quartile and engagement is low — wrong offer page").
5. **Next**: chain per §7.

**Match symptom table:**

| Ad side | On-site side | Diagnosis | Next plan |
|---------|--------------|-----------|-----------|
| CTR high | LP CVR healthy | aligned | — |
| CTR high | LP CVR weak, engagement low | message / offer mismatch (wrong page) | `landing-page-reception` |
| CTR high | LP CVR weak, funnel leaks deeper | on-site funnel issue | `site-funnel-diagnosis` |
| CTR low | n/a | creative/relevance, not LP match | route to creative plans |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Ad–Landing Page Match — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <campaigns / pages>

## Match findings
| Campaign → LP | CTR (ad) | LP CVR / engagement | Verdict |
|---------------|----------|---------------------|---------|

## Mismatch detail
<which pairs mismatch and why; evidence>

## Next Step
<chained plan; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per campaign→LP CTR / clicks (ad) and CVR / engagement_rate / purchases_rate (on-site) — current/prior/Δ%.
- diagnosis block: aligned vs mismatch pairs with evidence.
- recommendation block: chained plan per mismatch; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: message/offer mismatch → `landing-page-reception`; deeper funnel leak → `site-funnel-diagnosis`. Low CTR is a creative issue, not LP-match — route to creative plans.

**Data notes:**
- `#4` and `#7` are different calibers joined by mapping — never add them together.
- Equal-length windows, same model on the ad side; same on-site window on the web side.
- A weak page reading at low traffic is noisy — require enough sessions before calling mismatch.
- Empty `records` on either side ≠ 0 — handle per §3; if the join key is missing, say so rather than guessing the mapping.
