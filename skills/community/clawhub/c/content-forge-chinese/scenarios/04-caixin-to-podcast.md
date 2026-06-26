# 场景 4：财新文章 → 通勤播客

## 一句话定位
财新付费文章 URL → 绕付费墙抓取 → NotebookLM 双人对话播客 → 通勤路上听。

## 触发词

- 「财新文章生成播客」「这篇财新转播客」
- 「把财新报道做成通勤播客」
- 「财新月刊 / 周刊 转音频」

## 为什么单独做？

财新（caixin.com）的付费墙策略和海外站点不同：
- ❌ Googlebot / archive.today / Google Cache 在国内/对财新都基本无效
- ✅ 有效路径：手机 App 长截图 OCR、订阅用户 cookie 注入、AMP 页面、搜索引擎收录的快照

本场景**预设国内特化路径**，避免无效尝试。

## 输入

| 字段 | 必填 | 说明 |
|---|---|---|
| 财新文章 URL | ✅ | `https://www.caixin.com/2026-xx-xx/xxx.html` |
| 播客风格 | ⬜ | `深度对谈` / `新闻速递` / `辩论式`，默认深度对谈 |
| 时长偏好 | ⬜ | `8min` / `15min` / `25min`，默认 15min |
| 输出语言 | ⬜ | `中文` / `中英双语`，默认中文 |

## 输出

- 播客 mp3（NotebookLM 生成的双人对话）
- 文字稿（NotebookLM 自动生成的 transcript）
- 元数据：标题、原文 URL、生成时间、时长

## 抓取策略（国内特化）

按以下顺序尝试：

```
Priority 1: 用户 cookie 注入（如有订阅）
  ├─ 用户提供 caixin.com 登录后的 cookie
  ├─ Playwright 直接带 cookie 访问，得完整内容
  └─ ✅ 最优路径，质量满分

Priority 2: AMP 页面
  ├─ URL 改造：caixin.com/xxx.html → caixin.com/amp/xxx.html
  ├─ AMP 版部分文章不限免可见
  └─ 🟡 概率 ~40%

Priority 3: 微信公众号搜一搜
  ├─ 财新部分文章会同步到「财新网」公众号
  ├─ wexin-read MCP 抓公众号版（往往无付费墙）
  └─ 🟡 概率 ~30%（同标题搜索）

Priority 4: 财新 App 截图 OCR
  ├─ 让用户手机长截图 → 上传图片
  ├─ 调 OCR（PaddleOCR / 用户 API）提文字
  └─ 🟡 适合一次性获取

Priority 5: 用户手动复制粘贴
  ├─ 给出明确指引："请你打开 App 全选文章正文，粘贴给我"
  └─ 🟢 100% 兜底
```

## 工作流

### 生成路径决策树

```
财新 URL / 文章文本
  ↓
[Step 1] 抓取（按优先级）→ article.md
  ↓
[Step 2] 检测 NotebookLM 可用性
  └─ `notebooklm status` → 可用 → 走路径 A（推荐，Audio Overview 效果最好）
  └─ 不可用 → 降级走路径 B（直接 LLM 生成播客文字稿）
```

### 路径 A：NotebookLM 路径（推荐）

```
[Step A1] 内容预处理
  ├─ 财新特有：作者信息、发表日期、文末"特别声明"剥离
  ├─ 财新长文常含图表 → 提取图片描述
  └─ 输出：clean_article.md

[Step A2] 上传 NotebookLM（Playwright 浏览器上传）
  node scripts/notebooklm-playwright.js upload-text "财新·<文章标题>" "<文章标题>" "<content>"

[Step A3] 生成 Audio Overview（核心）
  node scripts/notebooklm-playwright.js generate "财新·<文章标题>" audio [outputDir]
  # 脚本自动：打开笔记本 → 点击"音频概览" → 等待生成完成
  # 可选：添加自定义 prompt 文本

[Step A4] 下载 mp3 + transcript
  ├─ 自动下载到 ~/Downloads/neirong-gongfang/caixin-podcast/<日期>/
  ├─ 文件命名：<日期>-<标题截短>.mp3
  └─ 同目录附 transcript.txt

[Step A5] 询问落地
  ├─ AirDrop 到手机？
  ├─ 上传到播客 App？
  └─ 写入 IMA / 飞书（保存文字稿）？
```

### 路径 B：C 方案（降级 fallback）

```
[Step B1] LLM 生成播客对话稿
  → 将 article.md 按"通勤播客"prompt 转换为双人对话文字稿
  → 保留关键数据和引用

[Step B2] 输出 podcast-script.md（含时间戳估算）

[Step B3] 落地同上
```

---

## Audio Overview 自定义 Prompt

```
请基于这篇财新文章，生成一段中文双人对谈播客。

风格要求：
- 两位主持人：一位是宏观经济记者，一位是行业研究员
- 不读文章，而是讨论文章 —— 提出疑问、补充背景、给出立场
- 涉及数据 / 政策时，主持人之间互相挑战："这个数据是怎么得出的？"
- 中段穿插一段"读者视角"：如果我是普通投资者 / 从业者，这意味着什么
- 结尾给"3 个值得追踪的下一步指标"

时长目标：~15 分钟，平均语速。

禁止：
- 朗读式播报
- 重复文章原句
- 编造文章未提的数据
```

## 通勤播客小工具：导入到播客 App

生成 mp3 后，本 Skill 可选自动：

1. **AirDrop 到 iPhone** —— `osascript` 调系统分享
2. **写入 NAS 共享文件夹** —— 让家里的 Apple TV / Plex 看见
3. **Push to Pocket Casts** —— 通过 Files 上传

或更优雅的：搭一个**私人播客 RSS**，把 mp3 放到云存储，生成 RSS XML，在播客 App 订阅 —— 每篇财新自动出现在播客 App 里。

## 降级方案

| 失败点 | 降级 |
|---|---|
| 所有 P1-P5 都拿不到全文 | 让用户手动粘贴或换文章 |
| NotebookLM 生成 Audio Overview 失败 | 改用 ChatTTS / Edge-TTS + 自写双人脚本 |
| mp3 下载断流 | NotebookLM 重试，或截屏视频用 ffmpeg 提音轨 |

## 输出物示例

```
~/Downloads/neirong-gongfang/caixin-podcast/2026-05-20/
├── article.md
├── meta.json
├── 2026-05-20-中国出口结构调整.mp3   # 14:32
├── transcript.txt
└── source-link.txt   # 原文 URL，方便回查
```

## 🛡️ 诚实度契约

> 详见 `references/honesty-rules.md`

### ⚠️ 本场景最大风险

NotebookLM Audio Overview 生成的"双人对话"是 **AI 演绎的虚拟主播**，不是真嘉宾说的话。
听众有"听到 = 真实"的心理暗示，必须显著标注。

### 完整度声明（按抓取路径分）

| 抓取路径 | source_completeness | ai_inference_ratio |
|---|---|---|
| 用户 cookie 拿到完整文章 | full | medium（NotebookLM 演绎） |
| AMP 部分内容 | partial | high |
| 公众号镜像 | partial | high |
| 仅元数据 | metadata-only | very high（不建议出播客） |

### 输出 mp3 + transcript 必带

播客文件本身改不了，但**目录里必须放一份说明文件**：

```markdown
# 听之前请先读

🤖 本播客由 NotebookLM 基于以下 source 演绎生成：
- 原文 URL: [link]
- 完整度: [full / partial / metadata-only]

⚠️ 播客中的对话内容**不是任何真人说过的**。
两位"主持人"是 NotebookLM 生成的虚拟人，他们的判断/分析/演绎可能：
- 不在原文中出现
- 包含 AI 训练数据的背景知识
- 把单一观点扩展为辩论形式

请以原文为准，把播客作为"快速过一遍主旨"的辅助工具。
```

### 输出 schema 必带

```json
{
  "source_completeness": "...",
  "ai_inference_ratio": "high",
  "method": "NotebookLM Audio Overview",
  "warnings": [
    "播客内容为 AI 演绎，非真人对话",
    "判断和分析可能不在原文出现"
  ]
}
```
