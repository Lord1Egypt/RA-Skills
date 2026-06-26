# fitness-coach-lite

A Telegram-native personal workout tracker — low-friction input, status tracking, dynamic training suggestions, and daily/weekly/monthly reports.

---

## 安装 | Installation

**从 GitHub 安装：**
```prompt
安装 fitness-coach-lite skill：https://github.com/youhan2021/fitness-coach-lite
```

**从 ClawHub 安装（clawhub.gg）：**
```prompt
从 ClawHub 安装 fitness-coach-lite
```

---

**首次使用 — 初始化训练计划：**
```prompt
导入训练计划：
周一：坐姿划船, 高位下拉, Face pull
周二：飞鸟, Chest press
周三：悬挂肩胛, 坐姿划船（轻）, 卷腹
周四：臀桥, Leg press, 腿弯举
周五：臀桥, 悬挂肩胛, 高位下拉（轻）
周六：坐姿划船, 高位下拉, Chest press
周日：臀桥, Leg press, 腿外展, 卷腹
```

---

## 功能 | Features

- 🏋️ **训练记录** — 自然语言或结构化输入，无需轮询确认
- 😫 **状态追踪** — 累/出差/经期/恢复模式等上下文记录
- 📋 **动态训练建议** — 根据状态自动调整方案
- 📊 **报告生成** — 日报 / 周报 / 月报 / 阶段总结
- ⚖️ **身体数据** — 体重/体脂追踪（独立于训练记录）

---

## 目录结构 | File Structure

```
fitness-coach-lite/
├── SKILL.md              # Skill definition for OpenClaw
├── README.md             # This file
├── scripts/
│   └── workout.py        # Core CLI script
└── data/
    ├── plan.example.json # 示例计划
    ├── plan.json         # 当前训练计划
    ├── history.json       # 统一历史（训练+状态+快照）
    ├── body_status.json   # 身体状态（已忽略）
    └── .current_workout.json  # 训练中途进度（临时）
```

---

## 使用方法（prompt 指令）| Usage

```prompt
# 训练记录
今天跑了40分钟
深蹲60kg 5x5，卧推30kg 5x5
晚上练了腿
走了8000步
今天拉伸了15分钟

# 状态记录
今天很累
昨晚没睡好
出差几天
经期中
恢复模式
膝盖有点不舒服
这周只能练两次

# 查询和报告
今天练了什么
这周练了几次
给我日报
给我周报
给我月报
给我阶段总结

# 计划管理
更新训练计划 <JSON或文字>
运动计划查看
记录方案变更 <原因>

# 身体数据
更新身体数据 体重=70 体脂=18
记录身体数据 体重=69.5
查看身体数据
身体数据历史
```

---

## Quick Actions（适合 Telegram Inline Keyboard）

```
[🏋️ 练什么] [📝 记录训练] [📊 查看报告]
[😫 状态记录] [⚖️ 体重记录] [📋 训练计划]
```

---

## 数据格式 | Data Format

### history.json（新版统一格式）

```json
{
  "records": [
    {
      "date": "2026-04-20",
      "type": "workout",
      "workout": {
        "summary": "练了背",
        "exercises": [
          {"name": "坐姿划船", "weight_kg": 25, "sets": [{"reps": 8}, {"reps": 8}]}
        ],
        "duration_min": 40,
        "note": ""
      }
    },
    {
      "date": "2026-04-20",
      "type": "status",
      "status": "tired",
      "detail": "昨晚没睡好"
    }
  ],
  "plan_versions": [
    {"date": "2026-04-20", "reason": "出差降频"}
  ],
  "snapshots": []
}
```

---

## 状态类型 | Status Types

| 用户词 | 存储值 |
|--------|--------|
| 累、很累 | `tired` |
| 没睡好、睡眠差 | `poor_sleep` |
| 出差 | `travel` |
| 经期、生理期 | `period` |
| 不想练X、讨厌练X | `avoiding:{部位}` |
| 这周只能练X次 | `frequency_limit:{N}` |
| 恢复、休息一下 | `recovery` |
| 膝盖不舒服、肩膀疼 | `injury:{部位}` |
| 状态不错 | `good` |
| 正常 | `normal` |

---

## 报告模板 | Report Templates

### 日报
```
📅 2026-04-20 日报
━━━━━━━━━━━━━━━
🏋️ 训练：坐姿划船 25kg×3组 / 高位下拉 25kg×3组
⏱️ 约 35 分钟
😫 状态：累（昨晚没睡好）
━━━━━━━━━━━━━━━
```

### 周报
```
📅 周报（4/14 - 4/20）
━━━━━━━━━━━━━━━
🏋️ 训练次数：4次
😫 状态：累×2 / 正常×3 / 出差×1
📉 执行率：4/5 计划日（80%）
⚠️ 问题：周二因出差未训练
━━━━━━━━━━━━━━━
```

---

## 在 OpenClaw 中使用 | Using in OpenClaw

| 命令 | 说明 |
|------|------|
| `运动计划 <文字>` | 文字 → 自动生成 JSON 计划 |
| `运动计划 <json>` | 直接导入 JSON |
| `运动计划查看` | 查看当前计划 |
| `开始运动` | 开始今日训练（交互式） |
| `跳过此动作` | 跳过当前动作 |
| `运动历史 [天数]` | 输出一张表格显示训练记录 |
| `添加记录 <日期> <动作>` | 手动添加训练记录 |
| `重置今日` | 清除今天训练记录 |
| `更新身体数据 <字段>` | 更新身高/体重/体脂等基本信息 |
| `记录身体数据 [体重] [体脂]` | 记录当天体重体脂到历史 |
| `查看身体数据` | 查看当前身体状态 |
| `身体数据历史 [天数]` | 查看体重体脂变化历史 |
| `记录状态 <状态>` | 记录今天的身体/训练状态 |
| `日报` / `周报` / `月报` / `阶段总结` | 输出对应报告 |

---

## License

MIT
