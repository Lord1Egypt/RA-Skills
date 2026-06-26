# Follow News

> 自动化科技资讯汇总 — 163 个内置数据源，7 层管道，一句话安装。

[English](README.md) | **中文**

[![Tests](https://github.com/tangwz/follow-news/actions/workflows/test.yml/badge.svg)](https://github.com/tangwz/follow-news/actions/workflows/test.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ClawHub](https://img.shields.io/badge/ClawHub-follow--news-blueviolet)](https://clawhub.com/tangwz/follow-news)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 💬 一句话安装

跟你的 [OpenClaw](https://openclaw.ai) AI 助手说：

> **"安装 follow-news，每天早上 9 点发送一份科技日报。"**

搞定。Bot 会自动安装、配置、定时、推送——全程对话完成。

更多示例：

> 🗣️ "配置一个每周 AI 周报，只要 `llm` 和 `ai-agent` 板块，每周一发到 Discord #ai-weekly"

> 🗣️ "安装 follow-news，加上我的 RSS 源，并包含 `kol` 主题"

> 🗣️ "现在就给我生成一份科技日报，跳过 Twitter 数据源"

或通过 CLI 安装：
```bash
clawhub install follow-news
```

## 📊 你会得到什么

基于 **163 个内置数据源** + **6 个默认报告主题** 的去重科技日报：

| 层级 | 数量 | 内容 |
|------|------|------|
| 📡 RSS | 65 个订阅源 | OpenAI、Simon Willison、Hugging Face、HN、36氪… |
| 🐦 Twitter/X | 61 个 KOL | @sama、@karpathy、@paulg、@garrytan、@dotey… |
| 🔍 Web 搜索 | 4 个查询主题 | `llm`、`ai-agent`、`kol`、`frontier-tech` + 时效过滤 |
| 🐙 GitHub | 23 个仓库 | 关键项目的 Release 跟踪（LangChain、vLLM、DeepSeek、Llama…） |
| 🗣️ Reddit | 8 个子版块 | r/MachineLearning、r/LocalLLaMA、r/OpenAI、r/ExperiencedDevs… |
| 🎙️ Podcast | 自定义源 | RSS 播客订阅源、YouTube 播放列表/频道、小宇宙播客，以及可选转录文本 |

### 数据管道

```
       run-pipeline.py (~30秒)
              ↓
  RSS ────────┐
  Twitter ────┤
  Web ────────┤── 并行采集 ──→ merge-sources.py
  GitHub ─────┤                          ↓
  GitHub Tr. ─┤              enrich-articles.py（可选）
  Reddit ─────┤                          ↓
  Podcast ────┘
              排名信号 → 去重 → 主题分组
              ↓
    Discord / 邮件 / PDF 输出
```

**排名信号**：优先级源、多源交叉验证、时效性、互动度、Reddit 讨论热度以及已报道惩罚。

## ⚙️ 配置

- `config/defaults/sources.json` — 163 个内置数据源（65 RSS、61 Twitter、23 GitHub、8 Reddit、6 Podcast）
- `config/defaults/topics.json` — 6 个主题：`llm`、`ai-agent`、`kol`、`hackernews`、`frontier-tech`、`podcast`
- 用户自定义配置放 `workspace/config/`，优先级更高

## 🎨 自定义数据源

开箱即用，内置 163 个数据源，并支持自定义 podcast 源——但完全可自定义。将默认配置复制到 workspace 并覆盖：

```bash
# 复制并自定义
cp config/defaults/sources.json workspace/config/follow-news-sources.json
cp config/defaults/topics.json workspace/config/follow-news-topics.json
```

你的配置文件会与默认配置**合并**：
- **覆盖**：`id` 匹配的源会被你的版本替换
- **新增**：使用新的 `id` 即可添加自定义源
- **禁用**：对匹配的 `id` 设置 `"enabled": false`

```json
{
  "sources": [
    {"id": "my-blog", "type": "rss", "enabled": true, "url": "https://myblog.com/feed", "topics": ["llm"]},
    {
      "id": "training-data-podcast",
      "type": "podcast",
      "name": "Training Data",
      "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8",
      "platform": "youtube",
      "enabled": true,
      "priority": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": true,
        "backend": "yt-dlp",
        "languages": ["en", "zh", "zh-Hans"]
      }
    },
    {
      "id": "xiaoyuzhou-example",
      "type": "podcast",
      "name": "Xiaoyuzhou Example",
      "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
      "platform": "xiaoyuzhou",
      "enabled": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": true,
        "backend": "opencli",
        "languages": ["zh"]
      }
    },
    {"id": "openai-rss", "enabled": false}
  ]
}
```

不需要复制整个文件——只写你要改的部分。

Podcast 源使用 `type: "podcast"`。RSS 播客订阅源不需要额外工具；YouTube 播客源使用 `platform: "youtube"`，并可通过可选的 `yt-dlp` 运行时抓取元数据和转录文本。小宇宙播客源使用 `platform: "xiaoyuzhou"`，URL 形如 `https://www.xiaoyuzhoufm.com/podcast/<podcast_id>`。小宇宙元数据发现使用 OpenCLI，且没有直接 API 或 HTML fallback；转录后端 `auto`/`opencli` 会对小宇宙单集使用 OpenCLI。`opencli` 转录后端只对小宇宙源有效。

## 🔧 环境变量

```bash
# Twitter/X Backend (auto priority: opencli > getxapi > twitterapiio > official)
export TWITTER_API_BACKEND="auto"  # auto|opencli|getxapi|twitterapiio|official
export OPENCLI_BIN="/path/to/opencli"  # optional; defaults to opencli on PATH
export OPENCLI_MAX_WORKERS="10"  # optional; increase parallel OpenCLI workers
export OPENCLI_CLOSE_TABS_AFTER_RUN="1"  # optional; close OpenCLI-created X/Twitter tabs after fetch
export OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN="1"  # optional; close Chrome automation windows opened by OpenCLI
export GETX_API_KEY="..."        # GetXAPI fallback
export TWITTERAPI_IO_KEY="..."   # twitterapi.io fallback
export X_BEARER_TOKEN="..."      # Official X API v2 fallback
# Web Search
export TAVILY_API_KEY="tvly-xxx"   # Tavily Search API
export BRAVE_API_KEYS="k1,k2,k3"   # Brave Search API keys, comma-separated for rotation
export BRAVE_API_KEY="..."         # Single Brave key
export WEB_SEARCH_BACKEND="auto"   # auto|brave|tavily
# GitHub
export GITHUB_TOKEN="..."          # GitHub API
# Podcast Transcript
export YTDLP_BIN="/path/to/yt-dlp"  # optional; defaults to yt-dlp on PATH
# Other
export BRAVE_PLAN="free"           # Override Brave rate limit: free|pro
```

OpenCLI 是默认优先后端，因为它可以复用已经登录的 Chrome/Chromium 会话，不再强制要求 Twitter API 凭据。CI、无浏览器环境，或已经配置 API 密钥的用户仍可通过 API 后备后端运行。

如需使用 OpenCLI 后端，用户需要自行安装 OpenCLI 可执行文件，并确保它在 `PATH` 上，或通过 `OPENCLI_BIN` 指向其绝对路径。在 OpenClaw 中，还需要安装 `jackwener/opencli` Skill，这样 agent 才能运行 `opencli doctor`、检查浏览器桥接，并协助排查 X 登录态问题。

OpenCLI 的稳定性取决于本机浏览器扩展桥接状态。抓取器默认使用 10 并发 OpenCLI 请求（`OPENCLI_MAX_WORKERS=10`，上限 10），同时默认会关闭本次 OpenCLI 抓取中新建的 X/Twitter 标签页（`OPENCLI_CLOSE_TABS_AFTER_RUN=1`），并在 macOS 上关闭 OpenCLI 本次打开的 Chrome 自动化窗口（`OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN=1`），不会关闭执行前已经存在的窗口。

RSS 播客订阅源不需要额外工具。YouTube 播客元数据和转录文本抓取需要 `yt-dlp`；请将它安装到 `PATH`，或通过 `YTDLP_BIN` 指向可执行文件。缺少 `yt-dlp` 时，对应 YouTube 播客源会标记为失败，但不会阻塞其他数据源。

小宇宙播客元数据发现需要 OpenCLI。运行这类源之前，请先安装、配置并完成 OpenCLI 的小宇宙认证；当 `opencli` 不在 `PATH` 上时，可通过 `OPENCLI_BIN` 覆盖可执行文件路径。小宇宙元数据发现没有直接 API 或 HTML fallback。转录方面，后端 `auto`/`opencli` 会对小宇宙单集使用 OpenCLI；非小宇宙播客源会拒绝 `opencli` 转录后端。

## 📦 依赖

### 核心依赖

本技能需要 Python 3.8+ 和两个可选依赖以增强功能：

```bash
pip install -r requirements.txt
# 或
pip install feedparser>=6.0.0 jsonschema>=4.0.0
```

- **feedparser** — RSS/Atom 订阅源解析（未安装时回退到正则匹配）
- **jsonschema** — 配置文件的 JSON Schema 验证

### 可选依赖

```bash
pip install weasyprint yt-dlp
```

- **weasyprint** — 启用 PDF 报告生成
- **yt-dlp** — 启用 YouTube 播客元数据和转录文本抓取；`YTDLP_BIN` 可指向独立可执行文件

## 🧪 测试

```bash
python3 -m unittest discover -s tests -v
```

## 🧪 产品验收测试

修改摘要渲染行为前，先运行验收测试：

```bash
python3 -m unittest tests.test_acceptance_digest -v
```

当预期摘要需要更新时，重新生成 golden 文件，并在提交前检查差异：

```bash
UPDATE_GOLDEN=1 python3 -m unittest tests.test_acceptance_digest -v
git diff -- tests/golden/daily-discord.md
```

如需手动准备 Codex 验收上下文：

```bash
python3 scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --prepare-codex-context /tmp/follow-news-acceptance \
  --output /tmp/follow-news-acceptance/expected.md
```

## 📂 仓库地址

**GitHub**: [github.com/tangwz/follow-news](https://github.com/tangwz/follow-news)

## 🌟 相关引用

- [Awesome OpenClaw Use Cases](https://github.com/hesamsheikh/awesome-openclaw-usecases) — OpenClaw 社区精选用例合集

## 📄 开源协议

MIT License — 详见 [LICENSE](LICENSE)
