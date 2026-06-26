# 数据格式

默认数据文件是一个 JSON 文件，顶层结构如下：

```json
{
  "records": [
    {
      "name": "张三",
      "calendar": "lunar",
      "month": 11,
      "day": 6,
      "year": 1949,
      "leap_month": false,
      "remind_before_days": 1,
      "source": "idcard",
      "idcard_masked": "110105********002X",
      "solar_birthday": "1949-12-31",
      "created_at": "2026-03-13T10:00:00"
    }
  ]
}
```

默认通知配置文件建议放在：

```json
{
  "channels": [
    { "type": "agent" },
    {
      "type": "email",
      "enabled": false,
      "host": "${BIRTHDAY_SMTP_HOST}",
      "port": "${BIRTHDAY_SMTP_PORT}",
      "username": "${BIRTHDAY_SMTP_USERNAME}",
      "password": "${BIRTHDAY_SMTP_PASSWORD}",
      "from": "${BIRTHDAY_EMAIL_FROM}",
      "to": ["${BIRTHDAY_EMAIL_TO}"],
      "use_tls": true,
      "subject": "生日提醒"
    }
  ]
}
```

这些 `${...}` 占位值会在运行时自动读取同名环境变量。

## 字段说明

| 字段 | 含义 |
| --- | --- |
| `name` | 人名，作为主要展示字段 |
| `calendar` | `lunar` 或 `solar` |
| `month` | 生日月份 |
| `day` | 生日日期 |
| `year` | 出生年份，可选，但建议保留以便计算年龄 |
| `leap_month` | 农历闰月标记，公历记录固定为 `false` |
| `remind_before_days` | 提前几天提醒，默认 `1` |
| `source` | `manual` 或 `idcard` |
| `idcard_masked` | 脱敏后的身份证号码，仅用于回显和排查 |
| `solar_birthday` | 原始公历生日，身份证导入时建议保留 |
| `created_at` | ISO 时间戳 |

通知配置中的 `channels[].type` 当前支持：

- `agent`：把提醒信息直接输出给当前 agent
- `email`：发送邮件；Python 版本走 SMTP，JS 版本优先尝试本机 `sendmail`
- `stdout`：标准输出
- `webhook`：按配置发送到指定地址；如果执行环境限制网络，调用方应处理失败结果

## 约束

1. `calendar=solar` 时，`leap_month` 必须为 `false`
2. `calendar=lunar` 时，提醒日需要先换算为当年的公历日期
3. `remind_before_days` 必须是大于等于 `0` 的整数
4. 同名记录默认视为覆盖更新，由调用方决定是否先读取确认

## 输出原则

列出记录或提醒时，至少输出：

- 姓名
- 存储生日
- 存储口径（农历或公历）
- 下一次实际提醒对应的公历日期
- 距离提醒日还有几天
- 若有出生年份，则输出即将到来的年龄
