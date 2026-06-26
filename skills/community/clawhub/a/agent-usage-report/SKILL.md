---
name: agent-usage-report
description: 生成 OpenClaw Agent 使用周报。当用户说"周报"、"生成周报"、"工作周报"、"agent usage report"、"usage report"、"帮我写周报"、"生成使用报告"时使用此技能。自动读取 session 日志和 memory 文件，统计任务量、工具调用、成本、高频功能，并输出结构化周报。
---

# Agent Usage Report

生成 OpenClaw Agent 的使用周报，包括运行数据、高频工具调用、memory 日志摘要。

## 快速使用

```bash
python3 <skill-path>/scripts/generate_report.py
```

默认输出上周（周一~周日）的统计数据。

## 参数选项

| 参数 | 说明 |
|------|------|
| `--start YYYY-MM-DD` | 指定开始日期 |
| `--end YYYY-MM-DD` | 指定结束日期 |
| `--workspace /path` | 工作区路径（默认 `~/.openclaw/workspaces/bot6`） |
| `--output file.txt` | 保存到文件而不是打印 |

### 示例

```bash
# 默认上周周报
python3 <skill-path>/scripts/generate_report.py

# 指定日期范围
python3 <skill-path>/scripts/generate_report.py --start 2026-04-01 --end 2026-04-07

# 保存到文件
python3 <skill-path>/scripts/generate_report.py --output ~/weekly-report.txt
```

## 输出内容

- **运行数据概览** — session 数、消息数、工具调用数、成本
- **高频工具调用 TOP10** — 统计所有工具使用频次
- **Memory 日志摘要** — 从 `memory/` 目录提取本周记录片段
- **异常记录** — 待扩展（可从 session 错误日志中提取）

## 数据来源

- Session 日志：`~/.openclaw/agents/<agentId>/sessions/*.jsonl`
- Memory 文件：`~/.openclaw/workspaces/bot6/memory/*.md`

## 扩展周报内容

如果需要更完整的周报（风险记录、优化、下周计划），需要人工补充以下内容：

1. **风险记录** — 本周遇到的具体问题
2. **优化对策** — 解决方案和改进行动
3. **下周计划** — 下一周的演进方向

这些内容建议由使用者根据实际使用场景补充到报告末尾。

## 配合其他技能

- 结合 `session-logs` skill 可以查询更详细的历史记录
- 配合 `clawhub` 可以将报告分享或存档
