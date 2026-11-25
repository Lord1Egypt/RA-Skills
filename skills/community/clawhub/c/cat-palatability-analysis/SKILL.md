---
name: cat-palatability-analysis
version: 1.0.0
license: MIT
description: 猫适口性双盆（两盆）试验数据分析。当用户提供「猫适口性试验记录」类 Excel（含原始记录单 sheet，含余料量A/B、首口料、组别、餐次），并要求计算对比数（采食差≥4g判胜负）、A/B显著性检验（配对t+Wilcoxon）、首选率、平均顿采食量/顿采食中位数、异常数据剔除或生成可视化图表时使用。输出清洗后数据、汇总 Excel、Markdown 报告和多张图表。Cat palatability two-bowl test analysis: win counts, paired t-test, Wilcoxon, first-bite preference, intake stats.
keywords: [猫适口性, 双盆试验, 两盆法, 宠物食品, 对比数, 首选率, 顿采食量, 显著性检验, cat palatability, two-bowl test, pet food]
metadata:
  openclaw:
    emoji: "🐱"
    requires:
      bins: [python3]
---

# 猫适口性试验分析

## 用途

分析双盆法猫适口性试验的原始数据。从「原始记录单」sheet 读取每只猫每餐的余料量与首口料，经异常剔除后，输出对比数、显著性、首选率、采食量描述统计与可视化图表。

## 何时使用

- 用户提供符合猫适口性试验记录模板的 `.xlsx`（含「原始记录单」sheet）
- 用户要求：对比数、采食量显著性分析、首选率、平均/中位顿采食量、异常剔除、可视化图表
- 关键词：猫适口性、双盆实验、对比数、首选率、顿采食量、适口性试验

## 快速开始

```bash
pip install -r requirements.txt   # 首次运行
python scripts/analyze_palatability.py "<输入xlsx路径>" -o "<输出目录>"
```

调整对比数阈值：

```bash
python scripts/analyze_palatability.py "data.xlsx" -o "./out" --win-diff 4
```

先拿示例数据验证环境与格式（内置生成器，2 秒跑通）：

```bash
python scripts/analyze_palatability.py assets/sample_cat_palatability.xlsx -o ./demo_out
```

依赖：`pandas`、`numpy`、`scipy`、`openpyxl`、`matplotlib`。

## 数据格式要求

脚本按固定列位置解析「原始记录单」sheet（与现有模板一致）：

| 内容 | 位置 |
|---|---|
| 抬头 | 第 1–4 行内含单盆给料量数值（默认 40g） |
| 位置行 | 第 6 行，每餐 A 列写「A左」或「A右」 |
| 数据区 | 第 8 行起，序号为数字的行 |
| 列布局 | 组别(0)、序号(1)、猫号(2)；每餐 3 列：余料A、余料B、首口料；备注(18) |
| 分组 | 组别列出现「第一组/第二组/第三组」时切换当前组 |
| 首口料枚举 | A料 / B料 / 同时采食 / 无采食 / 未观察 |

若模板列位置变动，修改脚本顶部 `MEAL_COLS`、`POS_ROW_INDEX`、`COL_NOTE` 等常量。

## 统计口径（已与用户确认）

1. **采食量** = 单盆给料量 − 余料量（g）。
2. **对比数**：同一猫同一餐，
   - `采食A − 采食B ≥ 4g` → A胜 +1
   - `采食B − 采食A ≥ 4g` → B胜 +1
   - `|差| < 4g` → 平局，不计入胜负
   - A胜率 = A胜 / (A胜 + B胜)
3. **异常剔除（双轨）**：
   - 备注含关键词 `待核/涂改/模糊/呕吐/软便/打翻/拒食/异常/混食/换人/位移/设备异常/未记录`
   - 每餐各组对 A/B 采食量分别做 IQR 1.5 倍离群检测
   - 采食量缺失也剔除
   - 全部剔除项写入剔除清单与报告
4. **显著性**：同一猫同一餐 A vs B 为配对设计。同时输出配对 t 检验（含 Cohen's dz）与 Wilcoxon 符号秩检验；以差值 Shapiro-Wilk 正态性结果决定主结论方法（p ≥ .05 用配对 t，否则 Wilcoxon）。
5. **首选率**：仅 `首口料 ∈ {A料, B料}` 计入分母；首选率 = A首选 / (A首选+B首选)。同时 / 无采食 / 未观察 不计入。
6. **平均顿采食量 / 中位数**：按组、按餐对有效记录的采食量求均值与中位数。
7. **左右位置偏倚**：比较 A左 / A右 的平均 A 首选率，报告偏倚指数。

## 输出

| 文件 | 内容 |
|---|---|
| `cleaned_data.csv` | 清洗后长表（每行 = 一猫一餐） |
| `removed_data.csv` | 剔除记录及原因 |
| `analysis_results.xlsx` | 12+ sheet：显著性、对比数（按组/猫/餐）、首选率（按组/餐）、采食量统计、位置偏倚、剔除清单等 |
| `report.md` | 完整 Markdown 报告，含所有统计表与结论 |
| `图1_对比数柱状图.png` | 各组 A胜/B胜次数 |
| `图2_首选率柱状图.png` | 各组首选率 |
| `图3_平均顿采食量折线.png` | 各组各餐均值 |
| `图4_顿采食中位数折线.png` | 各组各餐中位数 |
| `图5_AB采食量箱线图.png` | 清洗后 A/B 分布 |

## 执行流程

1. 确认输入 xlsx 含「原始记录单」sheet，列布局与模板一致。
2. 运行脚本，检查控制台输出的原始/剔除/有效记录数是否合理。
3. 打开 `report.md` 核对：剔除清单、显著性主结论方法、首选率分母、位置偏倚指数。
4. 若报告异常（如全部剔除、显著性方法与预期不符），检查输入数据或调整 `--win-diff`、脚本顶部常量。
5. 将报告与图表交付用户。

## 注意事项

- 三组料不同，汇总表只做「组内」比较；跨组只能比同口径指标（如 A 料首选率），并列出各组 A/B 料名称。
- 报出任何首选率时必须同时给出有效记录数作为分母。
- 首选率与采食占比结论不一致时，以采食占比为主并在报告说明。
- 若位置偏倚指数 > 10%，须提醒用户增加餐次重测或说明。
- **IQR 小样本限制**：每组每餐有效样本 < 4（`IQR_MIN_N`）时不执行 IQR 离群检测，脚本会打印警告。常规设计（每组 ≥ 6 只猫）不受影响；猫数少时离群只能靠备注剔除，需在报告中说明。
- 备注按「整猫整行」生效：一行备注会剔除该猫当餐全部 5 餐记录，符合现场记录习惯，交付时需向用户确认。
- 脚本默认中文图表字体 `SimHei`/`Microsoft YaHei`；无字体时退化为英文，图形仍可用。

## 资源

- `scripts/analyze_palatability.py`：完整分析脚本（解析、清洗、统计、图表、报告）。
- `references/statistical_rules.md`：统计口径详细说明与判定边界示例。
- `assets/sample_cat_palatability.xlsx`：示例原始记录单（模拟数据，含脏数据用例）。
- `assets/generate_sample.py`：示例数据生成器，可改数值复现或造测例。
- `requirements.txt`：Python 依赖。
