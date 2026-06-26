---
name: daily-morning-meeting
slug: daily-morning-meeting
version: 1.0.1
description: "每日早会自动执行技能。多Agent抓取全网热点，整理成早会简报发送给CEO。"
metadata: {"openclaw":{"emoji":"🌅","os":["linux","darwin","win32"]}}
---

## 每日早会技能
### 功能说明
- 每天早上指定时间自动触发（默认9:00）
- 调用全网搜索能力抓取当日热点新闻、行业要闻、政策动态、财经资讯等重要内容
- 多Agent协同分析讨论资讯内容，筛选高价值信息
- 整理成结构清晰、重点突出的早会简报
- 自动将简报发送给CEO
### 配置说明
1. 执行时间：可通过cron任务配置自定义执行时间
2. 资讯范围：支持自定义关注的行业、领域关键词
3. 接收人：可配置简报接收人列表
### 依赖技能
- `qclaw-cron-skill` 定时任务调度
- `multi-search-engine` 全网资讯检索
- `agent-orchestrator` 多Agent协同处理
- `message` 消息推送
### 手动执行
运行以下命令立即触发早会简报生成：
```bash
python C:\Users\Admin\.qclaw\workspace\skills\daily-morning-meeting\main.py
```