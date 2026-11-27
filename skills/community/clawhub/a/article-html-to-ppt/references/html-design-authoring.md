# HTML 设计面 → 原生对象（`html-import`）

`create` 的页面默认写成受限 HTML/CSS，再由固定工具编译为现有场景记录。来源可以是报告/文档、
逐页稿或用户口述文字；不需要生图模型。浏览器提供真实的网格/弹性布局与文字测量，模型无需手算绝对坐标；
编译结果仍是 `task.json` 中的 text/shape/path/table/chart/image 节点与内容记录，
`validate`、字体预检、构建、渲染、独立审核与交付门禁完全不变。HTML 不进入 PPTX，
任务中的脚本从不执行：页面里出现 `<script>` 会被拒绝，提取器由工具自带并注入。

先运行 `python3 -m engine design capabilities`。工具在当前执行环境中实测浏览器的文字提取与 PNG 输出，并列出当前 `fontconfig` 已匹配的常见拉丁/中文字体（`fonts.latin` / `fonts.cjk`，实际渲染仍需 `preflight` 核验）。
`html_design_surface.available` 为 false 时，查看 `reason`、`cause`、`browser` 与 `next_action`。
macOS 上，`sandbox_parameters_mac.mm` 报 `Input/output error (5)` 时会返回 `HTML_BROWSER_SANDBOX_BLOCKED`，原因标为 `nested_browser_sandbox_blocked`。在 Codex 这类受限宿主中，按宿主的审批流程在外层沙盒之外重跑 `capabilities`，通过后用同一方式运行 `html-import`。保留 Chromium 自身的沙盒。宿主无法放行时可用 `engine design author` 继续生成原生对象。
已安装独立 Chromium Headless Shell 时，可将 `PPTSMITH_BROWSER` 设为其可执行文件的绝对路径，再运行同一项探测（无效路径会明确返回 `HTML_BROWSER_OVERRIDE_INVALID`）。
工具优先使用 PATH 中的 `chrome-headless-shell` 或 `chromium-headless-shell`，随后自动探测本机 Playwright 缓存中的 `chrome-headless-shell` 及系统浏览器。macOS 下默认使用临时浏览器配置与模拟钥匙串，若受限沙盒拦截宿主 `~/Library` 访问会自动用隔离临时 `HOME` 重试一次。
每次成功的页面导入用同一浏览器进程提取布局并截图。图片重建仍走 recreate，原生模板改页仍走 template。
HTML 预览是作者自己的草图，**不得**登记为外部设计目标或 recreate 目标。

## 流程

1. **准备来源**。用户粘贴/逐页稿保存为 `user-input.md`；PDF、DOCX、网页等文档先抽取为带页/节锚点的
   文本，如 `sources/report.md`（`## p.3 经营概况` 这类标题行），作为追溯依据。
2. **内容重构并写 `page-plan.md`**：定每页首要信息与主视觉；同一组数据只编码一次（图与同数表合并，
   数值直接标在图上）；按读者问题而非来源章节编号分组；限定、口径和来源仍然上屏。
   文档转演示时，先定叙事与页序（封面、目录/导语、章节、正文、结论、结尾），页数不等于来源页数，但须与信息体量匹配：长报告（如含 10+ 独立趋势或专题）应按大章合理分配展开页，不要为了硬压总页数将 4–5 个独立子主题挤成一页小字卡片墙，也不要把原著并列的两大章节生硬揉成一张章扉页。
   - **章节编号与扉页 1:1 闭环**：一旦设置目录与章扉页，目录中的**每一个一级章节**都须配齐对应的章节起始页（不可漏掉首章或后半部分章节；短简报若不设章扉页则全册统一不设），且**目录编号、章扉页大号与正文眉标编号必须使用同一套体系**（严禁目录按 `01–04` 编，章扉页却改按原著集群号编 `01–02`）。
   - **同页编号阅读顺序一致**：当眉标或标题并列多个编号主题（如“趋势 03 & 04”）时，页面从左到右/从上到下的排列顺序须与编号一致，不得倒序。
   逐页稿还须遵守 [逐页稿合同](outline-to-deck.md)。
3. **整册主题（行业适配 + 品牌特征提取）**：先识别内容所属行业与是否存在明显品牌主体，确定共享的画布、色板角色、固定字阶（建议 5–7 档）、统一字体栈、页眉/眉标编号与页脚规范（如封面不印页码），记录在 `brief.md` 中并作为全册 CSS 基线。各页复用同一主题，正文构图随内容关系变化。
   - **优先提取内容中的品牌特征**：当源文档或正文明确归属某品牌/机构（如麦肯锡/BCG 研报、企业财报、产品发布会、政企方案）且用户未要求换风或去品牌时，优先从源 PDF/DOCX/PPTX 的封面、章节页、图表主色与留白气质中提取品牌视觉特征；仅有纯文本时，结合该品牌公认的色系、克制程度与排版语境定调。未提供官方 Logo 文件时不得手绘或伪造 Logo。
   - **按行业语境定制风格**：无特定品牌（或在品牌基调之上）时，按行业、受众与文体匹配视觉系统，而不是套用单一默认风格（见下文[行业与品牌风格定调](#行业与品牌风格定调)）。
4. **图片**：用户提供的 logo、产品图、照片先登记，再在 HTML 中引用：

```bash
python3 -m engine design ingest --task-dir "$TASK" --file logo.png --asset-id logo --role illustration \
  --pages page-1 --source 用户提供的公司标识
```

5. **逐页写 HTML 并导入**：

```bash
# 逐页稿
python3 -m engine design html-import --task-dir "$TASK" --page page-2 --file pages/p02.html \
  --source-file user-input.md --source-heading 第02页
# 文档来源（可重复多个 --source-file）
python3 -m engine design html-import --task-dir "$TASK" --page page-5 --file pages/p05.html \
  --source-file sources/report.md --source-kind document
```

6. **看结果再改**：打开返回的 `preview`（浏览器截图），处理 `design_lint`、`untraced`、`coverage`、
   `browser_warnings`，修改 HTML 并重复导入。截图只用于迭代；验收以构建后的真实 PPTX 预览为准。
7. **轻量补写元数据与备注**（无需导出整册 `author.json`）：用 `set-meta` 填写 `design.brief`，用 `set-page` 逐页写入备注与 `composition`（`reading_path` 引用导入后的内容 ID）；中途增删或调整页序使用 `add-page` / `remove-page` / `reorder-pages`：

```bash
python3 -m engine design set-meta --task-dir "$TASK" --brief-file brief.md
python3 -m engine design set-page --task-dir "$TASK" --page page-2 \
  --notes-file notes/p02.txt --composition-file compositions/p02.json
```

完成后运行 `validate --complete`、`preflight`、`build`，再进入独立审核与交付。局部微调既有对象可用 `patch`；仅在需要整册离线重构节点时才使用 `compact` + `author`。

导入只替换该页的场景与内容记录（图片随 `data-asset` 一起重新生成，不会丢失）。`composition`
引用的 ID 若已不存在，会被移除并在结果中标记 `composition_reset: true`。给关键元素设置稳定的
`data-cid` 可避免这种情况。

## 画布与结构

- 恰好一个 `id="slide"` 的根元素，尺寸等于任务画布，**1 CSS px = 1 pt**（如 1440×810 或 960×540）。
- 推荐：根元素 `position:relative`，大区块绝对定位，区块内部用 flex/grid 流式排版。
  长度不确定的文字放在流式容器里，不要用固定 `top` 逐行摆放。
- 每个文字块是一个元素；同一句内的样式变化用内联 `span`/`b`，显式换行用 `<br>`，正文的 `data-cid` 放在外层文字块。不要在同一元素中
  混排文字与块级子元素。单行标签加 `white-space:nowrap`，防止目标软件换行不同。

## 支持与不支持

| 可用 | 编译为 |
| --- | --- |
| `background-color`（可带 rgba 透明度）、`border`、统一或不对称 `border-radius` | 矩形/圆角矩形；不对称圆角编译为精确三次贝塞尔自由曲线；单边边框为独立细矩形 |
| 文字：`font`、`color`、`line-height`、`letter-spacing`、`text-align`、`padding` | 原生文本框；内联样式为 spans；精确行高 |
| `<table>` 的 `colspan`/`rowspan`、格内文字样式、底色、对齐、内边距、四边实线 | 原生表格保留合并区域与局部文字格式，格内 `p`/`div` 段落以换行分隔；其他边线样式会提示并按实线绘制 |
| `<svg data-native-svg>` 内的 path、line、rect、circle、ellipse、polygon、polyline | 可编辑自由曲线；路径支持绝对和相对 M/L/H/V/Q/C/Z，可用 g 分组变换，圆弧形图元转为三次曲线 |
| 带 `data-chart` 的元素 | 原生图表（数据可编辑，含堆积柱/条图） |
| 带 `data-asset="资产ID"` 的空元素（可加 `data-fit="cover"`、`border-radius`、`data-image-layer="background"`） | 原生图片（可替换，支持圆角透明裁切），预览中由工具填入实际图片 |

不支持：`img`/`script`/`iframe`/表单/链接、`url()`、`@import`、`@font-face`、事件属性、
`svg <use>`。渐变、背景图、`transform`、竖排在报告中给出警告；阴影被忽略；
`opacity` 请改用 rgba；`::before/::after` 的文字与列表符号不会被提取，
需要的符号请写成真实文字。
越出画布边缘的圆形/圆角装饰会按画布裁切为自由曲线，保留真实弧线。`reference`/`target` 资产不能放到页面上；`raster_data` 图片需用作者 JSON
绑定内容并登记接受。

## 数据属性

| 属性 | 用途 |
| --- | --- |
| `data-cid="p6-title"` | 指定内容 ID（`composition.reading_path`、`claim_content_id` 引用） |
| `data-src="sources/report.md / p.3"` | 该元素及子元素的来源定位；缺省为来源文件 + 标题或页 ID |
| `data-authored`（= `wording`） | 模型撰写/提炼的措辞（断言标题、摘要、标签）；**其中数字必须出自来源** |
| `data-authored="derived"` | 由来源数据计算得到的值（合计、差值、占比），计算方法写入 `page-plan.md`；也支持标在表格的单个 `<tr>`/`<td>`/`<th>` 上，其余数据格仍严格核对来源 |
| `data-authored="nav"` | 页码、章节编号、页眉等导航标记 |
| `data-native-svg` | 将支持的路径与图元编译为原生形状；未标记的 SVG 会被忽略并警告 |
| `data-chart='{...}'` | 原生图表规格，见下 |
| `data-asset` / `data-fit` | 已登记图片的位置与适配方式（`contain` 默认，`cover` 裁切铺满） |

图表规格（元素留空即可，预览由工具按规格绘制；编译时生成原生图表）：

```json
{"type": "line", "categories": ["1月", "2月"], "min": 75, "max": 100, "major": 5,
 "series": [{"name": "准时足量到货率（%）", "values": [82, 85], "color": "4B4FD6", "area": true}],
 "labels": true, "markers": true, "font": "Inter"}
```

`type` 支持 `line`、`column`、`bar`、`stacked_column`、`stacked_bar`、`pie`、`doughnut`。每个系列的数值个数须与分类数一致。折线系列可设 `area: true`。省略 `font` 时原生图表继承本页主要字体。
开启 `legend` 后，可设 `legend_position` 为 `bottom` 或 `right`。`label_number_format` 和 `axis_number_format`（或 `axis.number_format`）接受 Excel 数值格式（如 `0.0%`，数据 0.25 显示为 25.0%）。HTML 草图预览显示常见小数、千分位及百分比格式。其他格式会提示 `CHART_LABEL_FORMAT_NATIVE_PREVIEW_REQUIRED`，请查看原生 PPTX 渲染。含前导零或超过 JavaScript 安全整数范围的分类、系列编号用引号写为字符串，以保留全部数字。
饼图和环图使用一个非负系列，总和须大于零。`colors` 按分类循环设置扇区颜色（其他图表按系列着色），`label_colors` 可逐扇区设置标签颜色。环图的 `hole_size` 范围为 10–90，表示内半径占外半径的百分比。
截断数值轴时须在页面上说明，并保留原稿刻度。`major` 为正数，显式刻度最多允许 200 个区间。
**单值轴同量纲红线**：`column`/`bar`/`line`/`stacked_*` 等单数值轴图表严禁混放不同物理或统计量纲的指标（如把 `GW` 电力容量与 `%` 占比、或金额与倍数并排画在同一根 Y 轴上）；多量纲指标必须拆为两个独立图表或“图 + KPI 卡”，违反将触发 `CHART_MIXED_UNITS` 阻断错误。

## 追溯与覆盖

`--source-file`（逐页稿可配 `--source-heading` 截取该页）启用两个方向的检查：

- **上屏 → 来源**：文字、表格单元格、图表分类与数值逐项在来源中查找（忽略空白与 `·→⇄⚠` 等装饰符）。
  普通文字和表格按原文匹配，数字须完整。改写文字（`wording`）按十进制数值和百分号核对，识别正负号、千分位、全角数字及等值小数。图表原始数值按大小和符号核对；涉及单位换算时，应注明计算依据。`derived`、`nav` 记为已核对并附不确定说明。
  其余记录返回 `untraced_content`，**任务不变**：修正措辞或数字，或确认属于有意撰写后加对应标记。
- **来源 → 上屏**：报告未出现的数字与短语。逐页稿默认完整上屏，数字缺失必须处理；文档转演示是有选择的
  提炼，覆盖报告用于确认没有漏掉关键数据，而不是要求全文上屏。

没有来源文件时只能用 `--assume-checked` 声明已人工核对。

## 版面检查（`design_lint`）

导入在浏览器几何上自动检查。存在**错误**时返回 `imported_with_lint_errors`（退出码 1），保留 `preview.png` 与 `report.json` 供排查，**不写入 `task.json`**，修正后重新导入；仅有警告时写入并返回 `imported_with_findings`：

| 代码 | 级别 | 含义 |
| --- | --- | --- |
| `TEXT_OVERLAP` | 错误 | 文字与文字、表格、图表或前景图片相交 |
| `TEXT_OVER_BACKGROUND_IMAGE` | 警告 | 文字叠在声明为 `data-image-layer="background"` 或大面积底层 `cover` 背景图上，须在真实预览核对对比度 |
| `TEXT_OUTSIDE_CONTAINER` | 错误 | 文字超出所在卡片/色块 |
| `TEXT_OVERFLOWS_BOX` | 错误 | 固定尺寸元素放不下文字（隐藏行/列） |
| `OUTSIDE_SLIDE` | 错误 | 对象超出画布 |
| `CHART_MIXED_UNITS` | 错误 | 单值轴图表的分类或系列混用了明显不同的物理/统计量纲（如 `GW` 与 `%`） |
| `CJK_TEXT_WITHOUT_CJK_FONT` | 警告 | 字体栈中未识别出常见中文字体名，用字体预检核对实际字形与替代字体 |
| `SMALL_TEXT` | 警告 | 小于 9pt（按 1440 宽等比换算） |
| `FLAT_HIERARCHY` / `WEAK_HIERARCHY` | 警告 | 字号少于 3 级，或最大字号不足正文 2.2 倍 |

警告可以有正当理由（如密集附录页），须在 `page-plan.md` 说明。机器检查只排除明显缺陷，
不证明设计质量；独立审核仍看实际 PPTX 预览。

## 字体

`font-family` 写成“拉丁字体, 中文字体”栈（如 `'Inter','Noto Sans CJK SC'`），编译时自动设置
`ea_family`。只用本机已安装、目标软件可用的字体；不要依赖网页字体。符号（⇄ → ✓ ⚠ ₂）放在
确认含该字形的字体中，`preflight` 会按实际使用的字体逐个字形核对。

## 行业与品牌风格定调（设计坐标，不是固定模板）

动手写第一页 HTML 前，先在 `brief.md` 写清本次的**行业语境、品牌提取依据（若内容含品牌）与整册 CSS 主题变量**，避免中途风格漂移或逐页字号/眉标失控：

- **品牌优先原则**：内容中出现明确品牌主体时（例如麦肯锡报告、小米/苹果产品稿、特定银行或车企方案），先从输入材料提取主色、辅色、底色明暗倾向、线条粗细与排版性格（如咨询冷峻网格 vs 消费电子高对比大字 vs 金融机构稳重低饱和），让读者一眼认出品牌气质；用户明确指定其他风格或要求中性脱敏时以用户要求为准。
- **行业视觉适配参考**（按内容气质微调，禁止机械照搬固定色值）：
  - **战略咨询 / 行业研报**：高信噪比、克制冷峻主色（如品牌蓝/深藏青）配单点强调色、结论式断言标题（Action Title）、严整网格、清晰数据标签与口径脚注。
  - **科技 / AI / 硬件与消费电子**：强视觉对比（深色封面/高潮页或极简高白）、高辨识品牌色/科技强调色、大尺度核心参数卡与模块化几何排版。
  - **金融 / 投资 / 财报与审计**：低饱和稳重色系、高秩序浅表格（数值右对齐、单位入表头）、正负涨跌语义色清晰、严守注释与统计口径。
  - **工业制造 / 能源 / 政企与工程**：结构化分区、工程蓝/工业灰与安全语义色、清晰流程/架构/里程碑表达、稳重留白。
  - **消费 / 零售 / 文旅与创意**：更强视觉张力与场景氛围、善用真实产品/场景图留出文字区、色板贴合品牌调性与受众情绪。
  - **医疗 / 生命科学 / 学术研究**：高明度洁净底色（白/极浅灰蓝）配清透青蓝或品牌主色、强调实验流程、临床证据与严谨文献出处。
- **跨页一致性护栏**：全册共用同一套 `:root` 颜色变量、固定字号阶梯、一致的中英字体栈与统一的章节眉标格式（例如全册统一带或不带 `01/02/03` 编号）；封面与封底通常隐藏普通页码与页脚线。

## 设计方法（可迁移手法，不是固定模板）

- **入口**：每页一个最先被看见的东西（主数字、主关系图、深色主视觉区、主图片），尺寸和位置拉开层级；
  字号至少分 4–5 级，主数字远大于正文。
- **按指标/对象聚合**：定义、公式、口径、趋势、明细放在同一列或同一卡片，避免跨区查找。
- **关系用结构表达**：流程用箭头带，制衡用 ⇄ 成对，因果用 原因→机制→结果→影响 行；
  不为凑图形把并列画成因果。
- **语义色**：同一状态/指标在流带、表头、标签、强调条上同色；正文色和提示色固定。
- **浅表格**：无竖线、细横线、关键行底色高亮，数值右对齐，单位并入表头或标题。
- **限定醒目**：口径警示、截断坐标、待核实数据用固定提示样式放在相关位置或页脚。
- **非正文页**：
  - 封面用大标题 + 品牌/主题视觉 + 少量元信息，隐藏普通内页页码；
  - 目录页聚焦全册章节导航与页码映射，不把大篇幅“研究方法/评估体系”与目录 50/50 拼在同一页争抢焦点（方法论应独立成页或置入附录）；
  - 章节扉页全册须采用**统一的视觉模板与底色体系**（不可一张深底一张浅底），以大编号 + 章节标题 + 简洁导语营造停顿与呼吸感，**不在右侧硬插孤立竖线或塞满颗粒度不等的卡片列表（如 1:1:1:2:5 混装）**；
  - 结尾页给出结论、讨论题或行动收口而非只写“谢谢”，且严格遵循全册页码约定（约定封底隐藏页码时不再印 `END · 14/14`）。
  这些页与正文共享主题，但构图明显不同。
- **图片**：图片承担信息或氛围，不做无关装饰；照片用 `cover` 裁切并留出文字区，logo 用 `contain`。

每次任务按当前内容、所属行业、品牌特征、受众与参考建立视觉体系，不把无关上一任务的品牌或版式沿用到新任务。

## 已知差异

- LibreOffice 会在中文与西文/数字之间自动加间距；PowerPoint/WPS 需实机检查。
- 原生图表由图表引擎重绘，外观按规格近似预览；表格行高在目标软件中可能随字体度量增高。
- 浏览器截图与 PPTX 渲染不同源：两者都要看，但只有 PPTX 渲染是交付证据。
