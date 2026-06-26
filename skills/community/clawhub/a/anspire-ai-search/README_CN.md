d<div align="center">

[English](./README.md) | **中文**

</div>

---

# Anspire 实时搜索

> 面向 AI 生态的下一代实时智能搜索引擎

一个 [OpenClaw](https://openclaw.ai) Skill，将 [Anspire](https://aisearch.anspire.cn) 实时搜索能力直接接入你的 AI 智能体——无需浏览器，无需爬虫，一个环境变量即可启用。

**MIT** · [![ClawHub](https://img.shields.io/badge/ClawHub-anspire--search-blue)](https://clawhub.ai/Anspire-AI/anspire-search) · [![Anspire](https://img.shields.io/badge/Powered%20by-Anspire-purple)](https://aisearch.anspire.cn)

### 为什么选 Anspire？

| 能力 | 说明 |
|---|---|
| 🌐 全渠道内容捕捞 | 并行捕捞主流搜索引擎、百科、新闻资讯、学术资源，实时抓取 |
| 🧠 多模态内容检索 | 语义解析 + 图文跨模态关联检索，覆盖文字、图片、新闻、机票酒店 |
| 🔗 跨域信息融合与认知增强排序 | 基于混合式集群与联邦学习框架，并行捕捞主流搜索引擎，实时覆盖百科、新闻资讯、学术资源等信息源 |
| ⚡ 毫秒级知识更新 | 突破传统搜索系统的信息滞后瓶颈，实现毫秒级的知识更新与策略迭代 |

### 安装方式

**方式一 —— ClawHub 安装（推荐）**

```bash
clawhub install anspire-search
```

**方式二 —— 直接从 GitHub 安装**

让 OpenClaw 直接读取本仓库的 SKILL.md：

```bash
openclaw skills add https://raw.githubusercontent.com/Anspire-AI/Anspire-search/main/SKILL.md
```

---

### 配置

**方式一：持久化配置（推荐）**

将 API Key 添加到系统配置，这样每次启动都会自动加载：

**macOS/Linux：**

```bash
# 对于 zsh 用户（macOS 默认）
echo 'export ANSPIRE_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc

# 对于 bash 用户
echo 'export ANSPIRE_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows：**

```cmd
# 永久设置（需要重启终端）
setx ANSPIRE_API_KEY "your_key_here"

# 同时为当前会话设置（可选，立即可用）
set ANSPIRE_API_KEY=your_key_here
```

**方式二：临时配置（仅当前会话有效）**

```bash
# macOS/Linux
export ANSPIRE_API_KEY=your_key_here

# Windows (cmd)
set ANSPIRE_API_KEY=your_key_here

# Windows (PowerShell)
$env:ANSPIRE_API_KEY="your_key_here"
```

> ⚠️ 注意：临时配置在关闭终端或新开聊天窗口后会失效，需要重新设置

> 在 [aisearch.anspire.cn](https://aisearch.anspire.cn) 注册获取 API Key

### 使用方式

**方式一：Agent 模式（自动）**

安装后，OpenClaw agent 在需要实时信息时会自动调用此 Skill。

**方式二：直接执行脚本**

使用提供的封装脚本进行手动搜索：

```bash
# Python 封装（推荐）- 格式化输出
python scripts/search.py "搜索关键词" --top-k 10

# Python 封装 - JSON 输出
python scripts/search.py "搜索关键词" --json

# Shell 封装
./scripts/search.sh "搜索关键词" 10
```

**方式三：直接调用 API**

```bash
curl --silent --show-error --fail --location --get \
  "https://plugin.anspire.cn/api/ntsearch/search" \
  --data-urlencode "query=搜索词" \
  --data-urlencode "top_k=10" \
  --header "Authorization: Bearer $ANSPIRE_API_KEY" \
  --header "Accept: application/json"
```

### 输出格式

```json
{
  "results": [
    {
      "title": "页面标题",
      "url": "https://example.com/page",
      "content": "文章正文内容...",
      "score": 0.997,
      "date": "2026-03-10T10:10:00+08:00"
    }
  ]
}
```

### 使用时机

| 场景 | 示例 |
|---|---|
| 📰 时事新闻 | "最新 AI 政策" / "今日科技头条" |
| 📈 市场动态 | "今日 A 股行情" / "比特币最新价格" |
| 🔬 查证核实 | "2026 年最新研究报告" |
| 🌍 实时事实 | "上海今天天气" / "现在几点" |

### 文件结构

```
anspire-search/
├── SKILL.md              # Skill 文档
├── .env.example          # 环境变量模板
├── scripts/
│   ├── search.py         # Python 封装（推荐）
│   └── search.sh         # Shell 封装
├── README.md             # 英文说明
└── README_CN.md          # 本文件
```

### 依赖

| 依赖 | 说明 |
|---|---|
| `ANSPIRE_API_KEY` | 必填——在 [aisearch.anspire.cn](https://aisearch.anspire.cn) 注册获取 |
| `curl` | 必填——macOS/Linux 预装，Windows 10+ 可用 |
| `python3` | 可选——使用 Python 封装脚本时需要 |

### 许可证

MIT © [Anspire-AI](https://github.com/Anspire-AI) · [aisearch.anspire.cn](https://aisearch.anspire.cn)
