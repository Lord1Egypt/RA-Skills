---
name: content-publishing-suite
slug: content-publishing-suite-skill
displayName: Content Publishing Suite
version: "1.1.18"
description: This skill should be used when a fact-checked and compliance-approved final Markdown draft needs to be turned into multi-channel publishing assets — WeChat article (135-editor-compatible inline HTML), WeChat image-summary card (公众号发图/摘要图/图文卡/810×1080), LinkedIn post, standalone responsive HTML page, and an archive ledger (local record plus optional Notion entry). It only orchestrates publishing and format conversion; it does not repeat fact-checking and does not auto-publish. Can optionally pair with a dedicated WeChat-layout skill if one is installed. Trigger keywords: 发布物料, 排版并入库, 多平台发布, 定稿发到微信, 公众号发图, 摘要图, 图文卡, 810×1080, publishing suite, multi-channel publish, final draft to WeChat/LinkedIn, package for publishing.
description_zh: 内容发布套件
description_en: Content publishing suite
agent_created: true
---

# Content Publishing Suite

将一篇**已审核定稿**稳定转换为多个渠道的发布物料，并生成入库记录。本 Skill 是发布编排层，不做事实核验、原创性复核或跨材料审计（那些由上游 Skill 负责），也不自动执行任何外部发布动作。

> 本文档中 `{SKILL_DIR}` 自动替换为 Skill 实际安装路径。

## When to use

- 用户拥有一篇已通过终检的定稿（industry-deep-dive-pipeline 的 `07-final.md`，或显式标记「已审核」的等价 Markdown），要求产出微信 / LinkedIn / 独立 HTML / 入库物料。
- 用户要求"把这篇发到多个平台""生成发布包""排版并归档"。

## Do not use

- 内容尚未完成事实核验或合规审核 → 先走 industry-deep-dive-pipeline / claim-to-source-auditor / cross-material-consistency-auditor。
- 只需要单纯的微信排版且本地已安装专门的微信排版 Skill / 已有平台建稿流程 → 直接用该工具即可，无需本套件。
- 需要新写正文、改写或补充事实 → 属于写作/核验环节，不属于发布编排。

## Input

```yaml
draft:
  path:                     # 已审核定稿 Markdown
  title:
  author:
  date:
approval_gate:              # 必须满足其一
  final_check_json:         # industry-deep-dive-pipeline 产物；需 Gate B approved、red-line hits 0、credential/privacy P0 0
  reviewed_marker: false    # 或定稿首部带 `状态: 已审核` / `reviewed: true` 且用户确认
channels: [wechat, linkedin, html, archive]
output_dir:
external_action: dry-run    # 默认只生成不发送
read_only_upstream: true    # 不引入上游未覆盖的新事实
```

必须满足其一，否则拒绝进入：

1. 提供 `final-check.json`（industry-deep-dive-pipeline 产物）且 `Gate B: approved`、`red-line hits: 0`、`credential/privacy P0: 0`；或
2. 定稿文件首部带有显式 `状态: 已审核` 或 `reviewed: true` 标记，并由用户在请求中确认"已审核"。

下游若引入任何上游未覆盖的**新事实**，必须暂停并提示回退上游重新核验，不得静默发布。

## Output channels

| 渠道 | 产物 | 说明 |
|------|------|------|
| 微信长文 | `wechat_snippet.html`（可粘贴片段）+ `wechat_preview.html`（手机框预览） | 135 编辑器兼容内联样式；不自动建草稿 |
| 微信发图摘要 | `wechat_summary_card.jpg`（810×1080）+ `wechat_summary_copy.md` | 长文二次分发物料：主题图重排、摘要、关键词和原文链接占位；不替代长文封面 |
| LinkedIn | `linkedin-post.md` | hook + 正文 + 3-5 话题标签；中/英按目标读者 |
| 独立 HTML | `standalone.html` | 响应式单页，含目录与参考链接 |
| 入库 | `archive-ledger.json`（本地）+ 可选 Notion 记录 | 标题/渠道/时间/状态；可选 page ID 写入并回读 |

## Workflow

```
摄入定稿 → 输入门禁 → 封面 brief/prompt → 2.35:1 长文封面 → 摘要卡视觉重排 → 逐渠道生成物料 → 输出门禁（脚本校验）→ 生成 package-manifest → 入库台账 → 外部动作门禁（需确认才发送）
```

### Step 1: [Deterministic + LLM] Ingest and input gate

读取定稿 Markdown，确认满足输入门禁。记录标题、作者、日期、核心判断。未通过门禁立即停止。

### Step 2: [LLM] Generate per-channel assets

- **微信长文**：依 `references/wechat-style.md` 和 `references/wechat_layout_baseline.json` 将 Markdown 转为全内联 `<section>` HTML。唯一排版基线固定为：标题 23px 居中；摘要块 15px / 行高 1.7；正文 16px / 行高 1.8 / `margin-bottom:1.5em` / `letter-spacing:1px`；小标题 18px、`#1a1a1a`、`margin:2.5em 0 1em`、左侧 4px 深蓝线、`padding-left:10px`。**普通正文段落、列表、引用和表格信息条禁止设置 `text-align`，避免编辑器导入后触发“文字对齐异常”结构检测；只有标题需要居中时才允许 `text-align:center`，且仅作用于 `<h1>`。正文不要使用 `text-align:left/justify` 这类多余默认值。**生成器不得自行写入另一套字号。**微信长文摘要最多 120 字符，默认控制在 30 字符以内；必须与标题形成配合，作为正文引子或一句实质结论，禁止把摘要卡配文或首段长篇复制进来。**文末必须加 `<v2></v2>`；生成后必须运行 `scripts/validate_wechat_layout.py <snippet> --baseline references/wechat_layout_baseline.json --title <title>`。不通过即停止交付。绝不使用 `<style>`、`<script>`、外联 class、外层 `<div>` 容器。模板见 `templates/wechat-snippet.html`。
- **长文封面**：在任何摘要卡设计前，先建立封面 brief 和 prompt，生成无文字长文封面底图，并按 2.35:1 规则裁切成最终封面。记录 brief、prompt、原始生成图和最终封面路径；未完成封面链路不得进入摘要卡设计。
- **微信发图摘要**：封面完成后只加载 `tech-writing-pipeline` 的 **6.1「公众号发图摘要卡：固定骨架，有限自适应」**、`scripts/check_summary_card_6_1.py` 与 `scripts/summary_card_6_1_baseline.json`，以它们为唯一视觉与结构规范；本 skill 只负责编排、交付与台账，不能用本段摘要替代 6.1。规格属 B 层交付硬约束，按选定物料触发，写作阶段不加载。同步生成 `wechat_summary_card.jpg`（810×1080、3:4）和 `wechat_summary_copy.md`。卡片必须执行 A/B/C/D 四区、56px 左右安全边距、左对齐阅读路径、系列既定视觉语言、三色上限、一个主体结构加一个对照状态、主题行与一条最多三行的核心判断；仅能在主题隐喻、主体位置、同系列色盘微调、主题行和核心判断五项中自适应。不得把 2.35:1 长文封面机械裁切为摘要卡；A 区必须基于最终封面视觉进行重排。文案应保留长文的判断闭环，而不是只写一句口号；包含短摘要、关键词/Hashtags、`【原文链接：待填】`和后台使用说明。图片不预制公众号账号水印，平台上传后的自动标识即可。**摘要卡必须完整内嵌发布套件文档**：成品图路径、配图文字全文（可直接复制）、关键词和后台使用方式写入 `发布套件_<篇名>.md` 专节（对齐篇 2 格式）；单独的 `wechat_summary_copy.md` 只是资产副本，不能替代套件内文。
- **LinkedIn**：依 `templates/linkedin-post.md`，取独立英文正文文件的核心判断作 hook，正文压缩到 200-300 字，末尾 3-5 个话题标签。无 Markdown、无内部备注、无未公开数据、无流程元信息。**前置依赖硬规则：英文正文（`正文-EN`）定稿之前不得生成 LinkedIn caption；未完成时在发布套件与台账中把 LinkedIn/X 标记为"前置依赖：英文正文未完成"，不产出任何英文物料，不得从中文定稿直接翻译替代。**LinkedIn 正文应作为文章主目录下的独立内容文件，不以零散 `linkedin-post.md` 作为文章主文档。
- **Substack / 英文长文**：英文长正文作为文章主目录下的独立 `正文-EN` 文件；发布套件只登记标题、副标题、渠道说明和文件路径，不重复粘贴全文。
- **英文正文门禁**：英文正文完成后、任何 LinkedIn/X/摘要英文物料生成前，加载 `tech-writing-pipeline/references/english-ai-writing-strategy.md`，建立 `Claim / Evidence / Counterargument / Boundary / What the reader should not infer` claim map，并通过作者性门禁。P0 包括虚构或无来源归因、空泛开场承载主信息、反方只列不裁决、中文句序直译；P1 包括组合式修辞包装、模板化对举、破折号或三项并列密集、积极形容词超过证据。单个风格词、服务于机制说明的 LinkedIn 清单或有事实功能的结构母题不单独构成 AI 腔；detector 分数不进入发布 PASS/FAIL。
- **独立 HTML**：依 `templates/standalone.html`，生成响应式单页，含标题/作者/日期/目录/正文/参考链接。平涂风格、大量留白、**绝对排除科技电路风、发光、数字网格**。
- **入库台账**：追加一条记录到 `archive-ledger.json`（不存在则新建），字段见 `templates/archive-record.json`。

### Step 3: [Deterministic] Output gate (script validation)

运行确定性脚本校验每个渠道文件是否满足格式合约。包含微信摘要卡时，必须同时启用视觉链路门禁：

```bash
python3 {SKILL_DIR}/scripts/validate_publish_output.py \
  --package <output_dir> --enforce --require-visual-chain \
  --cover-brief <cover_brief.md> \
  --cover-prompt <cover_prompt.md> \
  --cover-image <cover-2.35.jpg> \
  --summary-card <wechat_summary_card.jpg> \
  --summary-card-html <wechat_summary_card.html> \
  --summary-contract <summary-card-contract.json> \
  --summary-copy <wechat_summary_copy.md> \
  --summary-baseline <approved_baseline.html> \
  --summary-checker <tech-writing-pipeline>/scripts/check_summary_card_6_1.py
```

P0 阻断（如微信缺 `<section>`/`<v2>`、含 `<script>`、HTML 无结构、台账缺字段、封面链路缺文件、封面比例错误、摘要卡尺寸错误或 6.1 baseline 失败）；P1 提示（如 LinkedIn 超长）。脚本退出码 2 表示存在 P0。作者内部笔名清单通过环境变量 `PUBLISH_PEN_NAMES`（逗号分隔）传入，不硬编码。

### Step 4: [Deterministic] Package and ledger

```bash
python3 {SKILL_DIR}/scripts/build_publish_package.py \
  --draft <定稿.md> \
  --approved-gate <final-check.json 或 --approved 标志> \
  --channels wechat,linkedin,html,archive \
  --output <output_dir> \
  --root-layout-dir <项目根目录> \
  --root-layout-stem <篇名-排版-日期>
```

脚本产出各渠道文件、更新 `archive-ledger.json`、输出 `package-manifest.json`。

### Step 5: [Human] External-action gate

任何实际推送、经文章管理平台建草稿、写 Notion 的动作前，**必须列出目标并取得用户确认**。默认只生成不发送（`--dry-run`）。确认后才执行，且写后必须回读核验（Notion 用 page ID 写入、幂等键防重复）。

## Hard Rules

1. 未通过输入门禁（无 `final-check.json` approved 或无显式"已审核"标记）一律拒绝进入，不得代替上游做核验。
2. 发布物料中零对话痕迹、零流程元信息、零内部备注/笔名/未授权数据。
3. 微信物料必须全内联样式、`<section>` 包裹、文末带 `<v2></v2>`；禁止 `<style>`/`<script>`/外联 class/外层 `<div>`。
4. 工作文档与发布物中人名一律用真实姓名或中性表达；作者内部笔名从 `PUBLISH_PEN_NAMES` 读取用于拦截，不硬编码进本 Skill。
5. 任何外部动作（推送、建草稿、写 Notion）默认 `--dry-run`，必须先列目标并取得用户确认；写后必须回读核验。
6. 凭据只走环境变量（Notion 用 `NOTION_TOKEN`、库 ID 用 `NOTION_DB_ID`；文章管理平台经既有 MCP/连接器），绝不硬编码。
7. 微信发图摘要卡必须为 810×1080（3:4），且图与文案都围绕同一篇已审核长文；图中不重复添加公众号账号水印。台账需记录 `summary_card` 路径。
8. 跨渠道数字一致性：同一篇长文衍生的多渠道物料（微信 / Notion / 平台版）发布前必须做关键数字与案例名的跨文件比对，不一致一律退回上游，不得带歧义发布。
9. 一旦交付包含微信发图摘要，必须先加载 `tech-writing-pipeline` §6.1、对应基准与校验器并逐项验收；未加载或无法访问时，停止摘要卡制作并说明缺少的规范，不能凭本 skill 的简写规则自行补全。此处只加载该物料规格，不要求通读整份写作参考层。
10. 脚本只读取用户指定的定稿、写入用户指定的输出目录；不引入网络外送。
11. 发布套件 ready 的前置条件包含封面 brief、封面 prompt、最终 2.35:1 长文封面、摘要卡 A 区视觉依赖、摘要卡文章级内容契约、摘要卡 6.1 范围门禁和 baseline 逐字段门禁；基础渠道格式脚本通过不能替代这些视觉、内容与流程门禁。
12. 微信排版和摘要卡都必须使用确定性校验器：排版校验字号/行高/颜色/间距/背景/结构；摘要卡校验 A/B/C/D 文本、A 区素材、背景、位置和配文锚点。只有自然语言复核没有脚本结果时，不得标记 ready。
13. 英文渠道物料必须继承英文正文的 claim map、作者性门禁和事实边界；不得绕过英文正文直接从中文定稿生成英文 caption、摘要或社媒文案。
14. 微信长文摘要必须单独执行长度与功能门禁：不得超过 120 字符，通常控制在 30 字符以内；摘要要与标题互补，承担正文引子或实质结论之一，不得使用摘要卡长配文或正文首段替代。

## Failure Handling

| Scenario | Action |
|---|---|
| 输入门禁不满足 | 停止；输出缺失项清单并提示先完成上游核验 |
| 输出门禁出现 P0（退出码 2） | 不生成 manifest；列出每条 P0 及所在文件，修复后重跑 |
| 下游发现上游未覆盖的新事实 | 暂停发布，回退上游重新核验，不得静默发布 |
| 外部写入失败 | 先重试一次并交叉验证；仍失败则保留本地台账、报告原因，不留半写状态 |
| 定稿含未解析的复杂内嵌内容（图表/带字图片） | 标记为不可解析，请求文本抽取或人工确认 |
| 目标渠道未指定 | 默认生成全部四渠道并提示 |

## Output Format

```text
<output_dir>/
├── wechat_snippet.html
├── wechat_preview.html
├── summary-card-contract.json
├── wechat_summary_card.jpg
├── wechat_summary_card.html   # 6.1 视觉链路门禁所需的卡片 HTML
├── wechat_summary_copy.md
# 项目根目录同步：篇名-排版-日期.html + 篇名-排版-日期_snippet.html
├── linkedin-post.md
├── standalone.html
├── archive-ledger.json        # 追加式入库台账
└── package-manifest.json      # 本次发布包清单（各文件路径 + 门禁结果）
```

gate 报告：P0/P1 列表；有 P0 时明确标注"未通过、禁止发布"。

## References

| 资源 | 用途 |
|------|------|
| `references/wechat-style.md` | 微信 135 内联样式规范、组件样式代码 |
| `references/wechat_layout_baseline.json` | 微信字号、行高、颜色、间距、背景和结构的唯一基线 |
| `scripts/validate_wechat_layout.py` | 微信排版确定性校验器，阻断样式漂移 |
| `references/channel-contracts.md` | 各渠道输出格式合约（校验规则依据） |
| `templates/wechat-snippet.html` | 微信片段模板 |
| `templates/linkedin-post.md` | LinkedIn 帖子模板 |
| `templates/standalone.html` | 独立 HTML 单页模板 |
| `templates/archive-record.json` | 入库台账条目模板 |
| `templates/notion-mapping.example.json` | Notion 映射样例（凭据走 `NOTION_TOKEN` 环境变量，库 ID 占位符不写真实值） |
| `scripts/build_publish_package.py` | 组织产物、更新台账、输出 manifest |
| `scripts/validate_publish_output.py` | 各渠道格式合约校验，输出 P0/P1 gate |
| `tech-writing-pipeline/references/english-ai-writing-strategy.md` | 英文正文的 AI 强特征、claim map、作者性与渠道门禁唯一规则源 |

## Verification

- [ ] 运行 `validate_publish_output.py --enforce --require-root-layout --require-visual-chain` 及完整参数，退出码 0（无 P0）。
- [ ] 封面 brief 与 prompt 已落盘，最终长文封面为 2.35:1；摘要卡依赖最终封面视觉，不使用初版或从零自由设计资产。
- [ ] 微信片段含 `<section>`、文末 `<v2></v2>`、无 `<script>`/`<style>`/外层 class。
- [ ] 微信片段通过 `validate_wechat_layout.py`：标题 23px、小标题 18px、正文 16px/1.8，颜色、间距、背景与强制结构均无漂移。
- [ ] 根目录同步落盘 `篇名-排版-日期.html` 与 `篇名-排版-日期_snippet.html`；发布目录保留 `wechat_preview.html` 与 `wechat_snippet.html`，两组文件内容一致。
- [ ] 摘要卡文章级契约已落盘，包含系列标签、主题行、核心判断、页脚标题、A 区素材、卡片背景和配文锚点。
- [ ] 微信发图摘要卡为 810×1080（3:4）、主题图为基于最终封面的竖幅重排而非横版硬裁、无重复账号水印；摘要副本含关键词和原文链接占位；6.1 范围门禁、内容契约和 baseline 逐字段比对均通过。
- [ ] LinkedIn 无 Markdown 标记、无内部备注/笔名。
- [ ] 独立 HTML 以 `<!DOCTYPE html>` 开头，无科技电路风/发光/数字网格。
- [ ] `package-manifest.json` 各渠道均生成，`archive-ledger.json` 已追加一条。
- [ ] 外部动作前已取得用户确认；默认 dry-run。
- [ ] 摘要卡制作前已加载 6.1 基准与校验器并逐项验收，未以发布套件的简写规则替代；未加载时已停止制作并记录缺失规范。

## Pitfalls

- 把未审核稿当作已审核直接发布——必须先过输入门禁。
- 英文正文未完成就生成 LinkedIn caption——LinkedIn 必须从英文正文取核心判断；没有 `正文-EN` 就把 LinkedIn/X 在套件与台账中标记为前置依赖，不预置任何英文物料，也不得从中文定稿翻译充当。
- 摘要卡配文只存成单独 md 文件、发布套件文档里只给路径——摘要卡的成品图、配图文字全文、关键词和使用方式必须完整内嵌发布套件文档（对齐篇 2 格式），否则发布时找不到可直接复制的内容。
- 发布套件文档只写标题、摘要和几个文件路径——套件必须同时写清每个渠道的文件、标题、摘要/正文、关键词、操作步骤、渠道阻塞依赖、台账状态和外部动作状态；被前置依赖阻塞的渠道也要写清原因，不能用空文件或占位文案伪装完整。
- 微信普通正文段落误加 `text-align:left/center/justify`，编辑器内容结构检测会将其标为“文字对齐异常”，并可能造成不同终端显示不一致。普通正文、列表、引用和表格信息条不写 `text-align`；仅标题 `<h1>` 保留居中对齐。
- 微信物料误加 `<style>`/外层 `<div>`，粘贴进 135 编辑器后样式被剥离。
- 同时存在多套排版基线（例如 23/18/16 与 24/20/16）会让生成器、模板、校验器和历史文件各自漂移。排版基线必须集中在 `wechat_layout_baseline.json`，任何生成器或模板修改都必须先改基线并重跑校验，不能在 SKILL.md、参考文档和脚本里分别维护字号。
- 只生成发布目录内的 `wechat_preview.html` / `wechat_snippet.html`，不落根目录标准命名，会造成项目归档缺件。发布完成后必须同步根目录 `篇名-排版-日期.html` 与 `_snippet.html`，并在 manifest 中登记。
- LinkedIn 残留 Markdown 加粗/列表符号或内部笔名，平台不渲染或泄漏内部信息。
- 在 example/模板里写真实 Notion 库 ID 或凭据——一律用占位符与环境变量。
- 外部写入未回读核验，导致重复写入或半写状态。
- `validate_publish_output.py` 会重写包目录中的 `publish-gate.json`。如果门禁报告还承载英文渠道、事实口径或 dry-run 的人工记录，运行确定性校验后必须重新合并这些字段，并再次解析 JSON，不能把脚本生成的最小报告直接当作完整交付记录。
- 视觉链路的 PNG 尺寸解析必须使用真实 PNG 签名字节（`b"\\x89PNG\\r\\n\\x1a\\n"`）；若源代码误写成双反斜杠字面量，校验器会误报“无法读取 PNG/JPEG 尺寸”。遇到该错误先检查文件签名与解析器，再改用 JPG 绕过，修复后重新运行完整视觉链路门禁。
- 下游悄悄补一句"新事实"绕过上游核验——任何新事实都要回退上游。
- 把横版封面当公众号发图摘要卡——长文封面是 2.35:1；发图摘要是 810×1080 的独立二次分发物料，需主题图重排、长文摘要、关键词和原文链接占位。
- 先做摘要卡、后补封面 prompt/封面图——封面视觉链路必须先完成：封面 brief/prompt → 2.35:1 长文封面图 → 以最终封面为视觉基准重排 A 区并叠加系列标签 → 摘要卡结构门禁 + baseline 逐字段门禁 + 手机视觉对齐门禁 → 发布套件 ready。摘要卡 6.1 结构通过只证明尺寸、布局和文字字段正确，不能替代最终封面依赖和视觉对齐检查；因此必须使用 `validate_publish_output.py --require-visual-chain` 把这些依赖变成 P0，而不能只把顺序写在 Pitfalls 里。当前系列按 §6.1 的 baseline v2：封面图完整铺满 810×400、无承接条；`images/boundary-layer-summary-card.html` 是 343px + 57px 的旧结构，不得作为母版。文字规范、基准 JSON、校验器与 v2 基准卡必须一致，任何升级同步重定 baseline。
- 把英文正文、LinkedIn 正文和摘要卡配文分别拆成多个根目录小文件——参考系列归档结构，渠道正文分别保留为 `正文-EN`、`正文-LinkedIn-EN` 等主文档，摘要卡配文、封面 brief、渠道短句和发布动作集中写入一个 `发布套件` 文档；图片、HTML、JSON 仅作为发布资产和机器门禁文件。
- 在摘要图里再加“公众号·账号名”水印——上传后平台会自动显示账号标识，设计图不重复加，避免视觉重叠。
- 只加载发布套件并按其中的短说明制作摘要卡——这会遗漏 A/B/C/D 分区、固定文字层级、有限自适应边界和手机缩略验收。只要交付摘要卡，就必须加载 §6.1 及其基准、校验器；发布套件不再作为摘要卡视觉规范的替代品。规格必须完整验收，但不要求加载写作参考层全文。
- Markdown 表格转设计图后，微信片段不能继续保留脚本生成的残缺表头片段；应删除全部自动表格节点，只保留一个符合微信内联规范的图片占位，并在独立 HTML 中插入同一张表格设计图，避免重复占位或移动端表格溢出。
- 微信正文中的 Markdown 表格不能按逐行 `<table>` 生成：这会把分隔行 `---` 当作数据，并在手机端形成深色大色块。默认先判断该表是否需要作为干净图片交付；若需要图片，微信片段只放一个无标题、无说明、无额外装饰的 `<img>`，图片文件与 HTML 一起登记到 manifest。其他表格才改为浅底竖向信息条，独立 HTML 可保留完整 `<table>`。信息条的标签样式放在 `span` 或 `section`，正文 `p` 仍复用唯一排版基线，避免校验器把新组件误判为字号和间距漂移。
- 使用 `--require-visual-chain` 时，必须同时传入根目录排版参数和一个真实存在的已验收摘要卡基准文件；不要猜测不存在的 baseline 路径，也不要把“校验当前卡本身”伪装成跨卡基准。若仓库没有独立基准文件，应先定位此前已验收的摘要卡 HTML，或明确只运行范围门禁并记录未完成逐字段基准比对。
