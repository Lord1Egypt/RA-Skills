
<div align="center">

# 🧠 AI Academic Paper Researcher (AI 学术论文研究助手)

**专为 AI 科学家和爱好者设计的智能、全自动 arXiv 调研助手。通过自然语言驱动，实现搜索、顶会精确过滤、PDF 自动下载及本地文献库构建。**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-purple.svg)](#)

<br>

[**English**](./README.md) | [**简体中文**](./README_zh-CN.md)

</div>

---

## ✨ 为什么需要这个工具？

面对每天海量的 arXiv 提交论文，往往让人感到不知所措。这个工具将成为您的私人学术侦察员。无论您是追踪特定子领域最新进展的专业研究人员，还是寻找基础经典论文的爱好者，本技能都能在原始 arXiv 数据和精选的高价值知识之间架起桥梁。

### 🚀 核心特性

- **🧠 双模式智能检索**: 
  - **广泛搜索 (Broad Search)**: 撒网捕捉最新前沿趋势。
  - **顶会严格过滤 (Top-Tier Strict Filtering)**: 使用大语言模型 (LLM) 进行语义校验，确保下载的论文确实被您的目标会议（如 CVPR, NeurIPS, ICLR）接收。
- **⏱️ 智能排序**: 自动在“按时间”（追踪最新发布）和“按相关度”（挖掘经典/基础算法）之间进行智能切换。
- **🛡️ 领域隔离**: 自动追加 AI 专属分类标签（`cs.CV`, `cs.LG`, `cs.AI` 等），精准过滤掉来自物理或生物学等其他领域的重名噪音。
- **📂 本地文献库管理**: 静默流式下载 PDF，标准化规范文件名，并将记录自动追加到本地 CSV 中以防止重复下载。
- **🛡️ 防封禁保护**: 内置指数退避算法（Exponential backoff）和请求延迟，从容应对 arXiv 严格的 API 速率限制（429 报错）。

---

## 🧩 架构：它是如何工作的？

本技能由几个协同工作的核心组件构成，可与您的 AI Agent（如 OpenClaw）无缝集成：

| 组件 | 描述 | 作用 |
| :--- | :--- | :--- |
| **`SKILL.md`** | “大脑” | 指导 AI Agent 如何理解您的查询，选择正确的排序策略，并通过 `comment` 字段校验会议接收情况。 |
| **`arxiv_tool.py`** | “肌肉” | 健壮的 Python CLI 工具，负责请求 arXiv API、处理 HTTP 数据流、强制执行速率限制以及下载 PDF。 |
| **`target.csv`** | “过滤器” | 简单的用户自定义列表，包含您关注的顶会名称（如 `CVPR`, `ICCV`, `ICLR`）。LLM 将依据此列表校验论文。 |
| **`paper_list.csv`** | “记忆” | 在工作区中自动生成。记录已下载的 ArXiv ID，确保您永远不会重复下载同一篇论文。 |

---

## 🛠️ 安装与配置

**1. 安装依赖环境**
请确保您的 Python 环境中已安装以下包：
```bash
pip install arxiv requests
```

**2. 目录结构**
确保文件在您的 workspace 工作区中放置正确：

```text
workspace/
├── paper_list/                  # 自动生成：PDF 文件和 paper_list.csv 会存放在这里
└── skills/
    └── ai-paper-researcher/
        ├── SKILL.md             # Agent 提示词指令
        ├── arxiv_tool.py        # Python 核心脚本
        └── target.csv           # 您的目标会议名单 (如 CVPR, NeurIPS)
```

**3. 配置目标会议**
将您关注的会议名称添加到 `target.csv` 中（每行一个）：

```csv
target
CVPR
ICCV
NeurIPS
ICLR
```

---

## 🗣️ 如何使用（自然语言提示）

将技能加载到您的 AI Agent 后，只需用自然语言发号施令即可。以下是最佳的 Prompt 模板：

### 🔭 场景 1：追踪最新前沿（模式 A）

*非常适合在快速发展的领域进行每周文献梳理。*

> “调用 `ai-paper-researcher` 技能。帮我检索近一个月关于 **Agent security** 的最新论文。请按时间（date）排序，跳过顶会过滤步骤，并直接将最相关的论文下载到我的本地工作区。”

### 🏛️ 场景 2：深度挖掘顶会经典（模式 B）

*非常适合寻找经过同行评审和验证的基础性高价值工作。*

> “使用 `ai-paper-researcher` 技能。我想深入调研 **Agent security** 方向。请按相关度（relevance）排序，找出最具影响力的论文。请严格过滤结果，只下载那些已经被我 `target.csv` 列表中会议接收的论文。完成后请给我一份下载总结。”

### 🎯 场景 3：精准直接下载

*当您已经知道具体的 ID，不需要搜索时，直接绕过检索流程。*

> “使用 `ai-paper-researcher` 技能，跳过搜索步骤，直接帮我下载原始的 Adam 优化器论文 (ID: `1412.6980`) 以及 Focal Loss 论文 (ID: `1708.02002`)。”

---

## 💻 命令行使用（面向开发者）

如果您更喜欢绕过 AI Agent 直接在终端中使用，该 Python 脚本也是一个功能完备的独立工具：

```bash
# 按相关度搜索论文（返回带有 comment 字段的 JSON，供二次开发使用）
python arxiv_tool.py search "diffusion models" --max 10 --sort relevance

# 搜索最新发布的论文
python arxiv_tool.py search "diffusion models" --sort date

# 下载指定论文（自动处理命名及 CSV 记录持久化）
python arxiv_tool.py download 1412.6980
```

---

## 📜 致谢与开源协议

本项目的核心灵感和基础框架源自 [Ractorrr/arxiv-mcp](https://github.com/Ractorrr/arxiv-mcp) (🔍 AI-powered arXiv research assistant)。
在此基础上，项目进行了重度修改：剥离了复杂的数据库依赖 (MongoDB)，引入了严格的本地文件系统追踪机制，新增了基于 LLM 驱动的语义级会议过滤管线，并实现了高度鲁棒的流式下载策略以绕过 arXiv 的 API 限制。

**开源协议:** [MIT License](https://choosealicense.com/licenses/mit/) - 允许免费使用、修改和分发，无强制署名要求。