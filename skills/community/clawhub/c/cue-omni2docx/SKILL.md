---
name: cue-omni2docx
slug: cue-omni2docx
displayName: "Markdown 转 Word · MD 转 DOCX（表格还原）"
summary: "把 Markdown 转成中文排版的 Word：表格、目录、脚注一次成型；同一份也能出 HTML 与汇报 PPT。"
description: "Markdown 转 Word（.docx）/ HTML / PPT。不装 omni-reader 也能用：markdown 一条命令出中文排版文档，带表格与目录。接了 omni-reader 的解析结果，再多页锚点分页、真标题+目录、脚注溯源、多源证据附录。Triggers: 转成 word / 导出 docx / 生成 Word 文档 / md 转 docx / markdown to word / md2word / md2docx / 表格还原 / 公文排版 / 汇报 PPT"
version: "0.6.20"
license: MIT
consumes:
  - parsed-doc
inputs:
  - agent-writeup
produces:
  - rendered-docx
  - rendered-html
  - rendered-pdf
  - rendered-pptx
metadata:
  openclaw:
    requires:
      bins: ["python3"]
tags: [文档转换, Word, HTML, PPT, 解析重建, 公文, 诉讼, 研报]
---

# omni2docx — Markdown 转 Word · MD 转 DOCX（表格还原）

## 三分钟上手：不装 omni-reader 也能用

**你要的如果只是「把 markdown 变成能交出去的 Word」，本件不需要任何通道。**
一条命令，装完 `pip install python-docx` 就能跑：

```bash
python scripts/build_docx.py --md 产出.md --out 交付.docx --profile gov --page-numbers
python scripts/validate_docx.py --md 产出.md --docx 交付.docx
```

第一条出文档，第二条自检（末行 `判定 : PASS`）。输入是任何 markdown——agent 写的、你手写的、
从别处导出的都行。出的是中文排版：宋体/黑体、真 Heading 层级 + 可见目录、GFM 表格、脚注上标与注释节。
`--profile gov|legal|finance|default` 换制式；要 HTML 换 `render_html.py`，要汇报 deck 换 `render_pptx.py`，
参数同形（见下文「输出格式」与「排版能力」）。

**这条路上没有 omni-reader 也没有 omni-reader 的 MCP，一切照常。** 缺的只是下面这些「只有解析过才有」的东西：
源页锚点分页、逐字定位、录音/视频的时间戳与说话人标注、多源合并的证据溯源附录。
要这些，再接解析腿——见下文「首次使用：连上 Omni 解析通道」。

## 前置条件

| 依赖                                                           | 用途                                     | 缺失时                                                                              |
| ------------------------------------------------------------ | -------------------------------------- | -------------------------------------------------------------------------------- |
| **解析腿可连：宿主里配好 omni-reader 的 MCP**（现成 URL 那一腿不需要本机 Bridge） | 解析层取正文：`parse`／`get_parse_status`／`cancel_parse`；带 Bridge 的那一面再加 `read_result`／`read_outline`／`discard_result`／`save_result` | 连不上则场景②③（grounded 重建／多源合并）不可用，先按官方配置页 <https://cuecue.cn/hub/omni-reader> 连解析腿——URL 那一腿配好就能跑，不必装 Bridge；**场景①（`--md` 直出）不依赖 omni，仍可用**（缺的是页锚与逐字定位那一层） |
| **Bridge 就绪（只有大件 artifact 读回这一格需要它）** | 把被判 `kind=artifact` 的侧车按 `next_cursor` 逐跳 `read_result` 拼回，与回执声明的 digest 对拍（见「大件分支」那一节） | 没装 Bridge 时 URL 那一腿照样能解析，只是这条读回走不通：侧车取不回来，重建只能停在回执给的那一段（缺的是完整正文与逐字定位，不是排版）——本件不声称 URL-only 覆盖完整的大件重建流程 |
| **Python 3.9+ 且已装 `python-docx`**（`pip install python-docx`） | 渲染层：build_docx.py / validate_docx.py   | 引擎无法运行，先装依赖；调用方式用用户环境通用的 `python`，不假设任何特定安装路径                                    |
| **`python-pptx`**（`pip install python-pptx`；仅 PPTX 输出）  | 汇报渲染：render_pptx.py                    | 仅 PPTX 不可用；docx / HTML 输出不受影响                                                                  |
| **headless 浏览器**（Edge/Chrome/Chromium；仅 `--pdf`）      | HTML → 打印件 PDF                        | 明确提示"未找到浏览器，跳过 PDF"，**不静默失败**；用户装浏览器后再跑 `--pdf` 即可                                          |

- 跨平台：引擎为纯 Python + python-docx，Windows / macOS / Linux 均可运行；示例命令用相对路径与 `python`，不写死文件系统布局。
- 字体说明：预设制式用中文字体名（宋体/黑体/仿宋_GB2312/楷体）。docx 只携带字体名，在非 Windows 环境打开时 Word/WPS 会自动替换为本机字体；公文/法律等制式文档建议在 Windows/WPS 环境打开验收。

## 首次使用：连上 Omni 解析通道

**去哪连（三态分开看：装好 skill ≠ 已配凭据 ≠ 通道已连）**：装那枚 skill 只把文件放到位——`npx skills add sensedeal/cue-skills --skill cue-omni-reader`，跑完再列一次已安装 skill，名字在场只说明文件到位，这一步不产生连接。连接是下一个动作，且分两路：现成 URL 那一腿无需本机安装；本地文件那一腿要那枚 audited Bridge、最小根授权、跑 doctor，再让宿主 reload/reconnect。指路按官方页优先：解析腿配置专页 <https://cuecue.cn/hub/omni-reader>（凭据页 <https://cuecue.cn/hub/api-key>，key 存本地凭据设施，不进聊天、不在终端回显），安装细节见其配置文档 <https://github.com/sensedeal/cue-skills/blob/main/cue-omni-reader/references/setup.md>。**连上之后**，宿主列出的工具里应能看到这些名字：remote-only 那一面是 `parse`、`get_parse_status`、`cancel_parse` 三枚，带 Bridge 的那一面再加 `read_result`、`read_outline`、`discard_result`、`save_result`，共七枚——两路枚数不同，拿一个固定数去判两路必错一边。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。**本件不读凭据**：`CUE_API_KEY` 归通道侧自己取用，本包的转换与排版不发请求、不代持凭据。解析消耗与新账号赠送一律以服务端实时策略为准（那是积分口径），本件不代估也不代付，不承诺任何单价。

**不装不报错（限定：不调用解析这条腿，且本地输入与 python-docx 等前提齐备）**：没连上时场景②③（grounded 重建／多源合并）做不了，缺的是页级锚点还原与多源溯源那一层；场景①照常——零凭据一条命令可跑通：`python scripts/build_docx.py --md 产出.md --out 交付.docx --profile gov --page-numbers`，随后用同口径验收 `python scripts/validate_docx.py --md 产出.md --docx 交付.docx`。这条只证本包自己的渲染，不证通道可用。

## 定位：完整链路，两个环节有效组合

**完整链路 = 多模态解析（给 agent）→ agent 整合分析 → 按需生成文档（给用户）。  
生成阶段把解析侧已算出的元数据（grounding / outline / 画面时间点 / 说话人转写）  
再利用回文档——通用转换工具拿不到这些元数据，这是超越普通转换的核心。**

本 skill 是链路的组合器：

```
用户文件（PDF/扫描件/音视频/网页…）
   │  ① Agent 层：Omni parse（grounded）→ markdown + grounding + outline
   ▼     agent 据此推理：摘要 / 对比 / 抽取 / 整合 / 文书起草
Agent 工作产物（markdown，可带 [^n] 引用与〔来源：…〕标注）
   │  ② 用户层：同一渲染引擎，两种输入
   ├─ 输入 A 原文重建：解析 markdown + grounding → 页级保真 docx（场景②③）
   └─ 输入 B 产物直出：--md file.md → 专业排版 docx（场景①，免中间 JSON）
   ▼
用户可读可编辑的 docx：封面 / 目录 / 真标题 / 表格 / 溯源标注 / 上标引用 + 注释 / 页码标注 / 证据溯源附录
```

组合的粘合点（让用户能追溯 agent 的话）：

- `[^n]` 脚注引用 → Word **上标编号**，文末自动生成「注释」节
- `〔来源：视频帧 00:46〕` → **灰色小字**行内标注
- 溯源标注段（【画面】/【说话人】/【图说】/【图片】）保留 Omni 的视觉/转写证据
- **证据溯源附录**（合并模式自动）：各源的源页码范围 / 画面时间点 / 说话人转写段  
  由解析元数据回灌成表格，用户按页码/时间点直接对照原件

## 三大使用场景（按用户痛点设计）

| 场景                                 | 痛点                                      | 本 skill 对应能力                                                                                                                                            |
| ---------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **① Agent 产出 → 可交付文档**             | agent 默认生成 markdown，用户实际要 docx/pptx/pdf | 引擎天然支持**纯 markdown 输入**（无 grounding/outline 自动降级）：中文标题重建 + 真 TOC + 宋体/黑体 + 表格/列表/行内样式。后续接 PPTX/PDF 输出                                                   |
| **② Scanned PDF/不可编辑件 → 可编辑 Word** | 转换后版式对不上，核对/编辑工作量大                      | Omni 解析 scanned PDF → **页级分页保真**（grounded 源页锚点）；`--page-marks` 在每页边界标注「── 源第 N 页 ──」，改稿时直接对照原件；扫描件里的图章/签名/照片由 Omni 转成视觉描述，引擎渲染为带底纹的【图说】标注段              |
| **③ 多源证据整合 → 诉讼文书等**               | 证据来自截图/录音/照片/视频/规章，需保留各自格式与可溯源引用        | **多源合并模式**（`sources` 数组 → 每源一章 + 总目录 + 章间分页）；录音转写 `[说话人0 00:00-01:20]` → **说话人+时间戳标注段**（正文色，可直接引用"某时某人说"）；视频帧 `[画面 HH:MM]` → 带底纹视觉描述段；图像引用剥离 base64 留说明 |

## 输出格式：按用途选（agent 判断，不硬编码映射）

同一份解析结果可渲染为四种交付物，**选哪个取决于文档拿去干什么**——由 agent 结合场景知识判断，必要时向用户确认：

| 交付物     | 用途        | 语义                                                    | 引擎                                      | 依赖                                   |
| ------- | --------- | ----------------------------------------------------- | --------------------------------------- | ------------------------------------ |
| **docx** | 递交 / 编辑 / 归档 | **保真**：grounded 页锚点→分页符、outline→真标题+目录、表格/脚注/溯源标注逐项还原     | `scripts/build_docx.py`                 | python-docx                          |
| **HTML** | **展示**    | **可读可分享**：自包含单文件、目录锚点跳转、源页标注、表格/引用还原、打印样式；`--pdf` 可导打印件 | `scripts/render_html.py`                | 无额外（PDF 需本机 headless 浏览器）           |
| **PPTX** | **汇报**    | **可讲**：标题页/章节页/要点页/表格页；**要点上页、正文细节进演讲者备注**；超页自动续页并告警    | `scripts/render_pptx.py`                | python-pptx                          |
| **PDF**  | 打印 / 定稿   | 走 HTML→headless 浏览器打印，与 HTML 版面一致（不做像素级复刻）             | `render_html.py --pdf`                  | Edge/Chrome/Chromium                 |

**汇报（PPTX）的协作约定**：引擎不替 agent 决定讲什么。agent 按 slide 组织 markdown（`##` 一页、要点用列表、数据用表格），引擎只负责映射与制式；直接喂长文档时引擎按层级切页并对 `≤--split-level` 的标题分页，正文进备注，`--max-slides`（默认 80）兜底截断并提示先提炼。

**PPTX `--profile` 与 Word 不同语义**：上文参数表（字体/字号/页边距/缩进）是 Word 制式口径；PPTX 的 `--profile` 只切**deck 主题预设**（default/academic/gov/legal/finance 五套近单色主题，字段为色板与正文字体），不接受页边距/缩进等 Word 参数——deck 的版面由版式池与字号层级决定。未知预设名会报错并列出可选值；HTML 的 `--profile` 与 Word 同口径（吃同一套 DOC_PROFILES）。

## 为什么不是又一个 markdown→docx

通用转换（tencent-docx / html-to-docx / pandoc）只拿到 Omni 的**纯 markdown**，  
丢失了 Omni 解析时已算出的结构化信息，且中文排版粗糙：

| 维度      | 纯 markdown 转换（现有）                                     | 本 skill（消费 Omni 解析侧能力）                                                                   |
| ------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 源页边界    | 完全无知，只能吐连续正文                                          | **grounded 页锚点 → Word 分页符**（页级保真）                                                        |
| 标题层级    | LLM 猜 `#` 级别；PDF 正文无 `#` 的章节（"一、美国""1.标普 500 指数"）被当正文 | 从 Omni 干净 markdown 保守重建（中文序号 H1 + 指数型 H2 + 文档自带 `###` 标题）→ 真 Heading + 可见目录              |
| 目录 TOC  | 需重抽/猜                                                 | 文首生成**按层级缩进的可见目录**                                                                       |
| 中文渲染    | 西文字体渲染中文，字体不一致/缺字                                     | 正文宋体、标题黑体（设 `w:eastAsia`），贴近中文研报排版                                                       |
| 阅读顺序    | 单栏 OK，多栏乱                                             | grounded 序列保证顺序                                                                          |
| 表格      | 折叠多栏弱点                                                | GFM 表 → Word 表（列一致性护栏防破碎）；有序/无序列表；行内样式                                                   |
| 多模态视觉理解 | 图像引用/base64 原样塞进文档，画面描述混入正文                           | 视频帧 `[画面 HH:MM]` 与场景描述 → **带底纹的【画面】/【图说】标注段**；`![alt](data:base64…)` 剥离字节、保留说明（【图片：alt】） |
| 保真      | 软换行引入多余空格                                             | `clean_cjk_spaces` 只删紧贴 CJK 的空白，中文间多余空格消除、非空白字符按构造不动                                              |

> 一句话差异化：**通用转换丢结构、排版糙；本 skill 用 Omni 的 grounded 分页 + 章节重建 + 专业中文排版把结构与原貌重建回来。**

## 解析侧能力现状（决策要点；完整取数纪律见「工作流」步骤 1）

| 能力 | 状态 | 一句话口径 |
| --- | --- | --- |
| content / grounded | ✅ 可用 | 按该 part 的 `storage.kind` 现值分流：`inline` 直取回执（`parts.content.storage.text` / `parts.grounding.storage.value`），`artifact` 才顺游标逐跳读回（字节级无损已验） |
| `read_result` | 按 part 分流时可用 | 游标绑死 part 与 offset：跨 part 借用、自造 offset 一律 `INVALID_RESULT_CURSOR`（不可重试、不计费）；只在 `artifact` part 上起步 |
| `read_outline` | **不保证可得** | 同一 result_id 上可返回不可重试的 `RESULT_NOT_FOUND`；**缺省是常规路径**——引擎从 markdown 重建层级，可得且 `coverage=complete` 时才优先用官方层级 |
| layout（bbox） | ✅ 可用 | `detail=layout` 产出 `segments[].layout.items[]`（bbox/font/size）；**换 detail 不动正文**（content part 同字节同 digest），引擎当前消费页级锚 |

> `result_delivery` 请求值不改变实际交付形制、`result_delivery_effective` 也不回显——分流依据只有回执现值一条。


## 排版能力（--profile）：制式由 agent 按场景知识决定

**用户要什么文档、用在什么场景、该满足什么制式要求——这些判断交给 agent 的大模型能力  
与领域知识现场决策，本 skill 不预设"什么场景必须怎样"的硬规则。** skill 只负责把  
排版能力完整暴露出来，供 agent 任意组合：

引擎可控参数（`--profile` 接受三种形态：预设名 / 内联 JSON / .json 文件）：

| 参数                                              | 含义                                                       |
| ----------------------------------------------- | -------------------------------------------------------- |
| `body_east` / `body_latin` / `body_size`        | 正文中文字体（设 `w:eastAsia`）/ 西文字体 / 字号 pt                     |
| `heading_east` / `heading_sizes` / `title_size` | 标题中文字体 / H1–H6 字号数组 / 封面字号                               |
| `line_spacing`                                  | 行距：≥12 视为固定磅值，否则为倍数（如 1.5）                               |
| `first_line_indent`                             | 首行缩进字符数（按 body_size 换算 pt）                               |
| `margins_cm`                                    | 页边距 `{top,bottom,left,right}` cm                         |
| `table_style`                                   | Word 表样式名（`Table Grid`=朴素黑框 / `Light Grid Accent 1`=强调色） |

**内置预设只是参考值，不是决策规则**（agent 可直接用、可改、可完全自定义）：  
`gov`（公文 GB/T 9704：仿宋_GB2312 三号/28 磅/缩进 2 字/GB 页边距）、  
`legal`（诉讼：仿宋四号/24 磅）、`finance`（研报：宋体五号）、  
`academic`（论文：宋体小四/1.5 倍）、`default`（通用宋体）。

**排版质量基线（引擎强制，全制式统一）**：标题/封面一律黑色并按层级设字号  
（覆盖 Office 模板默认蓝色与"标题不大于正文"的层级崩塌）；全文零 CJK 伪斜体  
（引用/图说/图片说明用灰色区分，含中文的 `_强调_` 渲染为加粗）。

**对解析信息的利用选择同样交给 agent。** 引擎提供的能力开关：  
`--page-marks`（页边界标源页码）、`--no-toc` / `--no-pagebreak` / `--no-appendix`  
（关目录/分页/溯源附录）、profile 自定义（含溯源标注与表格的取舍空间）。  
agent 按对场景的理解自行决定取舍——例如诉讼证据文书通常需要页码标注与溯源附录、  
公文通常收紧目录与标注篇幅、研报优先表格数据完整——但**这些是场景知识，不是 skill 规则**；  
用户场景特殊（如内部规范有自己的制式）时 agent 应依用户事实构造自定义 profile。

### 与用户的交互原则

需要向用户澄清或确认时由 agent 自行把握分寸，skill 只定两条底线：

- 上下文已能判断的事（场景、制式、取舍）**直接做并说明一句**，不追问；
- 确需提问时**一次问清、给选项带默认**，排版细节（字体字号等）由制式承载，不烦用户。

## 工作流（必须用 Omni 原生工具取数，不自造解析器）

> **使用纪律**：取数按**回执里各 part 自己声明的 `storage.kind`** 分流——`inline` 就直接从
> `parse` / `get_parse_status` 的回执取整段文本，被判 `artifact` 的 part 才用 `read_result`
> 顺服务端为该 part 发的游标逐跳读回（字节级无损已验，见步骤 1 的大件分支）。
> **请求 `result_delivery="artifact"` 不改变实际交付形制**，`result_delivery_effective` 也不回显在
> MCP 回执里，所以分流依据只有回执现值这一条。
> `read_*` 两个续调用按条件走：`read_result` 只在对应 part 有游标时起步；`read_outline` 仍属
> **不保证可得**的可选支路——不可得（`RESULT_NOT_FOUND`／无 cursor 可起步）就走内联回执与引擎重建，
> 不把它当故障处理，也不预设原因。

### 步骤 1 — 原生 parse（grounded，内联取数）

调用 `mcp__omni_reader__parse`：

- `source`：本地文件路径（须在 omni 允许的根目录内，即 Bridge 的 allowed roots）或 URL。
- `detail`：本件产页级 docx，取 `"grounded"`；要元素级坐标（`bbox`/`font`/`size`）时改取 `"layout"`——
  **换 detail 不动正文**：同一件文档在两种表示下 content part 的字节与 digest 实测逐字同值，改的只是
  侧车表示（侧车是否走 artifact 只看该 part 自身的字节数，与请求值无关）。所以「要页码用 grounded、
  要坐标用 layout」可按需求选，不必因为换了 detail 就重跑正文核对。注意本件映射引擎当前消费的是
  页级锚，取 layout 时坐标字段照存进中间 JSON，版面级重建属后续阶段。
- `result_delivery`：`"artifact"`。**请求 artifact 不改变实际交付形制**：走 inline 还是 artifact 由
  该 part 自身的字节数单独决定（与另一枚 part 无关、与请求值无关），而 `result_delivery_effective`
  不回显在 MCP 回执里——本地记录里有、回执里没有，所以文案与判断都只写实际返回。  
  轮询 `mcp__omni_reader__get_parse_status` 至 `COMPLETED`。

**取数（按回执里该 part 的 `storage.kind` 现值分流）**：解析 `parse` 最终回执的  
`structuredContent.result.parts`：

- `parts.content.storage.text` → markdown 正文
- `parts.grounding.storage.value`（kind=`inline`）→ `omni.grounding.v1` bundle

**大件分支（正文被判 artifact 时）**：`kind=artifact` 的 part 随回执带 `next_cursor`，顺它逐跳
调 `read_result` 读到 `next_cursor` 消失，再把各跳字节按序拼回，与回执声明的 `parts.<part>.digest`
对拍（实测按游标读回是字节级无损的；每跳上限由服务端定，跳长会字符边界让位，不切 UTF-8 字符）。
游标是 base64(JSON)＋签名，**同时绑死 part 与 offset**：跨 part 借游标、自造前进 offset 一律返回
`INVALID_RESULT_CURSOR`（`retryable:false`、`billed:false`），不存在自主跳转的公开出口。
**两枚 part 各走各的路径，不混用**：`inline` 的侧车必须当场从回执整段存住（事后无游标可补取，
`save_result` 也交不出侧车——实测两种交付形制下它都只落正文一枚文件），被判 `artifact` 的侧车才按
游标逐跳读回；Bridge 的私有缓存不是公开面，本件不依赖它。

**可选官方 outline（不保证可得）**：若要从 `get_parse_status` 回执取 `local_result_cache.result_id`
试一次 `read_outline(result_id)` → `{coverage, nodes:[{id, level, title}]}`，
可得即优先采用官方层级，**层级深浅以返货自报的 coverage 值为准**；**不可得是本件常规路径**——直接落盘不带 `outline` 字段，引擎从 markdown 重建目录，不重试、不报故障。

- `coverage=none, nodes=[]` = 文档无可识别标题（正常语义，非故障），此时落盘不写 `outline` 字段、引擎走 markdown 重建。
- 有节点时写入 JSON `outline` 字段，引擎自动优先使用官方层级（引擎兼容 `{coverage,nodes}` 原样传入）。
- ⚠️ **可得性以实际返回为准**：该续调用与缓存条目、进程状态、有效期都相关；同一 result_id 上
  三次调用可能全部返回不可重试的 `RESULT_NOT_FOUND`，此时**盘上的结果文件依然在**（`save_result`
  仍可能成功），所以不得据此判定文档损坏，也不得据此向用户报故障。

### 步骤 2 — 落盘中间 JSON

```json
{
  "markdown": "<步骤1 parts.content.storage.text>",
  "grounding": <步骤1 parts.grounding.storage.value>,
  "outline": <可得时的 {coverage, nodes}；不可得或 coverage=none 时省略该字段>,
  "source": "<源文件描述>",
  "detail": "grounded"
}
```


- `outline` 提供且 coverage=complete 时引擎**优先用官方层级**；缺失或 none 时从 markdown 重建。

### 步骤 3 — 运行渲染引擎（按场景选格式）

```
# Word：保真重建（递交/编辑/归档）
python <skill_dir>/scripts/build_docx.py --json <中间json> --out <输出.docx>
python <skill_dir>/scripts/build_docx.py --md <agent产出.md> --out <输出.docx>

# HTML：展示（浏览器打开 / 分享 / 可打印）
python <skill_dir>/scripts/render_html.py --json <中间json> --out <输出.html> --profile gov
python <skill_dir>/scripts/render_html.py --md <agent产出.md> --out <输出.html> --pdf   # 同时导出 PDF
python <skill_dir>/scripts/render_html.py --md <agent产出.md> --out <输出.html> --inline
#   --inline：CSS 全部内联为 style 属性——粘贴微信公众号/富文本编辑器不重排（单文件照常自包含）
#   --toc-depth N 控制目录深度（默认 2）；需要来源署名用 --source-label "XX研报"
#   （默认不显示原始路径——含本机目录，既丑又泄隐私）

# PPT：汇报（deck，要点上页、细节进备注）
python <skill_dir>/scripts/render_pptx.py --md <slide提纲.md> --out <输出.pptx> --profile finance
python <skill_dir>/scripts/render_pptx.py --json <中间json> --out <输出.pptx> --max-slides 30
```

**PPT 语义版式池**（版式锁死、数量由内容决定——在提纲 md 中用 HTML 注释指令把版式
绑定到其后第一个标题；不写指令则 auto 自动选择）：

```
<!-- layout:kpi -->      KPI 塔看板：数字型要点渲染为大数字列（≤4），适合"数据一页看全"
<!-- layout:compare -->  两栏对比：垂直 hairline 中分、左 Before/右 After（该节无表格/图像时生效）
<!-- layout:timeline --> 纵向时间线：左 hairline 轴 + 方形节点，适合步骤/里程碑/时间序列
```

**Agent 编排约定（"不许编造"铁律）**：deck/doc 中的数字、日期、名称必须来自 Omni 解析
原文，禁止为排版好看编造或改写数据；KPI 塔只接收源文真实数字；无数据可用就留白，不造。

**不变性承诺的边界（不要夸大为"同输入恒同输出"）**：引擎只对**原文/证据位**保持
逐字不变——引文、数字、日期、名称、〔来源〕标注、说话人/画面转写、页码锚点、
脚注；这些一经写入不得被排版或重写改动。标题措辞组织、切页、版式、要点取舍属
设计决策，同一输入两次生成允许存在合理差异；验收（覆盖率/分页/表格数）也只对
证据位与结构计数断言，不断言全产物逐字节恒同。

- 自动：封面标题提取（"标题：xxx"）→ 中文字体 → markdown 章节重建 → 真标题 +  
  文首目录 → grounded 源页分页符 → 表格/列表/引用/行内样式 → 脚注上标 + 文末注释 +  
  〔来源〕灰标 → 溯源标注段。
- `--no-pagebreak` 忽略分页；`--no-toc` 忽略章节重建（仅纯 markdown + 表格/列表）；  
  `--page-marks` 分页处标注「源第 N 页」（核对原件）；`--page-numbers` 页脚 PAGE 域页码；  
  `--strip-emoji` 剥离 emoji/装饰符（验收器同口径剥离，防误报）；`--profile` 套制式——预设名  
  （gov/legal/finance/academic/default）或自定义 JSON（内联或 .json 文件，参数见上节表）。
- 表格识别兼容两种形态：带 `| --- |` 分隔行的规范 GFM 表；无分隔行的连续 `|` 行  
  （xlsx/部分导出常见，首行作表头）。正文段落里内嵌的 `|` 分隔文本是源数据质量，  
  原样保留不猜结构。OCR 件标题常有逐字母空格/拆字（词边界不可还原），渲染前  
  agent 宜先清洗 markdown 再转换。

### 步骤 4 — 验收（产品级，必做）

对产出做保真 + 结构校验，确认**字符级 CJK 覆盖率 ≥99% 判 PASS**且分页/标题/表格数量  
符合预期，再 `present_files` 交付。三种格式各有对应验收器（`--json`/`--md` 与渲染  
时输入保持一致）：

```
python <skill_dir>/scripts/validate_docx.py --json <中间json> --docx <输出.docx>   # 场景②③
python <skill_dir>/scripts/validate_docx.py --md <源md> --docx <输出.docx>          # 场景① --md 直出
python <skill_dir>/scripts/validate_html.py --json <中间json> --html <输出.html>   # 或 --md <源md>
python <skill_dir>/scripts/validate_pptx.py --json <中间json> --pptx <输出.pptx>   # 备注/正文/表格合并计入覆盖口径
```

三个验收器源输入同口径：`--json`（场景②③）或 `--md`（场景①直出的源 markdown），
与渲染时实际输入保持一致；渲染时未开目录的 HTML/PPTX 另加 `--no-toc`（docx 验收器
的目录项为信息项，不参与判定，无此开关）。

### 步骤 5 — 交付

`present_files` 打开/交付 `.docx` / `.html` / `.pptx`（`.html` 可在内置预览直接看）。

## 映射引擎字段约定（build_docx.py）

| 输入字段                | 必填 | 说明                                                                                                                                             |
| ------------------- | -- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `markdown`          | 是  | GFM / 纯文本 markdown（UTF-8）                                                                                                                      |
| `grounding`         | 否  | `omni.grounding.v1` bundle                                                                                                                     |
| `outline`           | 否  | `{coverage, nodes:[{level,title}]}`（兼容 nodes 直接为数组或包在 `{outline:...}`）；提供则优先于重建                                                                |
| `source` / `detail` | 否  | 仅写入 docx 属性 / 日志                                                                                                                               |
| `title` + `sources` | 否  | **多源合并模式**：`sources: [{markdown, grounding?, outline?, source}, ...]`，每源一章（H1=source 名，章间分页），总目录前置（章内层级自动 +1），`title` 为文档封面标题                  |
| `analysis`          | 否  | **agent 整合分析产物** `{markdown, source?}`：渲染为合并文档**首章**（[^n] 引用/〔来源〕标注照常），排在各证据源之前                                                                |
| （合并模式自动）            | —  | 文末自动生成**「证据溯源附录」**：把各源 grounding 页锚点（源第 N–M 页）、画面时间点（首/末时间戳）、说话人转写段（数量/说话人/起始时间）、outline 章节数回灌成表格，并自动推断源类型；`--no-appendix` 关闭，附录条目纳入总目录 |

内部逻辑：

- **封面标题**：行首显式标记 `标题：xxx` / `题目：xxx` / `Title: xxx`（大小写不敏感）提取为 Word `Title` 样式（研报/文章常见），并从正文去除以免重复。只认显式标记——"首行像标题就提"的启发式会误提正文首行、静默毁结构；也可用 `--title` 直接指定。
- **中文字体**：正文 `宋体`、标题/封面 `黑体`，均设 `w:eastAsia`，避免西文字体渲染中文导致缺字/不一致。
- **章节重建（无 outline 时）**：从 markdown 保守识别三类高置信结构 —— 行首中文序号 `一、二、…`  
  → H1；`N.XX指数` → H2（以"指数"识别，排除含 ETF/基金代码的推荐列表项）；文档自带  
  `###` 标题 → 对应 H1–H6。**有 outline 字段时跳过重建、用官方层级。**
- **outline 消费**（当提供）：`nodes[].title` 与 markdown 段落做规范化前缀匹配（兼容段落开头的  
  "一、"/"1." 等章节序号），命中即提升为对应 `level` 的 Heading；标题只取匹配前缀，余下作正文  
  （避免把整段长描述提升为标题）。
- **保真拼接**：段落按软换行拼接后用 `clean_cjk_spaces` 删除紧贴 CJK 字符的多余空格  
  （"核心 资产"→"核心资产"），保留英文词间空格。
- **grounded 消费**：`segments[].content_range_utf8` 为 UTF-8 **字节**偏移，引擎内部做  
  字节→字符换算；相邻段落源页变化时插入 `w:br w:type="page"`（首页不插）。
- **表格护栏**：列数不一致的"假表"（Omni 偶发锯齿布局表）降级为段落渲染，避免破碎表格；  
  列数一致的真实表格（如财务表）正常还原为 Word 表（表头加粗）。
- **多模态溯源标注**：Omni 解析视频/图片/音频/网页时不返回图像/音频字节，但产出  
  **文本形式的溯源标注**。引擎以高置信前缀识别并渲染为与正文明显区分的标注段：
  - `[画面 00:48] 场景: …` / `场景：` / `这张图片` / `图：` → **【画面】/【图说】**（灰斜体 + 底纹，Omni"看见的"）
  - `[说话人0 00:00-01:20] …` / `[00:48] …` → **【说话人N 时间段】**（标签加粗蓝 + 正文色，**可直接引用**——录音/视频证据场景）
  - `![alt](data:image;base64,…)` 剥离字节仅保留说明（【图片：alt】），纯装饰图丢弃
- **优雅降级**：无 outline → 无 TOC/标题提升（仍分页）；无 grounding → 无分页；纯 markdown（场景①）全部能力自动降级为基础渲染 + 中文标题重建。
- **引用渲染（agent→用户粘合）**：`[^n]` 脚注引用 → 上标编号（深蓝），`[^n]: 定义` 行剥出，  
  文末自动渲染「注释」节；`〔…〕` → 灰色小字（约定放"来源：…"）。注释节随所在  
  文档/章节收尾，合并模式下每章各自收尾。

## 验收口径（要点；逐版实测数据见 CHANGELOG）

- 三个验收器同口径：**字符级 CJK 覆盖率 ≥99% 判 PASS**。附加项：docx 查锚句命中（参考项）+ 分页/标题/表格计数 + **DX-02 表格边框护栏（tblPr/tblBorders 必须存在）**；pptx 备注/正文/表格合计计入覆盖 + 越界/重叠/字号几何审计 + **文本框溢出估算（PX-08 严重溢出即判 FAIL）** + 设计铁律；html 查目录/锚点/源页标注/自包含。渲染未开目录的 html/pptx 加 `--no-toc`。
- **验收违规带稳定规则编号**（质量门禁可定位到行，便于回归）：pptx 用 `PX-01…PX-08`（覆盖率/零页/空页/圆角/阴影/彩数/字号反差/文本框严重溢出）；docx 用 `DX-01`（覆盖率）/ `DX-02`（表格边框）。
- 源输入与渲染时实际输入一致：`--json`（场景②③）/ `--md`（场景①）。
- 实测结论：真实语料矩阵（xlsx / 研报 PDF / 网页 / 录音 / docx / PPTX / JPG OCR / 千页 PDF / 截断 PDF / 边界用例 / 多源合并 / `--md` 直出 / `--inline` 公众号导出，多制式组合）覆盖率全部 100%；唯一非 100% 为 99.4%——「标题」二字被提为封面标题所致（符合预期，非丢失）。三格式闭环回归含 inline 用例共 35 例全 PASS（`tests/run_all.py` 可复现）。


## 已知限制

1. 保真级别为**页级**（grounded）。元素级（bbox）数据可经 `detail=layout` 产出（实测  
   `layout.items[].bbox/font/size`），引擎消费 layout 的升级为后续阶段。**换 detail 不动正文**：
   同一件在 grounded 与 layout 下 content part 的字节与 digest 实测逐字同值，所以按需求在
   「页码保真」与「版面坐标」之间选，不必重跑正文核对。
2. `read_result` 是**按 part 分流的一环**：被判 `artifact` 的 part 顺服务端发的游标逐跳读回（实测
   字节级无损），`inline` 的 part 不需要它、也没有游标可起步。`read_outline` 仍是**不保证可得**的
   可选续调用（受缓存条目、进程状态与有效期共同影响；同一 result_id 上可返回不可重试的
   `RESULT_NOT_FOUND`）。**本件不依赖 outline 工作**：章节层级缺省由引擎从 markdown 重建——一条
   已实测的常规路径，不是降级异常；outline 可得时引擎优先采用官方层级。侧车一律不取
   `save_result` 的导出件：实测两种交付形制下它都只交正文一枚文件。
3. 段落跨源页边界时归入其起始字节所在页（MVP 简化）。
4. **图像/音频不嵌入，但溯源标注保留**：Omni 多模态解析不返回图像/音频字节，docx 亦不含  
   多媒体；但 Omni 产出的**文本溯源标注**（视频帧 `[画面 HH:MM]`、说话人转写  
   `[说话人N MM:SS-MM:SS]`、场景描述）由引擎识别并渲染为区分明显的标注段；  
   `![…](data:base64…)` 引用剥离字节、保留 alt 说明。
5. 复杂 markdown（嵌套表、脚注、数学公式）按文本降级；表格为**版式保真**非像素级还原。
6. **PPTX 是汇报 deck，不是版面复刻**：按标题层级切页、要点上页、正文进备注；不做"每源页一页"  
   的机械平铺，也不做像素级还原。表格按列数自动降字号，超长标题自动降字号。
7. **PDF 走 HTML 打印**（headless 浏览器），版面与 HTML 一致；本机无浏览器时明确提示跳过。  
   不做原生 PDF 排版（reportlab 路线），避免字体嵌入/分页/脚注的重复实现。
8. PDF 抽取/OCR 的**逐字母空格**（"T h e y"）不可还原词边界，不强修（强拼会产出  
   "demonstrateprecisionan" 这类错误串）；CJK 字间空格由 `clean_cjk_spaces` 正常消除。
9. **HTML/PDF 打印无页码**：Word 有 `--page-numbers`（页脚 PAGE 域）、PPTX 页脚有页码，但
   HTML 打印走浏览器，Chromium 系不支持 `@page` margin-box 的 `counter(page)`——要页码只能
   引入 paged-media polyfill（外部 JS，违背自包含单文件原则），故不做。**需要页码的定稿
   走 Word 或 PPTX**；HTML/PDF 面向屏幕阅读与分享，源页信息用 `--page-marks` 文内标注。
