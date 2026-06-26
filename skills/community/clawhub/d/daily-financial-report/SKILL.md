---
name: daily-financial-report
description: >
  完整流程：采集数据 → 生成 Word 日报 → 生成 PPT 简报 → 发送邮件。
  当用户说"生成每日金融日报"、"生成今日日报"、"生成晨报"时触发。
---

# 每日金融日报生成流程

## 执行顺序

```
Step 1 → collect-market-data/scripts/run_data_collection.py
Step 2 → generate-word-report/scripts/generate_word.py
Step 3 → generate-ppt-report/scripts/generate_ppt.py
Step 4 → send-email-to/scripts/send_email_to.py
```

- Step 1 包含两个子步骤（市场表现+经济数据 → 政策+企业+汇总），必须完整执行
- Step 2 和 Step 3 可并行执行，互不依赖
- Step 4 必须等 Step 2 和 Step 3 完成

## Step 1 数据采集内容

`run_data_collection.py` 执行两步数据采集：

| 子步骤 | 脚本 | 采集内容 | 数据源 |
|--------|------|----------|--------|
| **Step 1-A** | `collect_market_data.py` | 市场表现类（美股/A股/港股/欧股/亚太/大宗/外汇）+ 经济数据类 | API（akshare/TickDB/Sina/FRED等） |
| **Step 1-B** | `collect_news_websearch.py` | 政策动态 + 科技企业动态 + 环球市场速览 | Web Search（Tavily → Bocha → DuckDuckGo） |

输出文件：`E:\daily\{YYYY-MM-DD}\market_data.json`

各步骤详细说明见对应 Skill 的 SKILL.md：
- [collect-market-data](../collect-market-data/SKILL.md)
- [generate-word-report](../generate-word-report/SKILL.md)
- [generate-ppt-report](../generate-ppt-report/SKILL.md)
- [send-email-to](../send-email-to/SKILL.md)
