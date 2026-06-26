---
name: douyin-to-obsidian
description: 抖音视频文案自动提取工具，一键将抖音视频转为结构化 Obsidian 笔记。支持绕过风控、本地 Whisper 语音识别、长视频分段处理。
---

# Douyin to Obsidian

🎯 **抖音视频文案自动提取工具**

一键将抖音视频转为结构化 Obsidian 笔记，支持绕过风控、本地 Whisper 语音识别、长视频分段处理。

## 核心功能

- ✅ **智能识别** - 支持抖音短链/分享口令自动解析
- ✅ **绕过风控** - 自动绕过抖音滑动验证码和 SSR 数据封锁
- ✅ **本地识别** - 使用 Whisper AI 本地语音识别，零 API 成本
- ✅ **结构化输出** - 自动生成带 YAML Frontmatter 的 Markdown 笔记
- ✅ **长视频支持** - 自动分段处理，支持任意时长视频
- ✅ **自动安装** - FFmpeg 自动下载，无需手动配置

## 使用方式

### 快速开始

```bash
# 1. 安装依赖
pip install -r scripts/requirements.txt

# 2. 安装浏览器自动化
playwright install chromium

# 3. 运行提取
python scripts/run_extract.py "https://v.douyin.com/xxxxx/"
```

### 输入格式

支持多种输入格式：
- 完整 URL: `https://v.douyin.com/xxxxx/`
- 分享口令：`3.58 KJi:/ d@A.tR 06/21 通达信自选股+Python#qmt#量化交易 https://v.douyin.com/xxxxx/`
- 短链接：`https://v.douyin.com/xxxxx/`

### 输出示例

笔记自动保存到 Obsidian 目录（默认：`E:\icloud\iCloudDrive\iCloud~md~obsidian\myobsidian`）

```markdown
---
标题：视频标题
作者：作者名
链接：https://v.douyin.com/xxx
时长：7 分 42 秒
提取时间：2026-03-22 20:15:00
标签：#AI #杨立昆 #AGI
---

# 视频标题

完整的语音识别文案内容...
```

## 技术特点

### 反爬策略
- 精选模态链接绕过风控
- 自定义 User-Agent 和浏览器指纹
- 智能短链解析和重定向处理

### 语音识别
- OpenAI Whisper base 模型（中文优化）
- 支持长视频自动分段（默认 10 分钟/段）
- 自动标点符号和文本规范化

### 架构设计
- 基于 asyncio 的异步处理
- FFmpeg 自动下载和管理
- 临时文件自动清理

## 系统要求

- **Python**: 3.8+
- **磁盘空间**: 首次运行约 200MB（Whisper 模型 + FFmpeg）
- **操作系统**: Windows（macOS/Linux 需手动安装 FFmpeg）

## 依赖项

```txt
requests>=2.31.0
aiohttp>=3.9.0
ffmpeg-python>=0.2.0
openai-whisper>=20231117
openai>=1.0.0
playwright>=1.40.0
```

## 常见问题

### Q: 运行时提示找不到 ffmpeg？
A: 首次运行时会自动下载 FFmpeg（约 100MB），请确保网络连接正常。Windows 用户无需手动安装。

### Q: 语音识别很慢？
A: 首次运行需下载 Whisper 模型（base 模型约 150MB），后续会使用缓存。识别速度取决于 CPU 性能。

### Q: 如何修改保存路径？
A: 编辑 `scripts/run_extract.py` 第 50 行的 `base_dir` 变量。

### Q: 提取失败怎么办？
A: 检查网络连接，确保能访问抖音。如仍失败，查看生成的 `failed_page.html` 和 `failed_ssr_data.json` 文件。

## 文件结构

```
douyin-to-obsidian/
├── SKILL.md                 # 技能描述
├── README.md                # 详细说明
├── scripts/
│   ├── run_extract.py       # 主入口
│   ├── extractor.py         # 核心引擎
│   └── requirements.txt     # 依赖列表
└── reference/
    └── architecture.md      # 架构文档
```

## 更新日志

### v1.0.0 (2026-03-22)
- 🎉 初始发布
- ✅ 抖音短视频文案提取
- ✅ 本地 Whisper 语音识别
- ✅ FFmpeg 自动下载
- ✅ 结构化 Obsidian 输出

## License

MIT-0
