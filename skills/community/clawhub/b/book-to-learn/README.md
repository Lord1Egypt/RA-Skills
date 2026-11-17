# 📖 Book-to-Learn

**把「书 / 文档站 / 一份资料」拆成学习卡片。**

三种来源模式：**书籍**（PDF / DOCX / HTML / EPUB / TXT，拆解后每日推送一张卡片）、
**网站**（sitemap + 导航抓取）、**资料拆卡**（把国标 / 手册 / 教程 / 长网页拆成
「一图一知识点」的竖版卡片长图，一次性出图）。英文书自动联网核对术语并实时翻译；中文无翻译环节。

**跨平台为底**：默认产物落本地目录，IMA / 飞书只是可选渠道；操作手册与进度一律写在工作目录，不依赖任何平台。

## 🎯 核心价值：任务提示词与数据分离，自由变体

book-to-learn 最关键的设计是**拆书数据与推送提示词彻底分离**。拆书阶段生成的 `items.json` 是静态知识点库；每日推送时，定时任务执行的是一段**你可以随时修改的提示词**。

这意味着——同一本书的知识点数据，换一段提示词，就能变成完全不同的学习任务：

| 变体场景 | 提示词改造方向 | 效果 |
|----------|---------------|------|
| **英文工具书学习** | 默认提示词：翻译 + 术语核对 + 卡片 PDF | 每天一张中英对照知识点卡片 |
| **英语单词学习** | 改提示词：取知识点里的英文术语 → 联网搜索最新英语新闻 → 用该术语讲解新闻 | 把书本术语和实时新闻结合，告别死记硬背 |
| **文言文学习** | 改提示词：取知识点里的诗词 → 生成精美海报图片 → 推送 | 每天一张诗词海报，比文字卡片更有仪式感 |
| **复习模式** | 改提示词：不推送新卡片，随机抽 3 张已推送的卡片出题 | 间隔复习，巩固已学 |
| **深度模式** | 改提示词：取知识点 → 联网搜索相关论文/案例 → 附在卡片后 | 每个知识点都延伸到最新研究 |

**提示词分离的三大好处**：

1. **省 token**：复杂任务被分解成每天的定时任务，每次只处理一个知识点，不用一次性塞进整个上下文
2. **实时更新**：每天推送时联网搜索最新内容，知识点永远不过时——书是静态的，但每天的卡片是活的
3. **随时调整**：想改输出格式？想换学习重点？改提示词即可，不用重新拆书。今天要卡片，明天要海报，后天要出题，全凭你定

## ✨ 特性

- **三种来源模式**：书籍 / 网站（sitemap + 首页导航双通道，正文优先抓 .md 源）/ 资料拆卡
- **五种卡片类型**：A4 标准卡片、大字闪卡、移动端学习长图、中英对照文档、竖版知识卡片长图（3:4 / 9:16 / 1:1 / 4:3 / 16:9 五种画布）
- **多格式输入**：PDF、DOCX、HTML、EPUB、TXT、RTF，自动选择提取器并带回退链
- **中英文自适应**：英文内容联网核对术语 + 实时翻译；中文跳过翻译
- **两阶段架构**：拆书（一次性生成知识点数据）+ 推送（每次调用复用）
- **批量取卡**：`push_card.py next --book X --n 5` 一次取 N 张，`mark --ids a,b,c success` 一次性回写（`--n 1` 为每日一张 + 当日锁）
- **自适应防裁切**：拆卡引擎先测量内容高度，溢出则整体缩字号；内置像素级校验（尺寸 / 页数 / 空白 / 页脚），失败非 0 退出
- **推送前校验**：`validate.py` 检查内容源一致性 + 中英逐块对齐，块数不一致即中止
- **配置确认门禁**：配置未与用户逐项确认前，`next` 拒绝发载荷，防止未确认就开跑
- **提示词可变体**：同一数据，换提示词即可变成单词学习、诗词海报、新闻讲解等不同任务
- **文档层**：操作指南 + 进度笔记落本地持久化目录，会话记忆被压缩或换人接手后读文件即可恢复
- **开箱自检**：`setup_verify.py` 体检（依赖 / 光栅化通道 / 中文字体 / 破折号字体）+ `tests/` 离线自检
- **进度自维护**：推送成功才记录进度，失败自动重推同一张
- **失败通知**：任何环节失败通过 webhook 通知，且不计进度
- **通用化**：参数化配置，支持多本书，首次使用引导配置

## 🙏 致谢与参考

本项目在**多格式文本提取**的方法论上参考了 [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 项目（by [virgiliojr94](https://github.com/virgiliojr94)）。book-to-skill 将书籍转换为 AI agent 可检索的静态参考库；本项目在此基础上发展出**主动推送**模式——把书拆解为知识点后每日定时推送，变被动检索为主动学习。

两者的核心差异：

| 维度 | book-to-skill | book-to-learn |
|------|---------------|---------------|
| 目标 | 静态参考库，AI 按需检索 | 主动推送，每日一张卡片 |
| 输出 | SKILL.md + chapters + glossary | items.json + cards + 每日推送 |
| 语言 | 仅英文 | 中英文自适应 |
| 推送 | 无 | IMA PDF / 飞书卡片 |
| 变体 | 固定检索 | 提示词可自由变体 |

## 📦 安装

```bash
# 克隆
git clone https://github.com/sedey999/book-to-learn.git
cd book-to-learn

# 安装 Python 依赖
pip3 install -r requirements.txt
```

### 中文字体（PDF 生成所需）

PDF 卡片由 weasyprint 生成，依赖系统安装的中文字体。脚本已配置跨平台字体栈（微软雅黑/苹方/Noto CJK 等），自动适配 Windows / Mac / Linux。若 PDF 中中文显示为方块或空白，请确认系统已安装以下任一中文字体：

| 平台 | 推荐字体 | 安装方式 |
|------|----------|----------|
| **Windows** | 微软雅黑 | 系统自带，通常无需安装 |
| **macOS** | 苹方 / PingFang SC | 系统自带 |
| **Linux** | Noto CJK / 文泉驿 | `sudo apt install fonts-noto-cjk` 或 `fonts-wqy-microhei` |

> ⚠️ **weasyprint 在 Windows 上的安装提示**：weasyprint 依赖 GTK 运行时。Windows 安装时需先装 [GTK3](https://gtk.org/download/windows.php)，否则 `pip install weasyprint` 虽成功但运行时报错。如 Windows 上 weasyprint 难以配置，可考虑改用飞书卡片推送方案（无需 weasyprint）。

如需推送到 IMA 知识库，还需安装 [IMA skill](https://ima.qq.com/agent-interface)：

```bash
cd /tmp && curl -sL -o ima-skills.zip "https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip"
mkdir -p ima-skills-extracted && unzip -o ima-skills.zip -d ima-skills-extracted >/dev/null 2>&1
cp -r ima-skills-extracted/ima-skill <你的 skills 目录>/ima-skill   # 如 ~/.openclaw/skills/ima-skill

# 配置 IMA 凭证
mkdir -p ~/.config/ima
echo "<your_client_id>" > ~/.config/ima/client_id
printf '%s' "<your_api_key>" > ~/.config/ima/api_key
```

安装完成后，在仓库目录跑一次自检：

```bash
python3 setup_verify.py --selftest   # 体检 + 渲染自检
python3 render.py --list             # 看「卡片类型 → 引擎」映射
```

## 🚀 使用

### 三种模式入口

| 模式 | 入口 | 说明 |
|------|------|------|
| **A 书籍** | `book_setup.py` | 拆书 → 每日推送，完整流程见下方两阶段 |
| **B 网站** | `fetch_site.py` | 抓取在线文档站（sitemap + 首页导航双通道）→ catalog.json + raw/ |
| **C 资料拆卡** | `tile_setup.py` | 工作目录建任务文件夹（GUIDE.md / PROGRESS.md / cards.json / src/ / out/），强制「示例卡确认样式 → 全量文本稿确认 → 批量出图」三道门禁 |

### 阶段一：拆书（每本书执行一次）

```bash
SKILL_DIR=<skill 安装目录>   # 如 ~/.openclaw/skills/book-to-learn

# 1. 提取文本
python3 $SKILL_DIR/extract_text.py your-book.pdf --out full_text.txt

# 2. 初始化配置（AI 引导填写推送渠道 / 语言 / 通知 webhook 等）
python3 $SKILL_DIR/book_setup.py init <book-slug> --title "书名" --lang en

# 3. AI 分析结构，生成知识点大纲（需确认）
# 4. 确认后生成完整 items.json
# 5. 生成卡片和索引
python3 $SKILL_DIR/book_setup.py gen-cards <book-slug>
python3 $SKILL_DIR/book_setup.py gen-index <book-slug>

# 6. 下载内嵌配图
python3 $SKILL_DIR/book_setup.py download-imgs <book-slug>

# 7. 输出定时任务提示词（可在此基础上自由修改变体）
python3 $SKILL_DIR/book_setup.py prompt <book-slug>
```

### 阶段二：每日推送（定时任务调用）

将 Step 7 输出的提示词配置到定时任务软件，设定触发时间即可。提示词可自由修改——这就是“变体”的入口：改提示词，不改数据，学习任务就变了。

## 📚 示例案例：Open Music Theory

完整拆书案例（Open Music Theory，118 张卡片、272 张内嵌配图）正在 IMA 知识库「【权威】音乐理论与AI创作」->「每日一个知识点」文件夹中每日更新；案例完整文件见 GitHub 仓库 `examples/open-music-theory/`（本 ClawHub 包不含示例文件）。

### 案例信息

- **资料来源**：[Open Music Theory](https://viva.pressbooks.pub/openmusictheory)（viva.pressbooks.pub，开放教育资源）
- **拆解结果**：118 个知识点卡片，覆盖 10 个主题部分（基础、对位、曲式、和声、半音主义、爵士、流行音乐、20 世纪技法、十二音音乐、配器）
- **配图**：272 张原书配图（含 MuseScore 交互乐谱转静态图）以 base64 内嵌，离线可见
- **原文补全**：案例早期生成的 items.json 曾存在 explanationEn 截断在 6000 字符的问题；现已通过推送前强制运行 `extract_images.py`（Step 1b）从原书网站逐卡补全完整正文与图片，历史数据已全部修复
- **附件处理**：relatedLinks 中的文件附件（PDF/DOCX/图片等）自动下载、PNG 转 JPG、重命名后随主卡片上传
- **推送周期**：每日 1 张
- **推送目标**：IMA 知识库「【权威】音乐理论与AI创作」->「每日一个知识点」文件夹（实际运行中的知识库，欢迎在 IMA 中查看；自建部署时名称在首次配置中自选）

### 实际运行的定时任务提示词

以下是本案例实际部署中定时任务执行的完整提示词，展示了英文书推送的完整流程（含术语联网核对、翻译、PDF 生成、主文件上传、附属文件下载上传、进度记录）。你可以此为模板，修改为自己的变体任务：

```
执行 omt-daily-push skill：推送今日的 Open Music Theory 双语知识点卡片。

严格按 SKILL.md 流程执行（SKILL_DIR=/home/admin/.openclaw/skills/omt-daily-push）：

1. cd /home/admin/.openclaw/skills/omt-daily-push && python3 push_card.py next > /tmp/omt_payload.json
解析输出。若 skip=true（如 all_done/weekend/already_pushed/push_in_progress），告知并结束。提取 nextId 和 date_str 备用。（不要加 --force，让防重推守卫生效）

2. 从载荷 terminology 数组提取每个英文术语，使用 WebSearch（SearXNG skill）联网查询其在音乐理论领域的权威中文译法（检索词如 "music theory <term> 中文 译名"），汇总为 terminologyZh 对象。必须核对，不可凭记忆。

3. 将载荷 coreIdeaEn/explanationEn/quoteEn/applicationScenarios 翻译为简体中文：explanation 按换行分段对应翻译；术语首次出现用「中文（英文）」格式；译文准确专业；保留 markdown 链接结构，仅翻译链接文本。翻译 relatedLinks 的标题为中文。

4. 写入 /tmp/omt_zh.json（含 coreIdeaZh/explanationZh/quoteZh/applicationZh/terminologyZh/relatedLinksZh/note）。

5. 生成卡片式 PDF（脚本自动生成带中文主题的文件名）：
cd /home/admin/.openclaw/skills/omt-daily-push && python3 gen_card_pdf.py --payload /tmp/omt_payload.json --zh /tmp/omt_zh.json
从输出中提取生成的 PDF 路径（pdf字段），保存为 PDF_PATH 变量。

6. 上传主 PDF 到 IMA 知识库：
cd /home/admin/.openclaw/skills/omt-daily-push && python3 upload_ima.py --file "$PDF_PATH"

- 退出码 0 = 成功，继续步骤 7
- 退出码 2 = IMA 密钥失效（已自动发飞书通知），本次不计进度，告知用户后结束
- 退出码 1 = 其他错误，不更新进度，报告错误后结束

7. 下载并上传相关链接中的附属文件：
cd /home/admin/.openclaw/skills/omt-daily-push && python3 process_attachments.py --payload /tmp/omt_payload.json --date <date_str> --card-id <nextId> --out-dir /tmp/omt_attachments
- 脚本自动筛选文件链接（.pdf/.docx/.xlsx/.pptx/.png/.jpg 等）、跳过已内嵌图片、下载（带 UA）、PNG 自动转 JPG、统一重命名为 OMT_<date>_<nextId>_<原文件名>
- 读取 /tmp/omt_attachments/attachments.json，对 processed 数组逐个用 upload_ima.py 上传；附件失败不影响主进度，但需通知

8. 仅主PDF上传成功后记录进度（附属文件上传失败不影响进度记录）：
cd /home/admin/.openclaw/skills/omt-daily-push && python3 push_card.py mark <nextId> success

9. 汇报：今日推送第 X/118 张、主题、术语核对要点、PDF 及附属文件上传情况、所有文件已上传至 IMA 知识库「每日一个知识点」文件夹。
```

> 💡 **变体提示**：以上是“英文书 → 中英对照卡片”的标准流程。如果想变体，只需改这段提示词。比如：把步骤 2-4 换成“取知识点中的英文术语，联网搜索今天最新的相关英语新闻，用该术语讲解新闻”；或者把步骤 5 换成“生成一张精美诗词海报图片”。数据不变，任务随你变。

案例完整文件详见 GitHub 仓库：https://github.com/sedey999/book-to-learn/tree/main/examples/open-music-theory

## 🔧 推送方案

| 方案 | 优势 | 适用场景 |
|------|------|----------|
| **本地目录（默认）** | 零依赖零凭据，产物直接落工作目录 | 本地学习、自建归档 |
| **IMA PDF（可选）** | 知识库可检索、PDF 卡片式美观、配图内嵌离线可读 | 知识库积累、长期学习 |
| **飞书卡片（可选）** | 即时通知、交互式卡片、主动触达（webhook / Open API 两种方式） | 即时学习提醒、团队共学 |

默认 `pushMethod: local`（只落本地）；如需 IMA / 飞书，首次配置时选择并填写对应渠道。飞书 webhook 方案的图片通过免费图床（catbox.moe）上传获取 URL 后嵌入；飞书 Open API 方案原生直发图片/文件，无需图床。

## 📁 项目结构

```
book-to-learn/
├── SKILL.md                # 主指令（三种来源模式、配置确认门禁、拆书+推送流程）
├── extract_text.py         # 多格式文本提取（PDF/DOCX/HTML/EPUB/TXT/RTF）
├── fetch_site.py           # 网站模式：sitemap + 首页导航双通道抓取
├── book_setup.py           # 拆书编排（配置/大纲/卡片/定时提示词）
├── items_io.py             # 内容源读写（单文件 / 分章节两种布局）
├── render.py               # 卡片渲染调度（类型 → 引擎映射，config 可覆盖）
├── render_common.py        # 渲染公共工具库（字体/光栅化/校验）
├── gen_card_pdf.py         # A4 标准卡片 PDF（中英文自适应）
├── gen_card_pdf_large.py   # 大字闪卡 PDF
├── gen_card_long.py        # 移动端学习长图
├── gen_card_bilingual.py   # 中英对照文档
├── gen_card_tile.py        # 竖版知识卡片长图（3:4/9:16 等，自适应防裁切+像素校验）
├── tile_setup.py           # 资料拆卡任务初始化（GUIDE/PROGRESS/cards.json）
├── push_card.py            # 推送进度管理（多本书、批量取卡）
├── validate.py             # 推送前校验（内容源一致性 + 中英逐块对齐）
├── setup_verify.py         # 开箱自检（依赖/字体/渲染通道）
├── docs_layer.py           # 操作指南 + 进度笔记（本地为底，可选镜像知识库）
├── upload_ima.py           # IMA 知识库上传（密钥失效检测）
├── send_feishu.py          # 飞书 webhook 卡片推送（图床上传）
├── send_feishu_api.py      # 飞书 Open API 推送（原生图片/文件直发）
├── process_attachments.py  # 相关链接附件下载/转换/重命名
├── gen_image.py            # 闪卡式配图生成（变体场景）
├── normalize_quotes.py     # 中文弯引号规范化
├── notify_failure.py       # 通用失败通知
├── references/             # 设计规格/配置 schema/平台笔记/踩坑笔记
├── tests/                  # 离线自检测试
├── samples/                # 载荷示例
└── (完整示例案例见 GitHub 仓库 examples/ 目录)
```

## 🔒 安全

- 所有凭证（IMA Client ID / API Key、飞书 webhook）存储于本地配置文件，**不硬编码于脚本**
- 凭证仅发送给对应官方域名（ima.qq.com / open.feishu.cn），不发送给任何第三方
- 推送失败通知的 webhook 在首次配置时由用户填写

## 📄 License
