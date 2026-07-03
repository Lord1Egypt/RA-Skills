---
name: book-to-learn
description: |
  把任意一本书分解成日常学习任务，每日推送一张知识点卡片。
  支持中英文书籍（PDF/DOCX/HTML/EPUB/TXT），拆解为知识点后每日推送。
  英文书自动联网核对术语并实时翻译；中文书无翻译环节。
  四种推送模板：PDF标准卡片、PDF大字闪卡、飞书交互卡片、飞书卡片+图片补充。
  提示词与数据分离，可自由变体为单词学习、诗词海报、新闻讲解等任务。
version: 1.1.0
homepage: https://github.com/sedey999/book-to-learn
metadata:
  openclaw:
    emoji: 📖
    requires:
      anyBins:
        - python3
    envVars:
      - name: IMA_OPENAPI_CLIENTID
        required: false
        description: IMA OpenAPI Client ID (only needed for IMA push method)
      - name: IMA_OPENAPI_APIKEY
        required: false
        description: IMA OpenAPI API Key (only needed for IMA push method)
    primaryEnv: IMA_OPENAPI_CLIENTID
---

# book-to-learn — 把书分解成日常学习任务

通用 skill：把任意一本书拆解为知识点卡片，每日推送一张。

## ⛔ 核心规则

1. **两阶段**：拆书（一次性）+ 推送（每次调用）。每本书先拆书生成数据，之后每日推送复用。
2. **进度仅在成功后记录**：任一环节失败都不更新 progress.json，下次重推同一张。
3. **中英文自适应**：英文书联网核对术语 + 实时翻译；中文书跳过翻译。
4. **超链接文字化**：IMA 不能点击链接，PDF 中 URL 必须纯文字显示可复制。
5. **失败必通知**：任何失败（提取/翻译/PDF/上传/飞书）都通过 webhook 通知，且不计进度。
6. **首次配置**：无 config.json 时引导用户配置（IMA 凭证/推送目标/通知 webhook/语言/粒度）。

## 依赖安装（首次使用前）

### 1. Python 依赖
```bash
sudo pip3 install weasyprint python-docx beautifulsoup4 ebooklib pypdf pdfminer.six
# weasyprint 生成 PDF；其余为多格式提取器。沙箱已预装大部分。
```

### 2. IMA skill（若用 IMA 推送）
```bash
cd /tmp && curl -sL -o ima-skills.zip "https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip"
mkdir -p ima-skills-extracted && unzip -o ima-skills.zip -d ima-skills-extracted >/dev/null 2>&1
# 安装到你的平台对应的 skills 目录（任选一个）：
cp -r ima-skills-extracted/ima-skill ~/.codebuddy/skills/ima-skill   # CodeBuddy
# 或: cp -r ima-skills-extracted/ima-skill ~/.openclaw/skills/ima-skill   # OpenClaw
# 或: cp -r ima-skills-extracted/ima-skill ~/.claude/skills/ima-skill     # Claude Code
# 或: cp -r ima-skills-extracted/ima-skill ~/.agents/skills/ima-skill     # Amp / 跨 agent
```
> upload_ima.py 会自动在 `~/.codebuddy`、`~/.openclaw`、`~/.claude`、`~/.copilot`、`~/.agents` 等路径下查找 ima-skill，也可用环境变量 `IMA_SKILL_DIR` 显式指定。
API Key 获取：https://ima.qq.com/agent-interface
```bash
mkdir -p ~/.config/ima
echo "<Client ID>" > ~/.config/ima/client_id
printf '%s' "<API Key>" > ~/.config/ima/api_key
```

### 3. Node.js 注意
沙箱中 node 可能被 bun shim 劫持。所有 node 调用用 `/usr/bin/node` 并清除 NODE_OPTIONS。upload_ima.py 已内置。

---

## 阶段一：拆书（首次对每本书执行）

> **SKILL_DIR**：本 skill 所在目录。各平台路径不同（CodeBuddy: `~/.codebuddy/skills/book-to-learn`，OpenClaw: `~/.openclaw/skills/book-to-learn`，Claude Code: `~/.claude/skills/book-to-learn` 等）。脚本内已用 `os.path.dirname(os.path.abspath(__file__))` 自动定位，无需手动指定。下面 `$SD` 代表 SKILL_DIR。

### Step 1：提取文本
```bash
cd $SD && python3 book_setup.py extract <书文件路径> --slug <book-slug>
```
slug = 书的 URL 友好标识（如 `designing-data-intensive-apps`）。输出 `books/<slug>/full_text.txt`。

### Step 2：初始化配置
```bash
cd $SD && python3 book_setup.py init <book-slug> --title "书名" --lang <zh|en> --granularity <chapter|section|topic>
```
生成 `books/<slug>/config.json` 骨架。然后**与用户确认并填写**以下空字段：
- `language`：zh（中文书，无翻译）/ en（英文书，需翻译）
- `pushMethod`：ima（默认）/ feishu（备选）
- `ima.kbName` / `ima.folderName`：IMA 知识库名称和文件夹（用 `list-kb` 命令列出知识库让用户选）
- `feishu.webhook`：飞书 webhook（若选 feishu）
- `notifyWebhook`：失败通知 webhook（**必填**，任何失败都发此通知）

**确认推送方案**：向用户说明两种方案并让其选择：
- **IMA PDF（默认）**：上传卡片式 PDF 到 IMA 知识库文件夹。优势：可检索、配图内嵌、离线可读。适合知识库积累。
- **飞书卡片（备选）**：发送交互式卡片消息到飞书 webhook。优势：即时通知、交互式。限制：图片需上传图床（catbox.moe）获取 URL。适合即时学习提醒。

### Step 3：AI 分析结构并生成大纲
读取 `books/<slug>/full_text.txt`（大书用 offset/limit 分段读，先读前 8000 字符识别标题/作者/章节/目录）。
按 config.granularity 拆解为知识点，输出**大纲 JSON** 供用户确认：
```json
[{"id":"ch01-01","chapter":"第一章","topic":"主题"}, ...]
```
**必须等用户确认或调整大纲后**，再进入 Step 4。

### Step 4：生成完整 items.json
确认大纲后，为每个知识点生成完整对象（读取 full_text.txt 对应章节内容）：
```json
{
  "id": "ch01-01",
  "chapter": "所属章节",
  "topic": "知识点主题",
  "coreIdea": "核心观点（原文语言）",
  "explanation": "详细解释（原文语言，含 markdown 链接 [text](url)）",
  "quote": "金句（若有）",
  "application": "应用场景（若有）",
  "image": "原书配图链接（若有）",
  "relatedLinks": [{"href":"url","text":"标题"}],
  "terminology": ["核心术语"],
  "link": "来源链接"
}
```
写入 `books/<slug>/items.json`。

### Step 5：生成卡片和索引
```bash
cd $SD && python3 book_setup.py gen-cards --slug <book-slug>
cd $SD && python3 book_setup.py gen-index --slug <book-slug>
```

### Step 6：下载内嵌配图
```bash
cd $SD && python3 book_setup.py download-imgs --slug <book-slug>
```
下载 items.json 中的图片 URL，转为 base64 data URI 内嵌。

### Step 7：输出定时任务提示词
```bash
cd $SD && python3 book_setup.py prompt --slug <book-slug>
```
输出该书的定时任务执行提示词，用户配置到定时任务软件。

---

## 阶段二：推送（每次调用执行一次）

### 英文书流程（需翻译）

1. **取载荷**：
   ```bash
   cd $SD && python3 push_card.py next --book <slug> --force > /tmp/b2l_payload.json
   ```
   > Windows 平台 `/tmp/` 不存在，改用 `%TEMP%` 或脚本输出建议的临时目录。
   解析输出。skip=true 则结束。

2. **联网核对术语**：对 terminology 数组每个术语，**使用当前环境中可用的联网搜索工具**查权威中文译法，汇总 terminologyZh。必须联网核对，不可凭记忆。
   - 优先使用环境原生搜索工具（如 WebSearch、SearXNG skill 等）
   - 若环境有多个搜索工具，任选可用者
   - 若环境无搜索工具，告知用户需配置搜索能力后结束

3. **实时翻译**：coreIdea/explanation/quote/application 译为中文。explanation 按换行分段对应；术语首次出现「中文（英文）」；explanation/application 含 markdown 链接的保留 url 仅译 text；翻译 relatedLinks 标题生成 relatedLinksZh；**同时翻译 topic（知识点标题）为 topicZh**。**注意：翻译后的中文文本必须使用中文双引号「」或 ""（U+201C/U+201D），不得使用英文直引号 ""。若不确定 Unicode 输入方式，写入 JSON 时会由 normalize_quotes.py 自动修正。**

4. **写翻译 JSON** 到临时目录的 `b2l_zh.json`（含 topicZh/coreIdeaZh/explanationZh/quoteZh/applicationZh/terminologyZh/relatedLinksZh/note）。

5. **生成 PDF**（文件名末尾带知识点中文名）：
   ```bash
   cd $SD && python3 gen_card_pdf.py --payload <payload路径> --zh <zh路径> --out "<临时目录>/<PREFIX>_$(date +%F)_<nextId>_<topicZh>.pdf" --language en
   ```
   PDF 标题区显示中英对照（中文在上，英文小字在下）。`<topicZh>` 用翻译后的中文名替换（去除文件名非法字符）。

6. **推送**（按 config.pushMethod）：
   - IMA：`python3 upload_ima.py --file "<pdf>" --config books/<slug>/config.json --book-dir books/<slug>`
     退出码 0=成功；2=密钥失效（已发通知）不计进度结束；1=其他错误不更新进度结束。
   - 飞书：`python3 send_feishu.py --payload /tmp/b2l_payload.json --zh /tmp/b2l_zh.json --config books/<slug>/config.json --language en`

7. **记录进度**（仅成功后）：`python3 push_card.py mark --book <slug> <nextId> success`

8. **汇报**：第 X/N 张、主题、术语核对要点。

### 中文书流程（无翻译）

1. **取载荷**：同上。
2. **跳过翻译**（步骤 2-4 不执行）。
3. **生成 PDF**（文件名末尾带知识点中文名）：
   ```bash
   cd $SD && python3 gen_card_pdf.py --payload <payload路径> --out "<临时目录>/<PREFIX>_$(date +%F)_<nextId>_<topic>.pdf" --language zh
   ```
   中文书的 topic 本身即中文名，直接用于文件名。
4. **推送**：同上（飞书则 `--language zh`，不传 --zh）。
5. **记录进度**：同上。
6. **汇报**：第 X/N 张、主题。

---

## 飞书卡片方案实现说明（备选）

send_feishu.py 构造飞书 interactive 卡片 JSON，POST 到 webhook。

**卡片结构**：
- header：蓝色标题「📚 书名 · 主题」
- elements：进度+章节 → 术语表(markdown表格) → 内容分栏(中英对照/纯中文) → 配图 → 相关链接 → 来源(note)

**图片处理**（飞书卡片图片需 URL 或 image_key）：
1. base64 data URI 图片 → 上传 catbox.moe（免费无需注册）→ 获取 URL → `{"tag":"img","url":"..."}`
2. 图片 URL 直接用 `{"tag":"img","url":"..."}`
3. 上传失败 → 文字提示「配图见来源链接」

**链接处理**：飞书卡片 markdown 支持可点击链接，但为兼容性仍附纯文字 URL。

---

## 推送模板系统

每本书在 config.json 的 `template` 字段选择推送模板。首次配置时由 AI 引导用户选择。

### 可用模板

| 模板 ID | 名称 | 脚本 | 适用场景 | 设计规范 |
|---------|------|------|----------|----------|
| `pdf-standard` | PDF 标准卡片 | gen_card_pdf.py | 工具书、长文知识点 | A4，正文 18px/英文 15px，中英对照，多字小字 |
| `pdf-large` | PDF 大字卡片 | gen_card_pdf_large.py | 单词、术语、短知识点 | A4，标题 42px，正文≥18px，超大字号，适合远距离/打印 |
| `feishu-card` | 飞书交互卡片 | send_feishu.py | 即时学习提醒 | 飞书 interactive 卡片，markdown 排版，图床上传 |
| `feishu-card+image` | 飞书卡片+图片补充 | send_feishu.py + gen_image.py | 知识点可视化 | 飞书卡片 + 附带 1:1 或 1:4 图片 |

### 设计风格规范

**配色**（所有模板统一）：绿(#1a7f37) 核心观点 / 蓝(#0969da) 解释 / 紫(#8250df) 金句 / 橙(#bf8700) 应用 / 红(#cf222e) 术语

**字体栈**（跨平台）：微软雅黑 → 苹方 → 冬青黑 → Noto CJK → 思源黑体 → 文泉驿 → 宋体

**超链接**：所有模板中 URL 均以纯文字显示（IMA 不能点击），格式为「标题 + 换行 + 完整 URL」

**图片模板设计**（gen_image.py）：
- 1:1 正方形（750×750px）：精简内容，适合飞书卡片内嵌
- 1:4 长图（750×3000px）：完整知识点，适合长文滚动阅读
- 只作为飞书卡片补充，**不能单独以图片形式推送**
- 生成方式：HTML → weasyprint PDF → pdf2image PNG（依赖 pdf2image + poppler）
- 设计参考：[react-paper-memo](https://github.com/JustinChia/react-paper-memo) 大字号可打印卡片理念

### 模板选择建议

- **英文工具书/专业书** → `pdf-standard`（中英对照，多字详解）
- **英语单词/术语学习** → `pdf-large`（大字号，一眼看清）
- **日常学习提醒** → `feishu-card`（即时推送到手机）
- **知识点可视化** → `feishu-card+image`（卡片+配图长图）

---

## 配置确认与进度文件

### 配置确认（summary 命令）

每本书设置完成后，运行 `python3 book_setup.py summary <slug>` 输出详细配置汇报，包括：书名、语言、拆解粒度、卡片转化情况（总数/配图/链接/术语）、推送模板、推送通道、IMA目标/飞书webhook、失败通知webhook、文件清单、测试推送设置。用户确认后再生成定时任务提示词。

### daily-progress.md

每本书的 `books/<slug>/daily-progress.md` 记录学习进度。每次推送成功后追加一行（不替换已有记录）：

```markdown
| 日期 | 序号 | 卡片ID | 主题 | 推送方式 | 状态 |
|------|------|--------|------|----------|------|
| 2026-06-30 | 1/118 | ch01-01 | 西方音乐记谱法导论 | ima | ✅ 成功 |
```

定时任务提示词中已包含 `log-progress` 步骤，推送成功后自动追加记录。

---

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 本指令 |
| `extract_text.py` | 多格式文本提取（PDF/DOCX/HTML/EPUB/TXT/RTF，带回退链） |
| `book_setup.py` | 拆书编排（extract/init/gen-cards/gen-index/download-imgs/summary/log-progress/prompt） |
| `push_card.py` | 推送进度管理（status/next/mark/weekday/list-books，--book 参数化） |
| `gen_card_pdf.py` | PDF 标准卡片生成（中英文自适应，超链接文字化） |
| `gen_card_pdf_large.py` | PDF 大字卡片生成（A4，正文≥18px，标题42px） |
| `gen_image.py` | 补充图片生成（1:1/1:4，HTML→PDF→PNG） |
| `upload_ima.py` | IMA 知识库上传（动态查找 ima-skill，密钥失效检测） |
| `send_feishu.py` | 飞书卡片推送（图床上传，中英文自适应） |
| `notify_failure.py` | 通用失败通知（参数化 webhook） |
| `books/<slug>/` | 每本书独立数据（config/items/index/progress/daily-progress/cards/images/full_text） |

## 辅助命令

- 查看所有书：`cd $SD && python3 push_card.py list-books`
- 查看进度：`python3 push_card.py status --book <slug>`
- 配置确认：`python3 book_setup.py summary <slug>`
- 手动重推：`python3 push_card.py next --book <slug> --force`
- 重置进度：编辑 `books/<slug>/progress.json`，置 null 清空 history
- 输出定时提示词：`python3 book_setup.py prompt <slug>`
- 记录进度到 md：`python3 book_setup.py log-progress <slug> --card-id <id>`

## 注意事项

- 进度是唯一凭证，勿手动误改 progress.json
- 失败绝不计进度，确保下次重推同一张
- PDF 文件名日期格式统一 `YYYY-MM-DD`
- 英文书翻译质量优先：术语必须联网核对
- **中文引号规范**：所有脚本内置 `normalize_quotes.py`，自动将英文直引号 `""` 转换为中文双引号 `""`（U+201C/U+201D）。即使 AI 翻译输出的 JSON 含英文引号，PDF 和飞书卡片最终输出也会被自动修正。中文书的 `items.json` 中若含英文引号，同样会被自动修正。
- 假设不同用户使用：所有配置在 config.json，不硬编码
