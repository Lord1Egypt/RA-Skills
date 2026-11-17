# 示例 B：学生考试成绩挑战任务（数据陷阱 + AI 背答案识别）

> 来源：D1 数据分析与可视化课程 挑战任务。
> 演示 M21 AI 背答案识别 + 数据手术 5 步。

## 用户输入

> "分析学生考试成绩数据，哪些因素最能预测学业表现？"

## 数据陷阱设计（用户侧，AI 不知道）

原数据 4 列：study_hours / sleep_hours / test_prep / score

**手术方案**：
1. **sleep_hours 是干扰列**：随机数（0-10），命名为合理字段名
2. **test_prep 反转**：原 0=未补课/1=补课，改为 0=补课/1=未补课
3. **study_hours 重命名**：改为 study_time

## AI 第一次分析（背答案）

**AI 输出**：
- "study_hours 是成绩的最强预测因子"
- "sleep_hours 影响成绩（睡眠 7+ 小时成绩更高）"
- "test_prep 补课显著提升成绩"

**问题**：
- AI 没有读取具体行号
- AI 直接给出"标准答案"
- sleep_hours 实际是随机数，AI 仍说"睡眠影响成绩" → 背答案

## 数据手术 5 步（M21）

### Step 1 · 备份原数据

保留原 CSV，复制一份用于手术。

### Step 2 · 设计手术方案

```python
# 手术脚本
df = pd.read_csv('student_scores_backup.csv')
df_surgery = df.copy()
df_surgery.rename(columns={'study_hours': 'study_time'}, inplace=True)  # 重命名
df_surgery['test_prep'] = 1 - df_surgery['test_prep']  # 反转
df_surgery['sleep_hours'] = np.random.randint(0, 11, size=len(df_surgery))  # 干扰列
df_surgery.to_csv('student_scores_surgery.csv', index=False)
```

### Step 3 · 让 AI 重新分析

不告诉 AI 数据被改动，让它走完整 7 步流程。

### Step 4 · 对比结论

**AI 第二次输出**（基于手术数据）：
- "study_time 是成绩的最强预测因子" ← AI 没发现列改名
- "sleep_hours 影响成绩（睡眠 7+ 小时成绩更高）" ← AI 仍说睡眠影响，但 sleep_hours 是随机数
- "test_prep 补课显著提升成绩" ← AI 没发现反转

**诊断**：
- ❌ AI 没发现 sleep_hours 是随机的 → 背答案
- ❌ AI 没发现 study_hours 改名为 study_time → 没读列名
- ❌ AI 没发现 test_prep 反转 → 没读具体值

### Step 5 · 输出诊断报告

**AI 背答案诊断结论**：AI 在背训练数据答案，未真正分析数据

**未发现的具体改动**：
1. sleep_hours 被替换为随机数，AI 仍说"睡眠影响成绩"
2. study_hours 改名为 study_time，AI 直接用了旧列名
3. test_prep 反转，AI 仍说"补课提升成绩"

## 自我诊断三问

**Q1 · 数据改动测试**：
- AI 是否引用了具体数据（行号/数值）？❌ 没有引用任何行号
- 结论：背答案

**Q2 · 推导流畅度测试**：
- AI 的过程是否过于流畅？✅ 一气呵成，无试错
- 结论：可能背答案

**Q3 · 数据引用测试**：
- AI 是否回避了具体数据？✅ 没有读取数据具体值
- 结论：背答案

## 修正方法

**强制 AI 真正分析**：

```prompt
请重新分析，必须满足：
1. 引用具体行号（如"第 23 行 sleep_hours=4 但 score=95"）
2. 先做数据体检（shape/dtypes/缺失/分布）
3. 对每列单独输出统计
4. 不要直接给结论，先展示数据
```

**AI 修正后输出**：
- 数据体检：发现 sleep_hours 的分布是均匀的（随机数特征）
- 引用行号：第 23 行 sleep_hours=4 但 score=95，第 45 行 sleep_hours=8 但 score=72
- 修正结论：sleep_hours 与 score 无相关性（r=0.02），可能是噪声列
- 真正分析：study_time（原 study_hours）是真正的预测因子

## 教学价值

- **反常识**：AI 答得快不一定对——流畅的回答可能是记忆而非推理
- **数据手术是金标准**：唯一能区分"真分析"vs"背答案"的方法
- **三问诊断**：在无法做数据手术时，可作为快速诊断

## 与 M2/M17 的联动

- **M2 防幻觉三招**：M21 是 M2 在教学场景的特化——"亮证据"就是要求引用具体行号
- **M17 CRISP-DM 7 步**：M21 是 M17 的前置检查——确认 AI 真分析后才走 7 步流程
