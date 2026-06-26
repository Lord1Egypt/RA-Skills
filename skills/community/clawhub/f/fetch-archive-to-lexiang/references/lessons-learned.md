# 自省日志（Lessons Learned）

> 本文件是 fetch-archive-to-lexiang skill 的「组织记忆」。
> 每次用户指出错误、发现遗漏、或 Agent 自查发现问题后，**必须**将教训沉淀到此文件。
> Agent 在每次执行任务前**必须**读取此文件，避免重蹈覆辙。

---

> 🔀 **拆分提示（2026-06-24）**：PDF「提取/裁剪/翻译/富元素识别」类教训（L007 提取、L008 标题、L010 目录、L011 层级、L012 表格、L014 页眉、L015 嵌套、L016 统计卡、L017 多列、L018 图表完整性、L019 样式化表、L020 的脚注上标/识别部分）已迁移并整合进 **`pdf-rich-translate`** skill 的 lessons-learned。
> 下列教训保留作历史与**乐享渲染**参考（如何把识别结果建成 callout/原生表格块）；提取/识别的最新做法以 `pdf-rich-translate` 为准。L020 元规则（同类问题反复→全文同类排查+自动反思）对本 skill 同样适用。

## 📋 教训索引（按严重性排序）

### 🔴 P0 — 反复犯过的严重错误（必须彻底杜绝）

#### L020:【元规则】同类问题被反复指出 → 自动触发反思 + 主动全文同类排查（2026-06-24, 用户明确要求）
- **背景**：Work AI Index 任务里，用户先后指出"图漏了""统计框该用 callout""样式化表格没转表格块""卡片被拍平+`$^{19}$` 乱码"等。这些**本质是同一类问题（PDF 富样式元素被拍平/漏处理）的不同实例**。我每次只修用户截图里那一个，导致"修一个、冒一个"，用户被迫反复截图。用户最终明确要求："**当我多次明确指出同一个问题的时候，要自动触发反思机制，更新 skill。**"
- **根因**：
  1. **被动逐点修复**：把用户截图当"唯一待修项"，从不主动假设"还有同类实例"。
  2. **有规则≠已落实**：L017（多列卡片转表格）早已写入 skill，但我没有据此**全文扫一遍所有多列/卡片**，于是 2.4x 卡片只转了一行（半成品）、Three actions 卡片完全拍平都漏掉了。
  3. **反思要等用户开口**：把"更新 skill"当成用户额外指令，而非同类问题复发时的**自动动作**。
- **正确做法（强制）**：
  1. **识别"同类"信号**：当用户**第 2 次**（含）指出**同一类**问题（哪怕实例不同：另一张图、另一个表、另一处乱码），**立即**判定为"系统性问题"，**不准**只修被指出的那一个。
  2. **主动全文同类排查**：把该问题抽象成可检索的特征（如"多列卡片""`$^{N}$` LaTeX 残留""样式化表格图""孤立图注标题"），用脚本/grep **全文扫描所有实例**，列清单，**一次性全部修复**。修复后做"实例总数对账"。
  3. **自动反思（不等用户催）**：完成修复的**同一轮**里，主动把根因+正确做法写进 lessons-learned，更新 SKILL 自检清单并升版本号——这是同类复发的**默认动作**，不需要用户再说"更新 skill"。
  4. **回报方式**：向用户说明"这是 X 类问题，我已全文排查到 N 处并全部修复"，而非只说"这一处修好了"。
- **自检项**：用户就同一类问题开口 ≥2 次时，本轮交付必须包含：①全文同类清单 ②全部实例已修 ③skill 已自动更新。三者缺一即未完成。

#### L001: 图片遗漏（2026-06-04, 2026-06-15 多次发生）
- **问题**：使用 `WebFetch` 抓取文章后直接翻译上传，完全忽略了原文中的配图
- **根因**：Agent 走了「省事路径」——WebFetch 返回纯文本，Agent 没有意识到原文有图片就直接进入翻译和上传流程
- **正确做法**：
  1. 抓取前先用 WebFetch 快速扫描原文，**明确记录图片数量**
  2. 如果有图片 → **必须**用 `fetch_article.py` 抓取（下载图片到 images/）
  3. 如果 `fetch_article.py` 因沙箱限制无法运行 → 手动用 curl 下载每张图片
  4. 上传时必须用 `md_to_page.py` 或 MCP 三步图片上传流程
  5. **禁止**在有图片的文章中使用 `entry_import_content` 纯文本导入
- **自检项**：上传完成后，用 `block_list_block_children` 检查是否存在 `block_type: "image"` 且有 `file_id` 的 block

#### L002: WebFetch 被当作万能抓取工具 + 静态 HTML 解析漏图
- **问题1**：Agent 倾向于用 WebFetch 获取文章内容并直接使用，跳过 `fetch_article.py`
- **问题2**：用 curl + HTML 解析器检查图片时，只能找到静态 HTML 中的 `<img>` 标签。很多现代网站（如 Every.to）的章节配图通过 JavaScript 动态渲染，curl 抓取的 HTML 中根本不包含这些图片
- **根因**：Agent 选择了阻力最小的路径；且错误地认为 HTML 中 `<img>` 标签数量 = 文章实际图片数量
- **正确做法**：
  1. WebFetch **只能用于初步侦察**（判断文章语言、有无图片、大致结构），**不能作为正式抓取工具**
  2. 侦察图片时，**优先用 WebFetch 的 AI 模式**让 AI 分析完整页面内容来识别图片数量（AI 能看到动态渲染后的内容），而不是靠 curl + 正则匹配 `<img>` 标签
  3. 如果 WebFetch 报告的图片数量 > HTML 静态解析的数量 → 说明有动态加载的图片，必须用 `fetch_article.py --cdp` 或其他方式获取完整图片列表
- **例外**：纯文本无图片且不需要登录的文章，才可以用 WebFetch 的内容直接导入

#### L018: 图表完整性核对不彻底——漏「一页多图」与「页码空档藏图」（2026-06-24, 用户连续 3 次指出仍有漏图）
- **背景**：Work AI Index 转存后，用户**连续三次**截图指出「又有图漏了」。前两次我只做了"抽查统计框 + 单张图"式的"彻查"，每次都声称"已彻底解决"，结果仍有漏网。最终逐页渲染全本 79 页 PDF 才一次性揪出**剩余 4 张漏图**。
- **根因**：
  1. **一页多图**：报告里有的页面放了 **2 张图表**（如 p17、p39），我只取了第一张，把第二张的图注当成普通标题，后面没插图。
  2. **页码空档藏图**：我按"已知在线图表的页码"反推，p47/p50/p53 落在我以为的空档里，被整体跳过。
  3. **图注被当标题**：缺图的那张，其图注（一句完整描述句）被解析成 `##` 标题，孤零零没有图，肉眼扫 markdown 不易察觉。
  4. **验证假阳性**：基于过期的 `lexiang_blocks.json` 统计"图片数"，数字对上了就以为没问题，没有和 **PDF 实际图表总数**对账。
- **正确做法（一次到位的核对法）**：
  1. **逐页渲染整本 PDF**（低 DPI 即可）：`for i in range(len(doc)): doc[i].get_pixmap(dpi=70).save(...)`。
  2. **用颜色特征自动识别图表页**：本报告图表条形为粉/紫双色，统计「同时含粉色且含紫色像素的页」即图表页（可滤掉纯标题/卡片页）。代码见 work-ai-index 会话。
  3. **检测一页多图**：对图表页统计粉色条的**纵向像素分布**，若有 ≥2 个被大间隔隔开的聚类 → 该页有多张图，逐一裁剪（命名加后缀如 `chart_p39b`）。
  4. **三方对账（硬验收）**：`PDF 实际图表数 == 线上 image block 数 − 封面 − 作者页 == 本地 md 的 ![ 引用数`。三者不相等就是有漏/多，必须定位到具体页。
  5. **插图定位**：图注与正文某标题/段落一字不差，按文字匹配定位插入位置；插入前**重新拉取最新 block 列表**，多张图**从高 index 到低 index** 插入避免位移。
- **自检项**：交付前必须做"PDF 图表数 ⟷ 线上图片数 ⟷ 本地引用数"三方对账，并确认**每个图注块后面紧跟一张图**（尤其图注是标题样式时）。
- **同步更新**：SKILL.md Step 4 自检清单 + pdf-processing.md Step 4；本文件。

### 🟡 P1 — 偶尔犯的错误（需要注意）

#### L013: MCP `file_apply_upload` 无法产生可播放视频 + OpenAPI api_base / token 格式错误（2026-06-23）
- **问题1**：用 MCP 的 `file_apply_upload` + `file_commit_upload` 上传视频，产物 `entry_type=file + extension=video`，**视频无法在线播放**（只能下载）
- **根因**：MCP `file_apply_upload` 走的是普通文件上传通道（COS 直传），不触发 VOD 转码。只有 OpenAPI 的 `/cgi-bin/v1/kb/files/upload-params`（media_type=video）签发的 state，配合 `/cgi-bin/v1/kb/entries` 创建 `entry_type=video`，才会触发 VOD 转码
- **问题2**：`upload_video_via_openapi.py` 的 `DEFAULT_API_BASE` 原为 `https://lexiangla.com`（前端域名），导致 `/cgi-bin/token` 返回 404
- **正确 api_base**：`https://lxapi.lexiangla.com`（OpenAPI 专用域名，见官方文档 https://lexiang.tencent.com/wiki/api/ ）
- **问题3**：`get_access_token` 原用 `form_body`（`application/x-www-form-urlencoded`），但乐享 OpenAPI token 接口要求 `Content-Type: application/json` + JSON body
- **正确做法**：
  1. 视频上传**必须**用 `upload_video_via_openapi.py`（OpenAPI 三步流程），**禁止**用 MCP `file_apply_upload`
  2. `~/.lexiang/openapi.json` 只需 `app_key` / `app_secret` / `staff_id`，`api_base` 有默认值 `https://lxapi.lexiangla.com`
  3. token 接口必须用 JSON body（已在脚本中修正）
  4. 上传后 VOD 转码需要几秒到几分钟，`status` 从 `processing` 变为 `finished` 后可播放
  5. 删除旧条目可用 OpenAPI `DELETE /cgi-bin/v1/kb/entries/{entry_id}?space_id=xxx`
- **已修复**：`upload_video_via_openapi.py` 的 `DEFAULT_API_BASE` 和 `get_access_token` 函数
- **同步更新**：本文件；SKILL.md youtube 视频流程说明

#### L003: 翻译时丢失图片占位符
- **问题**：翻译英文文章为中英对照时，原文中的 `![](images/xxx)` 图片引用被翻译过程吃掉了
- **正确做法**：翻译时必须保留所有 `![](...)` 引用不动，或翻译完成后用锚点匹配重新插入

#### L004: 知识库配置不匹配
- **问题**：config.json 中的"贾维斯"知识库在当前 MCP 账号下不可用，导致 API 报错
- **正确做法**：优先使用用户记忆中的目标知识库（ajaxhe的个人知识库），config.json 作为 fallback

#### L008: 标题滥用导致乐享目录膨胀 + 标题双行
- **背景**：Work AI Index 转存后，用户反馈乐享目录极度膨胀、难以查看。
- **问题1（目录膨胀）**：解析出的 markdown 把作者名、人物叙事名、重复子标签（各地区/职能/行业下的 The posture / How AI gets absorbed / What workers are doing / The tradeoff）、纯数字百分比都标成了 `#` 标题，乐享按标题生成目录 → 目录被几百个无意义标题撑爆。
- **问题2（标题双行）**：翻译时把中文标题**另起一行**成为独立标题，导致同一章节英文、中文在目录里占**两行**。
- **正确做法**：
  1. **标题层级克制**：只给真正的章节/小节设标题；作者名/人物名/重复子标签/纯数字一律降级为加粗正文 `**...**`。每个大章节目录里一行即可。
  2. **标题单行双语**：`## English Title / 中文标题`（同一行 ` / ` 分隔），禁止中文另起一行。
- **同步更新**：SKILL.md 核心规则 #4 + Step 2；pdf-processing.md 乐享流程 Step 4/5；translate_gemini.py 提示词。

#### L010: 目录页（TOC）须单独重建为一行一章的清单
- **背景**：Work AI Index 转存后，目录页每个章节被拆成 3–4 行展示，非常冗余。
- **根因**：原文目录被乐享解析成**表格**（Page / Section 两列），双语翻译又把英文、中文各拆一行 → 一个章节占 3–4 行。
- **正确做法**：识别目录页，**丢弃表格**，重建为一行一章的清单 `- **Section N / 第 N 部分**：English Title / 中文标题 · p.NN`。
- **注意**：正文里真正的**数据表格**（如各工具对比）要保留——clean 渲染下它们是 HTML `<td>` 表格，不要误删。

#### L011: 标题层级须按文档逻辑重排（解析给的级别不可信）
- **背景**：Work AI Index 转存后，用户反馈"一些本属于二/三级的标题列到了一级，目录非常混乱"。
- **根因**：解析器给的 `#` 级别**不可信**——它把章节内的图表标题、小节大量标成 `#`（一级），导致目录里几十个一级标题、层级全乱。
- **正确做法**：忽略原级别，按文档真实逻辑重排：①只让**正文真正的大章节**（对应目录页那几条 + 标题页/作者/目录）= `#` 一级；②大章节内的图表/小节统一 `##` 二级；③附录中「地区/职能/行业」等并列项 = `###` 三级，其上的 Appendix A/B/C = 二级。
- **两个判定坑**：①中文译文以 `AI`/`UX` 等短词开头会污染"首个中文字符前取英文名"的切法——应优先识别 ` / ` 双语分隔（右侧以中文或≤4字符短词+中文开头时，左侧才是英文全名）；②`Government / public sector`、`Nonprofit / NGO` 这类名称**内部就含 ` / `**，不能当双语分隔符切断。
- **同步更新**：pdf-processing.md 乐享流程 Step 4；本文件。

#### L012: 表格翻译须中英同格 + 合并单元格用 HTML 还原
- **背景**：Work AI Index 转存后，用户反馈图表/数据表"中文翻译变成了新的一行""合并单元格没处理对，呈现效果与原文相差较远"。
- **问题1（中文另起行/表）**：翻译时把整行中文塞到英文行下方，甚至整张表再复制一份中文表 → 一张表变两张、行数翻倍、对应关系混乱。
- **问题2（合并单元格丢失）**：原文的 rowspan/colspan（如某列分类跨多行、顶部 banner 跨多列）和统计卡片布局被解析拍平成普通网格，语义走样。
- **正确做法**：把每个表**重建为原生 HTML `<table>`**——文本格内 `English<br>中文` 同格双语（纯数据/百分比格不翻译）；合并单元格用 `rowspan`/`colspan`；统计卡片用 2×N 的 `<td>` 网格。
- **关键发现**：乐享 `entry_import_content_to_entry` 的 **markdown 与 html 两种 content_type 都会透传内嵌 `<table>` 并渲染成真正的表格块**（实测 `col_span`/`row_span` 正确生效），所以 HTML 表直接嵌在 markdown 正文即可，不必切 content_type。可先用 `block_convert_content_to_blocks`（纯转换不落库）验证。
- **同步更新**：pdf-processing.md 乐享流程 Step 4；本文件。

#### L013: 名词定义用 callout 块 + 转存后局部修正走增量更新
- **背景**：Work AI Index 转存后，用户反馈"加粗文本变成了标题""名词定义应该用乐享自带的 callout 块"，并强调"做增量更新，不要每次重刷所有内容（太费 token）"。
- **问题1（术语成标题）**：`DEFINITION` + 术语 + 释义的"定义卡片"，解析把术语行（`Botsitting (n.)`）标成 `##` 标题，污染目录、丢卡片样式。
- **问题2（该用 callout）**：定义/提示这类内容应该用乐享原生 `callout` 块，而不是普通段落或标题。
- **正确做法**：用 `block_create_block_descendant` 建 `callout`（容器型，内容放 `children` 子 p 块；首行加粗术语 + 英文/中文释义；可设 `icon` 传 emoji 字符、`color` 默认 `#F2F8FE`），删掉原标题/标签块。markdown 无 callout 语法，全量导入只能退化成 `> quote`，故定义卡片优先用 block 工具单独建。
- **问题3（最关键·省 token）**：上传后的小修小补**禁止重跑 `md_to_page.py` 全量覆盖**。正确流程：`block_list_block_children` 拉块定位 → `block_create_block_descendant`/`block_delete_block`/`block_update_block(s)` 精准增删改 → 本地 `.md` 同步。多处编辑**按文档顺序从后往前**做（删除按 block_id 与位置无关、插入按 index，从后往前可避免子索引位移）。
- **同步更新**：pdf-processing.md 乐享流程 Step 4 + 新增 Step 7（增量更新）；本文件。

#### L014: 清除 PDF 页眉残留重复行 + 章节序号 kicker 并入标题
- **背景**：Work AI Index 转存后，用户发现 `SECTION 03` 成了标题上方的孤立短行（本应是标题的一部分），并要求把这类方案抽象进 skill 一步到位。
- **问题1（页眉家具散落全文）**：PDF 每页的页眉/页脚（章节名、`SECTION 0X`、`第 X 节`、`Appendix A, Region`）被解析成独立短段落，**同一句重复出现十几到几十次**（本例全文 67 个噪音块，仅 "How to Break…" 就重复 25+ 次）。清洗环节漏掉，全飘在正文里。
- **问题2（章节 kicker 丢失/错位）**：`SECTION 0X` 序号是标题的一部分，却被留成孤立短行，既丑又无意义。
- **正确做法**：①清洗时统计**逐字重复 ≥3 次的短行**+章节标题/SECTION/第X节等模式行，判为页眉家具全部删除（注意别误删"英文段+中文段"的双语正文）；②章节序号折进该章节 H1，统一 `# SECTION 0X · English Title / 中文标题`。
- **增量修复手法**：本例用 `block_update_blocks`（一次改 9 个 H1，上限 20）+ `block_delete_block_children`（`ids` 传 67 个块、`parent_block_id` 传根块，一次批删）两次调用搞定，远比重传 240KB 全文省 token。
- **同步更新**：pdf-processing.md 乐享流程 Step 4；本文件。

#### L015: 卡片/分项小标题要比父标题低一级
- **背景**：用户反馈 `Botsitting by the numbers` 下的 `Feeding the AI context` 等几个标题应是它的子级，而非平级。
- **根因**：解析把"某图表/分项标题 + 其下一组并列命名卡片"全标成同一级（都 `##`），层级关系丢失。
- **正确做法**：父标题（含 "by the numbers / comes in N forms / 分 N 类"等信号）后紧跟的一组**结构对称、各带说明的命名小标题**是其子项，降一级（父 `##` → 子 `###`）。本例修了两组：`Botsitting by the numbers` 下 4 项、`Botshitting comes in three main forms` 下 3 项 Offloading。
- **增量手法**：乐享 `block_update_block(s)` **不能改块类型**（h2↔h3），需**删除旧块 + 在原 index 重建为目标级**；多块时从后往前建（index 不位移）、最后 `block_delete_block_children` 批删旧块。
- **同步更新**：pdf-processing.md 乐享流程 Step 4；本文件。

#### L016: 统计高亮框（stat card）用 callout 块（📊）
- **背景**：用户确认 PDF 左侧大数字 + 右侧说明句的统计高亮框应放入乐享 callout，并要求按此策略优化剩余内容。
- **问题**：解析把 stat card 拆成 3–4 个孤立段落（数字行 + 英文 + 重复数字 + 中文），丢失 PDF 的视觉强调，与右侧原文差距大。
- **正确做法**：合并为 1 个 `callout`（`icon: 📊` / emoji-id `1f4ca`），块内 `**数字**` 加粗 + 英文说明 + 中文说明。与定义 callout（📖）区分图标。
- **本例**：共 14 个 stat callout（含此前 6.4、73% + 本次新增 12 个：35%、60%、1.3x、75%、63%、77%、30%、33%×2、32%、74%、28%）。
- **增量手法**：`apply_stat_callouts.py` 从后往前 `block_create_block_descendant` + `block_delete_block_children` 批删旧块。
- **同步更新**：pdf-processing.md Step 4；本文件。

#### L017: 多列信息图用 HTML 表格 + 加粗（不设标题）
- **背景**：用户反馈「Botshitting 三种形式」三列卡片被纵向堆叠、列内用了 `###` 标题，问是否可用 col/表格布局，且布局内不要设标题、高亮信息加粗即可。
- **问题**：解析把 N 列并排信息图拆成纵向段落 + 每列 h3 标题 + 标签/引用多段拆分；还混入解析噪音（如 `$m \ge 3$`）和图表残留数字行。
- **正确做法**：重建为 **1 行 N 列 HTML `<table>`**，`<td>` 内 `<strong>` 加粗列名/标签/百分比，**不设 `#` 标题**；中英同格 `<br>` 分隔。乐享 markdown/html 均透传 `<table>` 为表格块，`<strong>` 保留。`column_list` 也可用但表格更稳。
- **增量手法**：批删旧块（42 个）→ `block_create_block_descendant` 插入表格（先用 `block_convert_content_to_blocks` 取每列 elements）。脚本：`apply_three_col_table.py`。
- **同步更新**：pdf-processing.md Step 4；本文件。

#### L019: 原图是「样式化表格/卡片」时——转成乐享原生表格块 + 保留原图（2026-06-24）
- **背景**：用户指出「Common management reward follies」这张原图（两列对照表 We say we want… / But we actually reward…）在乐享里既没转成表格块、原图也没展示——它被解析拍平成了 32 个零散纯文本段落。
- **根因**：解析器把图内表格逐格拆成独立段落（表头 + 7 行 × 左右各中英 4 段），既丢了表格结构，也没保留原图。我前几轮也没主动识别这类"图其实是表/卡片"的内容。
- **正确做法**：
  1. **识别信号**：PDF 里成对/多列、带表头或箭头、行列对齐的卡片式内容（对照表、奖励谬误表、流程卡片等）——原图是结构化表格而非数据条形图。
  2. **既保留原图、又建原生表格块**（用户要"原图也展现 + 表格块"）：先裁剪整张表格图插入标题下方，再建一个可选中/可编辑的原生 `table` 块。
  3. **最省事的建表法 = `block_convert_content_to_blocks`**：把内容写成 **markdown 表格**（中英同格，英文 `**加粗**` + 中文常规，列内 ` ` 分隔即可），`content_type:"markdown"` 调用该工具，**直接返回完整 `table`+`table_cell`+`p` 的 descendant 结构**（含 `row_size/column_size/header_row`），把它喂给 `block_create_block_descendant` 即可落库——比手搓 16 个 cell + 16 个 p 的嵌套 JSON 可靠得多。
  4. **清理旧内容**：建好后用 `block_delete_block_children(ids=[...])` **按 block_id 批量删**那 N 个被拍平的旧段落（按 id 删与 index 无关，最稳）。
  5. **本地 md 同步**：把那段纯文本换成 `![原图](images/table_pNN.png)` + markdown 表格。
- **与 L012/L017 区别**：L012/L017 讲数据表/多列信息图重建为 HTML `<table>`；本条强调**主动识别"图=表/卡片"** + 用 `block_convert_content_to_blocks` 一步生成原生表格块 + **原图与表格块并存**。
- **同步更新**：pdf-processing.md Step 4；本文件。

#### L021: 播客/视频文字稿须含 Show Notes，置于逐字稿之前（2026-06-24, 用户反馈）
- **背景**：厚雪长波转存后，文字稿直接从 ASR 逐字内容开始，缺少节目介绍、嘉宾摘要、本期剧透时间线——而这些 shownotes 信息密度远高于逐字稿开头。
- **根因**：`podcast_to_lexiang.py` 只输出元信息 blockquote + 逐字稿；Agent 用 WebFetch 抓到的 shownotes 未写入 metadata，脚本也未自动从页面抓取。
- **正确做法**：
  1. 文字稿结构：`# 标题` → 元信息 → `## 节目介绍`（Show Notes，截断 footer）→ `## 逐字稿`
  2. 小宇宙：脚本 Step 0 从 `__NEXT_DATA__.episode.description` 自动抓取；yt-dlp description 仅为节目级简介，**不可代替**
  3. Agent 应在 WebFetch 阶段把完整 shownotes 写入 `metadata.json` 的 `shownotes` 字段（优先于自动抓取）
  4. 无 `chapters.json` 时，从 shownotes「1、09:36 标题」格式自动提取章节
  5. YouTube：`yt_download_transcribe.py` 在 `## 逐字稿` 前插入 `## 视频介绍`（description）
- **自检项**：播客/视频归档后，打开文字稿确认「节目介绍/视频介绍」在逐字稿之前且含摘要/时间线。
- **同步更新**：podcast_to_lexiang.py, yt_download_transcribe.py, podcast-audio.md, youtube-video.md, SKILL.md v2.8.0

#### L009: 翻译默认用当前模型，Gemini 改为备选
- **背景**：用户要求默认用运行 skill 的大模型翻译。
- **正确做法**：🥇 默认 Agent（当前模型）逐块翻译；🥈 仅当用户**明确要求**用 Gemini **且**提供 `GEMINI_API_KEY` 时才用 `translate_gemini.py`。用 gemini 脚本时务必校验是否有分块翻译失败（脚本失败会静默保留英文原文），发现未翻译区段需补译。

### 🟢 P2 — 已修复的小问题（备忘）

#### L005: `after=""` 不是置顶
- **问题**：API 文档说 `after=""` 会排到最前面，实际是排到最后面
- **修复**：必须用 `before=<第一个条目ID>` 来置顶

#### L006: block_create_block_descendant 的 index 参数必须是字符串
- **问题**：传整数 `index: 81` 会参数校验失败
- **修复**：传字符串 `index: "81"`

#### L007: 乐享内 PDF 用 AI 解析读原文（纠正旧说法）+ 图片须从原 PDF 提取
- **背景**：处理乐享内英文 PDF（《The Work AI Index: Global》，79 页）翻译归档任务时验证。
- **纠正**：旧 pdf-processing.md 称 `entry_describe_ai_parse_content` 受 80K 字符限制、不可用——**错误**。实测返回 149K+ 字符的结构化 markdown（带 `#` 标题层级 + `[IMAGE]` 块含中文图片描述），是读乐享内 PDF 原文的**正确首选**。已封装为 `scripts/lexiang_pdf_parse.py`。
- **图片坑**：解析返回的 `/assets/xxx` 图片链接需浏览器 JWT 会话，**MCP token 下载会 401**。图片只能从原始 PDF（`file_download_file` 下载）用 pymupdf 提取。
- **过度识别坑**：解析器把封面、头像、箭头图标、孤立数字色块都标成 `[IMAGE]`，需甄别只留真数据图表，避免上传一堆装饰碎片。
- **裁剪技巧**：报告图表常由几十个矢量/光栅碎片拼成，逐张提取无法还原；改用「最大填充矩形=卡片背景」检测裁剪整张图表卡片，再目视核对剔除文字卡片。
- **插图技巧**：报告每张图表标题与正文某个 `#` 标题一字不差，按标题关键字匹配插入 `![](...)`，位置天然正确，免去手算 block index。

---

## 🔄 规则演化记录

| 日期 | 触发事件 | 新增/修改的规则 | 影响范围 |
|------|----------|----------------|----------|
| 2026-06-03 | 首次图片上传失败 | 新增核心规则#5「图片不可丢失」 | SKILL.md |
| 2026-06-04 | baoyu.io 文章沙箱限制 | 新增 curl+HTML 解析组合方案 | tips-experience.md |
| 2026-06-04 | after="" 排序问题 | 修正置顶逻辑为 before 参数 | SKILL.md |
| 2026-06-09 | 新增原文链接保留要求 | 新增核心规则#2「原文链接必须保留」 | SKILL.md |
| 2026-06-15 | Every.to 文章图片遗漏 | 新增预检步骤、自检清单、自省机制 | SKILL.md, lessons-learned.md |
| 2026-06-15 | Every.to 章节配图遗漏（JS动态渲染） | L002 更新：静态HTML解析不可靠，WebFetch AI模式可识别动态图片 | lessons-learned.md |
| 2026-06-22 | 乐享内英文 PDF 翻译归档（Work AI Index） | 新增 `lexiang_pdf_parse.py` + pdf-processing.md「乐享内 PDF」专用流程；纠正 ai_parse 80K 限制旧说法（L007） | SKILL.md, pdf-processing.md, lessons-learned.md, scripts/ |
| 2026-06-22 | 用户反馈目录膨胀/标题双行/翻译方式 | 标题层级克制+单行双语（L008）；翻译默认当前模型、Gemini 转备选（L009） | SKILL.md, pdf-processing.md, lessons-learned.md, translate_gemini.py |
| 2026-06-22 | 用户反馈标题层级混乱（二/三级标到一级） | 按文档逻辑重排标题层级 + 双语/含斜杠名称判定坑（L011） | pdf-processing.md, lessons-learned.md |
| 2026-06-22 | 用户反馈表格中文另起行/合并单元格丢失 | 表格重建为 HTML（中英同格 + rowspan/colspan），实测 markdown/html 均透传（L012） | pdf-processing.md, lessons-learned.md |
| 2026-06-23 | 用户反馈术语成标题/该用 callout/要增量更新 | 定义卡片用 callout 块；转存后小修用块工具增量增删改、勿重刷全文（L013） | pdf-processing.md（新增 Step 7）, lessons-learned.md |
| 2026-06-23 | 用户反馈 SECTION kicker 成孤立行/要一步到位 | 清除页眉残留重复行 + 章节序号并入 H1；批量 update/delete 增量修复（L014） | pdf-processing.md, lessons-learned.md |
| 2026-06-23 | 用户反馈卡片小标题与父标题平级 | 卡片/分项标题降一级嵌套；改类型需删除重建（L015） | pdf-processing.md, lessons-learned.md |
| 2026-06-23 | 用户确认 stat 高亮框应放 callout | 统计卡片合并为 📊 callout 块；apply_stat_callouts.py 增量替换（L016） | pdf-processing.md, lessons-learned.md, apply_stat_callouts.py |
| 2026-06-23 | 用户问多列信息图能否用 col/表格、布局内不加标题 | 多列卡片重建为 HTML 三列表格 + strong 加粗（L017） | pdf-processing.md, apply_three_col_table.py |
| 2026-06-22 | 用户反馈目录页表格冗余 | 目录页单独重建为一行一章清单，保留正文数据表格（L010） | pdf-processing.md, lessons-learned.md |
| 2026-06-23 | YouTube 视频上传后无法播放（MCP file_apply_upload 产物 entry_type=file） | 修正 api_base 为 lxapi.lexiangla.com + token 改 JSON body + 视频必须走 OpenAPI（L013） | upload_video_via_openapi.py, lessons-learned.md |
| 2026-06-24 | 用户连续 3 次指出仍有漏图（一页多图/页码空档） | 逐页渲染全本 PDF + 颜色识别图表页 + 一页多图检测 + PDF/线上/本地三方对账（L018） | SKILL.md, pdf-processing.md, lessons-learned.md |
| 2026-06-24 | 用户指出样式化表格图未转表格块、原图也没展示 | 识别"图=表/卡片"→ block_convert_content_to_blocks 一步建原生表格块 + 原图并存 + 按 id 批删旧段落（L019） | pdf-processing.md, lessons-learned.md |
| 2026-06-24 | 用户指出又一张卡片被拍平+`$^{19}$` 乱码，并要求"同类问题反复=自动反思" | 【元规则】同类问题第 2 次被指出即判系统性问题，主动全文同类排查+一次性全修+自动更新 skill（L020）；并清理全文 `$^{N}$` LaTeX 残留→Unicode 上标、补修 2.4x/Three actions 卡片为原图+原生表格 | SKILL.md, pdf-processing.md, lessons-learned.md |
| 2026-06-24 | 用户要求播客 shownotes 置于逐字稿前 | Show Notes 自动抓取 + `## 节目介绍` 区块；YouTube description 同理（L021） | podcast_to_lexiang.py, yt_download_transcribe.py, podcast-audio.md, SKILL.md 2.8.0 |

---

## 📝 如何更新此文件

Agent 在以下时机**必须**更新此文件：

1. **用户指出错误后**：立即将错误、根因、正确做法记录为新的 Lesson
2. **自查发现问题后**：同上
3. **成功应用新技巧后**：如果是值得复用的新做法，记录到规则演化表
4. **模型/API 行为变化后**：如果发现之前的做法不再适用，更新对应 Lesson

格式要求：
- 每条 Lesson 必须包含：问题描述、根因分析、正确做法
- 按严重性分级：🔴 P0（反复犯的）、🟡 P1（偶尔犯的）、🟢 P2（已修复的）
- P0 教训对应的自检项必须同步更新到 SKILL.md 的自检清单中
