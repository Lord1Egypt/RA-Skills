---
name: english-daily-report
version: 1.2.2
description: 生成每日英语学习报告，包含新闻摘要、中文翻译、词汇注释、PDF 和音频版本。适用于：(1) 接收每日英语新闻摘要进行学习，(2) 获取中文翻译和词汇注释，(3) 生成 PDF 和音频版本用于离线学习
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires":
          {
            "bins": ["bash", "chrome"],
            "tools": ["tts", "web_search", "web_fetch"],
            "env": ["BRAVE_API_KEY(optional)"],
          },
        "install":
          [
            {
              "id": "chrome",
              "kind": "system",
              "label": "Google Chrome or Chromium (for PDF generation)",
              "check": "command -v google-chrome || command -v chromium || test -f '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'",
            },
          ],
      },
  }
---

# English Daily Report Skill - 英语每日报告

生成每日英语学习报告，包含新闻摘要、中文翻译、词汇注释、PDF 和音频版本。

## ⚠️ 前置依赖要求

**安装前请确认以下依赖已就绪：**

### 🔒 安全说明

本技能包含 PDF 生成脚本，已实施以下安全措施：

- **HTML 转义防护**：所有用户输入内容（标题、内容、翻译、词汇）均经过 HTML 实体转义
- **沙箱建议**：脚本在用户本地 workspace 运行，不访问外部网络
- **代码审查**：脚本开源可审计，位于 `scripts/generate-pdf-html.sh`

**建议**：首次使用前可审查脚本代码，确认无恶意内容。

| 依赖 | 类型 | 用途 | 是否必需 |
|------|------|------|----------|
| **Bash** | Shell | 运行生成脚本 | ✅ 必需 |
| **Chrome/Chromium** | 系统应用 | 无头模式渲染 PDF | ✅ 必需 |
| **TTS 工具** | OpenClaw 工具 | 生成音频 (MP3) | ✅ 必需 |
| **web_fetch 工具** | OpenClaw 工具 | 抓取新闻网页 | ✅ 必需 |
| **web_search 工具** | OpenClaw 工具 | 搜索今日新闻 | ⚠️ 可选（需 API 密钥） |
| **BRAVE_API_KEY** | 环境变量 | web_search 的 API 密钥 | ⚠️ 可选 |

### 检查依赖

```bash
# 检查 Chrome/Chromium
# macOS:
test -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" && echo "Chrome OK"
# Linux:
command -v google-chrome || command -v chromium || command -v chromium-browser

# 检查 TTS 工具（OpenClaw 内置）
openclaw help tts
```

### 安装 Chrome（如未安装）

- **macOS**: https://www.google.com/chrome/
- **Linux**: `sudo apt install chromium-browser` 或 `sudo yum install chromium`
- **Windows (WSL)**: 使用 Windows Chrome 路径

### 配置 TTS

TTS 使用 OpenClaw 内置工具，无需额外配置。可选配置语速：

```json
// ~/.openclaw/openclaw.json
{
  "messages": {
    "tts": {
      "edge": {
        "rate": "-15%"  // 负值=更慢，适合英语学习
      }
    }
  }
}
```

### 配置 Brave API（可选，用于真实新闻搜索）

```bash
# 获取 API 密钥：https://brave.com/search/api/
openclaw configure --section web
# 或设置环境变量：export BRAVE_API_KEY=your_key
```

---

## 工作流程

### 1. 获取新闻

**模式 A：真实新闻抓取（优先）**

使用 `web_search` 或 `web_fetch` 获取今日英语新闻：

```
# 前提：需要配置 Brave Search API 密钥
# 配置方法：openclaw configure --section web 或设置 BRAVE_API_KEY 环境变量

# 方式 1：使用 web_search 搜索今日新闻（freshness="pd" 表示过去一天）
web_search query="tech news" freshness="pd" count="5"
# 从返回结果中选择 1-2 篇，用 web_fetch 抓取具体内容

# 方式 2：直接用 web_fetch 尝试多个新闻源（无需 API 密钥）
# 按顺序尝试，直到成功获取内容
web_fetch url="https://www.chinadaily.com.cn/world"
web_fetch url="https://news.cgtn.com/"
web_fetch url="https://www.shanghaidaily.com/"
web_fetch url="https://www.globaltimes.cn/"
# 选择 1-2 篇相关新闻进行摘要
```

**⚠️ 重要：多链接尝试策略**

单个链接失败时，应依次尝试多个备用链接：
1. 先试首页/栏目页（如 `/world`、`/china`）
2. 再试具体文章页（从首页提取链接）
3. 至少尝试 3 个不同来源
4. 全部失败后才降级为模拟新闻模式

**模式 B：模拟新闻生成（降级方案）**

当无法获取真实新闻时（如 API 未配置、网站无法访问），生成模拟新闻用于学习：

```
- 基于当前时事趋势生成合理的新闻主题
- 创建约 100 词的英语学习材料
- 内容用于语言学习，非真实新闻报道
```

**⚠️ 重要：内容来源标注**

生成的报告必须明确标注内容来源：
- **真实新闻**：标注新闻来源和原始链接
- **模拟新闻**：标注"学习材料 · 非真实新闻"

这样用户不会误将模拟内容当作真实新闻。

### 2. 创建摘要

创建约 100 词的英语摘要，包含：

- **Title（标题）**: 清晰、描述性的 headline
- **Content（内容）**: 约 100 词，涵盖关键事实
- **Chinese translation（中文翻译）**: 完整翻译（全文释义）
- **Vocabulary（词汇）**: 5-8 个不常见单词及中文释义

### 3. 生成 PDF

使用附带的脚本：

```bash
# 格式：scripts/generate-pdf-html.sh "DATE" "TYPE" "TITLE" "CONTENT" "TRANSLATION" "word1:meaning1" ...
# TYPE: "real" = 真实新闻，"study" = 学习材料（模拟新闻）

# 真实新闻示例：
scripts/generate-pdf-html.sh "2026-03-26" "real" "News Title" "English content..." "中文翻译..." "word1:释义 1" ...

# 学习材料示例：
scripts/generate-pdf-html.sh "2026-03-26" "study" "News Title" "English content..." "中文翻译..." "word1:释义 1" ...
```

脚本功能：
- 根据 TYPE 参数显示不同的内容类型徽章（真实新闻/学习材料）
- 学习材料模式自动添加黄色警告框
- 创建带有漂亮渐变标题的 HTML
- 使用系统默认字体（自动检测中文字体）
- 通过 Chrome 无头模式转换为 PDF
- 保存到 `uploads/english-daily-DATE.pdf`

### 4. 生成音频

使用 TTS 工具将英语摘要转换为语音，然后复制到 uploads 目录：

```
# 生成 TTS 音频
tts text="<English news summary>"

# TTS 工具返回类似 /tmp/openclaw/tts-xxx/voice-xxx.mp3 的音频路径
# 使用正确的命名复制到 uploads：
cp <tts-output-path> uploads/english-daily-DATE.mp3
```

保存到 `uploads/english-daily-DATE.mp3`

#### 调整语速

如果音频语速太快，可以在 `openclaw.json` 中配置 TTS 语速：

```json5
{
  messages: {
    tts: {
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        rate: "-15%",  // 负值 = 更慢，正值 = 更快（范围：-50% 到 +50%）
        pitch: "-5%",
      },
    },
  },
}
```

**英语学习推荐语速：**
- `-10%` 到 `-20%`: 较慢，更适合学习者
- `0%`: 正常语速
- `+10%` 到 `+20%`: 较快，更自然的会话节奏

你也可以使用 `/tts` 命令在每个会话中调整设置。

### 5. 发送给用户

通过 Feishu（或其他渠道）发送三条消息：

1. **文本版本**: 格式化的摘要和词汇注释
2. **音频版本**: TTS 生成的 MP3，用于听力练习
3. **PDF 版本**: 精美的可打印 PDF

## 文件结构

```
english-daily-report/
├── SKILL.md（本文件）
├── scripts/
│   └── generate-pdf-html.sh  # PDF 生成脚本
└── references/
    └── example-report.md     # 示例报告格式
```

## 输出格式

### 文本版本

**真实新闻模式：**
```
📰 English Daily Report - 2026-03-26
【真实新闻 · Real News】

**China's Quantum Computing Breakthrough Achieves New Milestone**
来源：China Daily
原文链接：https://www.chinadaily.com.cn/a/202603/26/WSxxxxx.html

English content (~100 words)...

---

📖 全文释义

中文完整翻译...

---

📝 Vocabulary & Grammar Notes:

- **word1** (pos.): 中文释义
- **word2** (pos.): 中文释义
...
```

**模拟新闻模式：**
```
📰 English Daily Report - 2026-03-26
【学习材料 · Study Material · 非真实新闻】

**Global Education Technology Market Sees Rapid Growth**
⚠️ 本文为英语学习材料，基于真实时事趋势编写，非真实新闻报道

English content (~100 words)...

---

📖 全文释义

中文完整翻译...

---

📝 Vocabulary & Grammar Notes:

- **word1** (pos.): 中文释义
- **word2** (pos.): 中文释义
...
```

**⚠️ 标注要求：**
- 必须在报告开头清晰标注内容类型
- 真实新闻：注明来源和链接
- 模拟新闻：注明"非真实新闻"，避免误导

### PDF 版本

- 带有标题和日期的渐变标题
- 英语摘要部分
- 中文翻译部分
- 词汇部分（高亮显示单词）
- 页脚带有学习计划品牌标识

### 音频版本

- TTS 生成的英语朗读
- 清晰的发音，适合学习
- 保存为 MP3 格式，支持离线收听

## 提示

### 新闻来源

**国际新闻（某些地区可能需要代理）：**
- Reuters: `https://www.reuters.com/`
- BBC: `https://www.bbc.com/news`
- NPR: `https://www.npr.org/`
- AP News: `https://apnews.com/`

**国内英语新闻（无需代理即可访问）：**
- China Daily: `https://www.chinadaily.com.cn/`
- CGTN: `https://news.cgtn.com/`
- Shanghai Daily: `https://www.shanghaidaily.com/`
- Global Times: `https://www.globaltimes.cn/`
- Xinhua English: `http://www.xinhuanet.com/english/`

### 其他提示

- **词汇选择**: 选择 5-8 个不常见但实用的单词
- **音频长度**: 保持在 1 分钟以内，提高参与度
- **PDF 设计**: 系统字体自动检测中文字符
- **一致性**: 每天固定时间发送，帮助养成学习习惯

## 故障排除

### 依赖检查

**检查所有依赖是否就绪：**

```bash
# Bash (通常已预装)
bash --version

# Chrome/Chromium
# macOS:
test -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" && echo "Chrome OK" || echo "Chrome NOT FOUND"
# Linux:
command -v google-chrome || command -v chromium || echo "Chrome/Chromium NOT FOUND"

# OpenClaw 工具
openclaw help tts
openclaw help web_fetch
```

### Chrome/Chromium 未找到

**错误信息：** `ERROR: Chrome/Chromium not found`

**解决方案：**
1. 安装 Chrome：https://www.google.com/chrome/
2. 或安装 Chromium：
   - Ubuntu/Debian: `sudo apt install chromium-browser`
   - CentOS/Fedora: `sudo yum install chromium`
   - macOS: 使用 Homebrew `brew install --cask google-chrome`

### web_search 提示 "missing_brave_api_key"

`web_search` 需要 Brave Search API 密钥（可选）。

**解决方案：**
1. 申请 API 密钥：https://brave.com/search/api/
2. 运行 `openclaw configure --section web` 存储密钥
3. 或在 Gateway 环境中设置 `BRAVE_API_KEY` 环境变量
4. **或不配置**：技能会降级为多链接 web_fetch 模式或模拟新闻模式

### TTS 音频生成失败

**错误信息：** `TTS conversion failed`

**原因：** 未配置 TTS 提供商（Edge TTS 默认启用，无需 API 密钥）

**解决方案：**
1. 确认 OpenClaw 配置中启用了 Edge TTS（默认启用）
2. 检查网络连接（Edge TTS 需要访问微软服务）
3. 或配置 OpenAI/ElevenLabs API 密钥作为备选

### web_fetch 失败，显示 "fetch failed"

这通常意味着网站被阻止或网络无法访问。

**解决方案：**
1. 尝试其他新闻来源（参见提示部分）
2. 使用国内英语新闻（China Daily、CGTN 等）
3. 在 Gateway 环境中配置网络代理
4. 降级为模拟新闻模式（用于学习目的）

### PDF 中文字符显示为方框

macOS 上不应该出现此问题（自动检测中文字体）。如果出现方框：
- 检查 Chrome 是否已安装：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- 确保系统支持中文字体

### 找不到 Chrome/Chromium

脚本会自动检测以下位置的 Chrome/Chromium：
- **macOS**: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- **Linux**: `google-chrome`、`chromium` 或 `chromium-browser`（通过 PATH）
- **Windows (WSL)**: `/mnt/c/Program Files/Google/Chrome/Application/chrome.exe`

如果未找到，请安装 Chrome 或确保它在 PATH 中。

### TTS 音频未保存

TTS 工具会自动返回音频。使用 `message` 工具发送音频文件路径。


### 脚本权限被拒绝

确保脚本可执行：
```bash
chmod +x ~/.openclaw/workspace/skills/english-daily-report/scripts/generate-pdf-html.sh
```
