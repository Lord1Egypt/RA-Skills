# 财经新闻分析器

专业的财经新闻深度分析技能，帮助投资者快速理解新闻背后的投资信号。

## 快速开始

```bash
# 安装依赖
pip install requests beautifulsoup4 openai

# 分析今日财经新闻
python scripts/main.py --source all --limit 20

# 分析特定新闻源
python scripts/main.py --source wallstreetcn,36kr --limit 15

# 带关键词过滤
python scripts/main.py --keyword "AI，芯片，半导体" --source hackernews,github

# 生成行业周报
python scripts/main.py --industry 科技 --period weekly --output industry
```

## 功能特性

- ✅ 多源新闻抓取（28+ 新闻源）
- ✅ 情感分析（利好/利空/中性）
- ✅ 影响评估（行业/公司/市场）
- ✅ 关键信息提取
- ✅ 多种简报格式

## 输出示例

```markdown
# 📈 财经新闻简报
**日期**: 2026-03-09 | **来源**: 华尔街见闻，36 氪 | **总数**: 15 条

## 🟢 利好消息 (5 条)

#### 1. [英伟达发布新一代 AI 芯片，性能提升 300%](https://...)
- **来源**: 华尔街见闻 | **时间**: 22:48
- **影响**: 🟢 利好 | **置信度**: 高
- **相关股票**: NVDA (+), AMD (-), INTC (-)
- **一句话**: 英伟达新芯片可能巩固 AI 芯片领导地位

## 🔴 利空消息 (3 条)
...
```

## 文档结构

```
finance-news-analyzer/
├── SKILL.md              # 技能说明
├── scripts/
│   └── main.py           # 主脚本
├── references/
│   ├── ticker-map.md     # 股票代码映射
│   └── sentiment-rules.md # 情感分析规则
└── templates/            # 简报模板
```

## 相关技能

- news-aggregator-skill - 新闻抓取基础
- stock-analyzer - 股票技术分析

## License

MIT
