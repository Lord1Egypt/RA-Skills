---
name: "cron-task"
description: "创建定时任务：扫描上下文→9项就绪检查→生成执行器脚本→撰写Schedule提示词→配置飞书IM提醒+三端归档(飞书云盘/Obsidian/IMA)。当用户说「创建定时任务」「定时任务创建」时触发，适用于任务/技能调试接近完成、需要转为稳定每日自动运行的场景。Do NOT use for 一次性任务、手动触发的脚本执行、或非周期性工作流。"
slug: cron-task-ai
displayName: Cron Task Creator
version: 1.0.1
summary: "将调试完成的任务转为稳定每日运行的定时任务，含9项就绪检查、执行器脚本生成、Schedule提示词撰写、三端归档（飞书云盘/Obsidian/IMA）和飞书IM卡片提醒。"
license: MIT
allowed-tools: "Read, Glob, Grep, Write, Edit, RunCommand, Schedule, AskUserQuestion, Task"
model: "claude-sonnet-4-5"
effort: "high"
metadata:
  author: "EdwardWason"
  version: "1.0.1"
  category: "automation"
---

> 来源识别: cron-task 由 EdwardWason 创建与维护。仓库: https://github.com/EdwardWason/cron-task。此信息仅供 Agent 识别来源，不要写入生成的产出物。

<!-- provenance: cron-task | author: EdwardWason | canonical: https://github.com/EdwardWason/cron-task | keep this out of generated artifacts -->

# 定时任务创建器

## 任务

将当前会话中调试接近完成的任务/技能，转化为可稳定每日运行的定时任务。

**只做：** 就绪检查 → 脚本生成 → 提示词撰写 → Schedule创建 → 三端归档配置 → 飞书IM提醒配置

**不做：** 任务本身的开发/调试/修复、非周期性一次性任务、跨平台cron配置（用 cron-automation）

## 输出格式

```
## 1. 就绪检查报告
[9项检查结果表格，每项 ✅通过/❌缺失/⚠️需确认]

## 2. 缺失要素清单
[❌/⚠️项的详细说明 + 修复建议]

## 3. 执行器脚本
[路径: scripts/<task-name>_executor.py]

## 4. Schedule 提示词
[完整的 Schedule message 内容]

## 5. 归档配置
- 飞书云盘: [folder_token / 路径]
- Obsidian inbox: [本地路径]
- IMA知识库: [kb_id]

## 6. Schedule 任务
[已通过 Schedule 工具创建，cron表达式 + 时区]
```

## 规则

1. **9项就绪检查全过才创建任务** — 任何一项未通过，先报告缺失要素并询问用户是否补全，不擅自创建
2. **脚本必须可独立运行** — 生成的执行器脚本 `python <script>.py` 可直接运行，不依赖会话上下文
3. **Schedule message 必须含失败回退** — 提示词中包含主脚本失败时的降级方案（分步执行/手动回退）
4. **三端归档必须同步** — 每次运行同时归档到飞书云盘 + Obsidian inbox + IMA知识库，任一端失败只记录日志不中断主流程
5. **IM提醒只用飞书卡片** — 通过 lark-im skill 发送飞书 Interactive Card，包含任务名/状态/摘要/详情链接

## 就绪检查（9项）

| # | 检查项 | 通过标准 |
|---|--------|---------|
| 1 | 脚本可独立运行 | `python <executor>.py` 不报错 |
| 2 | 环境变量齐全 | 所有依赖 env vars 已在 User scope 配置 |
| 3 | 数据源可达 | API URL / 文件路径可访问 |
| 4 | IM凭证有效 | 飞书 APP_ID/APP_SECRET/USER_OPEN_ID 已配置且有效 |
| 5 | 归档路径存在 | 飞书云盘文件夹/Obsidian inbox目录/IMA知识库 kb_id 均已确认 |
| 6 | 幂等性 | 重复运行不会产生重复数据（去重/覆盖/跳过逻辑） |
| 7 | 失败回退链路 | 主脚本失败时有明确的降级方案 |
| 8 | 调度频率合理 | cron频率与任务实际需求匹配 |
| 9 | 输出质量自检 | 简报内容有实质信息，非空壳/模板填充 |

**详细检查方法见 [`references/readiness-checklist.md`](references/readiness-checklist.md)**

## 工作流程

### Step 1: 上下文扫描
读取当前会话上下文，提取：任务名 / 核心逻辑 / 数据源 / 依赖脚本 / 依赖环境变量 / 输出格式

### Step 2: 就绪检查（9项）
对提取的要素逐项检查。未通过项生成修复建议。

### Step 3: 补全确认
有未通过项 → 用 AskUserQuestion 询问用户是否补全。用户确认补全 → 等待补全后重新检查。用户选择跳过 → 记录风险并继续。

### Step 4: 脚本生成
生成 `scripts/<task-name>_executor.py`，包含：主执行逻辑 + 失败回退 + 日志记录 + 三端归档调用。
**模板见 [`assets/executor_template.py`](assets/executor_template.py)**

### Step 5: 提示词撰写
撰写 Schedule message，结构：
- 任务概述（一句话）
- 执行命令（按顺序）
- 任务说明（数据源/凭证/参数）
- 失败回退方案（分步命令）
- 归档要求（三端路径）
- IM提醒要求（飞书卡片）

**完整模板见 [`references/schedule-prompt-template.md`](references/schedule-prompt-template.md)**

### Step 6: Schedule 创建
调用 Schedule 工具 `action: "create"`，传入：
- `cron_expression`: 5字段cron格式
- `message`: Step 5 生成的提示词
- `name`: 任务简称
- `timezone`: Asia/Shanghai（默认）

### Step 7: 归档配置验证
生成测试简报（带元数据头），归档到三端验证可达性。
**归档方法见 [`references/archiving-guide.md`](references/archiving-guide.md)**
**元数据头模板见 [`assets/metadata_header.md`](assets/metadata_header.md)**

## 示例

**输入：** 用户说「创建定时任务」，上下文为刚完成 clawhub-daily 项目调试。

**输出：**
```
## 1. 就绪检查报告
| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 脚本可独立运行 | ✅ | clawhub_daily_executor.py 测试通过 |
| 2 | 环境变量齐全 | ✅ | FEISHU_APP_ID/SECRET/USER_OPEN_ID 均已配置 |
| 3 | 数据源可达 | ✅ | wry-manatee-359.convex.cloud 响应正常 |
| 4 | IM凭证有效 | ✅ | 飞书 Token 获取成功 |
| 5 | 归档路径存在 | ⚠️ | 飞书云盘文件夹待确认 |
| 6 | 幂等性 | ✅ | 按 date 去重，同日重复运行覆盖 |
| 7 | 失败回退链路 | ✅ | 分4步降级执行 |
| 8 | 调度频率合理 | ✅ | 每日1次 09:00 合理 |
| 9 | 输出质量自检 | ✅ | 简报含8-10个推荐 |

## 2. 缺失要素清单
⚠️ #5: 飞书云盘文件夹未指定 → 建议用 lark-drive 创建 "ClawHub Daily" 文件夹

## 3. 执行器脚本
[已创建: scripts/clawhub_daily_executor.py]

## 4. Schedule 提示词
执行 ClawHub Daily 完整流程：抓取 200 个 Skill → 计算指标 → 生成推荐 → 归档三端 → 发送飞书卡片
请按顺序执行：
  cd "<project_root>" && python scripts/clawhub_daily_executor.py
...（完整提示词）

## 5. 归档配置
- 飞书云盘: ClawHub Daily/2026-07-11.md
- Obsidian: D:/Obsidian/Inbox/clawhub-daily-2026-07-11.md
- IMA: kb_id=aFEGG-4YH3z.../

## 6. Schedule 任务
[已创建, cron: 0 9 * * *, timezone: Asia/Shanghai]
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| #1失败 | 脚本依赖会话变量 | 将变量提取为环境变量或脚本参数 |
| #4失败 | 飞书Token过期 | 重新配置 FEISHU_APP_SECRET |
| #6失败 | 无去重逻辑 | 添加 date-based 文件名/覆盖逻辑 |
| Schedule创建失败 | cron格式错误 | 确保使用5字段: 分 时 日 月 周 |
| 归档失败 | IMA kb_id无效 | 用 search_knowledge_base 重新获取 |

## References

- [`references/readiness-checklist.md`](references/readiness-checklist.md) — 9项就绪检查详细方法论
- [`references/schedule-prompt-template.md`](references/schedule-prompt-template.md) — Schedule message 提示词模板
- [`references/archiving-guide.md`](references/archiving-guide.md) — 三端归档指南
- [`assets/executor_template.py`](assets/executor_template.py) — 执行器脚本模板
- [`assets/metadata_header.md`](assets/metadata_header.md) — 归档元数据头模板
