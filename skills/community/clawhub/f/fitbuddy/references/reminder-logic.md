# Reminder Logic — Cron 提醒统一逻辑

## 输出规范

只输出最终给用户的消息，禁止输出思考过程/步骤/内部逻辑。语气：爱弥斯。

## 通用流程

1. 读 `skills/fitbuddy/fitbuddy-data/profile.json` → diet_strategy.weekly_plan + 宏量目标
2. 确定今天类型：high_carb / low_carb / mid_carb
3. 读 `skills/fitbuddy/fitbuddy-data/records/今天日期.json` → 今日记录

## 各类型逻辑

### weight
- 已记录 → 恭喜 + 对比昨天 + 简短鼓励
- 未记录 → 提醒称体重，提到今天是X碳日

### breakfast
- 已记录 → 汇报统计(吃了啥+热量+P/C/F) + 剩余目标
- 未记录 → 提醒吃早餐，结合碳日类型给建议

### lunch
- 已记录 → 汇报统计 + 今日累计 + 剩余目标，蛋白质差多就提醒晚餐补
- 未记录 → 提醒吃午餐，结合碳日类型给建议

### dinner
- 已记录 → 全天总结(总热量/宏量) + 达标评价
- 未记录 → 提醒吃晚餐，结合今日累计给建议

### water
- 已达标(water_ml >= water_target_ml) → NO_REPLY
- 未达标 → 提醒喝水，显示进度(已喝X/目标Y，还差Z ml)

### preworkout
- 休息日 → NO_REPLY
- 训练日+已记录 → 汇报统计 + 加油
- 训练日+未记录 → 提醒练前餐，建议碳水+蛋白质组合
