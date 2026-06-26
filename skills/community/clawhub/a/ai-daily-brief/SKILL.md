# AI 资讯日报抓取技能

## 功能
并行抓取多个 AI 资讯源，生成结构化日报并发送给用户。

## 使用方法
```bash
# 手动触发
openclaw run ai-daily-brief
```

## 抓取源
1. 36 氪 AI 频道：https://www.36kr.com/information/AI/
2. 极客公园 AI 新浪潮：https://www.geekpark.net/column/304

## 输出格式
- 标题 + 核心观点 + 深度总结（2-3 句话）
- 清晰的 Markdown 格式
- 发送到 warrior 的 Telegram

## 优化策略
- 使用 browser 工具并行抓取多个源
- 使用 snapshot 获取页面内容
- 提取 TOP10 最新资讯
- 结构化整理后发送
