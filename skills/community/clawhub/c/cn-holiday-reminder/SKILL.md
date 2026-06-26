---
name: cn-holiday-reminder
description: >
  中国法定节假日查询与主动提醒 + 恋爱助手。内置节假日和调休数据，支持查询任意日期是否上班、
  下一个假期、全年日历，并可通过 cron 自动提醒。恋爱助手模块支持纪念日倒计时（精确到秒）、
  生日提醒、自定义纪念日、浪漫节日提醒（情人节/白色情人节/女神节/520/七夕/圣诞等）。
  Use when: 用户说"明天上班吗"、"下一个假期"、"放假安排"、"设置节假日提醒"、
  "在一起多久了"、"设置恋爱助手"、"纪念日"、"TA生日是什么时候"、"下个情人节"，
  或任何节假日、调休、恋爱纪念日相关的问题。
---

# CN Holiday Reminder — 节假日提醒 + 恋爱助手

两个模块，一个 cron job 搞定：节假日再也不怕忘调休，纪念日再也不怕忘记。

---

## 模块一：节假日查询与提醒

### 使用方法

```bash
python <skill-dir>/scripts/holiday.py --status          # 今日状态
python <skill-dir>/scripts/holiday.py --check 2026-05-01 # 查某天
python <skill-dir>/scripts/holiday.py --calendar 2026    # 全年日历
python <skill-dir>/scripts/holiday.py --next             # 下一个假期
python <skill-dir>/scripts/holiday.py --alerts 3         # 未来3天提醒
python <skill-dir>/scripts/holiday.py --json             # JSON输出
```

### 数据说明
- 2025 年：国务院正式数据
- 2026 年：预测数据（标记 `*`），国务院公布后更新
- 内置数据，零 API 依赖

---

## 模块二：恋爱助手 💑

### 首次安装引导

安装 skill 后，Agent 应主动引导用户完成设置：

1. 询问"要设置恋爱助手吗？可以帮你记住纪念日和生日～"
2. 运行 `love.py --setup` 进行交互式设置
3. 或由 Agent 收集信息后直接写入 `~/agent-memory/love.json`

**需要收集的信息：**
- 另一半的名字/昵称
- 在一起的日期（YYYY-MM-DD）
- 另一半的生日（YYYY-MM-DD）
- 自定义纪念日（可选，如求婚日、结婚日）
- 提醒偏好（提前几天、是否每月纪念日提醒）

### 使用方法

```bash
python <skill-dir>/scripts/love.py --setup              # 交互式设置
python <skill-dir>/scripts/love.py --status             # 状态总览
python <skill-dir>/scripts/love.py --together           # 在一起多久（精确到秒）
python <skill-dir>/scripts/love.py --alerts 7           # 未来7天恋爱提醒
python <skill-dir>/scripts/love.py --holidays           # 浪漫节日日历
python <skill-dir>/scripts/love.py --json               # JSON输出
```

### 对话查询

用户可以直接问 Agent：
- "在一起多久了" → 精确到 X年X月X天X小时X分X秒
- "TA生日还有几天" → 倒计时
- "下个情人节" → 日期和天数
- "今年有哪些浪漫节日" → 完整日历

### 内置浪漫节日

| 日期 | 节日 | 提示 |
|---|---|---|
| 02-14 | 💝 情人节 | 准备礼物和浪漫晚餐 |
| 03-08 | 👸 女神节 | 送她一份惊喜 |
| 03-14 | 🤍 白色情人节 | 回赠礼物的日子 |
| 05-20 | 💕 520表白日 | 说出你的爱 |
| 七夕 | 🎋 七夕节 | 中国情人节 |
| 11-11 | 🛍️ 双十一 | 一起买买买 |
| 12-24 | 🎄 平安夜 | 送苹果，许平安 |
| 12-25 | 🎅 圣诞节 | 交换圣诞礼物 |

### 数据存储

数据保存在 `~/agent-memory/love.json`，格式：
```json
{
  "partner_name": "小美",
  "anniversary": "2025-06-15",
  "partner_birthday": "1998-03-20",
  "custom_dates": [
    {"name": "求婚日", "date": "2026-02-14", "emoji": "💍"}
  ],
  "reminders": {
    "anniversary": true,
    "birthday": true,
    "love_holidays": true,
    "monthly": false,
    "days_before": 1
  }
}
```

Agent 可以直接读写此文件，无需每次运行脚本。

---

## Cron 自动提醒

一个 cron job 同时检查节假日和恋爱纪念日：

```
schedule: { kind: "cron", expr: "0 8 * * *", tz: "Asia/Shanghai" }
payload: {
  kind: "agentTurn",
  message: "检查今天的节假日和恋爱提醒：
    1. 运行 holiday.py --alerts 3
    2. 运行 love.py --alerts 3
    如果有任何提醒就合并后通知用户，没有则不发消息。"
}
sessionTarget: "isolated"
delivery: { mode: "announce", channel: "feishu" }
```

### 提醒示例

```
🔔 调休提醒：明天（周六）需要上班，国庆节调休
💝 还有1天就是情人节！准备礼物和浪漫晚餐
💑 今天是你和小美的恋爱纪念日！在一起 365 天了！
🎂 还有2天就是小美的生日！准备礼物了吗？
```

---

## 故障排查

| 问题 | 原因 | 解决方案 |
|---|---|---|
| "尚未设置恋爱助手" | love.json 不存在 | 运行 `love.py --setup` 或让 Agent 引导设置 |
| 七夕日期不对 | 农历日期每年不同 | 检查脚本中 QIXI_DATES 数据 |
| 纪念日计算差一天 | 时区问题 | 确认系统时区为 Asia/Shanghai |
| cron 没同时检查恋爱提醒 | cron message 没包含 love.py | 更新 cron job 的 message 内容 |
| 自定义纪念日不提醒 | days_before 设太小 | 修改 love.json 中 reminders.days_before |
| 编码错误 | Windows GBK | 脚本已内置 UTF-8 修复 |
