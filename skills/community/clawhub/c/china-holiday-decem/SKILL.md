---
name: china-holiday
description: 中国法定节假日查询，基于 timor.tech 免费 API。支持查询指定日期节假日信息、批量查询、下一节假日、下一工作日、全年节假日列表，以及语音播报。触发场景：问"今天上班吗"、"明天放假吗"、"2026年有哪些节假日"、"清明节放几天"、"调休怎么调"等节假日相关问题。依赖：Python 3，仅使用标准库（urllib, json, datetime）。
---

# 中国节假日查询

调用 [timor.tech 免费节假日 API](https://timor.tech/api/holiday)，数据覆盖 2013 年至今，支持节假日、调休、补班查询。

## 依赖

- **Python 3**（仅标准库，无第三方依赖）
- 网络访问权限（调用 timor.tech API）

## 脚本

```
python3 skills/china-holiday/scripts/china_holiday.py <命令> [参数]
```

## 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `info [日期]` | 查询指定日期节假日 | `info 2026-10-01` / `info`（今天） |
| `batch <日期...>` | 批量查询 | `batch 2026-05-01 2026-06-01` |
| `next [日期]` | 下一节假日（含调休） | `next 2026-04-01` |
| `workday [日期]` | 下一工作日 | `workday` |
| `year [年份/月份]` | 全年/全月节假日 | `year 2026` / `year 2026-02` |
| `tts` | 今日节假日播报 | - |
| `tts-next` | 下一节假日播报 | - |
| `tts-tomorrow` | 明日节假日播报 | - |

## 响应字段说明

**日期类型 (type)**：
- `0` = 工作日
- `1` = 周末
- `2` = 节日
- `3` = 调休/补班

**holiday 字段**（非节假日为 `null`）：
- `holiday: true/false` — true=节日，false=调休
- `wage` — 薪资倍数（2=双薪，3=三薪）
- `after: true/false` — 假后/假前补班
- `target` — 调休对应的节日名

## 注意事项

- API 每日限额 10000 次/IP，免费足够个人使用
- 返回日期格式：`YYYY-MM-DD`
- 全年查询整年需加斜杠：`year 2026` → 请求 `/year/2026/`

## 致谢

节假日数据来源于 **提莫的神秘小站**（[timor.tech](https://timor.tech)），由独立开发者利用业余时间维护，每年更新节假日数据，服务稳定且完全免费。深深感谢作者的无私奉献 🌿
