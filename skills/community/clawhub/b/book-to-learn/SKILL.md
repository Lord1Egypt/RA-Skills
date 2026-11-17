---
name: book-to-learn
description: |
  把「一本书 / 一个在线文档站 / 一份资料」拆解成学习卡片。
  三种来源模式：书籍（PDF/DOCX/HTML/EPUB/TXT）、网站（sitemap + 导航抓取）、
  资料拆卡（把国标 / 手册 / 教程 / 网页拆成「一图一知识点」的竖版卡片长图，一次性出图）。
  英文内容自动联网核对术语并实时翻译；中文内容跳过翻译。
  卡片类型：A4 标准卡片、大字闪卡、移动端学习长图、中英对照文档、竖版知识卡片长图（3:4/9:16 等）。
  支持批量取卡（一次推 N 张）与可选的双语文档归档。
  跨平台可用：默认产物落本地目录，IMA / 飞书为可选渠道。
version: 1.6.1
homepage: https://github.com/sedey999/book-to-learn
metadata:
  openclaw:
    emoji: 📖  # ClawHub metadata, not rendered in PDF/image
    requires:
      anyBins:
        - python3
    envVars:
      - name: IMA_OPENAPI_CLIENTID
        required: false
        description: IMA OpenAPI Client ID（仅选用 IMA 推送时需要）
      - name: IMA_OPENAPI_APIKEY
        required: false
        description: IMA OpenAPI API Key（仅选用 IMA 推送时需要）
---

# book-to-learn — 把书 / 文档站 / 资料拆成学习卡片

## 三种来源模式

| 模式 | 来源 | 产出 | 节奏 |
|---|---|---|---|
| **A. 书籍** | 一本书（PDF/DOCX/EPUB/HTML/TXT） | A4 卡片 / 大字闪卡 / 学习长图 / 中英对照 | 拆解一次，之后**每天推一张** |
| **B. 网站** | 一个在线文档站 | 同上 | 同上（增量更新） |
| **C. 资料拆卡** | 一份资料（国标 / 手册 / 教程 / 网页） | **竖版知识卡片长图**（默认 3:4）+ 全量文本稿 | **一次性全部出图** |

依据用户要的东西选模式：**要「跟着学的每日推送」→ A/B；要「一整套可归档的知识卡片」→ C**。
C 模式完整规范见下方「模式 C」。

## ⛔ 核心规则

**0.（最高优先级）首次使用必须先与用户逐项确认配置，确认前不要开始拆解、更不要推送。**
确认清单写在 `config.confirmed.items`：来源与范围、语言与是否翻译、卡片类型、
推送渠道、命名与编号、文档（操作指南/进度笔记）存放位置、失败通知方式。
逐项确认后把结果写回 config（`confirmed.at` / `confirmed.by` / 各项置 `true`）。
未确认时 `push_card.py next` 会直接拒绝发载荷——这是刻意设的闸门，**不要绕过**。

**1.（模式 C 同样强制）拆卡模式的三道门禁，任何情况下都不得跳过：**
**① 先出 1 张示例卡让用户确认样式 → ② 生成全量文本稿让用户逐条确认 → ③ 才批量出图。**
理由：样式或文本没定就批量出图 = 全部返工。也不存在「时间紧就跳过」的例外。

2. **两阶段**：拆解（一次性，书籍=提取/大纲/内容源；网站=抓取/清单/内容源）+ 推送（每次调用）。
3. **进度仅在成功后记录**：任一环节失败都不更新进度，下次重推同一张。
4. **中英文自适应**：英文内容联网核对术语 + 实时翻译；中文内容跳过翻译。
5. **超链接文字化**：多数知识库/IM 不能点击链接，产物中 URL 必须纯文字、可复制。
6. **失败必通知**：任何失败（提取/翻译/渲染/上传/推送）都通过 webhook 通知，且不计进度。
7. **双轨编号**：文件名用「推送序号」（连续，如 `OC009`）；卡片内标记与笔记录入用
   「清单绝对序号」（`idx`，跳过也占号，如 `9 / 287`）。两轨不要混。
8. **每次推完必须列出「接下来 N 张」**（默认 N=10，`batch.listNextN`），供用户决定跳过哪几张。
9. **文档跟着任务走，且落在工作目录**：操作指南与进度笔记一律写进**工作目录**下的任务目录
   （见下「跨平台说明」），**不要建在 skill 目录里**。会话记忆被压缩或换执行者后，
   读这两份文件即可恢复上下文。
10. **渲染前先体检**：`python setup_verify.py`（缺依赖/缺字体/缺光栅化通道都会明确提示）。

## 跨平台说明（本 skill 以「不依赖任何平台」为底）

本 skill 面向多平台（Claude Code / CodeBuddy / OpenClaw / 各类 agent 沙箱 / 本地机器）。
**除「选用的推送渠道」外，任何环节都不应依赖某个特定平台。**

- **默认产物落本地**：不配置任何渠道时，产物就写在工作目录里。
  IMA、飞书都是**可选渠道**，只有用户明确选择时才需要它们的凭据与工具。
- **任务数据与文档落在持久化目录，不留在易失层**：
  - **模式 C（拆卡）**：在工作目录下新建一个**以任务命名的文件夹**（如 `标点符号规范/`）：
    ```
    <工作目录>/<任务名>/
      GUIDE.md       操作手册（读这一份就能接手，内嵌全部规则与踩坑）
      PROGRESS.md    进度（只增不删，底部最新）
      cards.json     唯一事实源
      src/           原文提取（full_text.txt 等）
      refs/          参考图 / 标准图（可选）
      out/           PNG 产物 + _check.json + _contact_sheet.png
    ```
  - **模式 A/B**：默认数据根是 `<skill目录>/books/<slug>/`（文档在其下 `docs/`）。
    **若本平台的 skill 目录不是持久层**（容器/沙箱里常会被重置），把数据根指到工作目录：
    ```bash
    export B2L_DATA_DIR="$PWD/b2l-data"
    # book_setup.py / push_card.py / docs_layer.py / fetch_site.py / validate.py 统一读取该变量
    ```
  - 平台笔记（如 IMA 笔记）只作**可选镜像**（`docs_layer.py mirror`）。
    「持久化目录为底」的原因：平台侧一旦没有删除/编辑接口，唯一的进度记录就被锁在一个地方了。
- **脚本自定位**：所有脚本用 `os.path.dirname(os.path.abspath(__file__))` 找自己，
  不依赖任何固定安装路径。下文 `$SD` 代表本 skill 目录。
- **平台适配细节**（含 IMA 环境注意事项）见 `references/platform-notes.md`。

## 依赖安装（首次使用前）

### 1. Python 依赖
```bash
pip3 install weasyprint pillow numpy pymupdf
pip3 install python-docx beautifulsoup4 pypdf pdfminer.six ebooklib striprtf   # 书籍多格式提取
# weasyprint 出 PDF；numpy 用于拆卡引擎的内容高度测量；pymupdf 做 PDF→PNG（纯 wheel，无需系统库）
# Windows/macOS 若 pip 装到用户目录，用 python3 -m pip install --user …
```
体检：`python3 setup_verify.py`（会分别报「渲染核心 / 光栅化通道 / CJK 字体 / 拆卡引擎」四块）。

### 2. 中文字体
- Linux：`apt-get install -y fonts-noto-cjk`（没有中文字体会渲染成方块）。
- macOS / Windows 一般自带（PingFang SC / Microsoft YaHei），脚本会自动探测。
- 探测不到时脚本会明确报错，而不是静默出方块。

### 3.（可选）IMA skill —— 仅当选用 IMA 推送
```bash
cd /tmp && curl -sL -o ima-skills.zip "https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip"
mkdir -p ima-skills-extracted && unzip -o ima-skills.zip -d ima-skills-extracted >/dev/null 2>&1
cp -r ima-skills-extracted/ima-skill ~/.codebuddy/skills/ima-skill   # 或 ~/.openclaw / ~/.claude / ~/.agents 下
```
> `upload_ima.py` 会自动在 `~/.codebuddy`、`~/.openclaw`、`~/.claude`、`~/.copilot`、`~/.agents`
> 等路径下查找 ima-skill，也可用环境变量 `IMA_SKILL_DIR` 显式指定。API Key 获取：https://ima.qq.com/agent-interface
> 凭据一律走环境变量（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`），**不要写进 config 文件**。
> 不用 IMA 的话，本节整节跳过。

### 4. Node.js 注意
部分沙箱里 node 可能被 bun shim 劫持。所有 node 调用用 `/usr/bin/node` 并清除 `NODE_OPTIONS`。`upload_ima.py` 已内置。

---

## 模式 A：书籍（首次对每本书执行）

> **SKILL_DIR**：本 skill 所在目录（各平台路径不同）。脚本内已自动定位，无需手动指定。下面 `$SD` 代表 SKILL_DIR。

### Step 1：提取文本
```bash
cd $SD && python3 book_setup.py extract <书文件路径> --slug <book-slug>
```
slug = 书的 URL 友好标识（如 `designing-data-intensive-apps`）。输出 `books/<slug>/full_text.txt`。

### Step 2：初始化配置
```bash
cd $SD && python3 book_setup.py init <book-slug> --title "书名" --lang <zh|en> --granularity <chapter|section|topic>
```
生成 `books/<slug>/config.json` 骨架，然后**与用户确认并填写**：
- `language`：zh（中文书，无翻译）/ en（英文书，需翻译）
- `pushMethod`：`local`（默认，只落本地）/ `ima` / `feishu`（webhook）/ `feishu-api`（飞书 Open API，支持图片/文件直发）
- `ima.kbName` / `ima.folderName`：仅 pushMethod=ima 时填（用 `list-kb` 命令列知识库让用户选）
- `feishu.webhook` / `feishuApi.*`：仅选飞书时填
- `notifyWebhook`：失败通知 webhook（**必填**，任何失败都发此通知）

**向用户说明推送方案并让其选择**：
- **仅本地（默认）**：产物写在工作目录，不推送。跨平台零依赖。
- **IMA PDF**：上传卡片式 PDF 到 IMA 知识库文件夹。优势：可检索、配图内嵌、离线可读。
- **飞书 webhook**：发送交互式卡片消息。优势：即时通知。限制：图片需上传图床。
- **飞书 Open API**：App ID + App Secret 直发指定会话。优势：支持原生图片/文件、无需图床。

### Step 3：AI 分析结构并生成大纲
读取 `full_text.txt`（大书用 offset/limit 分段读，先读前 8000 字符识别标题/作者/章节/目录）。
按 `config.granularity` 拆解为知识点，输出**大纲 JSON** 供用户确认：
```json
[{"id":"ch01-01","chapter":"第一章","topic":"主题"}]
```
**必须等用户确认或调整大纲后**，再进入 Step 4。

### Step 4：生成完整 items.json
为每个知识点生成完整对象（读取 `full_text.txt` 对应章节内容），写入 `books/<slug>/items.json`：
```json
{
  "id": "ch01-01", "chapter": "所属章节", "topic": "知识点主题",
  "coreIdea": "核心观点（原文语言）",
  "explanation": "详细解释（原文语言，含 markdown 链接 [text](url)）",
  "quote": "金句（若有）", "application": "应用场景（若有）",
  "image": "原书配图链接（若有）",
  "relatedLinks": [{"href":"url","text":"标题"}],
  "terminology": ["核心术语"], "link": "来源链接"
}
```
`items.json` 是唯一事实源：推送载荷直接读它的字段；`cards/*.html` 只作人工预览。

### Step 5-7：卡片/索引/配图/定时提示词
```bash
cd $SD && python3 book_setup.py gen-cards    <book-slug>   # 生成卡片预览
cd $SD && python3 book_setup.py gen-index    <book-slug>   # 生成索引（同时初始化 progress.json）
cd $SD && python3 book_setup.py download-imgs <book-slug>  # 下载配图并内嵌 base64
cd $SD && python3 book_setup.py prompt       <book-slug>   # 输出定时任务提示词
```

## 模式 B：网站

```bash
python fetch_site.py --base-url https://docs.example.com --slug mydocs \
    --include /start --exclude / /start/hubs --limit 300
```
- sitemap + 首页导航**双通道**核清单；正文优先抓 `<url>.md`；配图扁平化落盘。
- 抓完先看 `sections` 统计，**与用户确认章节范围与卡片总数**，再生成内容源。
- 增量更新：只喂新增 URL（`--urls-file`），保持已有 idx 不变。
- 完整流程见 `references/site-mode.md`。

---

## 模式 C：资料拆卡（把一份资料变成一套卡片长图）

**适用**：一份资料（国标 / 手册 / 教程 / 规范 / 长网页）→ 「一图一知识点」的竖版卡片长图，
一次性拆分、批量出图、归档。**不适用**：需要按日分批跟学的书籍（那用模式 A）。

### C.0 输出与目录（在工作目录里，不在 skill 里）
```bash
# 在工作目录下，用任务名建文件夹
python3 $SD/tile_setup.py init --dir "<工作目录>/标点符号规范" \
    --title "标点符号规范" --source "GB/T 15834-2011《标点符号用法》(docx)" --count 47
# 产物：GUIDE.md（手册）/ PROGRESS.md（进度）/ cards.json（骨架）/ src/ / refs/ / out/
```

### C.1 五道强制门禁（**一步都不能跳**）
| # | 动作 | 通过的标志 |
|---|---|---|
| 1 | 提取原文 → `src/full_text.txt`（**逐字提取，不要摘要**；段落/表格都要） | 全文可查 |
| 2 | 列知识点清单（编号 + 标题 + 要点 + 例子）+ 预计张数 | **用户确认范围与张数** |
| 3 | 只出**第 1 张示例卡** | **用户确认样式**（版式/配色/字号/信息密度） |
| 4 | `tile_setup.py export-md` 生成 `TEXT.md`（全量文本稿） | **用户逐条确认文本**（错别字 / 误正对比 / 例子遗漏 / 少见用法单独立卡） |
| 5 | 批量出图 → 逐张复核 → 归档 | 像素校验全通过 |

### C.2 命令速查
```bash
SD=<skill目录>; D="<工作目录>/标点符号规范"
python3 $SD/tile_setup.py export-md --dir "$D"                 # cards.json → TEXT.md（文本稿）
python3 $SD/gen_card_tile.py --cards "$D/cards.json" --outdir "$D/out"            # 批量出图（默认 3:4）
python3 $SD/gen_card_tile.py --cards "$D/cards.json" --outdir "$D/out" --only c07 # 只出某张（示例卡）
python3 $SD/gen_card_tile.py --cards "$D/cards.json" --outdir "$D/out" --ratio 9:16
python3 $SD/tile_setup.py check  --dir "$D"                    # 复检既有产物
python3 $SD/tile_setup.py sheet  --dir "$D" --cols 6           # 拼缩略总览图
python3 $SD/tile_setup.py log    --dir "$D" --entry "已出图 47 张。"   # 追加进度
python3 $SD/tile_setup.py status --dir "$D"
# 或走统一调度器：python3 $SD/render.py --type tile-3x4 --cards "$D/cards.json" --outdir "$D/out"
```

### C.3 cards.json（唯一事实源）
顶层：`group`（卡组名，显示在角标）/ `footer`（页脚来源文字）/ `ratio`（默认 3:4）/ `cards[]`。
每张卡：`id`（内部标识）/ `index`（序号，决定文件名前缀 `NN_` 与角标）/ `filename`（文件名主体）/ `title` / `subtitle` / `accent`（配色 key）/ `blocks[]`。

**blocks 六种类型**（`tag` 是左侧标签文字，`color` 是标签配色）：

| type | 用途 | 字段 |
|---|---|---|
| `text` | 核心用法 / 概述 | `text` |
| `list` | 要点 / 其他用法 / 注意事项 | `items[]`（支持 `\n` 换行） |
| `compare` | 易错对比（**误 / 正**） | `pairs[{wrong,right}]` |
| `marked` | 符号示意（字下加标记） | `text` + `mark:"dot"`（着重号）/ `"line"`（专名号） |
| `emphasis` | 一句话记忆点 | `text` |
| `diagram` | 字格 / 位置示意 | `rows[{label, note?, cells[]}]` |

`diagram` 的 cell（图元）可选形态：
`{"base":"字","mark":"。","where":"br"}`（字 + 位置标记：`bl/br/bc/c/l/r/top`）、
`{"t":"字"}`（灰字占位）、`{"c":"︱","pos":"c"}`（红色符号）、`{"w":0.5|2}`（半宽格 / 双宽格）、
`{"plain":true}`（去虚线框）、`{"vbar":true}`（竖线）、`{"pair":["甲","乙"]}`（同格两字）、
`{"vtext":"﹃\n字\n﹄"}`（同格竖排文本，`\n` 换行）、`{"glyph":"字","side":"right","plain":true}`（字右侧着重圆点）、
`{"base":"字","lmark":"︳"}`（**同格内**左侧内嵌专名号 / `︴` 为浪线式书名号）。

> 改内容**只改 cards.json**；删除/拆卡/重排一律写 `transform*.py` 脚本（幂等、可复跑），
> **不要手改 JSON**（易引入语法错误，也无法复跑）。

### C.4 渲染与版式规则
- 画布比例（`--ratio`）：**3:4（默认）**｜9:16｜1:1｜4:3｜16:9；`@192dpi` 输出 = CSS 尺寸 ×2。
- **内容自适应（核心机制）**：生成前先渲染一张超长页**测量内容真实高度**，超出画布则整体等比缩小
  字号/间距（k 从 1.0 递减，下限 0.62），直到完整落入画布——**从根本上杜绝「固定高度容器溢出被静默裁剪」**。
  k 落到 0.7 以下说明这张卡内容该**拆成两张**，不要硬塞。
- 页脚只有来源，**不放日期**；角标为 `第 index / total 张 · group`。
- 配色语义：核心用法=蓝 / 要点·其他用法=橙 / 易错=红（误红正绿）/ 提示=绿 / 图示=青。
- 中文正文一律用中文弯引号“”‘’；仅英文句 / 代码 / URL 内用直引号。
- **禁止 emoji**（weasyprint 不渲染）：用纯文字标记，如 `误 / 正`、`[OK]`。

### C.5 复核方法（**像素优先，视觉辅助**）
1. 每次出图**自动**做像素校验：尺寸是否等于画布 / **PDF 是否恰好 1 页**（>1 页 = 内容溢出）/
   是否空白 / **底部页脚底色带是否存在**。结果落 `out/_check.json`；**失败即非 0 退出，不要交付**。
   > 注意：页脚判定必须看**页脚底色带**，不能用「底部有没有文字像素」——溢出时正文文字也会
   > 落在页 1 底部，会造成**假通过**（实测 5 页 PDF 曾被判通过）。颜色容差 ≤3。
2. 复检：`tile_setup.py check --dir "$D"`；总览：`tile_setup.py sheet --dir "$D"`。
3. 放大局部人工复核时的**重要提醒**：视觉模型容易把「斜线 / 弯引号 / 细竖线 / 全角字符」
   误判成「裁切 / 缺失」，甚至会自相矛盾（一边说被裁切、一边说页脚完整）。
   **凡有疑问一律回到像素证据**（`_check.json` 的 `ink_bbox`、`footer_ink_ratio`），必要时把
   局部裁开再看。听视觉模型的判断前先问：像素支持它吗？

### C.6 踩坑清单（实战踩过，务必照做）
1. **固定高度容器溢出可能不产生第 2 页**，靠页数检测抓不到 → 必须「先测量真实高度，再缩字号」。
2. 测量高度时**阈值要与页面底色比较**（页脚底色是浅灰，用「接近纯白」判定会把页脚漏掉，导致内容比实测矮）。
3. 块 / 行设 `flex: 0 0 auto`（禁止压缩），否则长内容会把相邻元素挤出边界、造成重叠。
4. 空 `<span>` 画线宽度可能失效 → 改用 `border-left` 或显式 `width/height`。
5. weasyprint 下 `min-width: 0` 无效（拿它做 flex 收缩保护不管用）→ 用固定比例（如 `flex: 0 0 60%`）。
6. 「半字」标点要真的画**半宽格**，否则与说明不符。
7. **误 / 正对比必须是同一句话、仅差一处标点**；不要把规则讲解塞进「误」里当对比。
8. 顺序**就近**：易混对比、连用规则卡紧跟对应主卡，不单独成节。
9. 「少见用法」要**单独立卡**（如「问号·其他用法」「引号·其他用法」），不要只埋在要点里。
10. 原资料里的**内部章节号**（如「第 5 章」）、页眉页脚属于噪音，不要出现在卡片上。
11. 总览卡只作整体介绍，**不要**写「本卡组只讲易错点」这类限定语。
12. **字体家族列表必须简短（≤4 个）**：列表过长时 weasyprint 的逐字回退会整体退化，
    `unicode-range` 的破折号兜底会被静默忽略（渲染公共库已自动收敛为短栈）。
13. 着重号 **`.gl-vdot` 要用 `flex: 0 0 auto` + 固定宽高**，否则会被 flex 拉伸成椭圆。
14. 会话 / 环境重置会回滚文件 → 关键中间产物每轮改完**立即验证文件内容**（而不是依赖上一轮记忆）。

### C.7 归档（可选，按环境能力）
- 有上传能力的平台（如 IMA 知识库）：把 `out/*.png` + 文本稿一起放进去。
- **目标端若无删除接口**：重推前先把旧文件**改名**为 `【旧版N-可删除】…` 腾出干净名，再传新版，
  并**明确告知用户需要手动清理哪些旧文件**（API 删不掉）。
- 长 Markdown（含表格 `|`、反斜杠）写入被网关拦截时：改走「写文件 → 对象存储/上传接口 → 引用 key」的路径。

---

## 模式 A/B 的推送流程（每次调用执行一次）

### 英文书流程（需翻译）
1. **取载荷**（不要加 `--force`，让脚本自身的当日/周末/锁守卫生效，防重复推送）：
   `cd $SD && python3 push_card.py next --book <slug> > <临时目录>/b2l_payload.json`
   （Windows 无 `/tmp/`，用 `%TEMP%`）。
2. **联网核对术语**：对 terminology 每项，**用当前环境可用的联网搜索工具**查权威中文译法，汇总 terminologyZh。不可凭记忆。
3. **实时翻译**：coreIdea/explanation/quote/application 译为中文；explanation 按换行分段对应；
   术语首次出现「中文（英文）」；含 markdown 链接的保留 url 只译 text；翻译 relatedLinks 标题；
   **同时翻译 topic → topicZh**。中文一律用弯引号（`normalize_quotes.py` 会自动修正直引号）。
4. **写翻译 JSON** 到临时目录 `b2l_zh.json`（topicZh/coreIdeaZh/explanationZh/quoteZh/applicationZh/terminologyZh/relatedLinksZh/note）。
5. **生成卡片**：`python3 render.py --type <cardType> --payload <payload> --zh <zh> --out <产物路径> --language en`
6. **推送**（按 `config.pushMethod`）：
   - `local`：产物留在工作目录即可（无需推送）。
   - `ima`：`python3 upload_ima.py --file "<pdf>" --config books/<slug>/config.json --book-dir books/<slug>`
     退出码 0=成功；2=密钥失效（已发通知）不计进度结束；1=其他错误不更新进度结束。
   - `feishu`：`python3 send_feishu.py --payload … --zh … --config … --language en`
   - `feishu-api`：`python3 send_feishu_api.py --payload … --zh … --config … --language en`
     （如需同时发图片卡片，追加 `--image <png> --config …`）
7. **记录进度**（仅成功后）：`python3 push_card.py mark --book <slug> <nextId> success`。
8. **汇报**：第 X/N 张、主题、术语核对要点。

### 中文书流程（无翻译）
同上，但跳过步骤 2-4，`--language zh`，不传 `--zh`。

### 批量推送模式
```bash
python3 push_card.py list-next --book <slug> --n 10     # 预览（不加锁、不改状态）
python3 push_card.py next --book <slug> --n 5           # 取 5 张载荷
python3 push_card.py mark --book <slug> --ids id1,id2,id3,id4,id5 success
```
- `--n 1`（默认）保持「每日一张 + 当日锁 + 周末守卫」语义，适合定时任务。
- `--n > 1` 是**显式用户意图**：跳过当日/周末守卫与单卡锁，取完必须用 `--ids` 一次性回写。
- 大批量建议：**并行翻译 + 集中推送**（翻译可分工；写进度/写文档必须集中串行）。

## 卡片类型与渲染引擎（`render.py`）

```bash
python render.py --list                       # 看类型→引擎映射
python render.py --type long-study --payload p.json --zh z.json --out card.png
python render.py --type tile-3x4 --cards cards.json --outdir out            # 拆卡引擎
```

| cardType | 引擎 | 产物 |
|---|---|---|
| `pdf-standard` | gen_card_pdf.py | A4 标准卡片 PDF |
| `pdf-large` | gen_card_pdf_large.py | 大字闪卡 PDF |
| `long-image` | gen_image.py | 闪卡配图 PNG |
| `long-study` | gen_card_long.py | 移动端学习长图 PNG |
| `pdf-bilingual` | gen_card_bilingual.py | 中英对照文档 PDF |
| `tile-3x4` / `tile-9x16` / `tile-1x1` / `tile-4x3` / `tile-16x9` | gen_card_tile.py | **竖版知识卡片长图**（拆卡模式） |
| `feishu-card` / `feishu-card+image` | 推送层（见下方飞书方案） | — |

> 加自定义引擎不用改代码：在 config.json 里写 `"renderer": {"my-type": "my_engine.py"}`。
> 版式规范见 `references/design-spec.md`。

## 文档与进度

```bash
# 模式 A/B
python docs_layer.py init    --slug <slug> --title "…"
python docs_layer.py refresh --slug <slug>
python docs_layer.py log     --slug <slug> --entry "…"
python docs_layer.py status  --slug <slug>
python docs_layer.py mirror  --slug <slug>      # 可选：镜像到 IMA 笔记
# 模式 C
python tile_setup.py init|export-md|sheet|check|log|status --dir "<任务目录>"
```
**本地为底，平台镜像可选**。规范见 `references/workflow-notes.md`。

### 每一轮开工的固定动作
1. 读 `GUIDE.md`（模式 C）或 `docs/guide.md`（模式 A/B）——恢复规则；
2. `push_card.py status --book <slug>` / `tile_setup.py status --dir <D>`——定位进度；
3. 列「接下来 N 张」（模式 A/B）给用户确认是否跳过；
4. 再开始干活。
> 会话记忆被压缩后的恢复顺序：`GUIDE.md` → `PROGRESS.md` 底部 → `cards.json`/`progress.json` → 本文件 + `references/`。

## 脚本与文件清单

| 脚本 | 作用 |
|---|---|
| `setup_verify.py` | **开工前先跑**：依赖 / 光栅化通道 / 中文字体 / 破折号字体 / 拆卡引擎体检 |
| `render_common.py` | 渲染**纯工具**（字体探测、破折号兜底、MDX 清理、转义、表格、配图、裁白、光栅化） |
| `render.py` | 按「卡片类型 → 引擎」调度（含 tile-* 拆卡类型） |
| `gen_card_tile.py` | **拆卡引擎**（3:4 默认 / 9:16 / 1:1 / 4:3 / 16:9；自适应防裁切；内置像素校验） |
| `tile_setup.py` | **拆卡编排**（init / export-md / sheet / check / log / status；手册与进度写在工作目录） |
| `gen_card_pdf.py` / `gen_card_pdf_large.py` | A4 标准 / 大字卡片引擎 |
| `gen_card_long.py` | 学习长图引擎（800px，金句→术语→观点→要点） |
| `gen_card_bilingual.py` | 中英对照文档引擎（逐块对照） |
| `gen_image.py` | 闪卡配图引擎（1:1 / 1:4） |
| `fetch_site.py` | 网站模式抓取（sitemap + 导航双通道 → catalog.json + raw/） |
| `book_setup.py` | 书籍拆解编排（extract / init / gen-cards / gen-index / download-imgs / prompt） |
| `items_io.py` | 内容源读写（兼容 `items.json` 与分章节 `items/` 两种布局） |
| `push_card.py` | 进度与取卡（status / list-next / next / mark / weekday / list-books） |
| `validate.py` | 推送前校验：内容源一致性 + 中英逐块对齐 |
| `docs_layer.py` | 操作指南 + 进度笔记（本地为底，IMA 可选镜像） |
| `upload_ima.py` / `send_feishu.py` / `send_feishu_api.py` | 可选推送渠道 |
| `process_attachments.py` | 相关链接附件下载/转换/重命名 |
| `notify_failure.py` | 通用失败通知（参数化 webhook） |
| `tests/` | 渲染公共库自检 + 离线测试数据 |

数据目录：`books/<slug>/`（模式 A/B）或 `<工作目录>/<任务名>/`（模式 C）。

## references 索引

| 文件 | 内容 |
|---|---|
| `references/config-schema.md` | 配置项逐项说明 + 首次启动确认清单 |
| `references/site-mode.md` | 网站模式完整流程 |
| `references/design-spec.md` | 卡片版式规范（含拆卡 3:4 版式） |
| `references/pitfalls.md` | 踩坑清单（渲染/字体/流程/质量，跨平台表述） |
| `references/workflow-notes.md` | 操作指南 + 进度笔记规范，记忆压缩后的恢复路径 |
| `references/platform-notes.md` | **平台适配注意事项**（含 IMA 环境：凭据、上传、无删除接口等） |

> 注意：**关键规则与踩坑已内嵌在本文件与 `GUIDE.md` 里**，不依赖「去翻参考文档」；
> references 是加深与排障用的补充材料。

## 变更记录

- **1.6.1（2026-10-05，全面修复版）**：修复全量审查发现的 60+ 处问题。**高危**：
  `prompt` 对默认 pushMethod=local 现在正确生成本地落盘指令（原先错误生成飞书指令，
  默认配置每日推送必失败）；`mark` 增加 id 白名单校验（误传文件名不再静默重置整本书进度）；
  `lastPushedId` 不在 index.json 时报 stale_progress 而非从头重推；sitemap 索引
  （sitemapindex）正确展开子 sitemap（原先把子 sitemap 地址当页面 URL，真实页面全漏）；
  `normalize_quotes` 代码块/行内代码/URL 内的直引号受掩码保护（原先 `print("你好")`
  会被改成弯引号），smart 模式成为默认；`fetch_site.py` 增量更新（--urls-file）不再
  覆写毁掉 catalog.json（按 URL 合并、保旧 idx）；upload_ima 子进程异常不再把 COS
  凭据带进 traceback。**中危**：`--force` 现在可接管失败锁；批量 mark 按 index 顺序
  回写 lastPushedId；gen_card_long 支持 items.json 标准的字符串列表术语（中文学术语区
  不再消失）；progress/items/catalog 等 JSON 全部原子写；split 布局统一走 items_io
  （gen-cards/gen-index/download-imgs/log-progress 不再绕过）；prompt 生成校验步骤并
  传播 B2L_DATA_DIR；book_setup/gen_card_bilingual 等文档与 CLI 参数对齐（slug 两种
  写法都接受）；JSON 文件统一 utf-8 显式编码；飞书 webhook 不再发送 URL 型 img 元素
  （整卡被拒），Open API 版改为下载后上传拿 image_key；process_attachments 的 curl
  退出码纳入判定、同名附件加短哈希防覆盖。**低危**：gen_image 固定比例校验页数、
  PDF 产物魔数校验、HTML GB18030 回退解码、file:// 百分号编码、单引号属性解析、
  fitz 同名垃圾包防护、时区支持（B2L_TZ）、死代码清理等。
- **1.6.0**：新增**模式 C「资料拆卡」**——`gen_card_tile.py`（多比例竖版卡片长图，
  自适应防裁切，内置像素校验）、`tile_setup.py`（工作目录内的任务编排 + 内嵌经验的
  操作手册/进度）。跨平台改造：默认落本地、IMA/飞书降为可选渠道、文档一律落工作目录、
  新增 `references/platform-notes.md`；踩坑清单并入拆卡实战经验（测量阈值含页脚、
  `flex: 0 0 auto`、weasyprint `min-width:0` 无效、视觉模型误判以像素为准、字体家族 ≤4、
  着重号圆点防拉伸等）。复核定稿：拆卡校验改为**双硬判据**（PDF 页数必须为 1 +
  底部页脚**底色带**存在），修掉「内容溢出却校验假通过」的漏洞；默认 `pushMethod` 统一为
  `local`；A/B 模式数据根支持环境变量 `B2L_DATA_DIR` 重定向到持久化目录。
- 1.5.0：新增网站模式、四种卡片类型与调度器、渲染公共库、内容源双布局、批量推送、
  首次启动确认门禁、校验脚本、文档层、环境体检与自检。
- 1.4.1：书籍多格式提取 / 三种推送方式 / 进度与失败通知。

---

## 飞书推送方案说明（可选渠道）

### 方案一：Webhook（send_feishu.py）
构造飞书 interactive 卡片 JSON，POST 到 webhook URL。
- header：蓝色标题「书名 · 主题」（禁止 emoji）
- elements：进度+章节 → 术语表（markdown 表格）→ 内容分栏 → 配图 → 相关链接 → 来源
- 图片：base64 → 上传 catbox.moe 取 URL（上传失败则提示「配图见来源链接」）

### 方案二：Open API（send_feishu_api.py）
App ID + App Secret 直发指定会话，支持原生图片/文件。
```json
{"pushMethod": "feishu-api",
 "feishuApi": {"appId": "cli_xxx", "appSecret": "xxx", "chatId": "oc_xxx"}}
```
也可用环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_CHAT_ID`。
创建应用：https://open.feishu.cn/app → 开通 `im:message` / `im:message:send_as_bot` / `im:resource` → 机器人加入目标群。
发送模式：`--payload [--zh]`（卡片）/ `--image <png>`（图片）/ `--file <pdf>`（文件）。

## 推送模板系统

每本书在 config.json 的 `template` 字段选择模板（首次配置时 AI 引导用户选）。

| 模板 ID | 名称 | 脚本 | 适用场景 |
|---|---|---|---|
| `pdf-standard` | PDF 标准卡片 | gen_card_pdf.py | 工具书、长文知识点 |
| `pdf-large` | PDF 大字卡片 | gen_card_pdf_large.py | 单词、术语、短知识点 |
| `feishu-card` | 飞书交互卡片 | send_feishu.py | 即时学习提醒 |
| `feishu-card+image` | 飞书卡片+图片 | send_feishu.py + gen_image.py | 知识点可视化 |

**配色**（Material 色系，所有模板统一）：绿 `#1e8e3e` 核心观点 / 蓝 `#1a73e8` 解释·标题栏 /
紫 `#7b1fa2` 金句 / 橙 `#f9ab00` 应用·术语 / 红 `#d93025` 术语标签·错误状态。
**字体栈**：跨平台（雅黑 → 苹方 → 冬青黑 → Noto CJK → 思源黑体 → 文泉驿 → 宋体），
渲染前由 `render_common.normalize_font_stack()` 自动收敛为**短栈**（见踩坑第 12 条）。
**超链接**：一律纯文字（多数知识库/IM 不能点击）。

## 配置确认与进度文件

- **配置汇报**：`python3 book_setup.py summary <slug>` 输出详细配置（书名/语言/粒度/卡片转化/
  模板/通道/目标/通知/文件清单），用户确认后再生成定时任务提示词。
- **daily-progress.md**：每本书 `books/<slug>/daily-progress.md`，每次推送成功后追加一行：
  ```markdown
  | 日期 | 序号 | 卡片ID | 主题 | 推送方式 | 状态 |
  |------|------|--------|------|----------|------|
  | 2026-06-30 | 1/118 | ch01-01 | 西方音乐记谱法导论 | local | 成功 |
  ```

## 辅助命令

- 查看所有书：`cd $SD && python3 push_card.py list-books`
- 查看进度：`python3 push_card.py status --book <slug>` ｜ `python3 tile_setup.py status --dir <D>`
- 配置确认：`python3 book_setup.py summary <slug>`
- 手动重推（跳过当日守卫，仅排障用；正常推送不要加 `--force`）：`python3 push_card.py next --book <slug> --force`
- 输出定时提示词：`python3 book_setup.py prompt <slug>`
- 记录进度到 md：`python3 book_setup.py log-progress <slug> --card-id <id>`

## 注意事项

- 进度是唯一凭证，勿手动误改 `progress.json`；失败绝不计进度，确保下次重推同一张。
- PDF 文件名日期格式统一 `YYYY-MM-DD`。
- 英文书翻译质量优先：术语必须联网核对。
- **禁止 emoji**：HTML→PDF→图片流程中任何 emoji 都无法渲染，一律用纯文字标记。
- **中文引号规范**：`normalize_quotes.py` 会把英文直引号自动修正为中文弯引号。
- **产物必须校验**：渲染后校验（尺寸 + 非空白 + 页脚），失败中止，不交付未验证产物。
- 假设不同用户使用：所有配置在 config 里，不硬编码；账号凭据只走环境变量。
