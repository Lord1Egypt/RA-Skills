# B站视频字幕助手 (Bilibili Subtitle Studio Skill)

这是一个专为 AI Agent 设计的 B 站视频分析组件，旨在通过自动化的字幕提取和处理流程，让 AI 能够“看懂”并精准定位视频内容。

## 🚀 核心功能

- **自动化字幕提取**：优先获取 AI 自动生成的字幕，自动回退到 UP 主上传的 CC 字幕。
- **登录态支持**：集成扫码登录脚本，突破 B 站 AI 字幕必须登录才能获取全文的限制。
- **内容深度分析**：基于原始文本生成结构化摘要，快速了解长视频干货。
- **精准时间搜索**：支持在带时间戳的 SRT 字幕中搜索关键词，定位视频具体位置。

## 📦 安装方法

你可以使用 [skills.sh](https://skills.sh) 工具将其安装到你的 AI 编码助手中（如 Claude Code, Antigravity, Cursor 等）：

```bash
npx skills add BAIKEMARK/bilibili-summary-skill
```

## 🛠️ 环境依赖

仅需安装 `requests`（必须）和 `qrcode`（推荐，用于显示扫码二维码）：

```bash
pip install requests qrcode
```

## 📖 使用指南

安装后，你可以直接对 AI 下达指令：

- “帮我分析一下这个视频讲了什么：[B站链接]”
- “视频里什么时候提到了‘配得感’？”
- “帮我提取这个 BV 号的字幕并生成摘要”

## 📂 结构说明

- `SKILL.md`: 核心指令集，定义了 Agent 的触发场景和逻辑。
- `scripts/fetch_subtitle.py`: 核心执行脚本，完全自包含，无外部依赖。
- `scripts/cookie_login.py`: B 站扫码登录工具。
- `scripts/search_timestamp.py`: SRT 时间戳精准搜索工具。

## 🔒 隐私声明

本工具仅在本地运行，你的 B 站 Cookie 会保存在当前项目目录下的 `cookie.txt` 中，不会上传到云端。请妥善保管该文件。

---
Powered by [Antigravity](https://github.com/google-deepmind/antigravity)
