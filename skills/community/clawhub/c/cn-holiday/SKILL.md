---
name: cn-holiday
version: 1.0.0
description: >
  中国节假日/调休查询 — 查某天是工作日还是休息日、是否调休补班、全年假期安排。
  触发词: 节假日, 调休, 补班, 放假, 上班, holiday, workday,
  今天上班吗, 明天放假吗, 春节放几天, 国庆放假, 下个工作日,
  或任何 "[日期] 是否放假/上班" 格式的输入。
---

# cn-holiday — Chinese Holiday & Work Schedule Skill

Query Chinese public holidays, 调休 (make-up workdays), and work schedules via the timor.tech API.

## Quick Start
1. No API key needed.
2. Run `bun scripts/holiday.ts --help` in this skill directory.
3. Pick the matching command from `references/command-map.md`.

## Workflow
1. Parse user intent — identify the date(s) and what they want to know.
2. Select the right command: `info`, `year`, `batch`, or `next`.
3. Run the script and return the result.
4. Interpret the result for the user in natural language.

## Response Interpretation

### `type.type` field meanings
| Value | Meaning |
|---|---|
| 0 | 工作日 (workday) |
| 1 | 周末 (weekend) |
| 2 | 节日 (holiday) |
| 3 | 调休补班 (make-up workday) |

### `wage` field meanings (加班工资倍率)
| Value | Meaning |
|---|---|
| 1 | 正常工资 |
| 2 | 双倍工资 |
| 3 | 三倍工资 |

### `holiday.holiday` field
- `true` = 放假 (day off)
- `false` = 补班 (make-up workday)

## Notes
- This skill is script-first and does not run an MCP server.
- Data source: timor.tech (based on State Council holiday announcements).
- No API key required.
- Covers current year and adjacent years' holiday schedules.
