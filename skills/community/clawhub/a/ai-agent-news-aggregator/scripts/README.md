# AI Agent News Aggregator - 使用指南

## 快速开始

### 1. 配置飞书会话 ID

编辑 `sources.json`，填入你的飞书会话 ID：

```json
{
  "feishu": {
    "channel_id": "oc_your_channel_id"
  }
}
```

**如何获取 channel_id？**
- 在飞书群聊中，查看 URL 或消息元数据
- 或联系 OpenClaw 管理员获取

### 2. 测试运行

```bash
# 步骤 1: 搜索新闻
python search_news.py --output step1_search.json

# 步骤 2: 去重
python deduplicate.py --input step1_search.json --output step2_deduped.json

# 步骤 3: 分类
python categorize.py --input step2_deduped.json --output step3_categorized.json

# 步骤 4: 生成摘要
python summarize.py --input step3_categorized.json --output step4_summarized.json

# 步骤 5: 推送到飞书
python push_to_feishu.py --input step4_summarized.json --config ../scripts/sources.json
```

### 3. 一键运行（推荐）

```bash
python run_pipeline.py --config sources.json
```

---

## 在 OpenClaw 中使用

### 一次性搜集

```json
{
  "action": "collect",
  "time_range": "24h"
}
```

### 设置定时任务

```json
{
  "action": "schedule",
  "cron": "0 9 * * 1-5",
  "time_range": "24h"
}
```

这会在工作日每天 9:00 自动推送前一天的资讯。

---

## 自定义数据源

编辑 `sources.json`：

```json
{
  "keywords": [
    "你的关键词 1",
    "你的关键词 2"
  ],
  "rss_sources": [
    {"name": "博客名", "url": "https://.../rss.xml"}
  ]
}
```

---

## 输出示例

```
🤖 AI Agent 每日简报 - 2026-03-16

🔥 头条
• LangChain 发布新 Agent 框架 - 支持 XX 功能 [https://...]

🛠️ 框架更新
• AutoGen v0.4.0 - 新增多 Agent 协作 [https://...]
• CrewAI 支持 XX [https://...]

📚 研究论文
• Multi-Agent Collaboration - arXiv [https://...]

🏢 公司动态
• Anthropic 发布 XX [https://...]

💼 行业应用
• XX 公司用 Agent 实现 XX [https://...]

---
共 12 条资讯 | 来源：DDG + 6 RSS 源
```

---

## 故障排除

### 问题：收不到推送

1. 检查 `channel_id` 是否正确
2. 确认飞书机器人权限
3. 查看脚本输出日志

### 问题：内容太少

1. 增加关键词数量
2. 添加更多 RSS 源
3. 降低 `min_relevance` 阈值

### 问题：重复内容多

提高去重阈值：
```bash
python deduplicate.py --threshold 0.9
```
