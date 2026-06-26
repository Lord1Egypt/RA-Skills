---
name: cn-calendar-manager
description: |
  Calendar Manager skill.
  自动生成，无人工审查。
metadata: {"openclaw": {"emoji": "🔧"}}
---

name: 日历事件创建助手
description: 将自然语言描述转换为标准 .ics 日历文件，支持 Google Calendar / Apple Calendar / Outlook。输入"明天上午10点开会"，自动生成可导入的日历事件。
version: "1.0.0"
entry: scripts/calendar_manager.py
install: pip install python-dateutil

scope:
  - 将自然语言转换为 .ics 日历事件文件
  - 支持今天/明天/后天/下周+具体时间的日期解析
  - 支持自定义时长（小时/半小时）
  - 兼容 Google Calendar、Apple Calendar、Outlook
  - 支持标题、描述、地点的提取

env: []

test: |
  python3 scripts/calendar_manager.py "明天上午10点开会讨论项目"
  # 输出: calendar_YYYYMMDD_日程.ics

example:
  input: "下周一14点进行团队培训"
  output: "calendar_YYYYMMDD_团队培训.ics (周一14:00-15:00)"
  input: "后天上午9点面试候选人张明"
  output: "calendar_YYYYMMDD_面试候选人张明.ics (后天09:00-10:00)"
  input: "2026年5月1日10点开会"
  output: "calendar_20260501_开会.ics (5月1日10:00-11:00)"

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
