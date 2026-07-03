# 📖 Book-to-Learn

**把任意一本书分解成日常学习任务，每日推送一张知识点卡片。**

支持中英文书籍（PDF / DOCX / HTML / EPUB / TXT），拆解为知识点后每日推送一张卡片到 IMA 知识库（PDF）或飞书（卡片消息）。英文书自动联网核对术语并实时翻译；中文书无翻译环节。

**它不只是一本书的阅读器，更是一个可自由变体的每日学习引擎。**

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

- **多格式输入**：PDF、DOCX、HTML、EPUB、TXT、RTF，自动选择提取器并带回退链
- **中英文自适应**：英文书联网核对术语 + 实时翻译；中文书跳过翻译
- **两阶段架构**：拆书（一次性生成知识点数据）+ 推送（每次调用复用）
- **两种推送方案**：IMA 知识库 PDF（默认）/ 飞书卡片消息（备选）
- **提示词可变体**：同一数据，换提示词即可变成单词学习、诗词海报、新闻讲解等不同任务
- **卡片式设计**：大字号、中英对照、术语表、配图内嵌、文件名带中文名
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
sudo pip3 install weasyprint python-docx beautifulsoup4 ebooklib pypdf pdfminer.six
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
cp -r ima-skills-extracted/ima-skill ~/.codebuddy/skills/ima-skill

# 配置 IMA 凭证
mkdir -p ~/.config/ima
echo "<your_client_id>" > ~/.config/ima/client_id
printf '%s' "<your_api_key>" > ~/.config/ima/api_key
```

## 🚀 使用

### 阶段一：拆书（每本书执行一次）

```bash
SKILL_DIR=~/.codebuddy/skills/book-to-learn

# 1. 提取文本
python3 $SKILL_DIR/extract_text.py your-book.pdf --out full_text.txt

# 2. 初始化配置（AI 引导填写 IMA 目标 / 通知 webhook / 语言等）
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

将 Step 7 输出的提示词配置到定时任务软件，设定触发时间即可。提示词可自由修改——这就是"变体"的入口：改提示词，不改数据，学习任务就变了。

## 📚 示例案例：Open Music Theory

`examples/open-music-theory/` 目录包含一个完整的拆书案例，基于开放乐理教材，**目前正在 IMA 知识库「【权威】音乐制作：风格与流派」中每日更新**。

### 案例信息

- **资料来源**：[Open Music Theory](https://viva.pressbooks.pub/openmusictheory)（viva.pressbooks.pub，开放教育资源）
- **拆解结果**：118 个知识点卡片，覆盖 10 个主题部分（基础、对位、曲式、和声、半音主义、爵士、流行音乐、20 世纪技法、十二音音乐、配器）
- **配图**：61 张原书配图已下载并以 base64 内嵌，离线可见
- **推送周期**：每工作日 1 张，约 24 周
- **推送目标**：IMA 知识库「【权威】音乐制作：风格与流派」→「每日一个知识点」文件夹

### 实际运行的定时任务提示词

以下是本案例实际部署中定时任务执行的完整提示词，展示了英文书推送的完整流程（含术语联网核对、翻译、PDF 生成、主文件上传、附属文件下载上传、进度记录）。你可以此为模板，修改为自己的变体任务：

```
执行 omt-daily-push skill：推送今日的 Open Music Theory 双语知识点卡片。

严格按 SKILL.md 流程执行（SKILL_DIR=/home/admin/.openclaw/skills/omt-daily-push）：

1. cd /home/admin/.openclaw/skills/omt-daily-push && python3 push_card.py next --force > /tmp/omt_payload.json
解析输出。若 skip=true（如 all_done），告知并结束。提取 nextId 和 date_str 备用。

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

7. 下载并上传相关链接中的附属文件（附件不加中文主题，保持简洁）：
- 遍历 relatedLinks，筛选出文件类型链接（.pdf/.docx/.doc/.xlsx/.xls/.ppt/.pptx 等）
- 带 User-Agent 伪装下载到 /tmp/ 目录
- 重命名格式：OMT_<date_str>_<nextId>_<原文件名>
  例：OMT_2026-06-29_ch01-01_WK-Introduction-to-Western-Musical-Notation.pdf
- 使用相同的 upload_ima.py 逐个上传到 IMA 知识库同一文件夹
- 记录成功/失败的文件数量

8. 仅主PDF上传成功后记录进度（附属文件上传失败不影响进度记录）：
cd /home/admin/.openclaw/skills/omt-daily-push && python3 push_card.py mark <nextId> success

9. 汇报：今日推送第 X/118 张、主题、术语核对要点、PDF 及附属文件上传情况、所有文件已上传至 IMA 知识库「每日一个知识点」文件夹。
```

> 💡 **变体提示**：以上是"英文书 → 中英对照卡片"的标准流程。如果想变体，只需改这段提示词。比如：把步骤 2-4 换成"取知识点中的英文术语，联网搜索今天最新的相关英语新闻，用该术语讲解新闻"；或者把步骤 5 换成"生成一张精美诗词海报图片"。数据不变，任务随你变。

案例完整文件详见 `examples/open-music-theory/`。

## 🔧 推送方案

| 方案 | 优势 | 适用场景 |
|------|------|----------|
| **IMA PDF（默认）** | 知识库可检索、PDF 卡片式美观、配图内嵌离线可读 | 知识库积累、长期学习 |
| **飞书卡片（备选）** | 即时通知、交互式卡片、主动触达 | 即时学习提醒、团队共学 |

首次配置时选择推送方案。飞书卡片方案的图片通过免费图床（catbox.moe）上传获取 URL 后嵌入。

## 📁 项目结构

```
book-to-learn/
├── SKILL.md                # 主指令（拆书+推送两阶段、首次配置流程）
├── extract_text.py         # 多格式文本提取（PDF/DOCX/HTML/EPUB/TXT/RTF）
├── book_setup.py           # 拆书编排
├── push_card.py            # 推送进度管理（--book 参数化，支持多本书）
├── gen_card_pdf.py         # 卡片式 PDF 生成（中英文自适应）
├── upload_ima.py           # IMA 知识库上传（密钥失效检测）
├── send_feishu.py          # 飞书卡片推送（图床上传）
├── notify_failure.py       # 通用失败通知
└── examples/
    └── open-music-theory/  # 示例案例（正在 IMA 知识库更新中）
        ├── SKILL.md
        ├── items.json      # 118 个知识点
        ├── cards/          # 118 张 HTML 卡片
        └── ...
```

## 🔒 安全

- 所有凭证（IMA Client ID / API Key、飞书 webhook）存储于本地配置文件，**不硬编码于脚本**
- 凭证仅发送给对应官方域名（ima.qq.com / open.feishu.cn），不发送给任何第三方
- 推送失败通知的 webhook 在首次配置时由用户填写

## 📄 License

MIT
