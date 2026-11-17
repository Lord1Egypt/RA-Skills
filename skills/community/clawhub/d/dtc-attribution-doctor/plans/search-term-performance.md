# Plan: Search Term Performance (search-term-performance)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Creative Intelligence Suite
- **functions.md scenario (mapping key)**: 搜索词表现分析
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#9 google_query` GAQL; context `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `ad-quality-score`, `attribution-brand-nonbrand`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: analyze actual search queries via `#9 google_query` (GAQL) for search channels — separate **converting** terms from **wasted** spend, split **brand vs non-brand**, and surface **negative-keyword candidates** that drain budget with no return. Anchor query-level efficiency against the campaign's true `roas` from `#4`, and internalize the search channel (Google / Microsoft) by user prompt rather than building a plan per platform.
- **solution space**: a search-term verdict — converting terms to protect, wasted terms to add as negatives, brand/non-brand spend split — as recommendations only, pending human execution.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "which search terms are wasting budget", "show me converting vs non-converting queries", "what negatives should I add", "brand vs non-brand search spend".
- **Boundary**: this plan analyzes search *queries* and recommends negatives / brand-split reads; it does NOT diagnose ad Quality Score components (→ `ad-quality-score`) and does NOT execute keyword or negative-list changes. Search-term data is a Google/Microsoft search-channel capability — it is not assumed available for Meta.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Search channel?** (Google / Microsoft; internalized per prompt — if unspecified, default Google and state so)
  2. **Period & comparison?** (default = last full week vs prior equal week)
  3. **Brand term definition?** (brand strings to classify brand vs non-brand; if unknown, infer from shop name and flag the assumption)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate. Also empty if the channel is non-search (no search-term report).
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`); `account_id` for the search platform (via `#2 connection_source`) before any `#9` GAQL call.
- **caliber**: query-level GAQL is platform-native (`#9`) — used for term-level structure; campaign-level efficiency reconciles to **true `roas`** from `#4`, never to `ad_net_roas`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#9 google_query` (GAQL) | `SELECT search_term_view.search_term, metrics.cost, metrics.clicks, metrics.conversions, metrics.conversions_value WHERE segments.date BETWEEN ...` | per-query cost / clicks / conversions / value for the search channel |
| b | `#4 ad_analysis_list` (search channel) | `{start_date,end_date,dimensions:"campaign",channel,model,goal}` | reconcile query economics to campaign true `roas` (vs `ad_net_roas`) |
| c | `#9 google_query` (prior, optional) | same GAQL, prior equal window | trend converting vs wasted terms over time |

- **caliber reminders**: see §1 and §6 of functions.md; key here — platform passthrough (`#9`) is for term-level structure and is **not summed** into Convbox roas; classify brand vs non-brand on agreed brand strings; take minimal GAQL fields (search-channel rate limits are stricter).

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (per-query GAQL); fetch b to anchor true `roas`; fetch c for trend if asked.
2. **Analyze — classify every query**:
   - **converting** (conversions > 0, acceptable cost/conv) vs **wasted** (spend, no/low conversions).
   - **brand vs non-brand** on the agreed brand strings — brand terms often over-credited; read non-brand as the true acquisition signal.
   - **negative-keyword candidates**: high-cost, zero-conversion, intent-mismatched queries.
3. **Compare**: rank terms by cost; for converting vs wasted, compute spend-share each; brand vs non-brand spend and conversion split; trend vs prior if c fetched.
4. **Conclude**: name the wasted-spend total and top negative candidates, the brand/non-brand split, and the converting terms to protect — reconciled to campaign true `roas`.
5. **Next**: route per the chaining table (§7).

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Search Term Performance — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Search channel:** <Google / Microsoft>　**Model:** <model>

## Verdict
Wasted spend <$X> across <N> terms. Top negatives: <list>. Brand/non-brand spend split <B% / NB%>; non-brand roas <X.XX>.

## Term Breakdown
| Search term | Cost | Clicks | Conv | Conv value | Class | Brand? |
|-------------|------|--------|------|------------|-------|--------|
(converting / wasted; brand / non-brand)

## Next Step
<negatives to add; brand-split follow-up; which plan to chain — "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: converting vs wasted spend-share, brand vs non-brand spend/conv split, wasted-spend total; reconciled to campaign true `roas`.
- diagnosis block: negative-keyword candidates + brand cannibalization read + evidence.
- recommendation block: negatives to add, terms to protect; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining:**
- low-relevance / wasted terms tied to ad relevance → `ad-quality-score`.
- brand vs non-brand attribution depth → `attribution-brand-nonbrand`.

**Data notes:**
- Search-term and query data come via `#9 google_query` (GAQL) and exist only for search channels (Google / Microsoft) — do NOT assume Meta has them.
- Channel is internalized by user prompt — no per-platform plan variants; mention which channel was read.
- Platform-native `#9` figures are not summed into Convbox roas; campaign efficiency reconciles to true `roas` from `#4`, never `ad_net_roas`.
- Brand vs non-brand depends on the agreed brand strings; if inferred, flag the assumption.
- Equal-length windows, same model/goal for any trend.
- Empty `records` ≠ 0 (no data, non-search channel, or tier not open) — handle per §3; never fabricate.
