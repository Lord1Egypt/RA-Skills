---
name: china-work-calendar
description: 中国法定节假日与工作日计算器。查某年某月工作天数、某日期是否上班、距离节假日倒计时、调休换休提示。支持2024-2027年全部法定节假日及已知调休日。When the user asks about Chinese holidays, workdays, overtime, holiday countdown, or vacation planning in China.
---

# 中国工作日历计算器

**Author: Lin Hui** | Version 1.0.0 | MIT License

快速、准确地计算中国法定节假日、调休工作日和节假日倒计时。

## 核心功能

- ✅ 查任意日期是否为工作日
- ✅ 计算两个日期之间的工作日数
- ✅ 查某年某月的工作日总数
- ✅ 节假日倒计时（距离某节假日还剩几天）
- ✅ 调休提示（哪个周末要上班）
- ✅ 支持 2024–2027 年全部法定节假日

## 触发词（Trigger Words）

> "今天上班吗" / "这周还剩几个工作日" / "清明节放几天" / "距离春节还有多少天" / "元旦加班怎么算" / "这月有多少个工作日" / "国庆节调休哪几天要上班" / "下周一是工作日吗" / "本月工作日" / "今年所有假期"

## 使用示例

### 查询某日是否为工作日

**输入：**
```
2026-04-27
```

**输出示例：**
```json
{
  "date": "2026-04-27",
  "weekday": "周一",
  "is_workday": true,
  "label": "工作日"
}
```

### 计算工作日数

**输入：** `2026-04-01` 到 `2026-04-30`

**输出示例：**
```json
{
  "start": "2026-04-01",
  "end": "2026-04-30",
  "workdays_count": 22,
  "holidays_this_month": ["清明节 4月3日-5日"]
}
```

### 节假日倒计时

**输入：** `2026-06-20`（端午节）

**输出示例：**
```json
{
  "target": "2026-06-20",
  "days_remaining": 54,
  "is_workday": false,
  "label": "休息日/节假日"
}
```

### 本月工作日总数

**输入：** `2026-04`

**输出示例：**
```json
{
  "year": 2026,
  "month": 4,
  "workdays_count": 22,
  "workdays": ["2026-04-01","2026-04-02","2026-04-03",...]
}
```

### 调休提示（国庆/春节等长假的调休日）

```
2026年国庆节：10月1日-7日放假
⚠️ 调休上班日：9月26日（周六）、10月3日（周六）、10月10日（周六）
```

## 技术实现

调用 `python3` 脚本，零外部依赖：

```bash
python3 scripts/china_work_calendar.py workdays <start> <end>
python3 scripts/china_work_calendar.py is-workday <yyyy-mm-dd>
python3 scripts/china_work_calendar.py holidays <year>
python3 scripts/china_work_calendar.py countdown <yyyy-mm-dd>
python3 scripts/china_work_calendar.py next-workday <yyyy-mm-dd>
```

## 支持的节假日（2024-2027）

| 节日 | 日期 | 天数 |
|------|------|------|
| 元旦 | 1月1日 | 1天 |
| 春节 | 农历正月初一 | 7天 |
| 清明节 | 4月4/5日 | 3天 |
| 劳动节 | 5月1日 | 3-5天 |
| 端午节 | 农历五月初五 | 3天 |
| 中秋节 | 农历八月十五 | 3天 |
| 国庆节 | 10月1日 | 7天 |

## 常见场景

| 场景 | 查询方式 |
|------|---------|
| 今天上班吗 | `is-workday 今天日期` |
| 报销/加班核算 | `workdays 出勤日期区间` |
| 请假多少天 | `workdays 请假首日 请假末日` |
| 出行计划 | `countdown 节假日日期` |
| 本月还剩几天班 | `workdays 今天 本月末` |

## 注意事项

- 脚本内置 2024-2027 年调休数据，由国务院每年公布的调休通知驱动
- 如需查询更远年份，请更新脚本中的 `HOLIDAYS` 和 `ADJUSTED_WORKDAYS` 数据
- 数据来源：中国人民政府网《国务院办公厅关于XXXX年节假日安排的通知》

## 更新日志

### v1.0.0 (2026-04)
- 首发版本
- 支持 2024-2027 年节假日计算
- 支持调休/换休自动识别
- 支持节假日倒计时
- 支持月工作日统计

## ⚠️ Disclaimer

This tool is provided "as is" for informational purposes only. Data accuracy is not guaranteed. Not financial, legal, or professional advice. Always verify critical information from official sources.

本工具仅供信息参考，不保证数据完全准确，不构成任何金融/法律/专业建议。请以官方来源为准。
