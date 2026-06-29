# 完整工作流与自动化

## 完整工作流

### 流程 A：搜索 → 解析 → 入库

当用户说"搜索本地关于 XX 的文件，提取要点保存"时：

1. **调用 es_search.py search** 找到匹配文件
2. **读取文件内容**（Read tool 或其他可用工具）
3. **解析归纳**要点，形成知识摘要
4. **调用 breadcrumb.py add** 将知识 + 原文路径存入面包屑
5. **汇总报告**搜索结果和入库情况

### 流程 B：每日复习

当用户说"今日复习"或"今天有什么知识需要回顾"时：

1. **调用 ebbinghaus.py daily-review** 获取今日应复习条目
2. **展示条目**给用户阅读
3. 用户确认后，**调用 ebbinghaus.py mark-reviewed** 更新复习记录

---

## 自动化/定时任务配置

> 以下为 Agent 语义指引。各 AI 平台根据自身能力实现。

### 定时任务 1：命题搜索 + 入库

**触发频率建议**：每天 1 次，凌晨执行

**Agent 执行逻辑**：
1. 调用 `es_search.py search "<命题关键词>"` 获取文件列表
2. 读取匹配文件，提取核心知识
3. 调用 `breadcrumb.py add` 将新知识入库

### 定时任务 2：每日艾宾浩斯复习

**触发频率建议**：每天 1 次，早晨执行

**Agent 执行逻辑**：
1. 调用 `ebbinghaus.py daily-review` 获取今日待复习条目
2. 向用户展示条目内容
3. 用户确认复习后，调用 `ebbinghaus.py mark-reviewed --id <ID>` 更新状态

### 定时任务 3：拓扑甜甜圈更新

**触发频率建议**：每天 1 次 或 每周 1 次

**Agent 执行逻辑**：
1. 调用 `topology_donut.py generate` 重新分析面包屑关联
2. 新关联发现时向用户报告更新摘要
3. 配合 `daily-review-expand` 在复习时自动利用拓扑扩展

---

## 跨平台调度指南

脚本本身是平台无关的纯 Python CLI，可由任意调度器触发：

| 平台 | 实现方式 | 命令示例 |
|------|---------|---------|
| **Linux/macOS cron** | `crontab -e` 添加定时任务 | `0 2 * * * python3 ~/.workbuddy/skills/everything-search-breadmemory/scripts/topology_donut.py generate` |
| **Windows 任务计划** | `schtasks` 命令行或 GUI | `schtasks /create /tn "拓扑甜甜圈更新" /tr "python topology_donut.py generate" /sc daily /st 02:00` |
| **macOS Launchd** | 创建 `.plist` 到 `~/Library/LaunchAgents/` | 配置 StartCalendarInterval 和 ProgramArguments |
| **WorkBuddy** | `automation_update` 工具 | prompt: "调用 topology_donut.py generate" |
| **Claude Code** | `.claude/settings.json` hooks | 同 cron 语法 |
| **GitHub Actions** | `.github/workflows/` YAML | `on: schedule: - cron: '0 2 * * *'` |
| **通用（手动）** | 用户手动执行 | `python topology_donut.py generate` |
