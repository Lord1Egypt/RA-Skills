# api-cost-compare

> 对比各大 LLM 提供商 API 定价的命令行工具

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

`api-cost-compare` 是一个轻量级的 CLI 工具，帮助你快速对比 Anthropic、OpenAI、DeepSeek、Google、OpenRouter、Mistral 等主流 LLM 提供商的 API 定价，做出更明智的模型选择。

---

## 快速安装

```bash
pip install git+https://github.com/minirr890112-byte/api-cost-compare.git
```

或者从源码安装：

```bash
git clone https://github.com/minirr890112-byte/api-cost-compare.git
cd api-cost-compare
pip install -e .
```

## 使用方法

安装后，使用 `api-cost-compare` 命令：

```bash
api-cost-compare --help
```

### 列出所有模型

```bash
api-cost-compare list
```

输出示例：

```
┌────────────────────────────────────┬──────────────┬──────────────┬──────────────┬──────────┬────────────┐
│ 模型名称                           │ 提供商       │ 输入价格 /1M │ 输出价格 /1M │ 上下文窗口│ 任务标签    │
├────────────────────────────────────┼──────────────┼──────────────┼──────────────┼──────────┼────────────┤
│ Gemini 1.5 Flash                   │ Google       │ $0.0750      │ $0.3000      │ 1M       │ chat,coding │
│ mistral-small                      │ Mistral      │ $0.2000      │ $0.6000      │ 128K     │ chat,coding │
│ deepseek-chat                      │ DeepSeek     │ $0.2700      │ $1.1000      │ 128K     │ chat,coding │
│ GPT-4.1-mini                       │ OpenAI       │ $0.4000      │ $1.6000      │ 1M       │ chat,coding │
│ deepseek-reasoner                  │ DeepSeek     │ $0.5500      │ $2.1900      │ 128K     │ 推理        │
│ Claude Haiku                       │ Anthropic    │ $0.8000      │ $4.0000      │ 200K     │ chat,coding │
│ Gemini 1.5 Pro                     │ Google       │ $1.2500      │ $5.0000      │ 2M       │ 推理        │
│ GPT-4.1                            │ OpenAI       │ $2.0000      │ $8.0000      │ 1M       │ 推理        │
│ mistral-large                      │ Mistral      │ $2.0000      │ $6.0000      │ 128K     │ 推理        │
│ GPT-4o                             │ OpenAI       │ $2.5000      │ $10.0000     │ 128K     │ 推理        │
│ gpt-4o (OpenRouter)                │ OpenRouter   │ $2.7500      │ $11.0000     │ 128K     │ 推理        │
│ Claude Sonnet 4                    │ Anthropic    │ $3.0000      │ $15.0000     │ 200K     │ 推理        │
│ claude-sonnet-4 (OpenRouter)       │ OpenRouter   │ $3.5000      │ $17.5000     │ 200K     │ 推理        │
│ Claude Opus 4                      │ Anthropic    │ $15.0000     │ $75.0000     │ 200K     │ 推理        │
└────────────────────────────────────┴──────────────┴──────────────┴──────────────┴──────────┴────────────┘
```

### 对比两个模型

```bash
api-cost-compare compare "GPT-4o" "deepseek-chat"
```

输出示例：

```
╭──────────────────┬──────────────────┬──────────────────╮
│ 指标             │ GPT-4o           │ deepseek-chat    │
├──────────────────┼──────────────────┼──────────────────┤
│ 提供商           │ OpenAI           │ DeepSeek         │
│ 输入价格 /1M     │ $2.5000          │ $0.2700 ✅       │
│ 输出价格 /1M     │ $10.0000         │ $1.1000 ✅       │
│ 上下文窗口       │ 128K             │ 128K             │
│ 任务标签         │ 推理             │ chat, coding     │
╰──────────────────┴──────────────────┴──────────────────╯
```

### 推荐最佳模型

```bash
# 对话任务推荐
api-cost-compare recommend --task chat

# 编码任务推荐，月度预算 $50
api-cost-compare recommend --task coding --budget 50

# 推理任务推荐
api-cost-compare recommend --task reasoning --budget 100
```

### 估算调用成本

```bash
api-cost-compare estimate --model "GPT-4o" --input 1000 --output 500
api-cost-compare estimate --model "deepseek-chat" --input 5000 --output 2000
```

---

## 支持的提供商

| 提供商 | 模型数 | 特点 |
|--------|--------|------|
| **Anthropic** | 3 | Claude Opus 4 / Sonnet 4 / Haiku |
| **OpenAI** | 3 | GPT-4o / GPT-4.1 / GPT-4.1-mini |
| **DeepSeek** | 2 | deepseek-chat (V3) / deepseek-reasoner (R1) |
| **Google** | 2 | Gemini 1.5 Pro / Gemini 1.5 Flash |
| **OpenRouter** | 2 | claude-sonnet-4 / gpt-4o（不同定价） |
| **Mistral** | 2 | mistral-large / mistral-small |

---

## 功能特性

- 📊 **实时定价对比** — 所有价格均为最新的官方 API 定价
- 🏷️ **任务标签系统** — 按对话、编码、推理分类推荐
- 💰 **成本估算** — 精确计算不同 token 用量下的美元成本
- 🎯 **智能推荐** — 根据任务类型和预算推荐最佳模型
- 🎨 **美观输出** — 基于 Rich 库的彩色终端表格
- 🌐 **中文界面** — 默认中文输出，友好易用

---

## 设计动机

在选择 LLM API 时，开发者往往面临多方面的考量：模型能力、响应速度、上下文窗口大小以及最重要的——成本。不同提供商的定价策略差异巨大，例如 DeepSeek 的输入价格仅为 GPT-4o 的十分之一左右，而 OpenRouter 作为中间层通常会有一定的溢价。

`api-cost-compare` 旨在解决这一痛点，将所有主流 LLM 提供商的定价信息集中在一处，帮助你快速做出选择。

---

## 项目结构

```
api-cost-compare/
├── api_cost_compare/
│   ├── __init__.py      # 包初始化
│   ├── providers.py     # 定价数据与核心逻辑
│   └── cli.py           # CLI 命令
├── pyproject.toml       # 项目配置
├── README.md            # 中文文档
├── README_EN.md         # 英文文档
└── LICENSE              # MIT 许可证
```

---

## 贡献

欢迎提交 Issue 或 Pull Request！如果你想添加新的提供商或更新定价，请编辑 `api_cost_compare/providers.py` 中的 `get_all_pricing()` 函数。

---

## 生态系统

| Tool | Description |
|---|---|
| [model-cost-advisor](https://github.com/minirr890112-byte/model-cost-advisor) | Recommend best LLM by cost |
| [model-watch](https://github.com/minirr890112-byte/model-watch) | Monitor models for degradation |
| [prompt-inspector](https://github.com/minirr890112-byte/prompt-inspector) | Scan prompts for censorship triggers |
| [code-inspector](https://github.com/minirr890112-byte/code-inspector) | AI-generated code quality analysis |


## 许可证

MIT © 2025 minirr890112-byte
