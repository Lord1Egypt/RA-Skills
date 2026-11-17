---
name: excel-data-cleaner
description: "This skill should be used when the user provides a raw spreadsheet or CSV and needs data cleaning and statistics. Trigger phrases include '数据清洗', '去重补空', '异常值处理', 'Excel 清洗', '透视统计', '这份表帮我整理分析一下'. It profiles the data, applies deterministic cleaning via script (deduplication, missing value handling, outlier detection), and produces a cleaned file plus a statistics report with conclusions."
agent_created: true
---

# Excel 数据清洗与统计

## Overview

输入原始数据表，完成「体检 → 清洗 → 统计 → 结论」一条龙。清洗交给脚本做（确定性、可复现），解读与结论由模型做。核心原则：**清洗前先看体检报告再决定策略，不做无声的数据改写**。

## When to use

- 用户给了一份 xlsx / xls / csv，要清洗、去重、补空、查异常值。
- 用户要分组汇总、透视统计、趋势对比并要结论。

## 依赖

脚本需要 pandas 与 openpyxl：

```bash
pip install pandas openpyxl
# 国内网络建议走镜像，pypi.org 可能极慢：
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas openpyxl
```

兼容性：已在 **pandas 3.0.6 / openpyxl 3.1.5** 实测通过（CSV 与 xlsx 两条读写路径）。脚本内部对文本列的判断同时兼容 pandas 2.x 的 `object` dtype 与 pandas 3.x 的 `str` dtype。

## Workflow

1. **先体检**（不要直接清洗）：运行脚本的概览模式，看清楚行数、列类型、缺失率、重复行、异常值分布。
2. **向用户确认清洗策略**：缺失怎么处理（删除 / 填充中位数 / 填充「未知」）、哪些列算重复的关键组合、异常值是剔除还是标记。用户没意见时按推荐默认走，并在报告里写清做了什么。
3. **执行清洗**：跑脚本生成清洗后文件 + 清洗报告。
4. **复核报告**：确认删除行数、填充数量、异常标记数是否合理。
5. **统计分析**：基于清洗后数据做分组聚合、对比、趋势。
6. **输出结论**：不止给数字，要说清「说明什么 / 有什么异常 / 建议怎么做」。

## 脚本用法

```bash
# 仅体检，不写文件
python scripts/clean_excel.py 原始数据.xlsx

# 完整清洗：去重 + 数值列中位数填充 + IQR 异常值标记
python scripts/clean_excel.py 原始数据.xlsx \
  --sheet Sheet1 \
  --out 清洗结果.xlsx \
  --dedupe --subset 订单号 \
  --numeric-fill median \
  --outlier iqr --outlier-action flag \
  --report 清洗报告.md
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--sheet` | 工作表名称，默认第一个 |
| `--out` | 清洗结果输出路径 |
| `--dedupe` | 删除完全重复行 |
| `--subset` | 判重依据列，逗号分隔（如订单号） |
| `--numeric-fill` | mean / median / zero / none |
| `--text-fill` | 文本缺失填充值，默认「未知」 |
| `--drop-row-na-threshold` | 缺失率高于该比例的行直接删除，如 0.5 |
| `--drop-col-na-threshold` | 缺失率高于该比例的列直接删除 |
| `--outlier` | iqr / zscore / none，默认 iqr |
| `--outlier-action` | flag（加一列标记，推荐）/ clip（盖帽）/ drop |
| `--report` | 清洗报告 Markdown 输出路径 |

## 输出模式

```
## 数据体检
- 规模：N 行 × M 列
- 列概览：列名 / 类型 / 缺失率 / 唯一值数 / 示例值
- 完全重复行：X 行
- 疑似异常值：列名 + 数量 + 取值范围

## 清洗记录
1. 删除完全重复行 X 行（剩 Y 行）
2. 「金额」缺失 12 处 → 中位数填充（值=…）
3. 「城市」缺失 3 处 → 填充「未知」
4. 「订单金额」标记异常值 5 条（箱线图法，超出 [Q1-1.5IQR, Q3+1.5IQR]）

## 统计分析
- 分组汇总表（维度 + 指标）
- 排名 TOP / BOTTOM
- 环比 / 同比 / 构成占比

## 结论与建议
- 数据说明什么（用业务语言）
- 异常点与需要核实的地方
- 下一步建议
```

## 关键规则

- **绝不静默改数据**：每一条清洗动作都要进「清洗记录」，说明处理了哪些行/列、策略是什么。
- **优先标记而非删除**：异常值默认打标记列（如 `_outlier_列名`），让用户自己决定是否剔除。
- **保留原始文件**：永远输出为新文件，不覆盖输入。
- **区分「缺失」与「零」**：金额 0 是有意义的业务数据，不要当成缺失填充。
- **文本列先去空格**：首尾空格、全角半角不一致会导致去重和分组失败，先规整。
- **看懂业务含义再统计**：求和 vs 去重计数（如 UV vs PV）要问清楚，不要默认 SUM。
- **日期列要显式转换**：转不成功的行要提示，而不是静默变成 NaT。

## 自检清单

- [ ] 清洗前已出体检报告并与用户确认策略
- [ ] 所有清洗动作记录在案且数量对得上
- [ ] 未覆盖原始文件
- [ ] 异常值是标记而非静默删除
- [ ] 统计口径（求和/去重）已明确
- [ ] 结论用业务语言写成句子，不是只丢一张表
