---
slug: ai-sentinel
name: AI前沿哨兵
version: 1.0.0
description: AI情报哨兵 - 自动采集、分析与报告AI领域最新动态的多源情报系统
trigger: "AI情报|AI哨兵|AI资讯|AI动态|科技新闻|论文追踪|开源项目追踪|晨报|晚报"
tools: [shell, filesystem, http]
author: xiaopengs
---

# AI前沿哨兵 (AI Sentinel)

> 你的AI情报指挥中心，自动采集、分析与报告AI领域最新动态

## 技能概述

AI前沿哨兵是一个开源的AI情报采集系统，帮助用户自动追踪AI领域的最新动态，包括开源项目、学术论文、技术博客、行业新闻等，并生成结构化的晨报和晚报。

**核心能力：**
- 🔍 多源信息采集（GitHub、arXiv、HackerNews、Twitter/X、RSS等）
- ⏰ 智能定时调度（晨报08:00、晚报20:00）
- 📊 智能分析评分（热度+新鲜度+来源可信度）
- 📄 自动化报告生成（Markdown格式）
- 🎛️ WebUI管理面板

## 适用场景

- AI从业者追踪最新技术动态
- 研究人员关注前沿论文
- 开发者发现优质开源项目
- 产品经理了解行业趋势
- 内容创作者获取素材

## 使用方法

### 1. 基本采集

当用户说"采集AI情报"、"生成AI晨报"、"追踪AI动态"时，执行以下步骤：

```bash
# 采集所有信息源
python scripts/collect.py --all

# 生成晨报
python scripts/reporter.py --type morning

# 生成晚报
python scripts/reporter.py --type evening
```

### 2. 单源采集

```bash
# 仅采集GitHub Trending
python scripts/collect.py --source github

# 仅采集arXiv论文
python scripts/collect.py --source arxiv

# 仅采集HackerNews
python scripts/collect.py --source hackernews
```

### 3. 查看报告

生成的报告保存在 `reports/YYYY-MM-DD/` 目录：
- `morning_report.md` - 晨报
- `evening_report.md` - 晚报
- `xiaohongshu_report.md` - 小红书风格报告

## 配置说明

### 信息源配置 (`config/sources.yaml`)

系统支持以下信息源：

1. **GitHub Trending** - AI开源项目热度排行
2. **arXiv** - 最新AI论文（cs.AI, cs.LG, cs.CL）
3. **HackerNews** - 开发者社区热点讨论
4. **Twitter/X** - AI大咖动态（需API Token）
5. **RSS博客** - 官方博客和技术媒体
   - Anthropic, OpenAI, Google AI, DeepMind
   - Hugging Face, xAI, Cursor
   - TechCrunch AI, VentureBeat AI
   - InfoQ全球/中文
   - MMChat AI资讯
6. **中国AI公司** - 官网新闻解析
   - 智谱AI、MiniMax、扣子Coze

### 调度配置 (`config/schedule.yaml`)

```yaml
schedule:
  morning:
    enabled: true
    time: "08:00"
  evening:
    enabled: true
    time: "20:00"
```

## 工作流程

1. **采集阶段** - 从配置的信息源拉取最新数据
2. **分析阶段** - 计算热度、新鲜度、质量评分
3. **筛选阶段** - 按优先级排序，过滤低质量内容
4. **生成阶段** - 使用Jinja2模板生成Markdown报告
5. **存档阶段** - 按日期保存到 `reports/` 目录

## 项目结构

```
ai-sentinel/
├── SKILL.md                    # 本文档
├── config/                     # 配置文件
│   ├── sources.yaml            # 信息源配置
│   ├── settings.yaml           # API配置
│   └── schedule.yaml           # 调度配置
├── scripts/                    # 核心脚本
│   ├── collect.py              # 采集入口
│   ├── analyzer.py             # 分析评分
│   ├── reporter.py             # 报告生成
│   ├── quality_scorer.py       # 质量评分系统
│   └── parsers/                # 平台解析器
│       ├── github_trending.py
│       ├── arxiv.py
│       ├── hackernews.py
│       ├── blog_rss.py
│       └── web_news.py
├── templates/                  # 报告模板
│   ├── morning_report.md
│   ├── evening_report.md
│   └── xiaohongshu_report.md
├── reports/                    # 报告存档
│   └── YYYY-MM-DD/
│       ├── morning_report.md
│       ├── evening_report.md
│       └── xiaohongshu_report.md
├── webui/                      # Web界面
│   ├── index.html
│   ├── style.css
│   └── app.js
└── references/                 # 参考文档
    ├── sources_guide.md
    └── api_setup.md
```

## 安装依赖

```bash
pip install requests feedparser pyyaml jinja2 schedule
```

## 扩展指南

### 添加新信息源

1. 在 `scripts/parsers/` 创建新解析器
2. 实现 `fetch()` 方法返回标准格式数据
3. 在 `config/sources.yaml` 添加配置
4. 在 `scripts/collect.py` 注册解析器

### 自定义报告模板

编辑 `templates/` 目录下的模板文件，使用Jinja2语法：
- `{{ title }}` - 标题
- `{{ items }}` - 条目列表
- `{{ analysis }}` - 分析内容

## 常见问题

**Q: Twitter采集失败？**  
A: 需要Twitter Developer账号和Bearer Token，未配置时自动跳过。

**Q: 如何添加自定义关键词？**  
A: 编辑 `config/sources.yaml` 中各源的 `keywords` 字段。

**Q: 报告保存位置？**  
A: 默认 `reports/YYYY-MM-DD/`，可在配置中修改。

## 仓库地址

https://github.com/xiaopengs/ai-sentinel

## License

MIT License - 详见 LICENSE 文件
