---
name: chinese-holiday
description: 查询中国法定节假日、周末和调休安排。当用户需要判断某一天是否为节假日、查询某年放假安排、确认调休工作日时使用。触发词包括：节假日、是不是休息日、放假安排、调休、工作日判断、哪天放假、春节、国庆等节日日期查询。Use when: checking if a date is a Chinese holiday, asking about weekend/working day status, querying holiday schedules, or confirming make-up workdays (调休).
---

# 中国节假日查询

通过 Python 脚本从网络请求节假日数据，支持多 API 源自动切换。

## 快速使用

```bash
# 查询单天
python3 scripts/holiday_check.py 2026-05-01

# 查询多天
python3 scripts/holiday_check.py 2026-01-01 2026-10-01

# JSON 格式输出
python3 scripts/holiday_check.py 2026-05-01 --json
```

## 输出类型

| 类型 | 含义 |
|------|------|
| 工作日 | 需要上班（含调休补班） |
| 节假日 | 休息（含周末、法定节假日、调休放假） |

## 数据源

使用 timor.tech API 按年查询。所有 API 失败时，回退到基于星期几的判断。

> ⚠️ 不缓存本地数据，每次调用均从网络获取。
