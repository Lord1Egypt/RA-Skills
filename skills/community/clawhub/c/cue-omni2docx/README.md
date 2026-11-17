# omni2docx — Markdown 转 Word · MD 转 DOCX（表格还原）

把 markdown 变成中文排版的 Word / HTML / 汇报 PPT；喂它 Omni Reader 的解析结果，
再多出源页锚点分页、逐字定位、说话人与时间戳标注、多源证据溯源附录这一层。
**不是又一个 markdown→docx**：通用转换只吃 markdown，拿不到 Omni 解析时已算出的
结构化信息（源页锚点、章节层级、画面/转写元数据），本件把它们映射回原生对象。

## 三分钟上手：不装 omni-reader 也能用

装完 `pip install python-docx`，两条命令就能出一份能交出去的 Word：

```bash
python scripts/build_docx.py --md 产出.md --out 交付.docx --profile gov --page-numbers
python scripts/validate_docx.py --md 产出.md --docx 交付.docx   # 末行 判定 : PASS
```

输入是任何 markdown（agent 写的、手写的、别处导出的都行），出的是中文排版 Word：
宋体/黑体、真 Heading 层级 + 可见目录、GFM 表格、脚注上标与注释节。
`--profile gov|legal|finance|default` 换制式；要 HTML 换 `render_html.py`，要汇报 deck 换 `render_pptx.py`。
这条路上没有解析腿，**代价**是缺了源页锚点分页、逐字定位、时间戳与说话人标注、多源证据附录那一层——
要这些才需要接 omni-reader（见下文「首次使用」）。

同一份解析结果可输出四种交付物，按用途选：**docx 保真**（递交/编辑/归档）、
**HTML 展示**（可读可分享、可打印）、**PPTX 汇报**（deck，要点上页、细节进备注）、
**PDF 打印**（HTML 走浏览器打印）。

## 是什么 / 不是什么

| 是 | 不是 |
|---|---|
| grounded 页锚点 → Word 源页分页符（页级保真） | 像素级版面复刻 |
| 官方 outline → 真 Heading 层级 + 可见目录 | PPT 的版面复刻（PPTX 是汇报 deck，按层级切页） |
| GFM 表格 / 脚注上标+注释节 / 〔来源〕灰标 / 上标引用 | 图像/音频字节嵌入（Omni 不返回字节，保留文本溯源标注） |
| 多源合并 + 自动「证据溯源附录」（页码/时间点/说话人） | 投资建议、内容创作 |

## 三类场景

1. **Agent 产出 → 可交付文档**：agent 的 markdown 工作产物 `--md` 直出，专业中文排版。
2. **Scanned PDF/不可编辑件 → 可编辑 Word**：`--page-marks` 在每页边界标注「源第 N 页」，改稿直接对照原件。
3. **多源证据整合 → 诉讼文书等**：`sources` 数组每源一章 + 总目录 + 证据溯源附录；录音转写段/视频帧标注段可直接引用。

## 上手（三步）

**装本件自己**：`npx skills add huhoo/cue-awesome --skill omni2docx`——这条只装本包；装完在你这一侧重列一次已安装 skill，清单里看得到 `omni2docx` 这个名字才算文件到位。没有 CLI 环境时的兜底是把本目录整个放进宿主支持的 skills 目录（`~/.workbuddy/skills/`）。

前置：`python3` + `pip install python-docx`；场景②③另需 omni-reader MCP 已连接（场景①不需要）。
PPTX 输出另需 `pip install python-pptx`；`--pdf` 另需本机装有 Edge/Chrome/Chromium（缺则明确提示跳过）。

场景②③那条解析腿的已连判据（解析走宿主里的 omni-reader MCP，本件的转换本身不发请求）**按路分写**：宿主列工具走的是 MCP 的 `tools/list` 握手，**连上之后**那份返回里应当能看到这些名字——remote-only 那一面是 `parse`、`get_parse_status`、`cancel_parse` 三枚，带 Bridge 的那一面再加 `read_result`、`read_outline`、`discard_result`、`save_result`，共七枚；两路枚数不同，拿一个固定数去判两路必错一边。列不到就是没连，场景②③做不了，场景①（`--md` 直出）不受影响。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。解析消耗以服务端返回为准，本件不代估也不代付（见「能力边界」第一条）。

### 首次使用：连上 Omni 解析通道

**去哪连（三态分开看：装好 skill ≠ 已配凭据 ≠ 通道已连）**：`npx skills add sensedeal/cue-skills --skill cue-omni-reader` 这一条只把文件放到位——跑完再列一次已安装 skill，名字在场只说明这一层，它不产生连接。配凭据是第二层（官方配置页 <https://cuecue.cn/hub/omni-reader>，凭据页 <https://cuecue.cn/hub/api-key>，key 存本地凭据设施、不进聊天也不在终端回显）；通道已连是第三层，判据按路分写见上一条（remote-only 三枚／Bridge 七枚，别拿一个固定数判两路）。URL 那一腿无需本机安装，本地文件那一腿要 audited Bridge、最小根授权、跑 doctor、再让宿主 reload/reconnect。名字在场只证它们被暴露，不证解析跑得通——URL 那一腿要拿一枚真实 URL 跑一次 parse 才证该路，本地文件那一腿要拿一枚真实本地文件跑一次 parse 才证该路（remote-only 不读本地件）；本件不自证也不代跑。**本件不读凭据**：`CUE_API_KEY` 由通道侧自己取用，本包的转换与排版不发请求、不代持凭据。解析消耗与新账号赠送一律以服务端实时策略为准（那是积分口径），本件不代估也不代付，不承诺任何单价。

**不装不报错（限定：不调用解析这条腿，且本地输入与 python-docx 等前提齐备）**：没连上只是场景②③（grounded 重建／多源合并）做不了，缺的是页级锚点还原与多源溯源那一层；场景①照常——零凭据一条命令 `python scripts/build_docx.py --md 产出.md --out 交付.docx --profile gov --page-numbers`，随后同口径验收 `python scripts/validate_docx.py --md 产出.md --docx 交付.docx`。这条证的是本包自己的渲染，不证通道可用。

```bash
# ① agent markdown 直出（免中间 JSON）
python scripts/build_docx.py --md 产出.md --out 交付.docx --profile gov --page-numbers

# ②③ Omni 解析重建：parse(grounded) 取 markdown+grounding(+同会话 read_outline) 落盘中间 JSON
python scripts/build_docx.py --json 中间.json --out 交付.docx --profile legal --page-marks

# 验收（必做）：字符级 CJK 覆盖率 ≥99% 判 PASS + 结构核对（--json 与 --md 两种源，与渲染时输入一致）
python scripts/validate_docx.py --md 产出.md --docx 交付.docx
python scripts/validate_docx.py --json 中间.json --docx 交付.docx

# 展示：自包含 HTML（可加 --pdf 同时导出打印件；--toc-depth 控目录深度）
python scripts/render_html.py --json 中间.json --out 展示.html --profile gov --page-marks --pdf

# 微信公众号：--inline 把全部样式内联进 style 属性，粘贴公众号/富文本编辑器不重排
python scripts/render_html.py --md 产出.md --out 推文.html --inline

# 汇报：deck（要点上页、正文进备注）；长文档建议 agent 先提炼提纲
python scripts/render_pptx.py --md slide提纲.md --out 汇报.pptx --profile finance --max-slides 30

# HTML / PPTX 同口径验收（备注/正文/表格合并计入覆盖口径；含越界/重叠/字号几何审计）
python scripts/validate_html.py --json 中间.json --html 展示.html
python scripts/validate_pptx.py --json 中间.json --pptx 汇报.pptx
```

Omni 取数纪律：全程用 agent 原生 MCP 工具（parse / get_parse_status / read_outline /
read_result）且**同会话**调用——不要为 omni 写 spawn 脚本（跨进程调 read_* 必然失败）。

## 场景制式（--profile）

排版参数由文档的使用场景决定，agent 按场景知识决策；预设只是参考值：
`gov`（公文 GB/T 9704：仿宋三号/28 磅/GB 页边距）、`legal`（诉讼：仿宋四号）、
`finance`（研报：宋体五号）、`academic`（论文：小四 1.5 倍）、`default`。
任意参数可覆盖：`--profile` 接受内联 JSON / .json 文件（字体/字号/行距/缩进/页边距/表样式等）。

质量基线：标题一律黑色并按层级设字号、全文零 CJK 伪斜体（中文强调→加粗）、
`--page-numbers` 页脚 PAGE 域、`--strip-emoji` 剥离装饰符。
封面标题：源文行首显式标记 `标题：` / `题目：` / `Title:` 提取为封面 Title（三种标记，不做启发式），
或用 `--title` 直接指定。

## 能力边界（诚实清单）

- **转换与排版在本机完成，脚本自身不发网络请求**；两处条件要说清：源文里若带 `http(s)://` 图片链，`--pdf` 导出时由浏览器自行取图（那一刻需要网，取不到就在版面上留空，本件不代下载——源文本地路径或非 `data:` 图像在 HTML 里只作文字标注）；而**经 omni 解析得到的输入，其解析消耗以服务端返回为准**——解析不是本件的能力（见「是什么 / 不是什么」节），本件不代估也不代付。
- 保真级别为**页级**（grounded）；元素级 bbox 数据可经 `detail=layout` 产出，引擎消费为后续阶段。
- `read_result` / `read_outline` 受**同会话约束**（`local_result_cache` 绑定 bridge 进程）；agent 原生会话内使用无碍。
- 段落跨源页边界时归入其起始字节所在页。
- 复杂 markdown（嵌套表、数学公式）按文本降级；表格为版式保真非像素级还原。
- 中文字体名（宋体/仿宋_GB2312/楷体等）在非 Windows 环境由 Word/WPS 自动替换，制式文档建议在 Windows/WPS 打开验收。
- PPTX 为汇报 deck：按标题层级切页、正文进演讲者备注、`--max-slides`（默认 80）截断并告警；不做每源页一页的机械平铺。
- PDF 经 HTML + headless 浏览器打印导出，版面与 HTML 一致；不做原生 PDF 排版。
- **打印页码只有 Word（`--page-numbers`）与 PPTX（页脚）有**：HTML/PDF 打印受浏览器限制（Chromium 不支持 `@page` margin-box 页码，polyfill 违背自包含原则），要页码的定稿走 Word/PPTX；HTML 的源页信息用 `--page-marks` 文内标注。
- PDF 抽取的逐字母空格（"T h e y"）不可还原词边界，不强修；CJK 字间空格正常消除。

## 验收口径

三种格式各有验收器，源输入同口径（`--json` 场景②③ / `--md` 场景①，与渲染时实际输入一致），
同以**字符级 CJK 覆盖率**（≥99% 判 PASS）为准：
`validate_docx.py`（+ 锚句命中 + 结构统计：分页/标题/表格数）、
`validate_html.py`（+ 目录/锚点/源页标注/自包含检查）、
`validate_pptx.py`（幻灯片正文+表格+演讲者备注合并计入覆盖口径，+ 越界/重叠/字号几何审计 + 设计铁律）。
渲染时未开目录的 HTML/PPTX 验收另加 `--no-toc`。
真实语料矩阵（xlsx / PDF 研报 / HTML / 音频转写 / docx / PPTX /
JPG OCR / 千页 PDF / 截断 PDF / 边界用例、多源合并、`--md` 直出、`--inline` 公众号导出，
多制式组合）实测覆盖率全部 100%。

### 规则编号：判什么、为何命中、怎么改才过

先说边界：**编号是回归定位用的地址，不是能力承诺**；下表按码内现值写，判定阈值一律以
`scripts/validate_pptx.py` 与 `scripts/validate_docx.py` 的码内现值为准——阈值改了以码为准，本文不另立标准。
PPTX 侧八条 PX-01／PX-02／PX-03／PX-04／PX-05／PX-06／PX-07／PX-08，DOCX 侧两条 DX-01／DX-02，逐条如下。

| 编号 | 判什么（码内现值） | 为什么会命中 | 怎么改才过 |
|---|---|---|---|
| PX-01 | deck 对源 markdown 的 CJK 逐字覆盖率 <0.99（正文＋表格单元格＋演讲者备注合并计） | 内容没进 deck：撞上 `--max-slides`（默认 80）截断、`--prose skip` 把整段正文丢掉，或源文里有渲染器不承接的块 | 照验收报告打印的「缺失 CJK 字符（种类）」回源文定位那段；提高或去掉 `--max-slides`，`--prose` 回到 `notes`／`body` 重渲 |
| PX-02 | 总页数 = 0 | 源 md 的标题层级低于 `--section-level`／`--split-level`，切不出一页 | 把切分层级降到文档真实层级，或先由 agent 提炼一层提纲再渲 |
| PX-03 | 空页数 > max(1, 总页数 // 10)（空页＝该页无文本、无表格、无图、也无备注） | 连续只有标题没有内容的分节——多因切分级别过细，或正文被前页的字符上限吃光 | 合并空节、降低 `--split-level`，或放宽 `--max-chars`／`--max-bullets` 让正文真的进到页上 |
| PX-04 | 形状 XML 里出现 `roundRect`（铁律：0 处） | 本件渲染器不产圆角矩形；命中意味着混进了外部模板形状或手工加的形状 | 回到渲染器产出，别在成稿 deck 里手工加形状；需要圆角的排版不属本件制式 |
| PX-05 | 形状 XML 里出现 `a:outerShdw` 或 `a:innerShdw`（铁律：0 处） | 同上，阴影同样来自外部模板或手工加工 | 同上；改回渲染器产出后复跑 |
| PX-06 | 有彩色种类 > `MAX_CHROMATIC`（现值 3；饱和度 >24 才算有彩色，近灰不计） | 混用多套配色，或往内容与 spec 里塞了额外颜色 | 固定一套 `--profile`（五套各自色板都在码内），正文与表格不再另配色 |
| PX-07 | 最大字号 ÷ 最小字号 < `MIN_CONTRAST`（现值 2.0；deck 内一个字号都没测出时不判） | 全 deck 只剩一种字号——标题被压到正文级，层级拉不开 | 让标题回到主题字号层级（换制式或去掉手工字号覆盖）后重渲；正文里别整段套同一字号 |
| PX-08 | 估计行高 > 盒高 1.3 倍的文本框数 > 0（估宽口径：CJK≈1em/字、ASCII≈0.56em、空格≈0.3em） | 单页文字过量，或含超长无空格串（URL、长编号）把行高撑爆 | 收紧 `--max-bullets`（默认 6）／`--max-chars`（默认 760）把该页拆开；长串手动断行或移进备注 |
| DX-01 | DOCX 对源文的 CJK 字符级覆盖率 <99.0%（锚句命中率只作参考，不计入判定） | 转换中有字符真的丢失（少见；多为跨表格单元格的短语被漏渲染） | 看报告列出的缺失字符样例回源文核对，再用与渲染时同源的 `--json`／`--md` 重跑验收 |
| DX-02 | 未应用表格边框的表格数 > 0（`table_borders_audit` 现值） | 表格绕过了 `style_table` 路径写进去（例如手工补表） | 走渲染器的表格路径出表；不要在成稿里手工加表格后直接交 |

几何审计里的**越界／重叠／过小字号是信息项**，不参与 PASS/FAIL——上面十条全清才给 PASS；
每条信息项都随报告打印计数，方便定位但不判分。

## 文件

| 文件 | 说明 |
|---|---|
| `SKILL.md` | agent 主指令（完整工作流、字段约定、解析侧能力现状） |
| `CHANGELOG.md` | 版本历史（每一版改了什么、怎么验的） |
| `scripts/build_docx.py` | Word 渲染引擎（单源/多源合并/markdown 直出） |
| `scripts/validate_docx.py` | 保真+结构校验器（docx） |
| `scripts/render_html.py` | HTML 展示渲染器（自包含单文件，可 `--pdf`/`--inline`） |
| `scripts/render_pptx.py` | PPTX 汇报渲染器（deck，要点上页/细节进备注/版式池） |
| `scripts/validate_html.py` | HTML 验收器（覆盖率 + 目录/锚点/自包含） |
| `scripts/validate_pptx.py` | PPTX 验收器（覆盖率含备注 + 几何审计 + 设计铁律） |
| `tests/` | 回归套件（合成语料，clone 后 `python tests/run_all.py` 可复现） |
