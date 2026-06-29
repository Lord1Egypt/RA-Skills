# CoopLens Source Methods

## Runtime date rule

At the start of every run, get the current date/time through a tool and display:

```text
检索执行日期：YYYY年MM月DD日（时区：...；通过工具获取）
```

Use the runtime year to build current searches. Do not assume that an old local year is still current.

## Required latest-source search bundle

For each concrete project, institution, partner, major or province-specific candidate list, immediately search and open the latest sources in this order. The analysis cannot proceed from memory, cached local data or stale excerpts:

1. **Regulator identity**: CRS/education regulator record, approval list,有效期,招生方式,办学地址,证书 and enrollment scale.
2. **School current admissions**: current-year招生简章,招生章程,本科招生网 notice,招生计划, tuition page, professional catalog, and explicit 当年是否招生/是否停招/是否暂停招生 evidence for the exact project/major/category.
3. **Provincial authority**: target-province education exam authority enrollment plan,专业目录,科类/选科, 招生批次, 院校专业组, 计划类型, batch control line and投档/录取分数线.
4. **Latest completed score/rank**: school admissions site, provincial exam authority, official admission result page, and one-score-one-rank table.
5. **Certificate and recognition**: school charter, CRS details, CSCSE/education authority pages where relevant.
6. **Curriculum and teaching**:培养方案, project handbook, course plan, college page and foreign partner course page.
7. **Outcomes**: employment quality report, undergraduate teaching quality report, college outcome page, official news, graduate-school reports and official competition/research pages.
8. **Rankings**: official ranking publisher pages only when ranking numbers are used; local ranking data is only an alias aid.
9. **Industry outlook**: official statistics, industry associations, listed-company reports, exchange filings, official annual/interim reports and reliable hiring/JD sources.
10. **Public discussion**: user-specified public discussion sources; use only aggregated signals in the report.
11. **Overseas-city living cost**: when an overseas stage is possible, search the foreign partner university's campus city cost of living through official university pages, student-budget pages, government/immigration finance guidance and current exchange-rate references.



## 当年是否招生入场闸门

For every concrete project or candidate, current-year admission status is the first gate. Do this before rank estimation, candidate sorting or recommending the project.

1. **Identity source**: open 教育部中外合作办学监管工作信息平台/CRS or 教育部官网 regulator page to confirm the project/institution identity, Chinese partner, foreign partner, major/category, approval status and validity. Treat this as identity/regulatory evidence, not as proof that the project recruits this year.
2. **Current-year recruiting source**: open the school本科招生网/招生办 official page, current-year招生章程/招生简章, and target-province招生计划/专业目录. These are the key sources for whether the exact project/major/category is included in the current year.
3. **Status labels**: every report must write one label per project/candidate: `继续招生/当年招生`, `未在当年招生计划中`, `当年停招/暂停招生`, or `未核到当年招生，待学校书面确认`.
4. **Decision effect**: if status is stopped, suspended, absent from current-year plan/catalog, or unresolved after official search, do not enter the project into rank formulas, 冲/稳/保判断 or serious candidate ranking. Put it under `仅关注/待核验，不参与排序` or `暂不建议填报` and list the exact official confirmation needed.
5. **Conflict handling**: if CRS/regulator identity exists but school/province current-year plans do not list the project, write the conflict plainly. Do not treat regulatory validity as current-year招生. Ask the school招生办/学院 for written confirmation.
6. **Manual confirmation**: tell the user to open the linked official pages and check current year, province, subject track, 招生批次, 院校专业组, plan type, project/major name and plan count.

Suggested minimum status card: `项目｜当前年份｜省份｜科类/选科｜招生批次｜院校专业组｜计划类型｜当年招生状态｜学校官网/招生办来源｜教育部/CRS来源｜省级专业目录来源｜人工确认｜质量等级`.

## 招生批次与专业组口径规则

不同招生批次的招生人数、投档线、专业线、最低分和最低位次可能完全不同。所有取数和分析必须先分批次，不得后合并：

1. 以目标省官方专业目录、招生计划或考试院投档表中的批次名称为准，记录 `提前批 / 本科批 / 普通本科批 / 综合评价批 / 专项计划 / 中外合作单列批 / 其他省级目录口径`。
2. 同一项目若在多个批次、多个院校专业组或多个计划类型出现，拆成多条记录；每条记录单独写招生计划人数、最低分、最低位次和批次控制线。
3. 当年招生计划与最近完成年度录取线必须核对是否属于同一招生批次和专业组；不一致时只能作弱参照，并在报告中说明不能直接比较。
4. 线差必须使用该数据所属批次的控制线；不得用本科批控制线去解释提前批、综合评价批、专项计划或其他单列批次的数据。
5. 普通专业基线、同校合作样本、同省同档样本必须标注批次；跨批次样本只能进入“弱参照/待核验”，不能作为公式中的 A/B 样本。
6. 如果来源页面没有写清批次、专业组或计划类型，写 `批次未核到/专业组未核到`，质量等级降级，且不得用于硬排序。

建议每条计划/录取数据使用最小字段：`年份｜省份｜科类/选科｜招生批次｜院校专业组｜项目/机构｜专业或大类｜招生计划人数｜最低分｜最低位次｜批次控制线｜来源链接｜人工确认｜质量等级`。


## QS/latest ranking handling

When using QS, search the official QS/TopUniversities ranking page at runtime and confirm the latest published edition shown by the page. Current examples can change; do not assume that a calendar year such as 2026 is still the newest edition if the official page has released 2027 or later. In the report:

- write the edition exactly as shown by the official page, e.g. `QS World University Rankings 2027`;
- link the ranking value or ranking statement directly to QS/TopUniversities;
- state that rankings are context, not proof of project quality, teaching quality, employability or admission difficulty;
- if only local ranking aliases are available, write `未核到可打开且内容对应的官方/权威排名原文` and do not use the number for recommendation strength.

## 个性化建议取数

用户提供家庭情况时直接使用；未提供时，不要反复追问，按情景给建议：

- 预算：宽裕 / 中等 / 紧张；连接到四年总投入、出国阶段费用、外方大学所在城市生活成本、汇率波动和延毕风险。
- 出国偏好：明确出国 / 可出国可不出国 / 不愿出国；连接到证书、留服认证、海外硕士和就业路径。
- 未来路径：保研/考研、海外硕士、就业、考公考编、国企事业单位、外企科技企业。
- 学习承受度：英语、GPA、全英文/双语、挂科和延毕风险。
- 城市/校区：是否接受异地校区、住宿和资源隔离。

建议必须写成“这个家庭该如何判断”，不能只写项目泛泛优缺点。

## Search-query pattern

Use the runtime year and target province. Examples:

- `{学校} {项目/学院/专业} {current_year} 招生简章`
- `{学校} {项目/学院/专业} {current_year} 招生章程`
- `{学校} {项目/学院/专业} {current_year} 是否招生 停招 暂停招生 学校官网 本科招生网`
- `{学校} {项目/学院/专业} 教育部 中外合作办学监管工作信息平台 CRS 招生状态`
- `{学校} {专业} {省份} {current_year} 招生计划 招生批次 专业组 学费`
- `{省份} 教育考试院 {学校} {专业} 招生批次 专业组 投档线 位次`
- `{学校} 本科招生网 {latest_completed_year} 录取分数线 位次 批次 专业组`
- `{学校/学院/项目} 教育部留学服务中心 留服认证 学历学位认证 官方`
- `{学校/学院/项目} 外方学位 留服认证 招生章程`
- `{学校/学院/项目} 就业质量报告 深造率 出国升学 保研 推免`
- `{项目/学院/专业} 本科生 一作 论文 官方`
- `{项目/学院/专业} 就业 知名企业 官方`

- `{外方大学} {city/campus} cost of living international students official`
- `{外方大学} student budget living costs accommodation official`
- `{外方大学所在城市} student living cost rent transport insurance official`
- `{外方国家/地区} student visa financial requirement living costs official`
- `{货币} 人民币 汇率 官方 今日`

For public discussion, use neutral search terms. Do not expose the source platform or account in the final report.


## Overseas-city living-cost evidence

If the student may go abroad/overseas for 1+ years, do not estimate living cost from memory. Search and open current sources for the foreign university city or campus:

1. Foreign university official cost-of-living or student-budget page.
2. Government, immigration or student visa finance requirement page.
3. Accommodation/rent, meals, transport, insurance/health, books/materials, local travel, visa/permit and emergency buffer.
4. Current exchange-rate source used for conversion into CNY.
5. Manual confirmation: the family should open the links and confirm city/campus, academic year, currency, included/excluded items, and whether the amount is minimum, average or recommended.

Report output:

- `境外城市生活成本与家庭预算适配` under the cost chapter or candidate card.
- Annual overseas exposure and four-year total exposure with quality grades.
- `预算差额 = 家庭年度预算 - 估计年度总支出` and the effect on 个性化推荐度评价.
- If city/campus or official cost data is not found, write `未核到可打开且内容对应的官方/权威原文` and downgrade cost confidence.



## 关键数据硬闸门

招生人数、分数线、分位数、升学率、出国率、就业率、保研率是极其重要的数据；扩展同义项包括招生计划人数、计划数、投档线、录取线、最低分、最低位次、排位、位次、深造率、境外升学率、毕业去向落实率、推免率。

1. 先找官方或可审计来源：目标省招生计划/专业目录、省考试院投档线、一分一段表、学校本科招生网、学校就业质量报告/毕业生就业质量报告、学院官方毕业去向说明、推免办法或推免名单公示。
2. 打开来源链接，确认页面内容中确实能找到对应年份、省份、科类/选科、招生批次、院校专业组、计划类型、项目/专业和数值。
3. 所有关键数据的可见数值必须写成 `约...` 并带来源超链接；推荐把数值本身做成链接。
4. 找不到就写未知：链接打不开、链接内容不含对应值、口径不一致、只有搜索摘要、只有非官方讨论、只有相近项目或旧年份，都写 `未知（未核到可打开且内容对应的来源链接）`。
5. 不得乱猜：不能用同校普通专业、相似项目、家长论坛、往年宣传口径或经验值推算升学率、出国率、就业率、保研率。
6. Markdown 完成后运行 `critical-data-source-check`；需要验证超链接寻找是否有数据时运行 `critical-source-evidence-check`。失败项必须改为未知后重新生成。

## Evidence rules

- A source is valid only if it opens and the content supports the displayed fact.
- For a numeric value used in ordering or calculation, link the number itself in Markdown and HTML, for example `[约589分](https://...)` or `<a href="...">约589分</a>`.
- All user-facing numeric data values carry `约`: scores, ranks, rankings, rates, tuition, plan counts, enrollment counts, rank gaps, cost totals, course ratios, industry scale, revenue, profit, hiring count and calculated ranges.
- If a value cannot be verified through a source that opens and matches the content, write `未知（未核到可打开且内容对应的来源链接）`; do not guess, infer, or fill a similar value.
- Do not write blanket claims such as “全部数据已核实” or “所有信息均来自公开渠道”. Also forbid any source paragraph that says all data, all information or all numeric conclusions already come from official/authoritative channels or already have fully verifiable links. Use item-level links plus manual-confirmation notes instead.
- Put important source links in the body near the value and also include one final `参考来源与核验说明` section.

## Latest admissions and score-line integration

Before giving a conclusion:

1. Determine whether the exact project/major/category still recruits in the current year; use school official admissions pages and target-province current-year plan/catalog as the current-year recruiting source, and CRS/教育部 regulator pages as identity evidence.
2. Determine whether the current-year admission brief/charter has been published.
3. Determine whether the current-year target-province plan is available.
4. Determine the latest completed admission year with public score/rank data.
5. Convert between score and rank only with the target-province one-score-one-rank table.
6. Distinguish direct project line, same-school ordinary reference, same-school cooperative/international reference and same-province comparable project reference.
7. For each plan/score/rank value, record 招生批次 and院校专业组; same project across different batches must be treated as separate records.
8. For no-history projects, use the three-scenario method in `references/live_rank_estimation.md`.


## Rank-estimation data proof and manual confirmation

Every rank-related section must include an evidence ledger. For each numeric input used in the formula, provide a link and a human-confirmation instruction:

- 数据项：what the value represents.
- 口径字段：年份、省份、科类/选科、招生批次、院校专业组、项目/专业、计划类型。
- 数值：write the value with `约`.
- 来源链接：the page that supports this exact value.
- 人工确认：the user should open the link and check year, province, subject track, 招生批次, major group, plan type, project name and value.
- 质量等级：A/B/C/D.

Only A/B/C values may enter formulas. D-level values may be mentioned only as weak context and cannot support ordering.

## CSCSE / 留服认证 evidence handling

For every foreign-degree claim, analyze 留服认证 independently:

1. Verify the exact foreign degree and awarding institution through CRS, admissions charter, school FAQ or school written answer.
2. Search the latest 教育部留学服务中心 / CSCSE authentication guide, service hall, application materials, process and result-query scope.
3. Distinguish `can apply`, `recent graduates have authenticated`, and `guaranteed authentication`. Never write guaranteed authentication unless official evidence for the exact project says so.
4. Distinguish foreign-degree authentication from traditional overseas-student benefits, city settlement, tax benefits, employer screening and public-sector route recognition.
5. For plan-outside or no-domestic学籍 paths, require stronger evidence and downgrade unclear items to `慎选` or `仅关注/待核验`.
6. If official sources answer the question, answer directly with links. If not, ask the school for written confirmation of certification materials, prior anonymized results, overseas-study requirement and domestic credential fallback.

## Negative public concerns

When a negative concern or doubt appears in public discussion:

1. **Officially verifiable concern**: answer directly if official or authoritative sources cover it. Typical topics:备案、计划内/计划外、学籍、证书、留服认证、招生计划、章程、学费、校区、选科、转专业、调剂、分数线.
2. **School-confirmation concern**: if the concern depends on actual execution, provide concrete questions. Typical topics: 外教比例、是否录播、课程难度、语言分层、挂科/延毕、实习支持、海外衔接、宿舍管理、资源共享.
3. **Experience-only concern**: summarize as a weak reputation signal and state that it cannot prove a fact.

Consultation wording should be practical:

- “请问该项目学生入学后是否有国内本科生学籍？学信网状态如何显示？能否邮件回复？”
- “请问外方教师承担哪些课程？是否有课程清单、授课比例和任课教师安排？”
- “请问近三届正常毕业率、延毕率、出国衔接通过率、语言未达标处理办法是否有公开口径？”
- “请问毕业证、学位证和外方证书样式、授予条件、是否必须出境学习，能否提供章程或培养方案依据？”
- “请问中外合作专业能否转入普通专业？服从调剂是否包含高收费项目？”

## Outstanding graduate outcomes

For existing institutions/projects:

- Prefer project-level evidence; if absent, use institution-level or college-level evidence with scope labels.
- Capture without names: selective graduate-school destinations, known employers, undergraduate first-author high-level papers, research awards, patents, competitions, scholarships and official honors.
- Use cautious wording: “官方材料显示有……类型成果”, “未核到项目级公开材料”, “该项目暂无毕业生公开成果”.
- Do not list student names, personal pages, photos, screenshots or social handles.

## Outcome scope labels

Use one of these labels in the report:

- `项目级公开材料`
- `学院/机构级公开材料`
- `学校级公开材料，仅作背景`
- `外方院校公开材料，仅作外方背景`
- `暂无本项目毕业生公开成果`
- `未核到可打开且内容对应的官方/权威原文`

## Markdown and static HTML source consistency

- Markdown is the source document.
- Static HTML is generated from the same Markdown and adds only layout/style.
- HTML must keep the same headings, facts, conclusions, source boundaries and disclaimer.
