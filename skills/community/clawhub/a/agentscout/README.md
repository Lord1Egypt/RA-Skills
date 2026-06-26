<div align="center">

# 🔍 AgentScout

**GitHub Agent 项目自动发现 × 小红书内容一键生成**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/auxito/AgentScout?style=social)](https://github.com/auxito/AgentScout)

[功能介绍](#-功能特性) · [快速开始](#-快速开始) · [使用指南](#-使用指南) · [配置说明](#%EF%B8%8F-配置说明) · [项目结构](#-项目结构) · [贡献指南](#-贡献)

</div>

---

## 🤔 这是什么？

你是否经常在 GitHub 上刷到很酷的 AI Agent 项目，想分享到小红书，但从写文案到做配图要花一整晚？

**AgentScout 帮你把这个过程缩短到 5 分钟。**

它会自动搜索 GitHub 上最新、最有趣的 AI Agent 开源项目，用 LLM 打分排名，然后为你选中的项目一键生成：

- 📖 **结构化分析教程** — 从架构到上手，每一步都写清楚
- ✍️ **小红书爆款文案** — 标题、正文、标签，拿来就发
- 🖼️ **6~9 张精美配图** — 封面、代码卡片、步骤图、总结卡，全套齐活

<div align="center">

```
GitHub 搜索 → LLM 评分排名 → 展示 Top3 → 深度分析 → 文案 + 配图 → 直接发布
```

</div>

## ✨ 功能特性

### 🔍 智能项目发现

- **多策略搜索**：关键词搜索 + 组织监控（langchain-ai / microsoft / openai 等 7 个组织）
- **自动去重**：SQLite 持久化，不会重复推荐同一个项目
- **实时数据**：直接调用 GitHub API，获取最新 star 数、更新时间、topics 等

### 📊 LLM 四维评分

每个项目从 4 个维度打分（1-10 分），加权计算总分：

| 维度 | 权重 | 评什么 |
|------|------|--------|
| 🆕 新颖度 | 30% | 是否提出新范式/新思路 |
| 🔧 实用性 | 30% | 能否解决真实痛点 |
| 📱 内容适配度 | 25% | 适不适合做小红书内容 |
| 🚀 易用性 | 15% | 上手难度如何 |

评分基准固定版本号（当前 `v1.0`），确保不同项目之间可比。

### 📖 深度项目分析

自动获取 README 全文 + 项目文件树 + 关键代码，用 LLM 生成：

- 一句话说清楚这个项目
- 它解决了什么问题（大白话版）
- 架构/流程图（Mermaid）
- 5 分钟跑起来（可复制的命令）
- 最有意思的技术亮点
- 踩坑提醒

### ✍️ 小红书文案生成

- **标题**：≤20 字，带 emoji，制造好奇心
- **正文**：300-500 字，口语化，像朋友分享
- **Hook 开头**：前两行决定展开率
- **智能标签**：固定标签池 + LLM 动态生成
- **禁用词过滤**：自动避开"赋能""抓手""底层逻辑"等词

### 🎨 全套配图生成

| 图片 | 类型 | 说明 |
|------|------|------|
| P1 | 封面（科技蓝） | 项目名 + 亮点 + Star 数 |
| P2 | 封面（终端风） | 暗色终端主题 |
| P3 | 架构卡片 | 技术架构可视化 |
| P4-P5 | 代码卡片 | Carbon 风格语法高亮 |
| P6-P7 | 步骤卡片 | 安装运行教程 |
| P8 | AI 概念图 | FLUX.1 等模型生成（可选） |
| P9 | 总结卡片 | 一句话总结 + 关注引导 |

三套方案并行：**HTML 模板渲染** + **代码高亮卡片** + **AI 图片生成**

## 🚀 快速开始

### 环境要求

- Python 3.10+
- GitHub Token（[生成地址](https://github.com/settings/tokens)）
- 任意 OpenAI 兼容的 LLM API Key

### 安装

```bash
git clone https://github.com/auxito/AgentScout.git
cd AgentScout

# 安装依赖
pip install -r requirements.txt

# （可选）安装 Playwright，用于 GitHub 页面截图
playwright install chromium
```

### 配置

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```env
# 必填
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
LLM_API_KEY=sk-xxxx

# 可选 - LLM 配置（默认 OpenAI）
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o

# 可选 - AI 配图（支持任意 OpenAI 兼容的图片 API）
IMAGE_API_KEY=sk-xxxx
IMAGE_BASE_URL=https://api.siliconflow.cn/v1
IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
```

### 运行

```bash
python -m src.pipeline
```

然后跟着提示操作就行：搜索 → 看排名 → 选一个 → 等生成 → 去 `output/` 拿成品。

## 📖 使用指南

### 完整流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  📡 搜索     │────▶│  📊 评分     │────▶│  🏆 排名     │
│  GitHub API  │     │  LLM 四维   │     │  展示 Top3   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │ 用户选择
                                                ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  📦 产出     │◀────│  🎨 配图     │◀────│  📖 分析     │
│  output/    │     │  6-9 张图   │     │  深度教程    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 产出结构

每次运行会在 `output/` 下生成一个目录：

```
output/2026-03-16_CoolProject/
├── analysis.md        # 结构化分析教程
├── post.md            # 小红书文案（含标签，可直接复制发布）
├── images/            # 所有配图
│   ├── P1_cover.png
│   ├── P2_terminal.png
│   ├── P3_architecture.png
│   ├── P4_code.png
│   ├── P5_code.png
│   ├── P6_steps.png
│   ├── P7_steps.png
│   ├── P8_concept.png    # AI 生成（需配置 IMAGE_API_KEY）
│   ├── P9_summary.png
│   └── github_screenshot.png
└── metadata.json      # 项目元数据 + 评分详情
```

## ⚙️ 配置说明

所有配置通过 `.env` 文件管理：

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `GITHUB_TOKEN` | 推荐 | - | GitHub Personal Access Token |
| `LLM_API_KEY` | ✅ | - | LLM API Key |
| `LLM_BASE_URL` | - | `https://api.openai.com/v1` | 任意 OpenAI 兼容端点 |
| `LLM_MODEL` | - | `gpt-4o` | 模型名称 |
| `IMAGE_API_KEY` | - | - | 图片生成 API Key（不填则跳过 AI 配图） |
| `IMAGE_BASE_URL` | - | `https://api.siliconflow.cn/v1` | 图片 API 端点 |
| `IMAGE_MODEL` | - | `FLUX.1-schnell` | 图片模型 |
| `SCORE_WEIGHT_*` | - | 见上表 | 四维评分权重 |
| `TOPK_SIZE` | - | `20` | 排行榜保留数量 |
| `PRESENT_TOP_N` | - | `3` | 每次展示给用户的项目数 |

> 💡 LLM 和图片 API 均使用 OpenAI 兼容协议，你可以指向 OpenAI / DeepSeek / SiliconFlow / Together AI 等任意服务商。

## 📁 项目结构

```
AgentScout/
├── src/
│   ├── pipeline.py                # 主流程编排（6 个阶段串联）
│   ├── config.py                  # 统一配置加载
│   │
│   ├── discover/                  # 🔍 项目发现
│   │   ├── github_searcher.py     #    GitHub 搜索 + 组织监控
│   │   ├── scorer.py              #    LLM 四维评分
│   │   └── ranking.py             #    TopK 排行榜
│   │
│   ├── analyze/                   # 📖 深度分析
│   │   └── project_analyzer.py    #    README/代码 → 结构化教程
│   │
│   ├── content/                   # ✍️ 内容生成
│   │   ├── copywriter.py          #    小红书文案
│   │   └── tag_generator.py       #    智能标签
│   │
│   ├── visual/                    # 🎨 配图系统
│   │   ├── composer.py            #    HTML 模板 → 图片
│   │   ├── code_card.py           #    Carbon 风格代码卡片
│   │   ├── screenshot.py          #    Playwright 网页截图
│   │   └── ai_image.py            #    AI 概念配图
│   │
│   ├── storage/                   # 💾 数据存储
│   │   ├── database.py            #    SQLite CRUD
│   │   └── models.py              #    数据模型
│   │
│   └── utils/                     # 🔧 工具层
│       ├── llm_client.py          #    OpenAI 兼容 LLM 客户端
│       └── image_client.py        #    OpenAI 兼容图片客户端
│
├── templates/                     # HTML 卡片模板（3 种配色）
├── output/                        # 生成的内容产出
├── data/                          # SQLite 数据库
├── .env.example                   # 环境变量模板
└── requirements.txt               # Python 依赖
```

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| GitHub API | PyGithub |
| LLM | OpenAI SDK（兼容协议） |
| 图片生成 | html2image + Jinja2 + Pillow |
| AI 配图 | OpenAI Images API（兼容协议） |
| 截图 | Playwright |
| 数据库 | SQLite3 |
| 终端 UI | Rich |

## 🗺️ Roadmap

- [ ] Web UI 界面（Streamlit / Gradio）
- [ ] 定时自动搜索 + 推送通知
- [ ] 支持更多平台文案风格（知乎 / Twitter / 公众号）
- [ ] 批量生成模式（一次处理 Top N 全部项目）
- [ ] Mermaid 流程图自动渲染为图片
- [ ] 自定义搜索关键词和组织列表（通过 CLI 参数）
- [ ] 评分 rubric 可视化对比

## 🤝 贡献

欢迎任何形式的贡献！

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/awesome-feature`)
3. 提交更改 (`git commit -m 'Add awesome feature'`)
4. 推送到分支 (`git push origin feature/awesome-feature`)
5. 打开 Pull Request

## 📄 License

本项目基于 [MIT License](LICENSE) 开源。

## ⭐ Star History

如果觉得这个项目有用，请给个 Star 吧！这是对作者最大的鼓励 ✨

---

<div align="center">

Made with ❤️ by [auxito](https://github.com/auxito)

</div>
