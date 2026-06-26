# Daniels Running Plan

基于 Jack Daniels跑步力作《Daniel's Running Formula》的 AI 跑步训练计划生成器。

## 功能

- 根据目标赛事（5K/10K/半马/全马）和当前能力，自动生成个性化训练计划
- 支持三种核心训练类型：E跑（轻松跑）、T跑（阈值跑）、I跑（间歇跑）
- 智能分配休息日、训练强度和跑量
- 输出格式：可读计划文本（.txt）+ 可导入 Excel 的 CSV（UTF-8 BOM）

## 工作原理

训练计划基于 Jack Daniels 博士的训练理论，通过以下关键指标计算配速：

| 缩写 | 名称 | 说明 |
|------|------|------|
| E | Easy Run | 轻松跑，HR 69%-79% |
| T | Threshold Run | 阈值跑，HR 83%-88% |
| I | Interval Run | 间歇跑，HR 95%-100% |
| L | Long Run | 长跑，距离超过 E 跑上限 |

**配速计算公式：**
- T 配速 = 目标比赛配速
- E 配速 = T 配速 + 45~60 秒/km
- I 配速 = T 配速 - 6 秒/400m

## 安装

### 通过 ClawHub（推荐）

```bash
npm i -g clawhub
clawhub install daniels-running-plan
```

### 手动安装

将 `daniels-running-plan.skill` 文件放入 `~/.openclaw/plugin-skills/` 目录。

## 使用方法

在 OpenClaw 中，告诉 AI 以下信息即可生成训练计划：

1. **目标赛事**：半马 / 全马 / 10K / 5K
2. **目标时间**：如 1:45:00
3. **当前能力**：跑步经验或最近比赛成绩
4. **每周休息天数**：1-3天
5. **开始时间**：第几周周一开始

AI 将自动生成训练计划，包含：
- 每周训练安排（E/T/I/L跑）
- 各训练类型的具体配速
- 训练原则和数据来源

## 计划输出

- **.txt 文件**：人类可读版，包含完整训练安排和配速说明
- **.csv 文件**：UTF-8 BOM 编码，可直接用 Excel 打开，中文不乱码

## 注意事项

- CSV 文件导入 Garmin Connect / TrainingPeaks 可能失败，建议在 Garmin Connect App 中手动创建训练模板
- 训练计划仅供参考，请根据身体状态调整
- 长跑（L > 10km）建议安排在周末，前后应有休息日

## 相关资源

- Jack Daniels, *Daniel's Running Formula*, 3rd Edition
- VDOT 配速计算器
