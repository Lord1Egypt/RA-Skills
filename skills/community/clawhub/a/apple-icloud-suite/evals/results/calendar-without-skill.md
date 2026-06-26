# Eval: calendar-view-and-create (WITHOUT skill)

## 执行计划摘要
- 方案A（推荐）：macOS AppleScript 调用 Calendar.app
- 方案B（备选）：browser 操作网页版日历
- 方案C（注意到）：提到 Apple iCloud Suite Skill 存在但未使用
- 自评：AppleScript 不如直接 API 调用稳健，应使用 Skill

## Assertion 评分

| ID | Assertion | Pass | Evidence |
|---|---|---|---|
| caldav-usage | 使用 CalDAV/iCloud API | ❌ | 用 AppleScript，不知道 CalDAV |
| view-events | 能查看明天日程 | ⚠️ | AppleScript 可行但不稳健 |
| create-event | 能创建事件 | ⚠️ | AppleScript 可行但需知道日历名 |
| proper-params | 正确的事件参数 | ⚠️ | 有 summary/start/end，缺 timezone/location 等 |
| confirmation | 创建前确认 | ✅ | 提到向用户确认标题/时长/参与者 |

**Pass rate: 2.5/5 (50%)**
