<div align="center">

# 🔭 AI前沿哨兵

**你的AI情报指挥中心**

*自动采集、分析与报告AI领域最新动态*

**一行命令追踪AI领域所有动态 — GitHub趋势、arXiv论文、技术新闻，一览无余。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/xiaopengs/ai-sentinel?style=social)](https://github.com/xiaopengs/ai-sentinel)

🌐 [项目展示](http://thinkspc.fun/static/sentinel/) · 📦 [ClawHub](https://clawhub.ai/skills/ai-intelligence-sentinel) · 🇺🇸 [English](./README.md)

</div>

---

## 🎯 你能得到什么

| 产品经理 | 开发者 | 企业高管 |
|:---:|:---:|:---:|
| 📊 每日AI行业报告自动送达 | 🔧 15+数据源一站式整合 | 📈 无需人工追踪AI动态 |
| 🔍 比竞争对手更早发现热门项目 | 💻 CLI工具 + WebUI完全掌控 | 📋 每份报告都有执行摘要 |
| ⏰ 晨报晚报准时推送 | 🛠️ 可自定义信息源和模板 | 🎯 仅展示高质量内容 |

---

## ⚡ 30秒快速开始

### 方式一：对话安装（推荐）

**第一步：安装技能**

复制以下提示词，发送给支持ClawHub的AI助手（OpenClaw、WorkBuddy、QClaw等）：

```
安装 ClawHub 和技能 请先检查是否已安装 ClawHub 商店，若未安装，请安装 npm i -g clawhub ，然后安装 ai-intelligence-sentinel 技能。
```

或通过ClawHub命令行：
```bash
npx clawhub@latest install ai-intelligence-sentinel
```

**第二步：使用技能**

安装完成后，用技能名称触发：
```
使用 ai-intelligence-sentinel 技能生成今日AI情报报告
```

或简化为：
```
ai-intelligence-sentinel 生成今日报告
```

### 方式二：命令行安装

```bash
# 安装依赖
pip install requests feedparser pyyaml jinja2

# 运行 — 立即生成一份完整的AI情报报告
python scripts/reporter.py --type full
```

**完成。** 你的第一份报告在 `reports/YYYY-MM-DD/full_report_*.md`

<details>
<summary>📖 完整安装步骤</summary>

```bash
# 克隆项目
git clone https://github.com/xiaopengs/ai-sentinel.git
cd ai-sentinel

# 安装依赖
pip install requests feedparser pyyaml jinja2

# 生成报告（自动采集 + 分析 + 生成）
python scripts/reporter.py --type full
```

</details>

---

## ✨ 核心功能

<table>
<tr>
<td width="50%">

### 🔍 多源采集
- **GitHub Trending** — AI开源项目热度
- **arXiv** — 最新论文 (cs.AI, cs.LG, cs.CL)
- **HackerNews** — 开发者社区讨论
- **15+ RSS源** — OpenAI、Anthropic、Google AI、DeepMind等
- **中国AI公司** — 智谱AI、MiniMax、扣子Coze

</td>
<td width="50%">

### 📊 智能分析
- **热度评分** — Stars、Forks、评论数
- **新鲜度权重** — 越新排名越高
- **来源可信度** — 官方博客 > 媒体 > 社区
- **质量评分** — 内容深度与完整性

</td>
</tr>
<tr>
<td width="50%">

### 📄 自动化报告
- **晨报** — 隔夜重点 (08:00)
- **晚报** — 全天汇总 (20:00)
- **完整报告** — 采集 + 分析 + 生成
- **多种格式** — Markdown、小红书风格

</td>
<td width="50%">

### 🎛️ 便捷管理
- **WebUI** — 可视化配置面板
- **CLI** — 完整命令行控制
- **定时任务** — 设置后自动执行
- **自定义模板** — 按需定制

</td>
</tr>
</table>

---

## 📋 使用方法

### 常用命令速查

| 需求 | 命令 |
|------|------|
| **立即生成完整报告** ⭐ | `python scripts/reporter.py --type full` |
| 采集所有信息源 | `python scripts/collect.py --all` |
| 生成晨报 | `python scripts/reporter.py --type morning` |
| 生成晚报 | `python scripts/reporter.py --type evening` |
| 仅追踪GitHub | `python scripts/collect.py --source github` |
| 仅追踪arXiv论文 | `python scripts/collect.py --source arxiv` |

### 报告类型

| 类型 | 功能 | 适用场景 |
|------|------|----------|
| `--type full` | 采集 → 分析 → 生成 | 立即获取情报 ⭐ |
| `--type morning` | 生成晨报 | 定时任务 |
| `--type evening` | 生成晚报 | 定时任务 |

---

## 📰 信息源覆盖

| 类别 | 来源 | 覆盖范围 |
|------|------|----------|
| **开源项目** | GitHub Trending | AI/ML项目 |
| **学术论文** | arXiv | cs.AI, cs.LG, cs.CL |
| **社区讨论** | HackerNews | 开发者热点 |
| **官方博客** | OpenAI、Anthropic、Google AI、DeepMind、HuggingFace、xAI、Cursor | 一手发布 |
| **技术媒体** | InfoQ(全球/中文)、TechCrunch AI、VentureBeat AI | 行业动态 |
| **中国AI** | 智谱AI、MiniMax、扣子Coze | 国产进展 |

---

## 📊 报告示例

**2026-04-12 晚报**

```markdown
📰 今日头条 (P0)

### GPT-6定档4月14日 — 200万Token上下文
OpenAI确认发布GPT-6，支持200万tokens上下文窗口...

### DeepSeek V4定档4月下旬 — 万亿参数
首个完全适配国产芯片的大模型...

🚀 重磅发布 (P1)
• 字节Seeduplex — 全双工语音模型
• 智谱GLM-5.1开源 — 最强开源模型
• Meta Muse Spark — 143亿美元投入，转向闭源

📊 统计：收录23条 · 重磅3条
```

---

## 🏗️ 项目结构

```
ai-sentinel/
├── scripts/
│   ├── collect.py          # 数据采集
│   ├── reporter.py         # 报告生成
│   └── parsers/            # 信息源解析器
├── config/
│   ├── sources.yaml        # 信息源配置
│   └── schedule.yaml       # 调度配置
├── templates/              # 报告模板
├── webui/                  # Web管理界面
└── reports/                # 生成的报告
```

---

## 📦 一键安装

```bash
npx clawhub@latest install ai-intelligence-sentinel
```

---

## 🔗 相关链接

| 资源 | 链接 |
|------|------|
| 📚 技术文档 | [README.md](./README.md) |
| 🌐 项目展示 | [thinkspc.fun/static/sentinel](http://thinkspc.fun/static/sentinel/) |
| 📦 ClawHub | [clawhub.ai/skills/ai-intelligence-sentinel](https://clawhub.ai/skills/ai-intelligence-sentinel) |
| 🦐 虾评Skill | [xiaping.coze.site](https://xiaping.coze.site/skill/08037f81-1e91-4115-80ad-2e2c1d0681d2) |
| 💻 GitHub | [xiaopengs/ai-sentinel](https://github.com/xiaopengs/ai-sentinel) |

---

## 🤝 参与贡献

欢迎贡献代码、提出问题或建议！

---

## 📄 许可证

MIT License — 自由使用于任何项目。

---

## 📝 更新日志

### v1.3.0 (2026-04-12)
- ✨ 新增 `--type full` 一键生成完整报告
- 优化报告生成流程

### v1.2.0 (2026-04-12)
- 📝 重构文档
- 添加项目展示页

### v1.0.0 (2026-04-10)
- 🎉 初始发布

---

<div align="center">

**为需要紧跟AI前沿的从业者打造。**

⭐ 觉得有用就点个Star吧！

</div>
