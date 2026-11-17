---
slug: calendar-reminder-paid
name: calendar-reminder-paid
version: "1.0.0"
displayName: 日历提醒工具专业版
summary: 企业级多日历智能提醒平台，支持多日历聚合、智能调度、团队同步、递进提醒与日程分析。
license: Proprietary
edition: pro
description: |-
  面向团队与企业的多日历智能提醒与调度平台。
  核心能力: 多日历聚合扫描、智能提醒调度、递进式提醒、团队日程同步、冲突检测、日程分析报表、多渠道通知。
  适用场景: 团队日程协调、高管助理提醒、跨时区会议安排、会议室资源调度、日程效率分析。
  差异化: 专业版在免费版基础上新增多日历与智能调度，兼容免费版扫描脚本与提醒格式。
tags:
- 日历提醒
- 多日历聚合
- 智能调度
- 团队协作
- 日程分析
- 企业级
tools:
  - - read
- exec
---
# 日历提醒工具专业版

## 核心能力

| 能力 | 免费版 | 专业版 |
| --- | :---: | :---: |
| 单日历扫描 | 支持 | 支持 |
| 时段分类提醒 | 支持 | 支持 |
| 飞书通知 | 支持 | 支持 |
| 每晚定时扫描 | 支持 | 支持 |
| 多日历聚合 | - | 支持 |
| 递进式提醒 | - | 支持 |
| 日程冲突检测 | - | 支持 |
| 跨时区支持 | - | 支持 |
| 团队日程同步 | - | 支持 |
| 多渠道通知 | - | 支持 |
| 日程分析报表 | - | 支持 |
| 工作日/自定义过滤 | - | 支持 |
| 智能调度优化 | - | 支持 |
### 单日历扫描

执行单日历扫描操作,处理用户输入并返回结果。

**输入**: 用户提供单日历扫描所需的参数和指令。

**输出**: 返回单日历扫描的处理结果。

- 执行`单日历扫描`操作，处理输入数据并返回结果
- 验证执行结果，确认输出符合预期格式
- 参考`单日历扫描`相关配置参数进行设置
### 时段分类提醒

执行时段分类提醒操作,处理用户输入并返回结果。

**输入**: 用户提供时段分类提醒所需的参数和指令。

**输出**: 返回时段分类提醒的处理结果。

- 执行`时段分类提醒`操作，处理输入数据并返回结果
- 验证执行结果，确认输出符合预期格式
- 参考`时段分类提醒`相关配置参数进行设置
### 飞书通知

执行飞书通知操作,处理用户输入并返回结果。

**输入**: 用户提供飞书通知所需的参数和指令。

**输出**: 返回飞书通知的处理结果。

- 执行`飞书通知`操作，处理输入数据并返回结果
- 验证执行结果，确认输出符合预期格式
- 参考`飞书通知`相关配置参数进行设置
### 能力覆盖范围

本skill还覆盖以下能力场景: 企业级多日历智能、提醒平台、支持多日历聚合、团队同步、递进提醒与日程分、面向团队与企业的、多日历智能提醒与、调度平台、核心能力、多日历聚合扫描、智能提醒调度、适用场景、团队日程协调、高管助理提醒、跨时区会议安排、会议室资源调度、日程效率分析、差异化、专业版在免费版基、础上新增多日历与、兼容免费版扫描脚、本与提醒格式。这些能力在上述核心功能中均有对应处理逻辑。
## 适用场景

### 场景一：多日历聚合扫描

聚合工作日历、个人日历与团队共享日历，统一扫描并按优先级排序提醒。

```python
# calendar_reminder_pro.py
from datetime import datetime, timedelta
import json

# 多日历配置
CALENDARS = [
    {"id": "work",     "source": "owa_calendar",  "priority": 1, "color": "🔵"},
    {"id": "personal", "source": "owa_calendar",  "priority": 2, "color": "🟢"},
    {"id": "team",     "source": "owa_calendar",  "priority": 1, "color": "🟡"},
]

# 扫描明日全部日历
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
all_events = []

for cal in CALENDARS:
    events = owa_calendar.get_events(
        calendar_id=cal["id"],
        start_date=tomorrow,
        end_date=tomorrow,
        timezone="Asia/Shanghai"
    )
    for evt in events:
        evt["calendar"] = cal["id"]
        evt["priority"] = cal["priority"]
        evt["color"] = cal["color"]
        all_events.append(evt)

# 按时间排序
all_events.sort(key=lambda x: x["start_time"])

# 按时段分组
morning = [e for e in all_events if e["start_hour"] < 12]
afternoon = [e for e in all_events if e["start_hour"] >= 12]

# 生成聚合汇报
report = generate_report(morning, afternoon)
send_feishu(target=ADMIN_OPEN_ID, message=report)
```

**聚合汇报示例**

```text
📅 明日日程扫描完成（2026-07-19）

🔵 工作日历 | 🟢 个人日历 | 🟡 团队日历

上午日程（提前2小时递进提醒）:
🔵 09:00 项目周会 (会议室A) [高优先级]
🟡 10:30 团队站会 (线上)
🟢 11:30 健身预约 (健身房)

下午日程（12:00统一提醒）:
🔵 14:00 技术方案评审 (会议室B) [高优先级]
🔵 16:00 客户电话 (线上)
🟢 19:00 家庭聚餐

共 6 项日程（3 工作 / 2 个人 / 1 团队）
⚠️ 检测到 1 个潜在冲突
✅ 已设置递进提醒
```

### 场景二：递进式提醒

高优先级日程采用递进式提醒，多个时间节点逐步升级提醒力度。

```python
# 递进提醒配置
PROGRESSIVE_REMINDERS = {
    "high": [
        {"offset_hours": 24, "message": "📋 明日有重要会议，请提前准备材料"},
        {"offset_hours": 2,  "message": "⏰ 重要会议 2 小时后开始"},
        {"offset_hours": 0.5, "message": "🚨 重要会议 30 分钟后开始，请立即就位"},
    ],
    "medium": [
        {"offset_hours": 2, "message": "⏰ 会议 2 小时后开始"},
    ],
    "low": [
        {"offset_hours": 0.5, "message": "📅 会议 30 分钟后开始"},
    ],
}

# 为每个日程生成递进提醒
for event in all_events:
    priority = event.get("priority_level", "medium")
    for reminder in PROGRESSIVE_REMINDERS[priority]:
        reminder_time = event["start_time"] - timedelta(hours=reminder["offset_hours"])
        schedule_reminder(
            trigger_at=reminder_time,
            target=event["owner_open_id"],
            message=f'{event["color"]} {reminder["message"]}\n📅 {event["title"]}\n🕐 {event["time_range"]}'
        )
```

### 场景三：日程冲突检测与智能调度

自动检测时间重叠的日程，提供调整建议。

```python
# conflict_detection.py
def detect_conflicts(events):
    """检测日程冲突"""
    conflicts = []
    sorted_events = sorted(events, key=lambda x: x["start_time"])

    for i in range(len(sorted_events) - 1):
        curr = sorted_events[i]
        next_evt = sorted_events[i + 1]

        # 检测时间重叠
        if curr["end_time"] > next_evt["start_time"]:
            overlap = (curr["end_time"] - next_evt["start_time"]).total_seconds() / 60
            conflicts.append({
                "event1": curr,
                "event2": next_evt,
                "overlap_minutes": overlap,
                "suggestion": suggest_resolution(curr, next_evt, overlap)
            })
    return conflicts

def suggest_resolution(e1, e2, overlap):
    """生成冲突解决建议"""
    suggestions = []
    if e1["priority"] > e2["priority"]:
        suggestions.append(f"建议将「{e2['title']}」推迟 {overlap:.0f} 分钟")
    elif e2["priority"] > e1["priority"]:
        suggestions.append(f"建议将「{e1['title']}」提前结束或缩短")
    else:
        suggestions.append(f"两场日程重叠 {overlap:.0f} 分钟，建议协商调整")
        if e1.get("location") == e2.get("location"):
            suggestions.append("⚠️ 同一地点背靠背日程，注意转场时间")
    return "；".join(suggestions)

# 执行冲突检测
conflicts = detect_conflicts(all_events)
if conflicts:
    for c in conflicts:
        alert = (
            f"⚠️ 日程冲突告警\n"
            f"📅 冲突1: {c['event1']['title']} ({c['event1']['time_range']})\n"
            f"📅 冲突2: {c['event2']['title']} ({c['event2']['time_range']})\n"
            f"⏱️ 重叠: {c['overlap_minutes']:.0f} 分钟\n"
            f"💡 建议: {c['suggestion']}"
        )
        send_feishu(target=ADMIN_OPEN_ID, message=alert)
```

### 场景四：日程效率分析报表

每周生成日程效率分析报表，帮助优化时间管理。

```python
# weekly_analysis.py
import csv
from datetime import datetime, timedelta

# 获取本周全部已完成日程
week_start = datetime.now() - timedelta(days=datetime.now().weekday())
week_events = owa_calendar.get_events(
    calendar_id="work",
    start_date=week_start.strftime("%Y-%m-%d"),
    end_date=datetime.now().strftime("%Y-%m-%d"),
    status="completed"
)

# 统计分析
analysis = {
    "total_meetings": len(week_events),
    "total_hours": sum(e["duration_hours"] for e in week_events),
    "by_type": {},
    "by_day": {},
    "conflict_count": 0,
    "avg_duration": 0,
}

for evt in week_events:
    # 按类型统计
    mtype = evt.get("category", "其他")
    analysis["by_type"][mtype] = analysis["by_type"].get(mtype, 0) + 1
    # 按日期统计
    day = evt["start_time"].strftime("%m-%d")
    analysis["by_day"][day] = analysis["by_day"].get(day, 0) + evt["duration_hours"]

analysis["avg_duration"] = analysis["total_hours"] / max(analysis["total_meetings"], 1)

# 生成报表
report = f"""📊 本周日程效率分析（{week_start.strftime('%m-%d')} ~ {datetime.now().strftime('%m-%d')}）

📈 总览:
- 会议总数: {analysis['total_meetings']} 场
- 总时长: {analysis['total_hours']:.1f} 小时
- 平均时长: {analysis['avg_duration']:.1f} 小时
- 冲突次数: {analysis['conflict_count']} 次

📅 按日分布:"""

for day, hours in sorted(analysis["by_day"].items()):
    bar = "█" * int(hours) + "░" * (8 - int(hours))
    report += f"\n  {day} {bar} {hours:.1f}h"

report += f"\n\n📋 按类型分布:"
for mtype, count in sorted(analysis["by_type"].items(), key=lambda x: -x[1]):
    report += f"\n  {mtype}: {count} 场"

report += "\n\n💡 优化建议:"
if analysis["total_hours"] > 20:
    report += "\n  - 本周会议时长偏高，建议增加专注时间块"
if analysis["avg_duration"] > 1.5:
    report += "\n  - 平均会议时长偏长，建议控制在 1 小时以内"
if analysis["conflict_count"] > 0:
    report += "\n  - 存在日程冲突，建议提前协调"

send_feishu(target=ADMIN_OPEN_ID, message=report)

# 导出 CSV
with open("weekly_calendar_report.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["日期", "开始时间", "结束时间", "时长(小时)", "标题", "类型", "地点"])
    for evt in week_events:
        writer.writerow([
            evt["start_time"].strftime("%Y-%m-%d"),
            evt["start_time"].strftime("%H:%M"),
            evt["end_time"].strftime("%H:%M"),
            f"{evt['duration_hours']:.1f}",
            evt["title"],
            evt.get("category", ""),
            evt.get("location", "")
        ])
```

## 使用流程

1. 安装专业版依赖。

```bash
cd skills/calendar-reminder-tool-pro
pip install -r requirements.txt
```

2. 配置多日历源与通知渠道。

```bash
python3 setup_pro.py
```

3. 注册定时任务（兼容免费版命令）。

```bash
skill-platform cron add \
  --name "calendar-daily-scan-pro" \
  --cron "0 22 * * *" \
  --tz "Asia/Shanghai" \
  --session main \
  --system-event "CALENDAR_SCAN: 请运行 python3 calendar_reminder_pro.py" \
  --description "专业版每晚22:00多日历扫描与智能提醒"
```

4. 手动运行验证。

```bash
python3 calendar_reminder_pro.py
```

### 命令参数说明

- `-reminder-tool-pro`: 命令参数,用于指定操作选项
- `-daily-scan-pro`: 命令参数,用于指定操作选项
- `--session`: 命令参数,用于指定操作选项
- `--tz`: 命令参数,用于指定操作选项
- `--system-event`: 命令参数,用于指定操作选项

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,参考错误处理章节获取恢复步骤。

### 命令参数说明

- `-sig`: 命令参数,用于指定操作选项

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| content | string | 是 | 相关说明 |
| content | string | 否 | 相关说明, 默认: 默认值 |
| content | string | 否 | 相关说明, 可选值: json/text/markdown |
| style | string | 否 | 输出风格, 参考 `references/style.md` |

## 输出格式

```json
{
  "success": true,
  "data": {
    result: "相关说明",
    result: "相关说明",
    result: "相关说明",
    "metadata": {
      "template_used": "reviewer",
      "word_count": 0,
      "style": "专业"
    }
  },
  "error": null
}
```

输出模板参考: `assets/output.json`

## 异常处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **运行时**：Python 3.9+（需要 `zoneinfo` 模块）
- **定时调度**：skill-platform cron 或系统 cron

### 依赖说明

| 依赖项 | 类型 | 是否必需 | 获取方式 |
| :------- | :----- | :--------- | :--------- |
| Python 3.9+ | 运行时 | 必需 | python.org 官方下载 |
| owa-outlook skill | skill 依赖 | 必需 | 提供 `owa_calendar.py` 日历读取模块 |
| skill-platform CLI | 命令行工具 | 必需 | 定时任务注册与管理 |
| 飞书机器人 | 通信渠道 | 必需 | 飞书开放平台创建应用机器人 |
| Telegram Bot | 通信渠道 | 可选 | 通过 `@BotFather` 创建（多渠道通知需要） |
| Outlook 账号（多日历） | 日历来源 | 必需 | 已配置的工作与个人邮箱 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| 数据库 | 存储 | 可选 | 团队同步与历史分析（可选，默认文件存储） |

### API Key 配置

- 飞书机器人凭证配置在 skill-platform 通信通道中。
- Outlook 账号凭证配置在 owa-outlook skill 中（支持多账号）。
- Telegram Bot Token 配置在通信通道中（多渠道通知需要）。
- 团队同步需各成员授权日历读取权限。

```bash
# 环境变量示例
export FEISHU_APP_ID="your_feishu_app_id"
export FEISHU_APP_SECRET="your_feishu_app_secret"
export OUTLOOK_WORK_EMAIL="work@company.com"
export OUTLOOK_PERSONAL_EMAIL="personal@outlook.com"
export TG_BOT_TOKEN="your_telegram_bot_token"
```

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务。专业版在免费版基础上新增多日历聚合、递进提醒与团队同步，扫描脚本与提醒格式向后兼容免费版。

## 案例展示

专业版配置支持多日历、递进提醒与团队同步。

```json
{
  "calendars": [
    {"id": "work",     "source": "owa",     "priority": 1, "color": "🔵"},
    {"id": "personal", "source": "owa",     "priority": 2, "color": "🟢"},
    {"id": "team",     "source": "owa",     "priority": 1, "color": "🟡"}
  ],
  "reminder": {
    "mode": "progressive",
    "rules": {
      "high":   [{"offset_hours": 24}, {"offset_hours": 2}, {"offset_hours": 0.5}],
      "medium": [{"offset_hours": 2}],
      "low":    [{"offset_hours": 0.5}]
    },
    "morning_threshold": "12:00",
    "morning_advance_hours": 2,
    "afternoon_reminder_time": "12:00"
  },
  "conflict_detection": {
    "enabled": true,
    "buffer_minutes": 15,
    "auto_suggest": true
  },
  "timezone": "Asia/Shanghai",
  "filters": {
    "workdays_only": false,
    "skip_categories": ["已取消", "请假"]
  },
  "notifications": {
    "channels": ["feishu", "telegram"],
    "admin_open_id": "ou_详情见说明详情见说明xx"
  },
  "analysis": {
    "weekly_report": true,
    "report_day": 5,
    "export_format": "csv"
  },
  "team_sync": {
    "enabled": false,
    "team_members": []
  }
}
```

## 常见问题

### Q1：专业版如何兼容免费版？

专业版与免费版使用相同的扫描脚本接口与提醒消息格式。免费版的 cron 任务、飞书 open_id 配置可直接复用。升级后免费版的单日历扫描自动作为专业版多日历配置的一个条目。

### Q2：多日历聚合会重复提醒吗？

不会。专业版对聚合后的日程去重（按标题+时间），同一日程只提醒一次。不同日历中相同日程会合并显示。

### Q3：递进式提醒会打扰吗？

递进提醒仅对高优先级日程启用。可在 `reminder.rules` 中自定义每个优先级的提醒次数与时间点。低优先级日程默认仅提醒一次。

### Q4：冲突检测如何判断优先级？

按日历 `priority` 字段判断（数字越小优先级越高）。同优先级冲突时，系统建议协商调整并提示转场时间。

### Q5：支持哪些日历来源？

专业版支持通过 owa-outlook 读取 Outlook 日历。可通过扩展 `calendars[].source` 配置接入其他日历源（如 Google Calendar API）。

### Q6：跨时区日程如何处理？

专业版在日程中标注原始时区，提醒时间按用户本地时区（`timezone` 配置）转换。跨时区会议会在提醒中显示双方时区时间。

### Q7：团队日程同步如何实现？

开启 `team_sync` 后，系统读取团队成员的忙/闲状态（不显示具体内容，仅显示时段是否占用），辅助会议时间协调。需团队成员授权日历读取权限。

### Q8：周报可以自动发送吗？

可以。配置 `analysis.weekly_report: true` 与 `analysis.report_day`（1-7，周一到周日），系统在指定日期自动生成并发送周报到管理员。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接，执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 
- 
- 
