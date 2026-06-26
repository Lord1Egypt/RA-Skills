# 🔬 Open Deep Research — SKILL for OpenClaw

> 一个给 AI Agent 用的深度研究工作流。不依赖额外 API，放进去就能用。

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-5B45E9)](https://openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/midboss1028-beep/claw-deep-research?style=social)](https://github.com/midboss1028-beep/claw-deep-research)

## 这是什么

把"研究"这件事从"搜一下然后总结"升级为真正的研究流程：

**一层搜索 → 提炼认知 → 发现盲区 → 继续深挖 → 合并输出**

灵感源自 [dzhng/deep-research](https://github.com/dzhng/deep-research)（17.8k ⭐）的核心算法——广度搜索 × 深度递归——但完全基于 OpenClaw 原生能力实现。

## 核心优势

| 特性 | 说明 |
|------|------|
| 🚫 **零额外成本** | 不需要 Firecrawl、OpenAI、Fireworks 等额外 API Key |
| 🎯 **模型无关** | 你用 DeepSeek、MiniMax、Claude 还是 GPT——不挑 |
| 🔌 **搜索不限** | MiniMax / Tavily / Brave / Google / Perplexity——能用就行 |
| 📦 **即装即用** | 一个文件夹，放到 skills 目录，重启即生效 |
| 🌏 **中英双语** | 输入中文出中文报告，输入英文出英文报告 |
| 💻 **跨平台** | macOS / Linux / Windows 通吃 |

## 安装

### 方式一：ClawHub（推荐）

```bash
clawhub install claw-deep-research
```

### 方式二：手动

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/midboss1028-beep/claw-deep-research.git
```

然后重启 OpenClaw 网关：

```bash
openclaw gateway restart
```

### 方式三：项目级使用

```
your-project/
  └── .agent/
      └── skills/
          └── claw-deep-research/
              └── SKILL.md
```

## 使用

### 显式触发

```
/deep 新能源汽车2026年竞争格局
/deep research AI Agent 市场分析
```

### 隐式触发

Agent 会自动识别你下面这类需求：

- "帮我深度研究一下 XXX"
- "深挖一下 XXX 领域"
- "出一份关于 XXX 的研究报告"
- "做个 XXX 的深度分析"

### 默认参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| breadth | 4 | 每层搜索方向数 |
| depth | 2 | 递归层级数 |
| 预估搜索量 | ~12次 | breadth × (1 + breadth/2) |

### 输出示例

完成研究后你会收到类似这样的东西：

```
🔬 开始深度研究：新能源汽车2026竞争格局，广度=4，深度=2
🔬 [深度 2/2] 本轮搜索完成，累计获取 18 条认知
🔬 报告生成中...

# 新能源汽车产业2026竞争格局 — 深度研究报告

## 摘要
...

## 核心发现
### 中国市场
...
### 全球格局
...
### 技术路线
...

## 来源
- https://...
```

## 工作原理

```
                           ┌─ 搜索1 → 提炼认知 → 递归(广度2,深度1)
        用户问题 ─→ 生成4路搜索 ── 搜索2 → 提炼认知 → 递归(广度2,深度1)
                           ├─ 搜索3 → 提炼认知 → 递归(广度2,深度1)
                           └─ 搜索4 → 提炼认知 → 递归(广度2,深度1)
                                            │
                                            ↓
                                   合并所有认知 → 最终报告
```

## 许可证

MIT — 随便用、随便改、随便分享。
