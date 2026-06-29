# Live Rank Estimation

## Purpose

Estimate admission rank references for Chinese-foreign cooperative programs using current official/authoritative inputs. The rank section must be a standalone chapter that first statistics, then analyzes, then predicts. The result is a reference for discussion, not an official current-year prediction.


## Mandatory chapter logic

Any report that mentions score line,投档线,最低位次, rank estimate,冲稳保, candidate feasibility or no-history project thresholds must include the chapter:

```markdown
## 三、位次预估：统计、分析与预测
```

The chapter must include the fixed rank-estimation disclaimer, a verifiable data ledger, statistical analysis, visible formulas, confidence, reversal conditions and a manual source-confirmation checklist.

The chapter order is mandatory:

1. `可验证数据统计`：source-linked numeric inputs and quality grades.
2. `统计口径与异常值排查`：year/province/subject/招生批次/院校专业组/plan-type consistency; different batches are separate records and cannot be merged.
3. `位差与线差分析`：absolute score gap, absolute rank gap, relative rank gap and line gap where data permits.
4. `本年位次估计的完整可核验推导`：inputs, baseline, gap samples, adjustments, formula, confidence and reversal conditions.
5. `结论区间与人工确认清单`：rank interval, evidence boundary and source-confirmation actions.

## Runtime inputs

Collect and link these inputs before estimating:

1. Runtime date and current year.
2. Target province and科类/选科.
3. Current-year招生简章/章程.
4. 当年是否招生核验（入场闸门）: school本科招生网/招生办 official current-year source, target-province招生计划/专业目录, and 教育部中外合作办学监管工作信息平台/CRS or 教育部官网 identity source.
5. Current-year target-province招生计划/专业目录, including 招生批次、院校专业组 and plan type.
6. Latest completed admission score/rank for the same project and the same 招生批次/院校专业组 if available.
7. Target-province one-score-one-rank table for the latest completed year.
8. Same-school ordinary major baseline when applicable.
9. Same-school cooperative/international-path samples when available.
10. Same-province same-tier cooperative/international-path samples.
11. Tuition/certificate/study-mode differences that may affect demand.

## Current-year admission status gate

Before any rank estimate, confirm whether the exact project/major/category recruits in the current year. If the school official admissions page or target-province current-year plan/catalog does not list the project, or an official source indicates stop/suspension, write `未在当年招生计划中` or `当年停招/暂停招生`, do not produce a current-year rank interval, and do not place the project into 冲/稳/保 or hard candidate ranking. CRS/教育部监管记录 is used for project identity; it cannot replace the school/province current-year admissions plan.

## Batch separation requirement

Before calculation, split admissions data by `招生批次 + 院校专业组 + 专业/大类`. If the same project has multiple batches or plan types, create separate rows and separate conclusions. Do not add plan counts across batches, do not average score lines across batches, and do not use one batch's control line to calculate another batch's line gap. Cross-batch evidence can only be marked as weak context unless the report explains why the provincial admission rules make the comparison valid.


## Statistical indicators

Use these indicators before any prediction:

```text
绝对分差 = 普通专业最低分 - 合作项目最低分
绝对位差 = 合作项目最低位次 - 普通专业最低位次
相对位差 = 绝对位差 / 普通专业最低位次 × 100%
线差 = 项目录取分 - 同招生批次控制线
趋势参照位次 = 最近完成年度项目位次 × (1 + 年均变化率)
```

Explain why each indicator is or is not available. For independent legal-person universities without ordinary-major baselines, replace the ordinary baseline with same-province same-band institutions and label the limitation.

## Evidence hierarchy

Use the strongest available evidence:

1. Direct project historical score/rank in the target province.
2. Same project in nearby years plus target-province one-score-one-rank rendering.
3. Same school + same province + similar major ordinary baseline and cooperative/international-path gap.
4. Same province + similar school tier + similar major cooperative/international samples.
5. New/no-history three-scenario estimate.
6. If all above are weak, put the project into “仅关注/待核验，不参与排序”.

## 本年位次估计的完整可核验推导

只要报告给出“本年/今年”的位次估计，必须把推导过程写给家长看。这里的“完整”指可核验的数据链和计算链，不是内部私有思考。

必写结构：

1. **输入数据**：所在省份、科类/选科、招生批次、院校专业组、计划类型、当年计划、最近完成年度专业线/投档线、一分一段换算、同批次控制线、同校普通专业基线、同省同档合作样本、费用/证书/出国要求等需求因素。关键数字必须数字本身带来源链接。
2. **基线选择**：说明为什么选择该普通专业/专业组/同档项目作为基线，说明招生批次是否一致，并说明不采用的替代基线。
3. **差值样本**：展示 `合作/国际项目位次 - 普通专业或同档基线位次 = 位次差`，说明样本数量和相似性。
4. **调整项**：招生计划变化、选科变化、专业热度、城市/校区、学费、证书含金量、是否必须出国、公开讨论需求信号。没有数据支撑时只能定性，不能伪造权重。
5. **计算过程**：写出算式，例如 `本年参照位次 = B普通基线位次 + A位次差样本 ± 调整项`，并给出区间而非单点。
6. **置信度**：强 / 中 / 弱，并说明由来源级别、样本数量、年份接近度和冲突情况决定。
7. **推翻条件**：列出会改变估计的官方信息，如当年计划数、专业组、选科、收费、证书规则、目标省专业线或一分一段变化。

缺少上述链条时，不得把数字写成预测结论；只能写历史参照或“仅关注/待核验”。

## New or no-history project method

For projects with 新开、首次招生、本省首招、新获批、新增专业 or no project-specific historical line:

### Step A: define the comparison object

- Identify the most similar ordinary-admission baseline: same school ordinary major, same school related major group, or a same-tier school ordinary major.
- If the institution has no ordinary-admission baseline, use same-province comparable independent/cooperative institutions and state why ordinary baseline is not applicable.

### Step B: collect gap samples

Collect at least two, preferably three to five, same-province samples showing ordinary vs cooperative/international rank gap. Each sample must include:

- school/project;
- major or major group;
- year;
- 招生批次 and院校专业组;
-普通线 or ordinary baseline;
- cooperative/international line;
- rank gap;
- source links for the numeric inputs.

### Step C: calculate three scenarios

Use rank as the primary unit.

```text
中性情景参考位次 = B普通招生基线位次 + A同省同档样本中位位次差
门槛偏高情景参考位次 = B普通招生基线位次 + A样本较小位次差
门槛偏宽情景参考位次 = B普通招生基线位次 + A样本较大位次差
```

Where:

- `B普通招生基线` means the rank of the ordinary-admission baseline.
- `A样本位次差` means ordinary baseline rank minus cooperative/international path rank, using the same province and latest completed year where possible.

### Step D: display boundary

Write this boundary clearly:

```text
这是基于最近公开历史数据的位次参照，不是今年录取预测；今年实际门槛会受招生计划、专业热度、学费、证书、家长认知、同分段竞品和省内志愿结构影响。
```

### Step E: weak-evidence handling

If any of these are missing, do not rank the item as a firm recommendation:

- current-year admission status, current-year plan, 招生方式 or招生批次;
- comparable baseline;
- at least one same-province gap sample;
- source links for numeric inputs;
- certificate/tuition/study-mode confirmation.

Put it into “仅关注/待核验，不参与排序” and list the exact missing evidence.

## Display requirements

- All numeric values use `约`, direct links and a manual-confirmation note.
- Every data row must visibly include 招生批次 and院校专业组; if unavailable, write 批次未核到/专业组未核到 and downgrade it.
- State sample count, sample weakness, data-quality grade and whether each source still needs human confirmation.
- State what would make the estimate shift upward or downward.
- Do not show a single-point estimate for a new/no-history project.
- Do not say “待补充数据” without explaining what must be checked and how.
