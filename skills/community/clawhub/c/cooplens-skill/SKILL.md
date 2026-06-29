---
name: cooplens-skill
description: Analyze Chinese-foreign cooperative undergraduate programs for parents. The skill verifies official sources in real time, estimates admission rank ranges including new/no-history projects, synthesizes anonymous public-discussion concerns without exposing platforms or identities, analyzes CSCSE / 教育部留学服务中心 authentication paths, searches overseas-city living costs when an abroad stage is possible, extracts parent-facing risk questions, produces Markdown with a table of contents, generates colorful mobile-first static HTML with native HTML and CSS, uses task-based artifact filenames, and separates 个性化推荐度评价（学生/家庭适配） from 项目综合实力推荐度评价（项目综合实力角度）.
version: "1.0.15"
---

# CoopLens Skill

## Fixed disclaimer

Every user-visible reply produced under this skill starts with this exact line and final Function 1/2/3/4 reports also end with it:

```text
重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。
```

Strict important-statement policy:

- The only visible sentence that may start with `重要声明：` is the exact fixed line above. Do not create alternative important statements for rank estimation, source collection, official verification, data reliability, or HTML generation.
- Full Function 1/2/3/4 Markdown and HTML reports must include the exact fixed line near the top and again in `## 附录：重要声明与人工确认提醒` at the end.
- `位次预估重要声明` may be used only as a heading. The sentence under that heading must be the exact fixed line above, not a custom rank-estimation disclaimer.
- Do not write blanket source declarations that imply everything has already been verified or comes from an official/authoritative channel. Use item-level source links, quality grades and manual-confirmation prompts instead.
- Phrases that claim all data, all information, or all numeric conclusions are already verified, official, authoritative, or linked are forbidden in all Function 1/2/3/4 reports and final answers.

## Read order

1. Read `references/core_workflow.md` before any CoopLens task.
2. For source collection, admission thresholds, rank estimation, tuition, overseas-city living costs, certificates, 留服认证, curriculum, outcomes, public discussion or current-year admissions, also read `references/source_methods.md`, `references/live_rank_estimation.md`, `references/rank_estimation_workflow.md`, `references/rank_statistical_estimation.md`, `references/cscse_authentication.md`, and `references/overseas_living_cost.md`.
3. For every Function 1/2/3/4 report, read `references/parent_manual_distilled.md` and `references/recommendation_rubric.md`, then use their parent decision lenses across the analysis.
4. For specified projects, institutions, partners or school + major combinations, read `references/public_platform_discussion.md` and synthesize public-discussion signals as a separate, non-official evidence layer.
5. For report structure and artifact checks, read `references/schema.md` and `prompts/report_modules.md`.
6. Use `scripts/cooplens_core.py` for local candidate lookup, ranking-name lookup, runtime date fallback, Markdown table-of-contents checks, mobile static HTML safe-build/render-gate checks, source-link checks and report policy checks.

## Operating contract

Clean startup page contract: when the user only asks to start/open CoopLens, show only the fixed disclaimer, runtime date and the exact four-entry startup block from `references/core_workflow.md`. Do not invent conversation starters from the local index, old prompts or model memory. The following exact starter lines and the page-failure recovery command are mandatory and must not be shortened:

```text
你可以这样发：1，香港中文大学(深圳)+理工实验班+广东，必须确保生成的静态页面能在手机上正常显示
你可以这样发：2，项目A vs 项目B vs 项目C，所在省份/分数或位次，必须确保生成的静态页面能在手机上正常显示
你可以这样发：3，浙江，物理类，约2.5万位，计算机或人工智能方向，预算约10万每年，必须确保生成的静态页面能在手机上正常显示
你可以这样发：4，广东，物理类，约 1200 位，港中深理科实验班今年能不能冲，必须确保生成的静态页面能在手机上正常显示
如果生成页面失败，请输入如此命令：基于 markdown 文件，生成用户友好的美观的适合手机阅读的静态页面，不能添加新的内容或图片，需要严格按照 markdown 文件的内容生成。
```


### Runtime date and latest-source collection

- At the beginning of every CoopLens execution, obtain the current date/time through an available runtime tool. Preferred order: `user_info.get_user_info`; otherwise run `python scripts/cooplens_core.py runtime-date` or an equivalent local date tool.
- Record internally: `current_date`, `current_year`, `timezone`, `date_source_tool`, `checked_at`.
- Display immediately after the fixed disclaimer: `检索执行日期：YYYY年MM月DD日（时区：...；通过工具获取）`.
- Based on the user’s school / project / partner / major / province, search the latest official or authoritative materials before analysis: current-year 招生简章, 招生章程, 招生计划, target-province enrollment catalog, subject requirements, tuition notice, certificate rules, 当年是否招生/是否停招/是否暂停招生 status, 教育部中外合作办学监管工作信息平台/CRS or 教育部官网 regulator page, school official admissions page, 教育部留学服务中心/CSCSE authentication guidance, latest completed score/rank lines, one-score-one-rank table, CRS/regulator entry, employment/further-study reports and current curriculum pages.
- Do not rely on local indexes, cached years, old reports or memory as final evidence. Local data is only for discovery, alias matching and search-query expansion.


### 当年是否招生入场闸门

- Before any Function 1/2/3/4 conclusion, recommendation, rank estimate or candidate ranking for a specific project, first verify whether the exact project/major/category is still recruiting in the current admission year.
- Preferred evidence order: target-province current-year招生计划/专业目录 and school本科招生网/招生办 official current-year page first; then current-year招生章程/招生简章; then 教育部中外合作办学监管工作信息平台/CRS or 教育部官网 regulator page for project identity. CRS validity only proves regulatory identity/approval; it does not by itself prove current-year enrollment.
- Every report must include a visible `当年是否招生核验（入场闸门）` or `招生状态` record for each analyzed project/candidate: current year, province, subject track, 招生批次, 院校专业组, plan type, official source, status label and manual confirmation action.
- Status labels must be one of: `继续招生/当年招生`, `未在当年招生计划中`, `当年停招/暂停招生`, or `未核到当年招生，待学校书面确认`.
- If the project is not found in the current-year official plan/catalog, or an official school/regulator source indicates stop/suspension, do not provide a current-year rank estimate, do not include it in hard ranking or serious candidate buckets, and place it under `仅关注/待核验，不参与排序` or `暂不建议填报`; historical score lines may be shown only as background with a clear non-current boundary.
- If current-year admission status conflicts across sources, stop using the item for formulas and ranking, list the conflict, and ask the school招生办/学院 for written confirmation before any填报 decision.



### 关键数据硬闸门

这些字段属于极其重要的数据：招生人数、招生计划人数、计划数、分数线、投档线、录取线、最低分、最低位次、分位数、排位、位次、升学率、深造率、出国率、境外升学率、就业率、毕业去向落实率、保研率、推免率。

- 关键数据必须先检索官方或可审计来源，并打开来源链接确认页面内容确实包含对应字段和值；仅看到搜索摘要、二手转述、论坛讨论或模型记忆不算来源。
- 关键数据如果检索不到、链接打不开、链接内容找不到对应值、年份/省份/科类/批次/专业组/项目口径对不上，找不到就写未知：直接写 `未知（未核到可打开且内容对应的来源链接）`，不得猜测、不得补齐、不得用相近项目或往年数字冒充。
- 所有关键数值在输出中必须写成 `约...`，并优先把数字本身做成来源超链接，例如 `[约6人](https://...)`、`[约650分/约1200位](https://...)`、`[约95%](https://...)`。禁止裸写 `6人`、`650分`、`1200位`、`95%`。
- 升学率、出国率、就业率、保研率如果没有项目/学院/学校公开报告或官方页面支撑，不要用同类学校、网络传闻或经验值估算；直接写未知。
- Markdown 报告生成后必须运行 `python scripts/cooplens_core.py critical-data-source-check <report.md>`；需要联网核对链接内容时运行 `python scripts/cooplens_core.py critical-source-evidence-check <report.md>`。任一失败都必须把无来源或验证不了的数据改为未知后重做。

### Core functions

1. **单项目深度分析**：answer whether the project is worth considering for the family’s path. First show 当年是否招生核验（入场闸门）. Then cover identity, plan status, certificate combination, 留服认证路径与风险, admission threshold, rank estimate, tuition/total cost, curriculum, teaching location, learning pressure, transfer/adjustment limits, four-year path, industry outlook, public-discussion concerns and questions to ask the school.
2. **多项目对比**：give a useful order or grouping instead of neutral prose. First verify each project’s current-year 招生状态 and exclude/降级 stopped or unconfirmed projects before ranking. Use project cards and clear qualitative labels such as 优先、备选、观察、慎选. Explain what condition would reverse the conclusion.
3. **按省份/分数/位次找候选**：collect current official data, first verify current-year 招生状态 for every candidate, identify candidate projects, estimate rank ranges only for projects with usable current-year admission evidence, and separate stopped/unconfirmed/weak-evidence projects into “仅关注/待核验，不参与排序”. Function 3 reports must place `## 目录` before any analysis section, then put the most important advice and candidate grouping first, secondary candidate-card comparisons next, and explanatory methodology/source-confirmation sections later. New or no-history projects must use the three-scenario rank-reference method only after the current-year admissions gate passes. Candidate cards must analyze each project’s 当年是否招生, advantages, disadvantages/risks, predicted rank range, tuition/total-cost pressure, CSCSE/留服 path, graduate-study and employment evidence, public concerns and parent questions.
4. **位次预估**：when the user mainly asks “今年多少位能上 / 新项目怎么估 / 同分段能不能冲”, first verify whether the exact project/major is recruiting this year. If it is stopped or not found in current-year official plans, do not create a current-year rank estimate; explain the stop/unconfirmed status and list confirmation actions. If the gate passes, create a standalone rank-estimation report. It must first give a clear reference-range conclusion and 冲/稳/保 judgment, then show the auditable workflow: 统计可验证数据 → 分析位差/线差/样本 → 预测区间. It must include source hyperlinks, an important rank-estimation disclaimer, data-quality grades, a manual source-confirmation checklist and a statement that every source must be opened and checked by a human.

### Real-time admission and rank estimation

- For every score/rank claim, first pass the `当年是否招生入场闸门`: collect current-year招生计划/专业目录 and school official admissions evidence showing whether the exact project/major/category is still recruiting. Then collect latest completed admission score/rank, one-score-one-rank table, same-school ordinary major reference and same-province comparable cooperative/international-path samples.
- Any current-year rank estimate must show a full user-visible, auditable reasoning path: 输入数据、基线选择、差值样本、调整项、计算过程、置信度、推翻条件. The report should expose formulas, assumptions and source-linked numbers that parents can audit; it must not present private hidden chain-of-thought.
- For new projects, first-year projects, target-province first intake, or no-history projects, show three scenarios: 门槛偏高 / 中性 / 门槛偏宽. Include the formula and linked numeric inputs. State clearly that this is a historical-reference estimate, not a current-year prediction.
- If the input chain is too weak, remove the item from ranked recommendations and put it into “仅关注/待核验，不参与排序”.
- Functions 1/2/3/4 must use the same standalone rank-estimation chapter whenever they discuss rank, score line or candidate feasibility. Do not scatter rank reasoning across unrelated sections. Inside the rank chapter, start with `位次预估结论先行`: reference range, 冲/稳/保 label, confidence and reversal condition. After that, show the statistical workflow.
- The standalone Function 4 must be named `位次预估` and must follow: `先统计 → 再分析 → 再预测`.
- Rank reports must include `位次预估结论先行`, `位次预估重要声明`, `可验证数据统计`, `位差与线差分析`, `本年位次估计的完整可核验推导`, and `人工确认清单`. Under `位次预估重要声明`, use only the fixed important statement; put manual source checking in `人工确认清单`, not in a new disclaimer.
- Every numeric input used in a rank formula must be directly linked and marked for human confirmation. The report must say that the user should manually open the source and verify year, province, subject track, batch, program group, major and value.
- In any visible rank-estimation chapter, the calculation/reasoning subsection must be visually separated from the conclusion. Markdown should put the formula and calculation chain under `计算过程` in a fenced code block or a clearly labeled line; the mobile HTML renderer must show this calculation area as black background with red text so parents can distinguish “calculation process” from the final recommendation.


### 招生批次严格区分规则

- 所有涉及招生计划、招生人数、投档线、专业线、最低分、最低位次、线差、位差、冲/稳/保判断和候选排序的数据，必须把 `招生批次` 作为独立必填字段处理。
- 同一学校、同一项目、同一专业或同一大类若在不同批次招生，例如提前批、本科批、普通本科批、综合评价批、专项计划、中外合作单列批、不同院校专业组或其他省级目录口径，必须拆成不同数据卡分别写，不得把招生人数、分数线或位次合并成一个数字。
- 当年招生计划、最近完成年度分数/位次、一分一段表、批次控制线、普通专业基线和同省同档样本必须尽量保持同省、同年、同科类/选科、同招生批次、同院校专业组或可解释的相近口径；口径不同只能作弱参照，不能直接进入公式或硬排序。
- 每条录取或计划数据的最小字段为：年份、省份、科类/选科、招生批次、院校专业组、项目/机构、专业或大类、招生计划人数、最低分、最低位次、批次控制线、来源链接、人工确认要点、质量等级。
- 如果来源未写清招生批次、专业组或计划类型，必须标注 `批次未核到/专业组未核到`，并把该数字降级为弱证据；不得用它支撑位次公式、位差/线差计算或候选排序。
- 分析中发现不同来源批次口径冲突时，先停止合并，列出冲突来源和需要家长/学校确认的问题；不允许为了给出结论而自行推断为同一批次。


### Latest QS and ranking source rule

When a report uses QS ranking, first search/open QS or TopUniversities official pages and identify the latest published edition at runtime. Do not assume the natural calendar year equals the ranking edition. If the official page shows `QS World University Rankings 2027`, use that instead of older 2026 values. Local ranking data is only an alias and recall aid; the visible ranking number must be supported by the official ranking publisher page or written as `未核到可打开且内容对应的官方/权威排名原文`.

### CSCSE / 留服认证

For every project involving a foreign degree, overseas stage, 4+0, 2+2, 3+1, 1+3, plan-outside path, or parent question about recognition, include an independent `留服认证路径与风险` analysis. Distinguish: 认证对象, 认证路径, 项目模式, 境外学习记录, 计划内/计划外, 国内学籍和国内证书兜底, 认证结果预期, 传统海归/留学生待遇边界, official evidence, risk level, and written questions for the school. Use the latest CSCSE / 教育部留学服务中心, national service platform, CRS, school charter and school written-answer evidence. Do not promise `一定能认证`, `保证认证`, `包认证`, or `等同海归`; write the boundary and downgrade unclear projects to 观察、慎选 or 仅关注/待核验.



### Overseas-city living cost

When a project may require or strongly encourage study outside the mainland, the cost analysis must search current online sources for the foreign partner university’s study city and living costs. Use university living-cost pages, official student-budget pages, government or immigration finance guidance, and current exchange-rate references where possible. Include rent/accommodation, food, transport, insurance/health, visa/permit, study materials, local travel and a currency buffer. The result must be linked, marked for manual confirmation, converted into annual and total exposure, and compared directly with the family’s stated annual budget. If the city or campus is not confirmed, say so and downgrade cost confidence.

### Public discussion and negative concerns

- Search user-specified domestic public-discussion spaces when tools allow, but user-visible reports must not display source platform names, source groupings, account names, user names, post titles, raw comments, screenshots, handles, profile links or identifiable story details.
- Reports may show only neutral search terms, positive themes, negative concerns, rebuttal/clarification themes, signal strength and school-consultation questions.
- Public discussion never proves official facts. If a concern can be verified through official school, regulator, provincial exam authority, education authority, employment report or other authoritative page, answer it directly with that source. If it cannot, convert it into concrete questions for the admissions office, college office, teaching affairs office, employment office or international office, and ask for written confirmation.

### Graduate outcomes

- For every project/institution with prior graduates, search official or authoritative evidence for outstanding outcomes without revealing any student names.
- Outcomes can include admission to globally selective universities, employment at well-known employers, undergraduate first-author high-level papers, competitions, patents, further-study scholarships or other official achievements.
- Do not show student names, profile links, screenshots or personal identifiers. If only school-level rather than project-level evidence is available, label the scope clearly. If the project has no graduates or no public official evidence, say that clearly.

### Parent-manual decision lenses

Use these lenses in every module: 办学身份、计划内/计划外、证书组合、留服认证、外方质量、四年总投入、语言/GPA/延毕压力、校区与资源、转专业与调剂、未来路径、公开讨论问题、官方核验边界.

### Recommendation ratings

Every report must show two separate recommendation ratings; never merge them into one average score:

1. `个性化推荐度评价（学生/家庭适配）`：judge whether this project fits the specific student and family situation. Use the student's score/rank, province, target major, budget, willingness to study overseas, CSCSE/留服认证 dependence, future path, English/GPA pressure tolerance, city/campus preference and risk tolerance.
2. `项目综合实力推荐度评价（项目综合实力角度）`：judge the project itself independent of one family. Use regulatory status, plan-in/plan-out status, Chinese and foreign partner strength, latest QS/THE/USNews or discipline ranking only when official latest pages are opened, major competitiveness, certificate and CSCSE clarity, tuition/return, curriculum, campus resources, graduate outcomes and unresolved risks.

Use clear levels instead of neutral wording:

- 个性化推荐度评价（学生/家庭适配）：高度适合 / 适合 / 边界适合 / 不太适合 / 不适合。
- 项目综合实力推荐度评价（项目综合实力角度）：强 / 较强 / 中等 / 偏弱 / 高风险。

If the two ratings conflict, explain it explicitly, e.g. `项目综合实力强，但对预算紧张且不愿出国的家庭不适合` or `项目综合实力一般，但对低预算且求稳国内证书路径的家庭可作为备选`. The conflict itself is useful information and must not be softened into “看个人情况”.

### Personalized family-fit advice

Every Function 1/2/3/4 analysis must translate evidence into family-specific advice. Use the user-provided family situation when available; otherwise provide scenario-based advice instead of stopping for clarification. If the user gives an annual budget, convert tuition, mandatory fees, domestic living expenses and possible overseas-city living costs into an annual/total budget gap. If the user gives a rank, compare it directly with the estimated rank range and show the safety margin or冲刺 gap. Cover at least: 家庭预算与费用压力、是否愿意出国或只接受国内完成、未来路径偏好（保研/考研/海外硕士/就业/考公考编/国企或外企）、英语与 GPA 压力承受度、城市/校区/住宿偏好, and the conditions under which the project should be upgraded or downgraded for that family.

### Output artifacts

- Do not generate a report artifact in document-export formats unless the user explicitly asks for one.
- Function 1/2/3/4 default artifacts are:
  - a complete direct chat answer;
  - a Markdown report with a visible `## 目录` after the runtime-date line;
  - a mobile-first static HTML page generated from the same Markdown.
- Every Function 1/2/3/4 completion must end with a visible `交付文件下载链接` block containing exactly two required clickable download links:
  - `静态网页（HTML）下载链接：` followed by a direct, individual, task-named `.html` file link;
  - `Markdown 文件下载链接：` followed by a direct, individual, task-named `.md` file link.
  These must be pure standalone HTML/Markdown file links. A `.zip`, `.rar`, `.7z`, `.tar.gz`, archive package, bundled folder, “打包下载”, “压缩包”, or a link to a ZIP that contains the HTML/Markdown does not count and is forbidden as the Function 1/2/3/4 report delivery. Plain filenames, hidden attachments, “已生成” wording, or non-clickable paths do not count. The link text or the same line must clearly contain `下载`.
- Do not create or attach a ZIP/report package for Function 1/2/3/4 outputs. The report artifacts themselves must be two separate files on disk: one `.html` and one `.md`. If the runtime tries to package them into a ZIP, discard that package for delivery and recreate/export the two individual files.
- Before sending the final answer, first run `python scripts/cooplens_core.py pure-report-file-check <task-name>.html <task-name>.md` to verify the local deliverables are truly a standalone `.html` file and a standalone pure Markdown `.md` file. A file whose visible name contains “HTML” but whose actual extension is `.zip`, or a ZIP containing an HTML-looking file without `.html` suffix, is not a valid HTML deliverable.
- Then save the exact final-answer draft to `final-answer.md` and run `python scripts/cooplens_core.py strict-final-delivery-check final-answer.md`. If it fails for any reason, do not send the answer; regenerate the two direct single-file links and rerun the script until it passes. Then also run `html-delivery-check`; Function 3 additionally runs `function3-delivery-gate-check`.
- Static HTML must use native HTML and CSS only: no JavaScript, no framework, no external CSS, no component library, no CDN, no images, no embedded tracking, no iframe and no hidden network calls.
- HTML must be a complete standalone document, not a fragment: `<!doctype html>`, `<html lang="zh-CN">`, `<head>`, UTF-8 charset, viewport meta, inline `<style>`, `<body>`, `<main>`, and matching closing tags are mandatory.
- HTML must be suitable for phone reading: viewport meta, single-column card layout, readable Chinese line-height, responsive width, large tap targets, breakable long links, accessible headings and enough spacing. Use visible color differentiation such as gradient hero, colored section cards, badges, callout boxes and distinct TOC chips while staying native HTML/CSS only. Markdown TOC/source links must render as clickable anchors that jump to the corresponding section, raw Markdown link syntax must not remain visible, and section/card containers must be closed.
- HTML must use the strict mobile WebView profile: `safe-html-build` must create ASCII-only element ids and internal anchors such as `sec-...`; visible Chinese heading text must not be used directly as an `id` or `href`. External `href` values must be ASCII-safe, stripped of accidental Chinese/full-width trailing punctuation, and must start with `http://` or `https://`. Visible Markdown separators must render as `<hr>`, not as `---` paragraphs. The page must include a visible hero title and a task-derived browser title; generic titles and visible internal version/generator wording are not allowed.
- HTML browser title and hero title must never be copied from `## 目录`, `目录`, `正文`, `重要声明`, or raw Markdown heading syntax. If the Markdown lacks a valid `# 报告标题`, derive a clean task title from the user request or artifact filename before running `safe-html-build`. A page whose `<title>` or hero `<h1>` is `## 目录` must be treated as failed HTML, even if a desktop browser opens it.
- Markdown and HTML must contain the same facts, same order, same conclusion and same source boundaries. HTML may add style/navigation only, not new visible analysis content.
- HTML must be generated through the safe-build gate, not hand-written as a separate answer. Required command: `python scripts/cooplens_core.py safe-html-build <report.md> --out <task-based-name>.html --error-out <task-based-name>_html_audit.json`, then `python scripts/cooplens_core.py html-syntax-check <task-based-name>.html`, `python scripts/cooplens_core.py html-report-check <task-based-name>.html`, and `python scripts/cooplens_core.py html-render-gate-check <report.md> <task-based-name>.html`.
- Do not repair HTML by hand after generation. If validation fails, repair the Markdown source or its directory headings, then rebuild from Markdown. A file that lacks the current safe-renderer marker, contains Chinese `id` values, unsafe `href` values, raw `---` separators, or a generic `CoopLens Report` title must be treated as failed HTML even if a desktop browser can open it.
- HTML is a required default deliverable, not an optional extra. A normal final answer for Function 1/2/3/4 is invalid unless it contains visible, clickable, task-named, direct download links for both the generated static webpage `.html` and Markdown `.md` report. The downloadable targets must be the pure HTML file and the pure Markdown file themselves, not a ZIP/archive/folder/package that contains them. Merely saying “已生成 HTML / 静态页面” without a `.html` download link is a failed delivery; merely attaching or naming the Markdown without a `.md` download link is also a failed delivery; using a `.zip`/archive link instead of either direct file link is a failed delivery.
- If HTML rendering or HTML 语法校验 fails, do not deliver the broken HTML and do not silently omit it. Show the user-visible failure reason in plain language, repair or regenerate the Markdown/TOC/anchors/title/source links, then run the full gate again. 不通过就重新生成：repeat this cycle until `html-syntax-check`, `html-report-check`, and `html-render-gate-check` all pass. The helper has a per-command safety cap to avoid infinite local loops, but the assistant must continue by correcting the Markdown and rerunning the gate rather than delivering failed HTML.
- Function 3 uses the same safe-build gate as Functions 1/2/4; because Function 3 has many candidate cards, it must additionally pass unresolved-anchor and duplicate-id checks before delivery. Function 3 final delivery must run `function3-delivery-gate-check`; if no direct pure `.html` download link and no direct pure `.md` download link appear, or if a ZIP/archive link is used as a substitute, the task is incomplete. Do not send the final answer; recreate direct file links and rerun the delivery gate until it passes.

- Artifact filenames must be based on the user’s analysis task, such as `{省份}-{项目或候选方向}-{报告类型}.md` and `{省份}-{项目或候选方向}-{报告类型}.html`. Do not name files after the runtime platform, generic runtime labels, browser/page labels, or source-collection labels. If the environment proposes a generic name, replace it with a task-derived Chinese slug before delivery.
- Every delivered Markdown and HTML report must visibly contain the fixed important statement near the top and again in `附录：重要声明与人工确认提醒` at the end of full reports. If a rank chapter exists, the HTML must also visibly contain `位次预估重要声明`, with the fixed important statement below it.

## Helper commands

Run from the skill root:

```bash
python scripts/cooplens_core.py runtime-date
python scripts/cooplens_core.py validate
python scripts/cooplens_core.py query --query "<学校/项目/专业>" --top 8
python scripts/cooplens_core.py rank-query --query "<学校或外方高校>" --top 8
python scripts/cooplens_core.py markdown-toc-check <report.md>
python scripts/cooplens_core.py safe-html-build <report.md> --out <report.html> --error-out <report_html_audit.json>
python scripts/cooplens_core.py html-syntax-check <report.html>
python scripts/cooplens_core.py html-report-check <report.html>
python scripts/cooplens_core.py html-render-gate-check <report.md> <report.html>
python scripts/cooplens_core.py html-consistency-check <report.md> <report.html>
python scripts/cooplens_core.py pure-report-file-check <report.html> <report.md>
python scripts/cooplens_core.py strict-final-delivery-check <final-answer.md>
python scripts/cooplens_core.py html-delivery-check <final-answer.md>
python scripts/cooplens_core.py function3-delivery-gate-check <final-answer.md>
# final-answer.md must contain exactly two visible direct report download links: one pure .html file and one pure .md file. Any .zip/archive/bundle/folder delivery link fails and must be regenerated.
python scripts/cooplens_core.py report-check <report.md>
python scripts/cooplens_core.py numeric-link-check <report.md> --annotate-out <marked.md>
python scripts/cooplens_core.py consolidated-source-check <report.md>
python scripts/cooplens_core.py official-latest-source-check <report.md>
python scripts/cooplens_core.py function2-check <report.md>
python scripts/cooplens_core.py function3-estimation-check <report.md> --annotate-out <marked.md>
python scripts/cooplens_core.py live-rank-estimation-check <report.md>
python scripts/cooplens_core.py rank-reasoning-check <report.md>
python scripts/cooplens_core.py personalization-check <report.md>
python scripts/cooplens_core.py public-platform-search-check <report.md>
python scripts/cooplens_core.py negative-consultation-check <report.md>
python scripts/cooplens_core.py graduate-outcomes-check <report.md>
python scripts/cooplens_core.py cscse-authentication-check <report.md>
python scripts/cooplens_core.py rank-workflow-check <report.md>
python scripts/cooplens_core.py rank-estimation-workflow-check <report.md>
python scripts/cooplens_core.py qs-latest-ranking-check <report.md>
python scripts/cooplens_core.py recommendation-split-check <report.md>
python scripts/cooplens_core.py recommendation-rating-check <report.md>
python scripts/cooplens_core.py manual-source-confirmation-check <report.md>
python scripts/cooplens_core.py parent-questions-check <report.md>
python scripts/cooplens_core.py postgraduate-recommendation-check <report.md>
python scripts/cooplens_core.py completion-gate-check <final-answer.md>
python scripts/cooplens_core.py final-product-audit-check <final-answer.md>
python scripts/cooplens_core.py html-important-statement-check <report.html>
python scripts/cooplens_core.py artifact-filename-check <final-answer.md>
python scripts/cooplens_core.py function3-deep-analysis-check <report.md>
python scripts/cooplens_core.py personalized-input-use-check <report.md>
python scripts/cooplens_core.py overseas-living-cost-check <report.md>
python scripts/cooplens_core.py link-check <report.md> --max-urls 20
```
