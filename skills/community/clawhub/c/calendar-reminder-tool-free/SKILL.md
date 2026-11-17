---
name: "calendar-reminder-tool-free"
description: "每晚自动扫描明日日历并通过飞书发送提醒，上午提前2小时、下午统一12点通知，适合个人单日历。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "日历提醒工具免费版"
  version: "1.0.0"
  summary: "每晚自动扫描明日日历并通过飞书发送提醒，上午提前2小时、下午统一12点通知，适合个人单日历。"
  tags:
    - "日历提醒"
    - "日程管理"
    - "飞书通知"
    - "个人效率"
    - "定时任务"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 日历提醒工具 免费版

## 概述

免费版日历提醒工具为个人用户提供自动化的日历日程提醒服务。每晚 22:00 自动扫描明天的日历，按时间段分类设置提醒：上午日程（12:00 前）提前 2 小时飞书提醒，下午日程（12:00 及以后）当天 12:00 统一飞书提醒。扫描完成后立即发送汇报消息，让你对明日安排了然于胸。

与专业版相比，免费版聚焦单个日历扫描与基础提醒规则，不包含多日历聚合、智能调度优化、团队日程同步与数据分析等高级能力。但两者的扫描脚本与提醒格式完全一致，便于后续平滑升级。

## 核心能力

| 能力 | 说明 |
| --- | --- |
| 每晚定时扫描 | 22:00 自动扫描明日全部日历日程 |
| 时段分类提醒 | 上午日程提前 2 小时提醒，下午日程 12:00 统一提醒 |
| 飞书通知 | 通过飞书机器人发送提醒消息 |
| 扫描汇报 | 扫描完成后立即发送明日日程汇总 |
| 手动触发 | 支持随时手动运行扫描脚本 |
| 时区感知 | 基于 Asia/Shanghai 时区处理时间 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：每晚自动扫描明日、日历并通过飞书发、送提醒、上午提前、下午统一、点通知、适合个人单日历、面向个人用户的日、历日程自动提醒工、核心能力、每晚定时扫描明日、按时段分类提醒、飞书消息通知、扫描完成汇报、适用场景、个人日程提醒、工作日历管理、会议防遗漏、每日日程预览、差异化、免费版聚焦单个日、历扫描与基础提醒、不含多日历聚合与、智能调度、适用关键词、calendar、reminder、定时扫描、会议通知等。

## 使用场景

### 场景一：个人工作日历提醒

每晚自动扫描明日工作日历，第二天按时收到飞书提醒，避免错过会议。

```text
# 22:00 扫描完成汇报（飞书消息）
📅 明日日程扫描完成（2026-07-19）

上午日程（提前2小时提醒）:
- 09:00 项目周会 (会议室A)
- 11:00 客户需求评审 (线上)

下午日程（12:00统一提醒）:
- 14:00 技术方案评审 (会议室B)
- 16:00 一对一沟通 (线上)

共 4 项日程，已设置提醒 ✅
```

### 场景二：上午会议提前提醒

第二天早上，上午的会议提前 2 小时收到飞书提醒。

```text
# 07:00 飞书提醒（针对 09:00 的会议）
⏰ 日程提醒
📅 项目周会
🕐 时间: 明天 09:00 - 10:00
📍 地点: 会议室A
⏳ 还有 2 小时开始，请做好准备
```

### 场景三：下午日程统一提醒

中午 12:00 统一收到下午全部日程的提醒。

```text
# 12:00 飞书提醒
📅 下午日程提醒
🕐 14:00 技术方案评审 (会议室B)
🕐 16:00 一对一沟通 (线上)

共 2 项下午日程，请合理安排时间
```

## 不适用场景

以下场景日历提醒工具免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 确保已安装依赖（owa-outlook skill、Python 3.9+、skill-platform CLI）。
2. 注册每晚扫描定时任务。

```bash
skill-platform cron add \
  --name "calendar-daily-scan" \
  --cron "0 22 * * *" \
  --tz "Asia/Shanghai" \
  --session main \
  --system-event "CALENDAR_SCAN: 请立即运行 python3 ~/.skill-platform/workspace/skills/calendar-reminder/calendar_reminder.py 并等待完成" \
  --description "每晚22:00扫描明天日历并设置提醒"
```

3. 修改脚本中的飞书 open_id。

编辑 `calendar_reminder.py`，将 `send_feishu` 函数中的 `target` 改为你自己的飞书 open_id：

```python
"--target", "user:ou_xxxxxxxxxxxxxxxx",
```

4. 手动运行一次验证。

```bash
python3 ~/.skill-platform/workspace/skills/calendar-reminder/calendar_reminder.py
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 示例

免费版配置通过脚本参数与环境变量控制。

```python
# calendar_reminder.py 配置部分

# 飞书通知配置
FEISHU_CONFIG = {
    "target": "user:ou_xxxxxxxxxxxxxxxx",  # 你的飞书 open_id
    "bot_name": "日历提醒助手",
}

# 提醒规则配置
REMINDER_RULES = {
    "morning_threshold": "12:00",      # 上午/下午分界
    "morning_advance_hours": 2,        # 上午日程提前提醒小时数
    "afternoon_reminder_time": "12:00", # 下午日程统一提醒时间
}

# 扫描配置
SCAN_CONFIG = {
    "timezone": "Asia/Shanghai",
    "scan_time": "22:00",              # 每晚扫描时间
    "lookahead_days": 1,               # 扫描未来天数
}
```

**定时任务配置**

```bash
# 查看已注册的定时任务
skill-platform cron list

# 查看任务详情
skill-platform cron get --name "calendar-daily-scan"

# 删除定时任务（如需重新配置）
skill-platform cron remove --name "calendar-daily-scan"
```

## 最佳实践

- **open_id 准确**：确保飞书 open_id 正确，可通过飞书管理后台查询。错误的 open_id 会导致提醒无法送达。
- **时区一致**：脚本使用 Asia/Shanghai 时区，若你在其他时区，修改 `SCAN_CONFIG.timezone`。
- **日历同步**：确保 Outlook 日历已与工作邮箱同步，脚本依赖 owa-outlook 读取日历数据。
- **提前测试**：首次配置后手动运行一次，确认飞书消息能正常接收。
- **定时任务检查**：定期确认 cron 任务正常运行，避免因系统重启导致任务丢失。
- **分界时间调整**：若上午/下午分界不是 12:00，可修改 `morning_threshold`。
- **提醒频率**：免费版每个日程仅提醒一次，如需多次提醒或递进式提醒，请升级至专业版。

## 常见问题

### Q1：每晚扫描没有执行？

检查定时任务是否正常注册并运行：

```bash
skill-platform cron list
skill-platform cron get --name "calendar-daily-scan"
```

若任务不存在，重新注册。若任务存在但未执行，检查 skill-platform 服务是否正常运行。

### Q2：飞书消息没有收到？

- 确认 `calendar_reminder.py` 中的飞书 open_id 正确。
- 确认飞书机器人已添加为你的联系人。
- 手动运行脚本测试是否能收到消息。

### Q3：提示"owa_calendar 模块未找到"？

需要先安装 owa-outlook skill，它提供 `owa_calendar.py` 模块用于读取 Outlook 日历。

### Q4：提示"zoneinfo 模块未找到"？

`zoneinfo` 模块需要 Python 3.9+。运行 `python3 --version` 检查版本，低于 3.9 请升级 Python。

### Q5：免费版支持多个日历吗？

免费版仅扫描单个默认日历。如需聚合多个日历（工作、个人、团队），请升级至专业版。

### Q6：可以修改提醒时间规则吗？

可以。在 `calendar_reminder.py` 的 `REMINDER_RULES` 中修改：
- `morning_advance_hours`：上午日程提前提醒小时数。
- `afternoon_reminder_time`：下午日程统一提醒时间。
- `morning_threshold`：上午/下午分界时间。

### Q7：周末会扫描吗？

会。定时任务每天 22:00 执行，包括周末。若周末无需提醒，可在脚本中添加周末跳过逻辑，或升级至专业版使用工作日过滤。

### Q8：如何手动触发扫描？

随时运行以下命令手动触发：

```bash
python3 ~/.skill-platform/workspace/skills/calendar-reminder/calendar_reminder.py
```

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **运行时**：Python 3.9+（需要 `zoneinfo` 模块）
- **定时调度**：skill-platform cron 或系统 cron

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
| :------- | :----- | :--------- | :--------- |
| Python 3.9+ | 运行时 | 必需 | python.org 官方下载 |
| owa-outlook skill | skill 依赖 | 必需 | 提供 `owa_calendar.py` 日历读取模块 |
| skill-platform CLI | 命令行工具 | 必需 | 定时任务注册与管理 |
| 飞书机器人 | 通信渠道 | 必需 | 飞书开放平台创建应用机器人 |
| Outlook 账号 | 日历来源 | 必需 | 已配置的工作邮箱 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 飞书机器人凭证配置在 skill-platform 通信通道中。
- Outlook 账号凭证配置在 owa-outlook skill 中。
- 免费版无需额外 API Key（除飞书与 Outlook 凭证外）。

```bash
# 环境变量示例
export FEISHU_APP_ID="your_feishu_app_id"
export FEISHU_APP_SECRET="your_feishu_app_secret"
export OUTLOOK_EMAIL="your_work_email@company.com"
```

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务。免费版为单日历扫描功能子集，扫描脚本与提醒格式与专业版完全兼容。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
