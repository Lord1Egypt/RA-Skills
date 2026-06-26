# Daily Calorie Balance 每日卡路里平衡总结

## 📋 功能说明

这个技能会自动合并你的食物摄入数据（Calorie Visualizer）和运动消耗数据（Garmin），计算每日卡路里平衡，并给出健康建议。

## ⚠️ 依赖技能（必需）

本技能依赖以下两个技能，**使用前必须安装**：

```bash
# 安装依赖
clawhub install calorie-visualizer
clawhub install clawhealth-garmin
```

脚本会自动检测依赖，如果缺少会给出安装提示。

### 依赖说明

- **calorie-visualizer** - 用于记录食物摄入数据（卡路里、蛋白质等）
- **clawhealth-garmin** - 用于同步和查询 Garmin 运动消耗数据

## 🚀 使用方法

### 手动查询

```bash
# 查询今天
python3 scripts/daily_balance.py today

# 查询昨天
python3 scripts/daily_balance.py yesterday

# 指定日期
python3 scripts/daily_balance.py 2026-03-29
```

### 自动发送（用于定时任务）

```bash
python3 scripts/daily_balance.py today --auto
```

## ⏰ 定时任务

建议设置每天北京时间 21:30 自动发送总结：

```bash
openclaw cron add \
  --name "每日卡路里平衡总结 -21:30" \
  --cron "30 21 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "python3 skills/daily-calorie-balance/scripts/daily_balance.py today --auto" \
  --announce \
  --enabled true
```

查看定时任务：
```bash
openclaw cron list
```

## 📊 输出示例

```
📊 今日卡路里平衡总结（2026-04-01 北京时间）

🍽️ 食物摄入：830 kcal
（主要餐食：白米饭、炒青菜、叉烧...）

🔥 Garmin 消耗：964 kcal
（活动消耗约 289 kcal | 总消耗 964 kcal）

⚖️ 净卡路里：-134.0 kcal
（轻微赤字）

💡 今日建议：
• 赤字良好，继续保持
• 整体状态：优秀
```

## 🔧 配置

### 数据源（自动检测）

脚本会自动在 workspace 目录下查找依赖技能：

- **食物摄入**：`workspace/skills/calorie-visualizer/calorie_data.db`
- **运动消耗**：`workspace/skills/clawhealth-garmin/data/health.db`

### 环境变量（可选）

```bash
# 自定义 workspace 路径
export CALORIE_VIS_WORKSPACE=/path/to/your/workspace
```

## 💡 平衡判断标准

| 净卡路里 | 状态 | 建议 |
|---------|------|------|
| > +500 | 明显盈余 | 盈余较多，明天可增加运动或减少摄入 |
| +100 ~ +500 | 轻微盈余 | 略有盈余，保持当前节奏即可 |
| -100 ~ +100 | 平衡 | 摄入消耗平衡，保持当前状态 |
| -500 ~ -100 | 轻微赤字 | 赤字良好，继续保持 |
| < -500 | 明显赤字 | 赤字较大，减脂效果好，注意不要过度节食 |

## 📝 注意事项

1. **先安装依赖技能** - 使用前确保 calorie-visualizer 和 clawhealth-garmin 已安装
2. 确保 Garmin 数据已同步（可以手动运行 `garmin sync`）
3. 食物记录要及时录入 Calorie Visualizer
4. 定时任务会在每天 21:30 自动运行
5. 如果当天没有数据，会显示"无记录"或"无数据"

## 🐛 常见问题

### 提示缺少依赖技能

```
❌ 缺少依赖技能：
  • calorie-visualizer
  • clawhealth-garmin

请先安装以下依赖技能：
  clawhub install calorie-visualizer
  clawhub install clawhealth-garmin
```

**解决方法**：按照提示安装缺少的技能。

### Calorie Visualizer 数据库不存在

```
⚠️ 警告：Calorie Visualizer 数据库不存在
   请先使用 calorie-visualizer 技能记录一些食物数据
```

**解决方法**：先使用 calorie-visualizer 记录一些食物摄入数据。
