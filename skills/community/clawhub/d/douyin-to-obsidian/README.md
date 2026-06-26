# Douyin to Obsidian

🎯 抖音视频文案自动提取工具，一键将抖音视频转为结构化 Obsidian 笔记

## 核心功能

- ✅ **自动提取** - 支持抖音短链/分享口令智能识别
- ✅ **绕过风控** - 自动绕过抖音滑动验证码和 SSR 数据封锁
- ✅ **本地识别** - 使用 Whisper AI 本地语音识别，零 API 成本
- ✅ **结构化输出** - 自动生成带 YAML Frontmatter 的 Markdown 笔记
- ✅ **长视频支持** - 自动分段处理，支持任意时长视频

## 快速开始

```bash
# 1. 安装依赖
pip install -r scripts/requirements.txt

# 2. 安装浏览器自动化
playwright install chromium

# 3. 运行提取
python scripts/run_extract.py "https://v.douyin.com/xxxxx/"
```

## 输出示例

笔记自动保存到 Obsidian 目录 (默认：`E:\icloud\iCloudDrive\iCloud~md~obsidian\myobsidian`)

```markdown
---
标题：视频标题
作者：作者名
链接：https://v.douyin.com/xxx
时长：7 分 42 秒
提取时间：2026-03-22 20:15:00
---

# 视频标题

完整的语音识别文案内容...
```

## 技术特点

- **反爬策略**: 精选模态链接绕过 + 自定义 User-Agent
- **语音识别**: OpenAI Whisper base 模型 (中文优化)
- **音频处理**: FFmpeg 自动下载和使用
- **异步架构**: 基于 asyncio 的高性能处理

## 系统要求

- Python 3.8+
- 首次运行约 200MB (Whisper 模型 + FFmpeg)
- 后续运行仅需存储空间

## 常见问题

### Q: 运行时提示找不到 ffmpeg？
A: 首次运行时会自动下载 FFmpeg，请确保网络连接正常。

### Q: 语音识别很慢？
A: 首次运行需下载 Whisper 模型 (~150MB)，后续会使用缓存。

### Q: 如何修改保存路径？
A: 编辑 `scripts/run_extract.py` 第 50 行的 `base_dir` 变量。

## 依赖项

- playwright - 浏览器自动化
- openai-whisper - 本地语音识别
- requests/aiohttp - 网络请求
- ffmpeg-python - 音频处理 (自动下载 FFmpeg 二进制)

## License

MIT-0