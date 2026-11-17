# functions.md — Convbox-DiagClaw Self-Serve Analytics · Data Operations & Scenario Catalog

## Metadata

- **version**: 1.1.0
- **Related files**:
  - [`access.yaml`](access.yaml) — API field definitions and samples (this file's "Data Interfaces" section is tightly bound to it)
  - [`SKILL.md`](SKILL.md) — Default entry point and capability scope
  - `plans/{plan}.md` — Per-atomic-scenario analysis blueprints (routed by scenario from SKILL.md)
  - `utilities/` — On-the-fly synthesis tools (e.g. web page / chart generation)
- **Role**: This file is the "data-access layer + scenario-permission table." `access.yaml` answers "how to call the interface and what the fields are"; this file answers "**which interface for which scenario, how to read the key metrics, and which scenarios are open to whom**."
- **Credentials**: All data fetches carry `CONVBOX_API_KEY` via the `ApiKey` header (read from an environment variable, **never written into any file in the package**).
- **Business preconditions**: The user has registered and configured the Convbox product and generated an API Key; Convbox already holds a complete data map and exposes **pre-aggregated** data through the 9 interfaces below. This Skill consumes aggregated results only — it performs no detail-level ETL.

---

## 1. Data Interfaces — which API for which scenario

| # | Interface id | Primary use | Key metrics / fields |
|---|---------|---------|----------------|
| 1 | `setting_goals` | Before analysis, confirm the conversion goals available for the shop to avoid choosing the wrong `goal` caliber | goals[].code |
| 2 | `connection_source` | Get the ad platform `account_id` (prerequisite for meta/google pass-through) | account_id, platform_type |
| 3 | `connection_destination` | Tracking governance: determine whether server-side / CAPI events are enabled | server_config.*, browser_config.*, configuration.code |
| 4 | `ad_analysis_list` | Paid-ad drilldown by channel→campaign→ad_set→ad | **roas (true) vs ad_net_roas (platform)**, conversions, new_lead_conversions, cpa/cpc/cpm/ctr/cvr (decimals), profit/margin (decimals) |
| 5 | `all_attribution_list` | All-channel (including organic) attribution detail, channel/campaign comparison | roas, ad_net_roas, profit, margin (decimal), new_lead_conversions |
| 6 | `all_attribution_sum` | Whole-window summary with the same parameters as #5 (read the summary before the detail) | same caliber as #5, at the aggregate level |
| 7 | `web_analysis_list` | On-site conversion funnel (home→product page→add-to-cart→purchase) | unique_users, product_view_users, atc_users, purchases, purchases_rate, engagement_rate |
| 8 | `meta_query` | Meta platform native-caliber pass-through (for discrepancy comparison) | platform-native fields (spend, etc.) |
| 9 | `google_query` | Google platform native-caliber pass-through (GAQL, for discrepancy comparison) | GAQL SELECT fields |

### Data-caliber notes (must follow)

1. **Do not mix the two ROAS calibers**: `roas` = Convbox first-party true attribution; `ad_net_roas` = self-reported by the ad platform. The platform systematically overstates due to view-through / brand-keyword cannibalization / returning customers being counted, so **budget and scaling decisions trust `roas` only**; `ad_net_roas` is for comparison to reveal the magnitude of overstatement (`ad_net_roas − roas`).
2. **Keep the attribution model consistent**: `model` (First click / Last click / Linear / Time decay / Data driven) changes attribution results; any comparison/trend must use the **same model**, default `First click`.
3. **`conversions` semantics**: `conversions` = primary conversions per the selected `goal`. Note the response field is `conversions` but to **sort** by it you must pass `sort_by=main_conversions` (see note 12). `new_lead_conversions` = new-customer conversions (0 when not instrumented). The new-customer caliber is central to judging "real incrementality vs cannibalization."
4. **Profit depends on cost configuration**: `profit / margin` require the shop to have COGS/shipping/fee rates configured in Convbox; if unconfigured, these fields may be empty — profit-type scenarios must first confirm costs are configured, otherwise degrade to a non-profit version and state so. all-attribution uses `profit/margin`, and `margin` is a **decimal** (0.27 = 27%).
5. **`dimensions` takes a single-value string**: all list interfaces' `dimensions` must be passed as a single-value string (e.g. `"channel"`). ad-analysis rejects any array with `code:400`; web-analysis tolerates a 1-element array but rejects multi-element arrays with `code:400` (older builds may instead collapse into a single erroneous `total:1` row). Also note `all_attribution_list`/`all_attribution_sum` live at `/api/all-attribution/...` — without the `/api/` prefix the gateway returns a bare `{code:404}`. `source/medium/landing_page` are empty when not instrumented.
6. **Unit calibers**: `margin` and `cvr` are returned as **decimals** (multiply by 100); `ctr`'s caliber is inconsistent with `cvr` (apparently already a percentage), confirm field by field before use.
7. **Pass-through result keys differ**: `meta_query` results are in `data.data` (not `records`, with `paging.cursors`); `google_query` results are in `data.results` (nested camelCase, `metrics.costMicros÷1e6` gives USD).
8. **Judge success by code**: successful responses are actually HTTP **201** with `message` = `Service succeed`; always judge by `code===1`, not by HTTP 200 or hard-matching the message.
9. **Pair detail with summary**: `all_attribution_list` (#5) and `all_attribution_sum` (#6) must be called paired with the **same parameters** — anchor the whole with the summary first, then drill into the detail.
10. **Pass-through is for comparison only**: `meta_query`/`google_query` return platform-native calibers and **must not be added directly to Convbox attribution calibers**; use only for "platform data vs on-site attribution discrepancy" diagnosis; their platform-side rate limits are stricter, so fetch the fewest fields needed.
11. **Empty data ≠ 0**: empty `records` may mean no data in the range, **or that the scenario is not open to the current subscription tier** (see section 2) — in no case should you **fabricate conclusions from empty data**; state it truthfully.
12. **`sort_by` uses a narrow whitelist — off-list fields silently return empty**: verified-sortable fields are `spend`, `main_conversions`, `cpa`, `ctr` (and on web-analysis, omit `sort_by`). Passing any other field — `conversions`, `conversion_value`, `profit`, `roas`, `ad_net_roas`, `margin`, `impressions`, `clicks` (and web-analysis `purchases`/`unique_users`) — makes the interface return `total:0` / empty `records` with **no error code**. These metrics still exist in every row; you just cannot sort by them server-side. To rank by such a metric: fetch with a whitelisted `sort_by` (or omit it) and a `page_size` large enough to capture all rows, then rank **in-kernel**.

---

## 2. Analysis Scenario Matrix (atomic scenario × role attention × call permission)

> **This is the most critical control information in this Skill.** It defines which atomic analyses exist, which roles they matter to, which subscription tier they require, and whether they are ready now.
>
> **Permission semantics (hard constraint)**: the `Tier` column is the Convbox subscription tier the scenario requires. If a scenario is marked at a higher tier (e.g. **Enterprise**) and the account behind the current API Key is below that tier, calling the relevant interfaces will **read empty data**; in that case you must clearly tell the user "this capability requires the corresponding tier" and **must not bypass the limit or run an invalid analysis on empty data**. The entire matrix is currently "Basic."
>
> **Role attention** (Must / Optional / —) is for **tailoring report focus by role**; it is a soft priority, not a hard permission. Hard permission is determined by `Tier` only.
>
> **Development status** (4 states):
> - `Planned` = planned, `plan` not yet provided; when requested, explain "this analysis is planned and not yet available."
> - `In-dev` = `plan` is being written and is nearly ready; not yet able to provide stable results externally.
> - `Live` = `plan` is ready and externally available; can be routed and executed normally.
> - `Deprecated` = retired or replaced; should no longer be routed; when requested, explain "this analysis has been retired" (and point to any replacement scenario).

**Role abbreviations**: F=Founder, MD=Marketing Director, CRM=CRM, SO=Site Ops, CS=Creative Strategist, MB=Media Buyer.

**Legend** — Role values: Must=必看, Optional=选读, —=不关注. Status: Planned=计划中, In-dev=开发中, Live=已上线, Deprecated=已弃用. (The "中文场景 (key)" column is the byte-for-byte join key to the CSV and to each plan's `functions.md scenario (mapping key)`.)

### Suite → Primary Data Interfaces (quick reference)

| Analysis suite | Primary interfaces |
|---------|---------|
| Growth Command Center | #6 #5 #4 |
| Performance Marketing Copilot | #4 #8 #9 |
| Creative Intelligence Suite | #4 #8 #9 |
| Site Conversion Diagnostic Suite | #7 |
| Retention & Lifecycle Engine | #5 #7 #3 |
| Campaign Review & Promotion Quality Suite | #5 #6 #4 |
| Attribution & Budget Allocation Suite | #5 #6 #4 |
| Profit Protection Dashboard | #5 #6 #4 |
| Market Expansion Diagnostic Suite | #5 #7 |
| Data Quality & Tracking Governance | #3 #2 #8 #9 |

### Growth Command Center

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| Growth health diagnostic | 增长健康度诊断 | Basic | Must | Must | Optional | Optional | — | Optional | In-dev |
| Channel-mix health diagnostic | 渠道组合健康度诊断 | Basic | Must | Must | Optional | — | — | Must | Planned |
| Budget expansion judgment | 预算扩张判断 | Basic | Must | Must | — | — | — | Must | In-dev |
| New-customer growth contribution | 新客增长贡献分析 | Basic | Must | Must | Must | Optional | — | Optional | Planned |
| MER / Blended ROAS monitoring | MER / Blended ROAS 监控 | Basic | Must | Must | Optional | — | — | Must | Planned |
| Growth anomaly prioritization | 增长异常优先级判断 | Basic | Must | Must | Optional | Optional | Optional | Must | Planned |
| Budget pacing / overspend alert | 预算 Pacing / 超支预警 | Basic | Must | Must | — | — | — | Must | In-dev |

### Performance Marketing Copilot

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| ROAS decline diagnostic | ROAS 下降诊断 | Basic | Optional | Must | Optional | Optional | Optional | Must | In-dev |
| CPA rise diagnostic | CPA 上升诊断 | Basic | Optional | Must | — | Optional | Optional | Must | In-dev |
| Campaign anomaly alert | Campaign 异常预警 | Basic | — | Must | — | Optional | — | Must | In-dev |
| Ad-spend scaling judgment | 投放扩量判断 | Basic | Optional | Must | — | — | — | Must | In-dev |
| CPC / CTR / CVR breakdown diagnostic | CPC / CTR / CVR 拆解诊断 | Basic | — | Must | — | Optional | Optional | Must | In-dev |
| Ad audience performance diagnostic | 广告受众表现诊断 | Basic | — | Must | Optional | — | Optional | Must | In-dev |
| Ad landing-page match diagnostic | 广告落地页匹配诊断 | Basic | — | Must | — | Must | Must | Must | In-dev |
| Bid-strategy optimization (tCPA / tROAS target derivation) | 出价策略优化（tCPA / tROAS 目标推导） | Basic | Optional | Must | — | — | — | Must | In-dev |

### Creative Intelligence Suite

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| Creative performance diagnostic | 素材表现诊断 | Basic | Optional | Must | Optional | — | Must | Must | In-dev |
| Creative fatigue diagnostic | 素材疲劳诊断 | Basic | — | Optional | — | — | Must | Must | In-dev |
| Hook performance analysis | Hook 表现分析 | Basic | — | Optional | — | — | Must | Must | Planned |
| Selling-point effectiveness analysis | 卖点有效性分析 | Basic | Optional | Must | Optional | Optional | Must | Optional | Planned |
| UGC / KOL content reuse value analysis | UGC / KOL 内容复用价值分析 | Basic | Optional | Must | Optional | — | Must | Optional | Planned |
| Content–landing-page consistency diagnostic | 内容-落地页一致性诊断 | Basic | — | Must | — | Must | Must | Must | Planned |
| Next-round creative brief generation | 下一轮素材 Brief 生成 | Basic | — | Optional | — | — | Must | Must | Planned |
| Search-term performance analysis | 搜索词表现分析 | Basic | — | Must | — | — | Optional | Must | In-dev |
| Ad quality-score diagnostic | 广告质量分诊断 | Basic | — | Must | — | Optional | Optional | Must | In-dev |

### Site Conversion Diagnostic Suite

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| On-site conversion funnel diagnostic | 站内转化漏斗诊断 | Basic | Optional | Must | Optional | Must | Optional | Optional | In-dev |
| Landing-page reception diagnostic | 落地页承接诊断 | Basic | Optional | Must | — | Must | Must | Must | In-dev |
| Product-page conversion diagnostic | 商品页转化诊断 | Basic | Optional | Optional | — | Must | Optional | Optional | Planned |
| Add-to-cart rate anomaly diagnostic | 加购率异常诊断 | Basic | — | Must | Optional | Must | Optional | Optional | In-dev |
| Checkout / payment anomaly alert | 结账 / 支付异常预警 | Basic | Optional | Must | — | Must | — | Optional | Planned |
| Shipping / tax / discount-code leakage diagnostic | 运费 / 税费 / 折扣码流失诊断 | Basic | Optional | Must | Optional | Must | — | Optional | Planned |
| Device-side conversion diagnostic | 设备端转化诊断 | Basic | — | Optional | — | Must | Optional | Optional | Planned |
| Page-speed / mobile-experience diagnostic | 页面速度 / 移动端体验诊断 | Basic | — | Optional | — | Must | Optional | Optional | Planned |

### Retention & Lifecycle Engine

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| User segmentation identification | 用户分群识别 | Basic | Optional | Must | Must | Optional | Optional | Optional | Planned |
| High-intent non-purchaser identification | 高意向未购买用户识别 | Basic | — | Must | Must | Must | Optional | Must | Planned |
| Cart-abandonment recall diagnostic | 弃购召回诊断 | Basic | Optional | Must | Must | Optional | — | Optional | Planned |
| Browse Abandonment diagnostic | Browse Abandonment 诊断 | Basic | — | Optional | Must | Optional | Optional | Optional | Planned |
| Checkout Abandonment diagnostic | Checkout Abandonment 诊断 | Basic | Optional | Must | Must | Must | — | Optional | Planned |
| Second-purchase activation diagnostic | 二购激活诊断 | Basic | Must | Must | Must | — | Optional | — | Planned |
| Winback churn-recall diagnostic | Winback 流失召回诊断 | Basic | Optional | Must | Must | — | Optional | — | Planned |
| EDM / SMS Flow health diagnostic | EDM / SMS Flow 健康度诊断 | Basic | Optional | Must | Must | — | Optional | — | Planned |
| User LTV / Cohort analysis | 用户 LTV / Cohort 分析 | Basic | Must | Must | Must | Optional | — | Optional | Planned |

### Campaign Review & Promotion Quality Suite

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| Campaign retrospective diagnostic | 活动复盘诊断 | Basic | Must | Must | Must | Must | Must | Must | Planned |
| Campaign new-customer contribution | 活动新客贡献分析 | Basic | Must | Must | Must | Optional | Optional | Optional | Planned |
| Campaign returning-customer contribution | 活动老客贡献分析 | Basic | Must | Must | Must | Optional | Optional | — | Planned |
| Promotion quality diagnostic | 促销质量诊断 | Basic | Must | Must | Must | Optional | Optional | Optional | Planned |
| Discount dependency diagnostic | 折扣依赖诊断 | Basic | Must | Must | Must | Optional | Optional | — | Planned |
| Post-campaign repurchase tracking | 活动后复购追踪 | Basic | Must | Must | Must | — | Optional | — | Planned |
| Campaign creative / channel performance review | 活动素材 / 渠道表现复盘 | Basic | Optional | Must | Optional | Optional | Must | Must | Planned |

### Attribution & Budget Allocation Suite

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| Channel budget allocation | 渠道预算分配 | Basic | Must | Must | Optional | — | — | Must | In-dev |
| Channel role identification | 渠道角色识别 | Basic | Must | Must | Optional | — | — | Must | Planned |
| Attribution conflict diagnostic | 归因冲突诊断 | Basic | Must | Must | Optional | — | — | Must | In-dev |
| First Click / Last Click comparison | First Click / Last Click 对比 | Basic | Optional | Must | Optional | — | — | Must | Planned |
| Brand / non-brand keyword contribution breakdown | 品牌词 / 非品牌词贡献拆解 | Basic | Optional | Must | — | — | — | Must | Planned |
| Remarketing true-incrementality judgment | 再营销真实增量判断 | Basic | Must | Must | Must | — | — | Must | In-dev |
| Marginal ROAS / marginal CAC diagnostic | 边际 ROAS / 边际 CAC 诊断 | Basic | Must | Must | Optional | — | — | Must | Planned |

### Profit Protection Dashboard

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| Profit attribution diagnostic | 利润归因诊断 | Basic | Must | Must | Optional | Optional | — | Optional | In-dev |
| Channel profit-quality analysis | 渠道利润质量分析 | Basic | Must | Must | Optional | — | — | Must | In-dev |
| Campaign profit retrospective | 活动利润复盘 | Basic | Must | Must | Optional | Optional | Optional | Optional | Planned |
| Discount cost diagnostic | 折扣成本诊断 | Basic | Must | Must | Must | Optional | Optional | — | Planned |
| Refund / return impact on marketing quality | 退款 / 退货对营销质量影响 | Basic | Must | Optional | Optional | Must | — | Optional | Planned |
| Payback-period diagnostic | 回本周期诊断 | Basic | Must | Must | Optional | — | — | Optional | Planned |
| LTV / CAC health diagnostic | LTV / CAC 健康度诊断 | Basic | Must | Must | Must | — | — | Optional | Planned |

### Market Expansion Diagnostic Suite

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| Country / market performance diagnostic | 国家 / 市场表现诊断 | Basic | Must | Must | Optional | Must | Optional | Must | Planned |
| CAC / CVR / AOV comparison | CAC / CVR / AOV 对比 | Basic | Must | Must | Optional | Must | — | Must | Planned |
| Payment success-rate diagnostic | 支付成功率诊断 | Basic | Optional | Must | — | Must | — | Optional | Planned |
| Country-level shipping / tax leakage diagnostic | 国家级运费 / 税费流失诊断 | Basic | Optional | Must | Optional | Must | — | Optional | Planned |
| New-customer quality analysis | 新客质量分析 | Basic | Must | Must | Must | Optional | — | Must | Planned |
| Market expansion prioritization | 市场扩张优先级判断 | Basic | Must | Must | Optional | Optional | Optional | Optional | Planned |

### Data Quality & Tracking Governance

| English Scenario | 中文场景 (key) | Tier | F | MD | CRM | SO | CS | MB | Status |
|---------|---------|------|---|----|-----|----|----|----|------|
| UTM compliance monitoring | UTM 规范监控 | Basic | Optional | Must | Optional | Optional | — | Must | Planned |
| Pixel / Server-side Tracking anomaly monitoring | Pixel / Server-side Tracking 异常监控 | Basic | Optional | Must | Optional | Must | — | Must | In-dev |
| Order / user / session match-rate monitoring | 订单 / 用户 / Session 匹配率监控 | Basic | Optional | Must | Optional | Must | — | Optional | In-dev |
| Ad-platform vs on-site data discrepancy diagnostic | 广告平台数据与站内数据差异诊断 | Basic | Optional | Must | Optional | Optional | — | Must | In-dev |
| Klaviyo / CRM data-sync monitoring | Klaviyo / CRM 数据同步监控 | Basic | Optional | Optional | Must | — | — | — | Planned |
| Metric-caliber management | 指标口径管理 | Basic | Must | Must | Must | Must | Optional | Must | Planned |

---

## 3. Report Assembly Conventions

> A plan produces only the **analysis core** — the "scenario-specific metric blocks / diagnostic blocks / recommendation items." **Report cadence, role tailoring, tone, and the unified template are defined centrally here** and assembled into the final report by this convention, so each plan doesn't repeat them.

### 3.1 Report cadence (cadence → ranges and comparison periods)

| Cadence | Current period | Comparison period (default) | Granularity | Detail bias |
|------|------|--------------|------|---------|
| Daily | Yesterday (T-1) | Prior day, or trailing-7-day same-position average | campaign / ad | Report anomalies and the day's to-dos only |
| Weekly | Last full calendar week (from Monday) | The week before that (equal length) | Channel / campaign | Trend + root cause + recommendations |
| Monthly | Last calendar month | Prior month; for strong seasonality use the same month last year (YoY) | Suite-theme level | Full retrospective + structural conclusions |
| Custom range | User-given `date_from`~`date_to` | Equal-length shift back, YoY optional | Per scenario | Per user need |

General: the two periods must be **equal length and same `model`**; promo weeks / seasonality must be flagged to avoid misjudgment from comparing directly against normal-sales periods.

### 3.2 Role tailoring (reuses the Must / Optional / — of the section 2 scenario matrix)

- **General is the default role**: when no role is specified, use **General** = show **ALL** blocks with **no trimming**. Named roles trim per the matrix below.
- Single-scenario report tailored by the **requesting role**: scenario marked "Must" for that role → main body core; "Optional" → appendix / collapsible; "—" → omitted.
- Multi-scenario / theme report: when aggregating, **include only the Must + Optional scenario blocks for that role**, skip the rest.
- Role-perspective emphasis: Founder = conclusions and profit / growth top-line; Marketing Director = global view; Media Buyer = channel / campaign actionables; CRM = retention / users; Site Ops = on-site conversion; Creative Strategist = creative.

### 3.3 Tone / audience

- **Executives (Founder / MD)**: conclusion-first, concise, low jargon; emphasize money (GMV / profit / true ROAS) and the decision to make.
- **Execution roles (MB / SO / CS / CRM)**: specific, with metrics and actionable steps, retaining necessary terminology.
- **General (default role)**: neutral and complete — no role-specific slant, present all blocks fully.
- **Language**: follow the language of the user's first message, consistently throughout (headers / insights / recommendations / notes).
- **General principle**: data-driven (always cite specific numbers), insights before recommendations, each insight paired with a next step; no exaggeration, no fabrication, state missing data truthfully.

### 3.4 Standard report template (universal skeleton)

```markdown
# <Theme / Scenario> · <Cadence> Report
**Shop:** <shop>　**Range:** <current period>　**Comparison:** <comparison period>　**Attribution model:** <model>　**Audience:** <role>

## One-line conclusion
<the single most important judgment + the 1–2 most important actions to take>

## Key metrics
| Metric | Current | Comparison | Change | Status |
|------|------|--------|------|------|
(Status flags: ✅ improved / 🟡 flat ±5% / 🔴 deteriorated)

## Diagnosis & root cause
<filled by the plan's diagnostic block: phenomenon → diagnosis → evidence>

## Recommendations
<three tiers — high / medium / monitor; each marked "recommendation, pending manual execution">

## Next steps / chaining
<follow-up actions or related scenarios to chain-trigger>

**Plans used:** <comma-separated plan slugs>
```

Each plan fills its own "metric block / diagnostic block / recommendation items" into the corresponding positions; this template's structure, status flags, and layout are **unified here**, and plans no longer define their own.

### 3.5 Interaction & clarification conventions

- **Do not run everything by default**: there's no need to run all channels and all flows every time; default to the user's current question and the scope the prompt points at.
- **Channels split internally from the prompt**: channel / creative diagnostics **do not create a separate scenario per platform (Google / Meta / TikTok / Microsoft …)**; the plan internalizes pass-through interfaces like `meta_query` / `google_query` and splits channels per the user's prompt — look at whichever is mentioned; if unspecified, clarify first, or take the major channels by spend share and state so.
- **Clarify ambiguity first**: when the range, channel, granularity, comparison caliber, attribution model, or role is unclear, converge with **1–2 short clarifying questions** before fetching; don't re-ask what can already be determined from memory / context.
- Each plan's "Triggers & boundaries" section must include a **pre-clarification** step listing the 1–3 items most worth clarifying for that scenario.

### 3.6 Output length & segmentation

A single over-long report message can be truncated by the front end. Control length at the source and segment long reports rather than emitting one oversized message.

- **Length budget**: keep a single report message within roughly **800 lines / 6,000 words**. Favor concision — one-line conclusion, a focused key-metrics table, and the essential diagnosis. Do not dump every channel/campaign/ad row into the main body; offer row-level detail as an on-demand appendix the user can request.
- **Auto-segment long reports**: when an assembled report (typically a multi-suite daily/weekly/monthly) would exceed the budget, do **not** send it as one message. Split
