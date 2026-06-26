---
name: daily-calorie-balance
description: 每天自动合并 Calorie Visualizer 食物摄入与 clawhealth-garmin 消耗数据，计算净余/赤字，并在北京时间每天晚上 21:30 主动发送总结。支持手动查询。
author: Grok-assisted
version: 1.2.0
user-invocable: true
dependencies:
  - calorie-visualizer
  - clawhealth-garmin
---

# Daily Calorie Balance 每日卡路里平衡总结（自动版）

## 技能目标

- **自动模式**：每天北京时间 21:30 主动生成并发送今日总结（通过 cron 调用）。
- **手动模式**：用户输入"今天卡路里平衡""今日摄入消耗""daily balance""净卡路里"等时立即执行。

## 执行流程（严格遵守）

1. **确定日期**：默认今天（使用系统当前日期，北京时间）。支持用户指定"昨天"等。
2. **读取食物摄入**：从 Calorie Visualizer 的记录（文件或数据库）获取今日总摄入 kcal。如果无记录，明确说明。
3. **读取 Garmin 消耗**：通过 clawhealth-garmin 查询今日 **总卡路里消耗** 和 **活动卡路里**（优先用活动卡路里）。
4. **计算**：净卡路里 = 摄入 - 消耗
   - 正数：盈余（轻微/明显）
   - 负数：赤字（适合减脂）
   - 接近 0：平衡
5. **生成总结** 并**主动发送**到你的聊天渠道（Telegram/WhatsApp 等）。

## 输出格式（必须严格使用，清晰友好）

输出的效果如下：

```
📊 今日卡路里平衡总结（{YYYY-MM-DD} 北京时间）

🍽️ 食物摄入：{XXX} kcal
（主要餐食：简要列出，如果有）

🔥 Garmin 消耗：{YYY} kcal
（活动消耗约 {ZZZ} kcal | 总消耗 {Total} kcal）

⚖️ 净卡路里：{+XXX 或 -XXX} kcal
（{盈余/赤字/平衡}）

💡 今日建议：
• [1-2 条简短实用建议，例如"赤字良好，继续保持"或"盈余较多，明天可增加步数"]
• 整体状态：{积极/需注意/优秀}
```

## 触发与调度

### 手动触发

直接聊天说相关关键词：
- "今天卡路里平衡"
- "今日摄入消耗"
- "daily balance"
- "净卡路里"
- "卡路里总结"

### 自动调度

通过 OpenClaw Cron 每天北京时间 21:30 执行：

```bash
openclaw cron add \
  --name "每日卡路里平衡总结 -21:30" \
  --cron "30 21 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "run daily-calorie-balance today --auto" \
  --announce \
  --channel qqbot \
  --to "D5EF2AE19BFAF72D2CE64E860CE46F95" \
  --enabled true
```

## 使用方法

```bash
# 手动查询今天
python3 scripts/daily_balance.py today

# 手动查询昨天
python3 scripts/daily_balance.py yesterday

# 指定日期
python3 scripts/daily_balance.py 2026-03-29

# 自动模式（用于 cron）
python3 scripts/daily_balance.py today --auto
```

## 依赖

### 必需技能（自动检测）

本技能依赖以下两个技能，安装时会自动检测：

- **calorie-visualizer** - 用于记录食物摄入数据
- **clawhealth-garmin** - 用于获取 Garmin 运动消耗数据

### 安装依赖

如果缺少依赖技能，脚本会提示你安装：

```bash
# 安装所有依赖
clawhub install calorie-visualizer
clawhub install clawhealth-garmin

# 或者一键安装本技能及其依赖
clawhub install daily-calorie-balance
# 然后手动安装依赖（clawhub 暂不支持自动安装依赖）
```

### 系统依赖

- Python 3.8+
- sqlite3 (Python 内置)

## 数据存储

- 食物摄入数据：`/home/admin/.openclaw/workspace/skills/calorie-visualizer/data/calorie_data.db`
- Garmin 消耗数据：`/home/admin/.openclaw/workspace/skills/clawhealth-garmin/data/health.db`
