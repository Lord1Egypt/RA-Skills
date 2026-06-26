---
name: competitor-radar
description: 竞品动态监控雷达。自动抓取竞品博客RSS、GitHub Release、HackerNews讨论，用AI评分筛选重要动态，生成结构化报告。当需要了解竞品最新动向、监控行业变化时使用。
license: MIT
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["python3"]
---

# Competitor Radar 🎯

自动监控竞品动态，生成结构化分析报告。

## 配置竞品

编辑 `config.yaml`，添加你要监控的竞品：

```yaml
competitors:
  - name: "竞品名称"
    domain: "example.com"
    blog_rss: "https://example.com/rss.xml"
    github_org: "github-org-name"
    keywords: ["关键词1", "关键词2"]
```

## 使用方法

```bash
# 扫描过去7天
python3 radar.py

# 扫描过去14天，保存报告
python3 radar.py --days 14 --output report.md

# 跳过AI评分（更快）
python3 radar.py --no-ai

# 使用自定义配置
python3 radar.py --config /path/to/my-config.yaml
```

## 数据来源
- 官网博客 RSS Feed
- GitHub Release / Tag
- HackerNews 提及

## 输出格式
Markdown 报告，按重要性分级（🔴重要 / 🟡值得关注 / ⚪一般）
