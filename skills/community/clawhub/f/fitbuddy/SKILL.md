---
name: fitbuddy
description: "专属健身追踪与饮食记录助手。支持体重/饮食/运动/饮水记录、BMR/TDEE自动计算、碳循环等饮食策略、食物数据库自动计算营养素、营养知识问答、训练计划制定、趋势图表、定时提醒。触发词：记录饮食/体重/运动/饮水、健身打卡/设置/初始化、今天吃了/练了、查看进度、训练建议、喝水了吗、蛋白质/碳水/脂肪/热量相关、饮食建议。Use when user mentions fitness tracking, diet logging, weight recording, exercise logging, calorie counting, nutrition questions, or asks about their fitness progress."
---

# fitbuddy — Fitness Buddy

## ⛔ 绝对规则

1. **数据路径**：`skills/fitbuddy/fitbuddy-data/`。脚本 cwd 为 `skills/fitbuddy/`
2. **先读 profile 再行动**：profile.json 有 BMR/TDEE/宏量/饮食策略，不要问用户已有的信息
3. **输出规范**：只输出最终用户消息，禁止暴露思考过程/步骤/内部逻辑
4. **安全红线**：热量缺口 ≤ 20% TDEE，减脂速度 ≤ 1kg/周，三大营养素缺一不可

## 初始化

如果 `fitbuddy-data/profile.json` 不存在 → 读 [references/init-guide.md](references/init-guide.md)

## 用户意图 → 执行

| 用户说 | 执行 |
|--------|------|
| 记录体重 | `record.py weight --date 今天 --kg 数值` → 更新 profile → 汇报+对比昨天 |
| 吃了什么 | `record.py meal --date 今天 --food-name "食物" --grams 克数` → 汇报热量/宏量/剩余 |
| 吃了菜品（番茄炒蛋等） | `record.py meal --date 今天 --food-name "番茄炒蛋" --grams 200` → 菜品自动拆解食材 |
| 模糊份量（一碗饭/一个鸡蛋） | **AI 侧翻译**：一碗饭→`--food-name "白米饭" --grams 200`，一个鸡蛋→`--grams 50`，一个鸡腿→`--grams 120`，一根香蕉→`--grams 100` |
| 吃了多个食物 | 逐条调用 `record.py meal`，每条自动保存 |
| 跟昨天一样 | `record.py meal --date 今天 --like-yesterday` → 追加昨日餐食 |
| 记错了/撤销 | `record.py undo --date 今天` |
| 还剩多少/今天吃了啥 | `record.py today --date 今天` → 读取后汇报 |
| 看进度 | `record.py progress --date 今天` → 进度条 |
| 看周报 | `record.py weekly --date 今天` |
| 看常吃什么 | `record.py patterns` |
| 喝水 | `record.py water --date 今天 --ml 数值` |
| 运动了 | `record.py exercise --date 今天 --name 名称 --sets 组 --reps 次 --weight 重量 --group 肌群 --type strength` |
| 改设置/改目标 | 直接改 profile.json |
| 训练建议 | 读 [references/exercise.md](references/exercise.md) + [references/training-plan.md](references/training-plan.md) |
| 营养知识 | 读 [references/nutrition-guide.md](references/nutrition-guide.md) |
| 该吃啥/推荐 | 读今日记录 + `calc.py daily` 算剩余 → 推荐补蛋白质缺口的食物组合 |

## 关键机制

**餐次自动判断**：`--meal` 不填时按时间自动归类（早6-10/午10-14/加14-16/晚16-21）

**默认份量**：food-db.json 的 `serving_g` 字段。`--grams` 不填时自动使用

**食物匹配**：`food-db search` 模糊匹配 → 找到用DB数据 → 找不到则估算营养素并用 `food-db add` 存入DB

**菜品**：food-db 中 `type: dish` 的条目，记录时自动按比例拆解成食材计算

**碳日目标**：`python scripts/calc.py daily --profile fitbuddy-data/profile.json --date 日期` 返回当天热量/宏量目标

## 定时提醒

逻辑统一在 [references/reminder-logic.md](references/reminder-logic.md)。

Cron 任务：`执行 fitbuddy 定时提醒。读取 skills/fitbuddy/references/reminder-logic.md，按照 <TYPE> 类型的逻辑执行。`

类型：weight / breakfast / lunch / dinner / water / preworkout

## 数据文件

```
fitbuddy-data/
  profile.json              — 用户档案
  records/YYYY-MM-DD.json   — 每日记录
  food-db.json              — 食物数据库
  user-patterns.json         — 用户习惯（自动维护）
```

## 参考文档

| 文件 | 内容 |
|------|------|
| [references/init-guide.md](references/init-guide.md) | 初始化引导 |
| [references/nutrition-guide.md](references/nutrition-guide.md) | 营养知识&份量估算 |
| [references/nutrition.md](references/nutrition.md) | 公式参考 |
| [references/exercise.md](references/exercise.md) | 运动指南 |
| [references/training-plan.md](references/training-plan.md) | 训练计划 |
| [references/budget-meals.md](references/budget-meals.md) | 平价饮食方案 |
| [references/reports.md](references/reports.md) | 报告&图表 |
| [references/channels.md](references/channels.md) | 提醒频道配置 |
| [references/reminder-logic.md](references/reminder-logic.md) | 提醒逻辑 |
