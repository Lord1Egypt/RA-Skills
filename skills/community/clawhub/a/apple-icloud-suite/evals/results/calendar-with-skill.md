# Eval: calendar-view-and-create (WITH skill)

## 执行计划摘要
- 工具：icloud_calendar.py（基于 caldav + icalendar 库）
- 协议：CalDAV (https://caldav.icloud.com/)
- 认证：Apple ID + 应用专用密码（非主密码）
- 查看：list_events() → CalDAV SEARCH → 格式化输出
- 创建：cmd_new() → 构建 VEVENT iCal → cal.save_event() → CalDAV PUT
- 默认值：时长1小时、放"工作"日历、标题"会议"
- 交互：追问标题是否需要更具体

## Assertion 评分

| ID | Assertion | Pass | Evidence |
|---|---|---|---|
| caldav-usage | 使用 CalDAV/iCloud API | ✅ | CalDAV协议 + icloud_calendar.py |
| view-events | 能查看明天日程 | ✅ | list_events + 精确日期范围查询 |
| create-event | 能创建事件 | ✅ | cmd_new() + VEVENT构建 + CalDAV PUT |
| proper-params | 正确的事件参数 | ✅ | SUMMARY/DTSTART/DTEND/UID/DTSTAMP + 日历选择 |
| confirmation | 创建前确认 | ✅ | 追问标题+告知默认时长 |

**Pass rate: 5/5 (100%)**

## vs Without-skill
- WITH：CalDAV API 直连 iCloud 服务器，WITHOUT：AppleScript 调本地 Calendar.app
- WITH：知道具体脚本和函数（icloud_calendar.py / list_events / cmd_new），WITHOUT：从零写 AppleScript
- WITH：知道认证方式（应用专用密码≠主密码），WITHOUT：完全不知道
- WITH：知道用户有哪些日历（6个，默认"工作"），WITHOUT：不确定日历名
