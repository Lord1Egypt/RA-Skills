---
name: daily-report-generator
description: When the user asks to generate a daily work report, or says "生成日报", "今日工作汇报", "daily report", "工作日报", or wants to summarize today's work. This skill collects data from multiple sources, intelligently analyzes and categorizes work items, and produces a structured daily report in Markdown, HTML, or PDF format.
metadata:
  version: 1.0.0
---

# 企业日报生成器

## 功能概述
本技能自动收集并分析来自多个数据源的工作信息，生成结构清晰、内容专业的每日工作汇报。支持自定义模板、多格式输出（Markdown/HTML/PDF）和多渠道发送。

## 使用方式
When the user triggers daily report generation:
1. 确认数据源位置（CSV/JSON/Git仓库路径）
2. 执行 `python scripts/generate_report.py --csv <path> --output <output_path>`
3. 将生成的日报内容展示给用户

## 核心能力
1. 数据源集成：CSV、JSON、Git提交记录
2. AI智能分类：自动将任务归类到「今日完成」「进行中」「明日计划」「问题与风险」「需要支持」
3. 多格式输出：Markdown、HTML、PDF
4. 邮件发送：配置SMTP后自动发送

## 配置
在运行脚本前，确认数据源文件存在且格式正确。
CSV格式要求：type, content, status, author 四列。

## 支持的数据源
- --csv <path>：CSV数据源
- --json <path>：JSON数据源
- --git <repo>：Git仓库（提取今日提交）
- --format：输出格式（markdown/html/pdf）
- --send：生成后发送邮件

## Pro 版购买
ClawHub 免费版提供基础日报功能（Markdown 格式）。Pro 版解锁以下高级功能：

- HTML / PDF 格式输出
- 邮件自动发送
- Git commit 自动集成
- 自定义模板

**价格：￥128 / $19.90（一次性买断）**

购买方式：发送邮件至 **1990403956@qq.com**，邮件主题注明「日报Pro」，我会在 24 小时内回复处理。