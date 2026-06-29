# CoopLens Report Modules

Clean startup page exact starter lines. These are also the regression targets for startup-page checks; do not shorten, reformat or remove the mobile static-page requirement:

```text
你可以这样发：1，香港中文大学(深圳)+理工实验班+广东，必须确保生成的静态页面能在手机上正常显示
你可以这样发：2，项目A vs 项目B vs 项目C，所在省份/分数或位次，必须确保生成的静态页面能在手机上正常显示
你可以这样发：3，浙江，物理类，约2.5万位，计算机或人工智能方向，预算约10万每年，必须确保生成的静态页面能在手机上正常显示
你可以这样发：4，广东，物理类，约 1200 位，港中深理科实验班今年能不能冲，必须确保生成的静态页面能在手机上正常显示
如果生成页面失败，请输入如此命令：基于 markdown 文件，生成用户友好的美观的适合手机阅读的静态页面，不能添加新的内容或图片，需要严格按照 markdown 文件的内容生成。
```


## Direct answer opening

Always start with:

```text
重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。
检索执行日期：YYYY年MM月DD日（时区：...；通过工具获取）
```


Important-statement and source-claim rules:

- Use only this exact important statement: `重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。`.
- Do not write any other sentence beginning with `重要声明：`; do not write `重要申明`.
- `位次预估重要声明` is only a heading. The line below it must be the fixed important statement.
- Full reports must end with `## 附录：重要声明与人工确认提醒` and repeat the fixed important statement there.
- Do not write blanket source claims that say all data, all information, or all numeric conclusions are already verified, official, authoritative, or fully linked. Use item-level source links and manual-confirmation notes instead.

Then give the parent the conclusion first, but only after the report has checked the current-year admission gate for the exact project/candidate. The conclusion must separately show `项目综合实力推荐度评价（项目综合实力角度）` and `个性化推荐度评价（学生/家庭适配）`. Avoid long neutral introductions.

## Function 1 module prompt: single project

Use this order:

1. **结论先行**：优先/备选/观察/慎选/暂不建议; separately state `项目综合实力推荐度评价（项目综合实力角度）` and `个性化推荐度评价（学生/家庭适配）`, then give the main reason and reversal condition.
2. **家庭画像与个性化判断前提**：budget pressure, overseas preference, future path, English/GPA tolerance and city/campus constraints. If missing, use scenarios.
3. **当年是否招生核验（入场闸门）与最新官方材料核验**：first verify whether the exact project/major/category still recruits this year through school本科招生网/招生办 official pages, current-year招生章程/招生简章, target-province招生计划/专业目录, and 教育部中外合作办学监管工作信息平台/CRS or 教育部官网 regulator identity evidence. Show a status label: `继续招生/当年招生`, `未在当年招生计划中`, `当年停招/暂停招生`, or `未核到当年招生，待学校书面确认`. Then show current-year招生批次/专业组/计划类型、章程/CRS、分数线、费用、证书、培养方案; show what was verified and what was not.
4. **位次预估：统计、分析与预测**：first show `位次预估结论先行` with reference range, 冲/稳/保 label, confidence and reversal condition; then show 可验证数据统计 and 人工确认清单, then 位差/线差/样本分析, then 本年位次估计与完整可核验推导. Direct same-batch historical line if available; otherwise new/no-history three-scenario range with formula and linked inputs. Always show 输入数据、基线选择、差值样本、调整项、计算过程、置信度、推翻条件. The `计算过程` formula chain should be placed in a fenced code block or a clearly labeled calculation line so the mobile HTML renderer can show it as 黑底红字.
5. **项目身份、证书与费用**：plan status,学籍, certificates, foreign degree conditions, four-year total cost and hidden fees. If an overseas stage is possible, add `境外城市生活成本与家庭预算适配` with linked current living-cost evidence for the foreign university city and direct comparison to the family’s annual budget.
6. **留服认证路径与风险**：认证对象、认证路径、项目模式、境外学习记录、计划内/计划外、国内证书兜底、认证结果预期、传统海归/留学生待遇边界、风险等级和家长书面提问。
7. **培养模式、课程与学习压力**：plain-language course explanation, language/GPA thresholds, foreign-teacher input, graduation pressure.
8. **毕业成果与未来四条路径**：existing graduate outcomes without names; domestic graduate exam, overseas master’s, postgraduate recommendation, employment.
9. **专业与行业前景**：industry direction, scale/prosperity, leading-company signals, AI impact, entry-level job changes, student response.
10. **公开讨论中的担忧与核验办法**：anonymous aggregate concerns only; direct official answers when possible; school questions otherwise.
11. **家长应向学校确认的问题**：ranked question list, grouped by证书/费用/教学/资源/未来路径.
12. **参考来源与核验说明**：consolidated clickable sources and boundaries.

## Function 2 module prompt: multi-project comparison

Use project cards, not dense wide tables.

Required comparison dimensions:

- overall order or grouping;
- separate project-strength recommendation and student/family-fit recommendation for each project;
- admission rank/range and evidence strength;
- current-year 当年是否招生/是否停招 status, and current-year招生计划/章程 status;
- identity, certificate certainty and CSCSE/留服认证 path;
- total cost, overseas-city living-cost exposure and budget gap;
- if going abroad, current living cost for the foreign university city with source links;
- curriculum and learning-pressure fit;
- graduate outcomes and evidence scope;
- future four paths;
- major/industry outlook over roughly four to eight years;
- public concerns and official-consultation questions;
- what would reverse the order.

Conclusion format:

```markdown
## 一、结论先行

- 优先候选：{项目}。理由：...
- 备选候选：{项目}。理由：...
- 观察候选：{项目}。理由：...
- 慎选候选：{项目}。理由：...

会推翻排序的条件：...
```

## Function 3 module prompt: province/score/rank candidate retrieval

Use the runtime year and target province. This function is not a short list generator; it is a candidate-screening report with enough information for parents to judge.

Required order after the fixed statement, runtime date and task H1:

1. **目录**：`## 目录` must appear before any analysis section. Do not put long background, source explanation or method text before the TOC.
2. **最重要建议（先看这里）**：give non-neutral buckets such as 优先候选 / 备选候选 / 观察候选 / 慎选候选 / 仅关注待核验. First排除 or降级 projects whose current-year招生状态 is stopped, absent from official current-year plans, or未核到. Mention the student’s stated rank and annual budget in the first conclusion block when provided. This section must tell the parent what to do first.
3. **用户画像与筛选口径**：province,科类/选科, 当年是否招生状态, 招生批次/专业组（用户未给也要按官方材料补全或标注未核到）, score/rank, target major, annual budget, overseas preference, 留服认证需求, future path and missing assumptions.
4. **候选项目卡片**：for every project kept in the serious list, include:
   - 项目综合实力推荐度评价（学生无关）;
   - 个性化推荐度评价（结合学生位次、预算、出国偏好）;
   - 当年是否招生核验（入场闸门）/ 预测可能位次 / 冲稳保判断 / 证据强弱 / 招生批次与专业组口径;
   - 核心优势;
   - 主要缺点或风险;
   - 证书、计划内/计划外和 CSCSE/留服路径;
   - 年度预算压力、四年总投入; if going abroad, foreign-city living-cost estimate with links;
   - 升学、保研/考研、出国/境申硕、就业去向和培养成果证据边界;
   - 公开讨论担忧的官方核验或学校咨询问题。
5. **横向对比**：do not use wide tables; use narrow cards. Compare same-batch rank safety margin, budget gap, CSCSE clarity, major fit, outcomes and risk.
6. **仅关注/待核验，不参与排序**：list weak-evidence projects and exactly which evidence is missing.
7. **位次预估：统计、分析与预测**：start with `位次预估结论先行`; then show verifiable statistics, rank/line-gap analysis and predicted possible rank ranges for each serious candidate. New/no-history projects use three scenarios or move to watchlist. This is important but explanatory, so it comes after the advice and candidate cards in Function 3.
8. **参考来源与核验说明、最新官方材料核验与人工确认**：current-year招生计划/专业目录, 招生批次/专业组/计划类型, project availability, latest completed score/rank lines and one-score-one-rank table. State what must be opened manually; do not claim all data has already been verified.
9. **家长行动清单**：what to open and what to ask the school in writing.
10. **附录：重要声明与人工确认提醒**：repeat the fixed important statement exactly.


## Function 4 module prompt: standalone rank estimation

Use this when the user mainly asks about a current-year rank estimate, score-line estimate, no-history project threshold, or whether a student can冲/稳/保.

Required order:

1. **结论先行**：给出参考区间、冲稳保判断、置信度 and reversal condition. Separately state `项目综合实力推荐度评价（项目综合实力角度）` and `个性化推荐度评价（学生/家庭适配）`. If the user provided rank or annual budget, state the rank gap and budget pressure immediately.
2. **当年是否招生核验（入场闸门）与最新官方材料核验/批次口径**：runtime year, whether the exact project/major/category recruits this year, current admissions brief/charter/plan, target-province catalog, 招生批次/专业组/计划类型, latest completed score/rank line, one-score-one-rank table, CRS/school status. If the current-year status is stopped, absent or未核到, stop the current-year rank estimate and move the project to `仅关注/待核验，不参与排序` or `暂不建议填报`.
3. **位次预估：统计、分析与预测**：
   - 位次预估结论先行：参考区间、冲/稳/保、置信度、推翻条件；
   - 位次预估重要声明；
   - 可验证数据统计：each numeric value has a link, quality grade, 招生批次/专业组字段 and manual confirmation instruction；
   - 统计口径与异常值排查；
   - 位差与线差分析；
   - 本年位次估计的完整可核验推导；其中 `计算过程` 必须和结论分离，建议使用 fenced code block 展示公式链，HTML 中必须呈现为黑底红字；
   - 结论区间与人工确认清单。
4. **新项目或无历史线处理**：use 门槛偏高 / 中性 / 门槛偏宽 scenarios. Do not give a single-point estimate.
5. **个性化建议**：connect estimate to family budget, overseas preference, future path, English/GPA tolerance and risk tolerance. If going abroad, include current foreign-city living costs and compare the resulting annual/total cost against the family budget.
6. **参考来源与核验说明**：list item-level sources and state which data still needs manual confirmation; never use a blanket statement that all data or numeric conclusions have already been verified.

## 当年是否招生核验展示模板

Every Function 1/2/3/4 report must include this gate before using score/rank or recommendation logic:

```markdown
### 当年是否招生核验（入场闸门）

- 招生状态：继续招生/当年招生｜未在当年招生计划中｜当年停招/暂停招生｜未核到当年招生，待学校书面确认
- 当前年份：YYYY
- 省份/科类/选科：...
- 招生批次/院校专业组/计划类型：...
- 学校官网或招生办来源：...
- 教育部/CRS 项目身份来源：...
- 省级专业目录或招生计划来源：...
- 对本报告的影响：可进入位次预估｜不进入位次预估｜不参与排序｜暂不建议填报
- 人工确认：请打开链接核对年份、省份、科类/选科、批次、专业组、项目/专业名称、计划人数和是否停招。
- 质量等级：A/B/C/D
```

If the gate fails, historical score lines can appear only as background and must not be converted into a current-year冲/稳/保 conclusion.

## Markdown table-of-contents requirement

Every Markdown report must include `## 目录` after the fixed important statement, runtime-date line and task H1, and before the first analysis section. Function 3 must not put any analysis, source explanation or method block before `## 目录`. The table of contents should link to the main H2 sections.

Preferred anchors:

- `#一结论先行`（功能 3 可用 `#一最重要建议先看这里`）
- `#二最新官方材料核验`
- `#三位次预估统计分析与预测`
- `#四项目身份证书与费用`
- `#五留服认证路径与风险`
- `#六培养模式课程与学习压力`
- `#七毕业成果与未来四条路径`
- `#八专业与行业前景`
- `#九公开讨论中的担忧与核验办法`
- `#十家长应向学校确认的问题`
- `#十一参考来源与核验说明`

## 招生批次与专业组展示模板

凡出现招生计划、招生人数、分数线、投档线、最低位次、线差、位差或候选排序，必须加入下面字段。若同一项目存在多个批次或专业组，复制本模板分别写；不得合并。

```markdown
### 招生批次与专业组口径

- 年份：...
- 省份：...
- 科类/选科：...
- 招生批次：提前批 / 本科批 / 普通本科批 / 综合评价批 / 专项计划 / 中外合作单列批 / 其他 / 批次未核到
- 院校专业组：...
- 计划类型：普通计划 / 中外合作单列 / 综合评价 / 专项计划 / 其他 / 未核到
- 专业或大类：...
- 招生计划人数：约...；来源：...
- 最低分/最低位次：约...；来源：...
- 同批次控制线：约...；来源：...
- 是否可进入公式：是 / 否。原因：...
- 人工确认：请打开链接核对年份、省份、科类/选科、招生批次、院校专业组、计划类型、项目名称和数值。
```




## 关键数据硬闸门模板

凡出现招生人数、招生计划人数、计划数、分数线、投档线、录取线、最低分、最低位次、分位数、排位、位次、升学率、深造率、出国率、境外升学率、就业率、毕业去向落实率、保研率、推免率，必须按下面格式写。搜索不到、验证不了或来源内容不含对应数据时，直接写未知，不要乱猜。

```markdown
- 招生人数：[约...人](来源超链接)。口径：年份 / 省份 / 科类 / 招生批次 / 院校专业组 / 计划类型 / 专业或大类。人工核对：打开链接核对是否含该值。
- 分数线/最低位次：[约...分/约...位](来源超链接)。口径：年份 / 省份 / 科类 / 招生批次 / 院校专业组 / 同批次控制线。人工核对：打开链接核对是否含该值。
- 升学率：未知（未核到可打开且内容对应的来源链接）。
- 出国率：未知（未核到可打开且内容对应的来源链接）。
- 就业率：未知（未核到可打开且内容对应的来源链接）。
- 保研率：未知（未核到可打开且内容对应的来源链接）。
```

执行要求：Markdown 完成后运行 `python scripts/cooplens_core.py critical-data-source-check <report.md>`；需要验证链接页面是否真的含对应数据时运行 `python scripts/cooplens_core.py critical-source-evidence-check <report.md>`。任一失败都把对应字段改成未知后重做。

## Static HTML generation prompt

Generate the HTML from the Markdown. Use native HTML and CSS only, with a polished mobile-first visual design:


- use visible color differentiation: gradient hero, colored section cards, soft background blocks for warnings, highlighted conclusion badges, source chips and a clearer TOC card;
- rank-estimation calculation areas (`计算过程`, formula chains, and fenced code blocks inside the rank chapter) should render as black background with red text;
- internal TOC links must be real `<a href="#...">` anchors and tapping them on a phone must jump to the matching section id;
- the fixed important statement must be visible near the top and inside `附录：重要声明与人工确认提醒` at the end; if a rank chapter exists, `位次预估重要声明` must be visible in the HTML and the line below it must be the fixed important statement;
- output file names must use the task content, not platform names, generic runtime labels, browser/page labels or source-collection labels;
- single file;
- inline `<style>` block;
- no JavaScript;
- no external dependency;
- no images;
- mobile-first single-column cards;
- `viewport` meta;
- readable Chinese typography;
- long links and long project names must wrap;
- source links must remain clickable;
- Markdown table-of-contents links must render as clickable internal anchors, but the final HTML ids/hrefs must be ASCII-only `sec-...` values generated by the renderer, not Chinese heading text;
- the file must start with `<!doctype html>` and include `<html lang="zh-CN">`, `<head>`, UTF-8 charset, viewport, the safe-renderer meta marker, inline `<style>`, `<body>` and `<main>`;
- every opened structural container such as `<section class="card">` must be closed;
- do not hand-code a separate HTML page; generate it from Markdown through `python scripts/cooplens_core.py safe-html-build <report.md> --out <task-name>.html --error-out <task-name>_html_audit.json`;
- run `python scripts/cooplens_core.py html-syntax-check <task-name>.html`, `python scripts/cooplens_core.py html-report-check <task-name>.html`, and `python scripts/cooplens_core.py html-render-gate-check <report.md> <task-name>.html` before delivery; then run `python scripts/cooplens_core.py pure-report-file-check <task-name>.html <task-name>.md` to ensure the delivered files are true single files, not archives;
- before sending the final answer, save it as `final-answer.md` and run `python scripts/cooplens_core.py strict-final-delivery-check final-answer.md`; only send after it returns `ok: true`;
- the final answer for Function 1/2/3/4 must include a `交付文件下载链接` block with two clickable download links: one task-named static webpage `.html` link and one task-named Markdown `.md` link; plain filenames or “已生成” text are not sufficient; ZIP/archive/package/folder links fail even when they contain the HTML/Markdown; 内容像 HTML 不等于交付的是 HTML 文件，`.zip` 或无 `.html` 后缀的容器必须判失败；
- if any HTML 语法校验 or render gate fails, report the HTML 渲染失败原因, correct the Markdown/目录/锚点/重复标题/链接问题, and 不通过就重新生成 until all gates pass; never deliver a failed HTML file;
- common failure reasons include non-ASCII ids, unsafe external href values with Chinese/full-width punctuation, visible `---` separator paragraphs, missing hero title, generic title, hero/browser title equal to `## 目录` because the Markdown lacked a valid task H1, missing important statement, unresolved anchors, duplicate ids or hand-written HTML without the safe-renderer marker;
- do not leave raw Markdown link syntax like `[文字](#anchor)` or `[文字](https://...)` visible in the rendered page;
- do not add analysis not present in Markdown.

Recommended CSS characteristics:

```css
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body { margin: 0; line-height: 1.75; background: linear-gradient(180deg,#eef2ff 0,#f8fafc 220px); }
main { width: min(100%, 920px); margin: 0 auto; padding: 14px; }
.hero { background: linear-gradient(135deg,#1d4ed8,#7c3aed); color: #fff; border-radius: 22px; }
.card { border-radius: 18px; padding: 16px; margin: 14px 0; background: #fff; border: 1px solid #e5e7eb; box-shadow: 0 10px 28px rgba(15,23,42,.08); }
.card-rank { background: linear-gradient(180deg,#fff7ed,#ffffff); border-color: #fed7aa; }
.rank-calc, .card-rank pre { background: #050505; color: #ff2d2d; border-left: 6px solid #ef4444; border-radius: 16px; padding: 12px; }
.card-auth { background: linear-gradient(180deg,#ecfdf5,#ffffff); border-color: #bbf7d0; }
.card-warning, .notice { background: #fff7ed; border-left: 5px solid #f97316; }
.toc a { display: block; min-height: 44px; padding: 10px 12px; border-radius: 12px; background: #eef2ff; margin: 8px 0; }
section, article, nav, p, li { overflow-wrap: anywhere; word-break: break-word; }
a { min-height: 44px; text-underline-offset: 3px; }
@media (min-width: 760px) { main { padding: 28px; } }
```




#### Title parsing guard

Before generating HTML, make sure the Markdown has a valid task-derived `# ...` title before `## 目录`. Do not let `## 目录` become the browser `<title>` or hero `<h1>`. If `html-report-check` reports `invalid browser title` or `invalid hero title`, rebuild from Markdown after adding a task title or passing `--title` to `safe-html-build`.

### Function 3 HTML render gate

功能 3 的候选项目多，最容易因目录锚点、重复标题或结构拼接导致页面失败。功能 3 必须：

1. 先输出完整 Markdown，不直接手写 HTML。
2. 每个候选项目卡片标题使用唯一名称，例如 `### 候选A：南方科技大学-XX项目`，不要连续使用多个完全相同的 `### 核心优势` 作为独立章节；最终 HTML 锚点必须由脚本生成 ASCII `sec-...`，不要手写中文 id。
3. 用 `safe-html-build` 生成 HTML，并查看返回的 attempts；随后运行 `html-syntax-check`、`html-report-check`、`html-render-gate-check`。
4. 若出现 HTML 渲染失败原因，例如 `TOC/internal anchor target missing`、`duplicate HTML id`、`static HTML missing visible fixed important statement`、`unbalanced <section>`、`unexpected closing tag`、`invalid browser title`，必须改 Markdown 后重新生成。
5. 不通过就重新生成：重复修正 Markdown 与重新运行三项 gate，直到通过为止；脚本单次重建有防死循环上限，但最终答复不能交付失败 HTML。
6. 若最终答复没有通过校验的、直接指向单个纯 `.html` 文件的下载链接，或没有对应的、直接指向单个纯 `.md` 文件的下载链接，视为功能 3 交付失败，不能发送；错误报告只能用于继续修复，不能替代 HTML。
7. `.zip`、`.rar`、`.7z`、`.tar.gz`、压缩包、打包文件、文件夹链接或“打包下载”不能作为功能 3 报告交付链接；出现这类链接即视为不符合，必须重做并重新运行校验直到通过。
8. 最终答复草稿必须先运行 `python scripts/cooplens_core.py strict-final-delivery-check <final-answer.md>`，再运行 `python scripts/cooplens_core.py function3-delivery-gate-check <final-answer.md>`；任一失败都不能发送。
9. 功能 3 最终答复末尾必须使用下面格式，不得只给一个文件，不得给 ZIP/压缩包：

```markdown
### 交付文件下载链接

- 静态网页（HTML）下载链接：[下载/打开 {任务命名}.html](当前环境提供的可点击单个 .html 文件链接)
- Markdown 文件下载链接：[下载 {任务命名}.md](当前环境提供的可点击单个 .md 文件链接)
```

## Recommendation split template

```markdown
## 一、结论先行

- 项目综合实力推荐度评价（项目综合实力角度）：强 / 较强 / 中等 / 偏弱 / 高风险。依据：监管身份、证书/留服、外方质量、专业与课程、费用回报、毕业成果和风险。
- 个性化推荐度评价（学生/家庭适配）：高度适合 / 适合 / 边界适合 / 不太适合 / 不适合。依据：学生分数/位次、家庭预算、出国偏好、未来路径、英语/GPA承受度和城市/校区偏好。
- 两者冲突说明：项目强但不适合谁；或项目一般但适合作为什么家庭的备选。
- 最终动作：优先 / 备选 / 观察 / 慎选 / 仅关注待核验。
- 推翻条件：...
```

## Latest official materials module template

```markdown
## 二、最新官方材料核验

- 当前年份材料：已检索 {current_year} 年招生简章/章程/计划，并核对学校官网、目标省考试院和排名数字涉及的 QS/TopUniversities 最新官方榜单。已核到：...；未核到：...
- 目标省计划：按招生批次、院校专业组和计划类型分条列出；同一项目多批次时不得合并。
- 最近完成年度分数线：必须写清招生批次、院校专业组、最低分、最低位次和同批次控制线；批次不一致只作弱参照。
- CRS/监管状态：...
- 费用与证书：...
- 对结论的影响：...
```


## CSCSE / 留服认证 module template

```markdown
## 五、留服认证路径与风险

- 认证对象：外方学位/境外文凭的准确名称；未核到则写未核到。
- 认证路径：教育部留学服务中心/CSCSE 当前官方路径；链接 CSCSE、认证服务大厅、CRS、招生章程或学校书面答复。
- 项目模式：4+0 / 2+2 / 3+1 / 1+3 / mixed / unknown。
- 境外学习记录：必需 / 可选 / 无 / 未核到；不要把外方学位直接等同传统海归。
- 计划内/计划外与国内兜底：国内学籍、国内毕业证、国内学位证、学信网。
- 认证结果预期：可能的认证类别或口径；必须写“需以教育部留学服务中心正式认证结果为准”。
- 风险等级：低 / 中 / 高 / 待核验。
- 家长书面提问：请学校确认近三届去标识化认证结果、认证所需材料、无法认证时的国内证书兜底。
```

## Public discussion module template

```markdown
## 八、公开讨论中的担忧与核验办法

### 公开讨论信号

- 中性检索词：...
- 正面主题：...
- 负面担忧：...
- 反驳/澄清：...
- 信号强弱：...

### 能直接核验的质疑

- 质疑：...
- 官方/权威材料答复：...
- 对判断的影响：...

### 需要问学校的问题

1. ...
2. ...
```

Do not show platform names, accounts, handles, post titles, raw comments or screenshots.

## Graduate outcomes module template

```markdown
## 六、毕业成果与未来四条路径

### 已有毕业成果（不列姓名）

- 公开材料范围：项目级 / 学院机构级 / 学校级背景 / 暂无本项目毕业生公开成果。
- 世界知名大学深造：...
- 知名企业或重点行业就业：...
- 本科生科研/一作高水平论文：...
- 竞赛、专利、奖学金或其他成果：...
- 核验边界：...

### 四条路径怎么准备

- 国内考研：...
- 出国/境申硕：...
- 保研/推免：...
- 就业：...
```

No student names or personal identifiers.

## Tone requirements

- Make a judgment; do not hide behind neutrality.
- When evidence is weak, say exactly which evidence is missing and how that changes the recommendation.
- “值得考虑” must be followed by “在什么条件下值得”.
- “不建议” must be followed by the main reason and possible reversal condition.


## Rank estimation chapter module

```markdown
## 三、位次预估：统计、分析与预测

### 0. 位次预估结论先行
- 参考区间：...
- 冲/稳/保判断：...
- 置信度：强 / 中 / 弱。
- 推翻条件：...

### 位次预估重要声明
重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。

### 1. 可验证数据统计
- 数据项：...
  - 数值：约...
  - 来源链接：...
  - 来源类型：省考试院 / 学校官网 / CRS / QS官方 / 权威平台。
  - 人工确认：请打开链接核对年份、省份、科类、招生批次、专业组、计划类型、项目名称和数值是否一致。
  - 质量等级：A / B / C / D。

### 2. 统计口径与异常值排查
- 年份、省份、科类/选科、招生批次、专业组、计划类型口径：...
- 一分一段换算：...
- 异常值或冲突来源：...

### 3. 位差与线差分析
- 绝对分差 = 普通专业最低分 - 合作项目最低分。
- 绝对位差 = 合作项目最低位次 - 普通专业最低位次。
- 相对位差 = 绝对位差 / 普通专业最低位次 × 100%。
- 线差 = 项目录取分 - 同招生批次控制线。
- 同省同档样本中位数：...

### 4. 本年位次估计的完整可核验推导
- 输入数据：目标省份/类别、招生批次、院校专业组、计划类型、当年计划、最近完成年度分数/位次、一分一段、同校普通专业基线、同省同档样本。
- 基线选择：为什么用这个普通专业、专业组或同省同分段项目作基线。
- 差值样本：合作项目位次 - 普通专业位次 = ...。
- 调整项：招生计划、选科要求、学费、证书、留服认证、出国要求、城市/校区、公开讨论需求信号。
- 计算过程：基线位次 + 差值样本 ± 调整项 = 本年参考区间。
- 置信度：强 / 中 / 弱。
- 推翻条件：如果当年计划、招生批次、专业组、选科、费用、证书规则或官方分数线变化，则如何调整。

### 5. 结论区间与人工确认清单
- 参考区间：...
- 不参与排序项：...
- 人工确认清单：...
```

## Personalized family-fit module

```markdown
### 家庭画像与个性化建议

- 预算压力：宽裕 / 中等 / 紧张 / 用户未提供，按三情景判断。若需要出国，必须加入外方大学所在城市生活成本、汇率和家庭年度预算差额。
- 出国偏好：明确出国 / 可接受 / 不愿出国 / 未提供。
- 未来路径：保研考研 / 海外硕士 / 就业 / 考公考编 / 国企事业单位 / 外企科技企业。
- 英语与 GPA 压力：高 / 中 / 低 / 未提供。
- 建议结论：该项目对这个家庭是优先、备选、观察、慎选还是仅关注待核验。
```
