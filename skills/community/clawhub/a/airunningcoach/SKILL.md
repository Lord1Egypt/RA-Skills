---
name: ai-running-coach
description: AI 跑步教练 - 基于 VDOT 理论和周期化训练的专业马拉松训练指导。使用场景：制定马拉松/半马训练计划、分析跑步数据（TCX/GPX）、计算配速/心率区间、比赛策略制定、训练问题咨询、伤病预防建议。
---

# AI 跑步教练技能

专业的马拉松训练指导，基于 Jack Daniels VDOT 理论和极化训练原则。

---

## 核心功能

| 功能 | 说明 | 触发示例 |
|------|------|----------|
| 训练计划制定 | 生成个性化周期化训练计划 | "帮我制定破 3 训练计划" |
| 配速/心率计算 | 基于 VDOT 计算各区间配速和心率 | "破 3 需要什么配速" |
| 跑步数据分析 | 解析 TCX/GPX 文件，分析训练表现 | "分析我今天的跑步数据" |
| 比赛策略制定 | 制定比赛配速和补给策略 | "全马比赛怎么配速" |
| 训练问题咨询 | 回答训练方法、伤病预防等问题 | "间歇跑怎么练" |
| 成绩预测 | 基于训练数据预测比赛成绩 | "我能跑多少" |

---

## 工作流程

### 1. 训练计划制定

**触发：** 用户提到"训练计划"、"马拉松"、"备赛"等

**步骤：**

1. **收集信息**（如未提供）：
   - 当前 PB 或最近比赛成绩
   - 目标赛事和目标时间
   - 当前周跑量和训练频率
   - 年龄、体重（可选）
   - 伤病史（可选）

2. **计算 VDOT**：
   ```bash
   python scripts/calculate_pace.py --race-time <分钟数> --distance 42.195
   ```

3. **生成计划**：
   ```bash
   python scripts/generate_plan.py --current-pb <HH:MM> --target <HH:MM> --weeks 24 --weekly-km <跑量>
   ```

4. **输出计划**：
   - 阶段划分（基础期、强化期、巅峰期、减量期）
   - 周训练安排（含配速、心率区间）
   - 关键训练课说明

**参考：** `references/training-zones.md`、`references/workout-types.md`

---

### 2. 配速/心率区间计算

**触发：** 用户询问配速、心率区间、VDOT 等

**步骤：**

1. **确定输入**：
   - 如有比赛成绩：用成绩计算 VDOT
   - 如有 VDOT：直接使用
   - 如有最大心率/静息心率：计算心率区间

2. **计算**：
   ```bash
   # 基于比赛成绩
   python scripts/calculate_pace.py --race-time 218 --distance 42.195 --max-hr 196 --resting-hr 55
   
   # 基于 VDOT
   python scripts/calculate_pace.py --vdot 44 --max-hr 196
   ```

3. **输出**：
   - 各配速区间（E/M/T/I/R）
   - 各心率区间（Z1-Z5）
   - 对应训练用途说明

**参考：** `references/training-zones.md`

---

### 3. 跑步数据分析

**触发：** 用户上传 TCX/GPX 文件或询问训练数据分析

**步骤：**

1. **解析文件**：
   ```bash
   python scripts/analyze_run.py <文件路径> --output json
   ```

2. **分析内容**：
   - 总距离、总时间、平均配速
   - 平均心率、最大心率
   - 平均步频
   - 心率区间分布
   - 配速稳定性

3. **给出建议**：
   - 训练强度是否合适
   - 心率是否偏高/偏低
   - 改进建议

**参考：** `references/training-zones.md`、`references/workout-types.md`

---

### 4. 比赛策略制定

**触发：** 用户询问比赛配速、补给策略、赛前准备等

**步骤：**

1. **收集信息**：
   - 目标赛事和目标时间
   - 当前训练水平（PB、最近训练配速）
   - 比赛地点和天气（可选）

2. **制定策略**：
   - 配速策略（匀速/负分割）
   - 补给计划（胶、盐丸、水）
   - 赛前一周安排
   - 比赛日清单

3. **输出**：
   - 各公里点目标时间
   - 补给时机
   - 心理策略

**参考：** `references/race-strategies.md`

---

### 5. 训练问题咨询

**触发：** 用户询问训练方法、伤病、装备等

**处理：**

1. **判断问题类型**：
   - 训练方法 → 参考 `references/workout-types.md`
   - 心率/配速 → 参考 `references/training-zones.md`
   - 比赛策略 → 参考 `references/race-strategies.md`

2. **给出专业回答**：
   - 基于跑步科学理论
   - 结合用户实际情况
   - 提供可执行建议

---

## 脚本说明

### calculate_pace.py

**功能：** 配速和心率区间计算

**参数：**
- `--vdot`：VDOT 值
- `--race-time`：比赛时间（分钟）
- `--distance`：比赛距离（公里，默认 42.195）
- `--max-hr`：最大心率
- `--resting-hr`：静息心率
- `--output`：输出格式（json/text）

**示例：**
```bash
python scripts/calculate_pace.py --race-time 218 --distance 42.195 --max-hr 196 --output json
```

---

### analyze_run.py

**功能：** TCX/GPX 数据分析

**参数：**
- `file`：文件路径（必填）
- `--output`：输出格式（json/text）

**示例：**
```bash
python scripts/analyze_run.py run.tcx --output json
```

---

### generate_plan.py

**功能：** 马拉松训练计划生成

**参数：**
- `--current-pb`：当前 PB（HH:MM 或分钟数）
- `--target`：目标时间（HH:MM 或分钟数）
- `--weeks`：训练周期（周，默认 24）
- `--weekly-km`：当前周跑量（默认 300）
- `--output`：输出格式（json/text）

**示例：**
```bash
python scripts/generate_plan.py --current-pb 3:38 --target 3:00 --weeks 24 --weekly-km 300
```

---

## 关键理论

### VDOT 理论（Jack Daniels）

- 基于比赛成绩量化跑步能力
- 提供 5 个配速区间（E/M/T/I/R）
- 科学指导训练强度

### 极化训练（80/20 法则）

- 80% 低强度（Z1-Z2）
- 20% 高强度（Z4-Z5）
- 避免"垃圾跑量"

### 周期化训练

- 基础期：有氧基础
- 强化期：阈值 + 间歇
- 巅峰期：马拉松配速 + 最长 LSD
- 减量期：恢复 + 保持

---

## 注意事项

1. **个体差异**：公式计算是参考，需结合个人感受调整
2. **循序渐进**：周跑量增幅不超过 10%
3. **恢复优先**：感觉疲劳时优先休息
4. **伤病预警**：持续疼痛应停止训练并就医
5. **数据局限**：TCX/GPX 解析依赖文件格式，部分数据可能缺失

---

## 参考文档

- `references/training-zones.md` - 训练区间定义
- `references/workout-types.md` - 训练课类型详解
- `references/race-strategies.md` - 比赛策略指南
