# Plan: Ad Quality Score (ad-quality-score)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Creative Intelligence Suite
- **functions.md scenario (mapping key)**: 广告质量分诊断
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#9 google_query` GAQL; context `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `landing-page-reception`, `creative-performance`, `search-term-performance`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: diagnose Google **Quality Score** and its three components — **expected CTR**, **ad relevance**, **landing-page experience** — via `#9 google_query` (GAQL) for search channels. Trace low QS to its downstream cost: higher CPC and lower impression share. Localize the weak component and tie low QS to a landing-page-experience or creative-relevance root cause, internalizing the search channel by user prompt.
- **solution space**: a per-keyword/ad QS verdict naming the weak component and its cost impact, with a routed fix — as recommendations only, pending human execution.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "why is my Quality Score low", "our CPCs are high on search", "low impression share on Google", "ad relevance / landing page experience issues".
- **Boundary**: this plan diagnoses Quality Score components and their CPC / impression-share impact; it does NOT do query-level negative-keyword work (→ `search-term-performance`) and does NOT execute landing-page or creative fixes. Quality Score is a Google search-channel concept — it is not assumed available for Meta.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Search channel?** (Google search — internalized per prompt; if unspecified, default Google and state so)
  2. **Period & granularity?** (default = last full week vs prior equal week; keyword or ad-group level)
  3. **Scope?** (whole search account, or a named campaign / ad group showing high CPC or low impression share)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate. Also empty if the channel is non-search (no Quality Score).
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`); `account_id` for the Google platform (via `#2 connection_source`) before any `#9` GAQL call.
- **caliber**: QS components and impression share are platform-native (`#9`); efficiency consequences reconcile to **true `roas`** from `#4`, never `ad_net_roas`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#9 google_query` (GAQL) | `SELECT ad_group_criterion.quality_info.quality_score, ...creative_quality_score, ...post_click_quality_score, ...search_predicted_ctr, metrics.average_cpc, metrics.search_impression_share WHERE segments.date BETWEEN ...` | QS + three components + CPC + impression share per keyword/ad group |
| b | `#4 ad_analysis_list` (search channel) | `{start_date,end_date,dimensions:"campaign",channel,model,goal}` | tie QS-driven cost to campaign true `roas` (vs `ad_net_roas`) |
| c | `#9 google_query` (prior, optional) | same GAQL, prior equal window | trend QS / CPC / impression-share movement |

- **caliber reminders**: see §1 and §6 of functions.md; key here — `#9` is platform-native QS structure, **not summed** into Convbox roas; take minimal GAQL fields (rate limits stricter); efficiency consequence reconciles to true `roas`, never `ad_net_roas`.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (QS + components + CPC + impression share); fetch b to anchor roas; fetch c for trend if asked.
2. **Analyze — decompose Quality Score** per keyword/ad group:
   - identify the **weak component**: expected CTR (`search_predicted_ctr`), ad relevance (`creative_quality_score`), or landing-page experience (`post_click_quality_score`).
   - quantify the cost: low QS → higher `average_cpc` and lower `search_impression_share`.
   - map component → root cause: weak ad relevance → creative/keyword mismatch; weak landing-page experience → LP issue; weak expected CTR → copy/positioning.
3. **Compare**: rank low-QS keywords by spend/impression-share loss; Δ vs prior if c fetched; tag 🟡/🔴.
4. **Conclude**: name the dominant weak component, its CPC / impression-share cost, and the implied root cause — reconciled to campaign true `roas`.
5. **Next**: route per the component table (§7).

**QS root-cause map (weak component → root cause → next):**

| Weak component | Root cause | Next plan |
|----------------|-----------|-----------|
| Landing-page experience (`post_click_quality_score`) | slow / mismatched / weak LP | `landing-page-reception` |
| Ad relevance (`creative_quality_score`) | creative–keyword mismatch | `creative-performance` |
| Expected CTR (`search_predicted_ctr`) | weak copy / wrong query intent | `search-term-performance` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Ad Quality Score — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Search channel:** <Google>　**Model:** <model>

## Verdict
<N> low-QS keywords driving <$X> CPC inflation / <Y%> impression-share loss. Dominant weak component: <component>.

## QS Breakdown
| Keyword / ad group | QS | Exp. CTR | Ad relevance | LP experience | Avg CPC | Impr. share |
|--------------------|----|----------|--------------|---------------|---------|-------------|

## Next Step
<weak component → routed fix; which plan to chain — "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: QS + three components, average CPC, search impression share — current/prior/Δ%/status.
- diagnosis block: dominant weak component + CPC / impression-share cost + implied root cause; reconciled to true `roas`.
- recommendation block: routed fix per weak component; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining:** see the QS root-cause map (§5) — each weak component routes to its next plan (`landing-page-reception`, `creative-performance`, `search-term-performance`).

**Data notes:**
- Quality Score and its components come via `#9 google_query` (GAQL) and exist only for Google search — do NOT assume Meta has them.
- Channel is internalized by user prompt — no per-platform plan variants; mention which channel was read.
- Platform-native `#9` figures are not summed into Convbox roas; CPC / impression-share cost reconciles to true `roas` from `#4`, never `ad_net_roas`.
- Equal-length windows, same model/goal for any QS trend.
- Empty `records` ≠ 0 (no data, non-search channel, or tier not open) — handle per §3; never fabricate.
