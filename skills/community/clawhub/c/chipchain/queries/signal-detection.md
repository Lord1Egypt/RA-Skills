# Signal Detection Workflow

**Question pattern:** "What's about to change in X supply chain?" / "Signal scan: Japanese materials companies" / "Any early signals on CMP slurry suppliers?"

This workflow detects supply chain changes BEFORE they show up in financial
results or English-language analyst coverage. It looks for leading indicators
in Asian-language filings, press, and procurement data.

For retrospective analysis of known events, use [change-detection.md](change-detection.md) instead.

## Freshness Rule: Signals Must Be New

A signal is only a signal if it represents a CHANGE from the previously known
state. "Company X has 10% market share" is information. "Company X went from
5% to 10%" is a signal. Every signal you report must answer three questions:

1. **When did this happen?** Date the signal. A qualification announced in
   2023 is not a signal in 2026.
2. **What was the previous state?** You need the baseline to know something
   changed. "Passed TSMC verification" only matters if they were NOT previously
   a TSMC supplier.
3. **Is this already priced in?** If English-language press already covered it
   months ago, the signal window has closed. Check whether Bloomberg, Reuters,
   or SemiAnalysis already reported it before including it as a signal.

**How to enforce freshness:**
1. Get today's date
2. Calculate the cutoff: today minus 60 days
3. Append the current year to every search query
4. For every result, check its publication date against the cutoff
5. Results dated AFTER the cutoff go to Signals Detected
6. Results dated BEFORE the cutoff go to Known State (baseline)
7. Results with no date at all go to Known State

Anything older than 60 days has likely been digested by the market already,
even for thinly covered small-caps.

**Stale signals are not worthless.** They become baseline data for future
comparison. Log them under "Known State" in your output, not under "Signals
Detected."

## The Three Signal Types

### Signal 1: Filing Delta (highest conviction)

Year-over-year change in customer/supplier lists in annual filings. A customer
appearing in or disappearing from the regulated disclosure sections.

| Country | Section to diff | Threshold |
|---|---|---|
| Japan | 主要販売先 (EDINET 有価証券報告書) | >10% of revenue |
| Korea | 주요 거래처 (DART 사업보고서) | >10% of revenue |
| China | 前五名客户销售额 (cninfo annual report / IPO 招股说明书) | Top 5 by amount |
| Taiwan | 主要供應商 / 前十大供應商 (MOPS 年報) | Often anonymized |

**What to look for:**
- A semiconductor fab appearing as a NEW customer (bullish for the supplier)
- A customer disappearing from the list (bearish: lost share, or supplier grew enough to dilute below threshold)
- Revenue concentration increasing or decreasing (risk profile shift)
- Coded customers (客户A, 供應商B) changing positions year-over-year

**Practical note:** Year-over-year comparison usually requires searching for the
same company's filing section across two years. Search for "[company name] +
[section header] + [year]" for each year and compare the snippets. If both
filings aren't accessible in a single session, report what you found and flag
the gap.

**Lead time:** 3-6 months after the change occurred (filing lag), but potentially
weeks or months before English-language coverage picks it up. For small-cap
Japanese TSE Standard stocks with zero sell-side coverage, the window can be long.

**CRITICAL: Only the delta is a signal.** A filing showing "Customer A = 30% of
revenue" is not a signal. A filing showing Customer A went from 0% to 30%, or
from 30% to below threshold, IS a signal. You must compare against the prior
year's filing. If you can't access the prior year, flag the gap.

**Evidence type:** Type 4 (Financial disclosure). Reaches CONFIRMED per evidence-guide.md.

### Signal 2: Qualification Announcement (medium conviction, long lead time)

A company announces it passed a fab's supplier verification process.

**Search terms:**

Korean:
```
[회사명] 고객사 인증 통과        → "passed customer certification"
[회사명] 납품 개시               → "began supplying"
[소재명] 국산화 성공             → "localization success for [material]"
[회사명] [팹명] 공급 계약        → "supply contract with [fab]"
```

Chinese (Simplified):
```
[公司名] 通过客户验证            → "passed customer verification"
[公司名] 进入供应链              → "entered supply chain"
[公司名] 实现量产                → "achieved mass production"
[公司名] 导入 [晶圆厂]          → "introduced to [fab]"
[材料名] 国产替代 突破           → "domestic substitution breakthrough"
```

Chinese (Traditional):
```
[公司名] 通過 [晶圓廠] 驗證     → "passed [fab] verification"
[公司名] 打入 供應鏈             → "broke into supply chain"
[公司名] 取得認證                → "obtained certification"
```

Japanese:
```
{会社名} 認定取得                → "obtained qualification"
{会社名} 供給開始                → "began supply"
{会社名} 採用決定                → "adoption decided"
{材料名} 量産開始                → "mass production started"
```

**Lead time:** 6-18 months before volume revenue. But qualification does not
guarantee volume orders. Many companies that pass verification never achieve
meaningful revenue from that customer. Treat qualification as a lead, not a
confirmed supply relationship.

**CRITICAL: Date the qualification event, not the article.** A recent article
recycling an old qualification is not a new signal. Look for the actual date
the verification was completed. If the article doesn't specify when, treat
it as stale until you can confirm timing from a primary source.

**Evidence type:** Type 3 (Qualification signal). Caps at STRONG INFERENCE per evidence-guide.md.

**False positives to watch for:**
- Qualification at a domestic Chinese fab (SMIC, CXMT) does NOT predict
  qualification at TSMC or Samsung. The processes are different.
- "通过验证" for mature nodes (28nm) says nothing about advanced nodes (sub-7nm)
- Companies sometimes announce "entering qualification" (进入验证阶段) which is
  far earlier and less certain than "passed qualification" (通过验证)
- **Recycled announcements.** Companies re-announce old qualifications in new
  press releases to boost visibility. Check whether the underlying event has
  a specific date. If the same qualification was reported last year, it is
  not a new signal.

### Signal 3: Capex Pipeline (high conviction when combined)

A supplier announces capital investment near a confirmed fab site.

**Search terms:**

Japanese:
```
{会社名} 新工場 建設 半導体       → "new factory construction, semiconductor"
{地名} 半導体 関連 投資           → "[location] semiconductor-related investment"
{会社名} 設備投資 増産            → "capex, capacity expansion"
熊本 半導体 サプライヤー          → "Kumamoto semiconductor supplier"
千歳 Rapidus サプライチェーン     → "Chitose Rapidus supply chain"
```

Korean:
```
[회사명] 신공장 반도체 소재        → "new factory semiconductor materials"
평택 반도체 소재 공급              → "Pyeongtaek semiconductor materials supply"
[회사명] 설비투자 증설             → "facility investment expansion"
```

Chinese:
```
[公司名] 新建工厂 半导体材料      → "new factory construction semiconductor materials"
[地名] 半导体 配套 项目           → "[location] semiconductor supporting project"
[公司名] 环评公示                 → "environmental impact assessment notice"
```

**Lead time:** 12-24 months before revenue impact (construction to production).

**CRITICAL: Distinguish announcement from completion.** A factory announced
last year and operational now is not a new signal. The announcement was the
signal. Check construction status: announced, under construction, or operational.
Only "under construction" or "just announced" count as active signals.

**Evidence type:** Type 6 (Circumstantial) alone, but often combines with other
signals to reach STRONG INFERENCE. A factory is a hard commitment you cannot fake.

**Failure mode:** Fab delays. A supplier who built a factory expecting JASM Fab 2
in 2027 now has idle capacity if the fab slips to 2028. Focus on suppliers whose
products are node-agnostic (water treatment, gas delivery, exhaust systems)
rather than node-specific (advanced photoresist, EUV components).

## Investigation Method

1. **Define scope** — Which material segment? Which geography? Which time horizon?
2. **Load context** — Read relevant entity files, lexicons, and evidence-guide.md
3. **Establish baseline** — What is the KNOWN state? Check entity files, prior
   investigations, and verification logs. You need the "before" to detect the "after."
4. **Search for all three signal types in parallel** — Spawn sub-agents by language:
   - Agent 1: Filing delta search (compare current vs. prior year filings)
   - Agent 2: Qualification announcements in target language press
   - Agent 3: Capex/facility announcements near fab clusters
   - **Instruct all agents to append current year + quarter and discard results older than 90 days for signals (older results go to Known State)**
5. **Date every finding** — If a finding has no date, it is not a signal. Log it
   under Known State, not Signals Detected.
6. **Classify each signal** — Filing Delta / Qualification / Capex Pipeline
7. **Check: is this actually new?** — Was this already known? Already in the
   entity files? Already covered in English press? If yes, it's baseline, not signal.
8. **Apply evidence type caps** from evidence-guide.md
9. **Map investment implications** — Who gains? Who loses? On what timeline?
10. **Run counterfactual** — Could this signal be noise? What would disprove it?

## Output Format

```markdown
# Signal Detection: [Scope]

## Source Registry
[Standard Phase 1 registry with evidence]

## Known State (baseline, not new)
[What was already known before this scan. Provides context for the signals.]

## Signals Detected

### Signal: [Description]
- **Date detected:** [when this was published/filed]
- **Type:** Filing Delta / Qualification / Capex Pipeline
- **Direction:** Positive for [Company X] / Negative for [Company Y]
- **Evidence type:** [per evidence-guide.md]
- **Confidence:** [per SKILL.md levels]
- **Estimated time to financial impact:** [months]
- **Where to verify:** [specific filing section, in specific language]
- **What would invalidate this:** [specific falsifier]

## No Signal Found
[Materials/companies scanned where nothing changed. This is information too.]

## What I Could Not Verify
[Gaps: filings that were inaccessible, years that couldn't be compared,
languages not searched]

## Search Log
[Standard search log]

## Recommended Next Steps
[Specific follow-up searches the agent can execute now]
```

## What This Workflow Does NOT Do

- It does not say "buy" or "sell." It detects supply chain changes.
- It does not provide valuation analysis. The user has Bloomberg for that.
- It does not predict timing of market pricing. A signal can be correct and
  take 6-18 months to be reflected in the stock price.
- It does not cover fast-moving events (export control announcements, natural
  disasters). News feeds are faster for those. This workflow catches the slow
  structural signals that unfold over quarters.
