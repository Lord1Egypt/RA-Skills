---
name: financial-data-collection
description: 中国财政部财政收支数据采集与分析。当用户提到以下场景时使用本 skill：(1) 抓取财政数据 - 触发词：抓取财政数据、采集财政数据、最新财政数据、财政数据采集；(2) 分析财政数据 - 触发词：分析财政数据、分析财政赤字、研究财政收入、对比财政收支。负责运行财政部官网的财政数据采集 pipeline，并对采集结果和导出数据进行结构化分析，也负责对采集过程中的爬取异常给出修复建议。
version: 1.0.0
changelog: |
  1.0.0 - 初始版本：支持财政部财政收支数据采集、累计值转单月值推导、财政赤字计算、数据分析图表生成
---

# 财政数据采集与分析 Skill

## 环境准备

本 skill 依赖 conda 环境 `scrapyEnv`，运行前确认环境已安装：

```bash
conda activate scrapyEnv
```

若环境不存在，根据项目的 `environment.yml` 创建：
```bash
conda env create -f $SKILL_DIR/FinancialDataCollection/environment.yml
```

## 入口脚本

```
python3 $SKILL_DIR/FinancialDataCollection/scripts/run_pipeline.py
```

可选参数：
- `--start-month YYYY-MM`：起始月份
- `--end-month YYYY-MM`：结束月份
- `--output-dir DIR`：输出目录（默认 `output`，统一存放于以下路径）

示例：
```bash
# 采集全部历史数据
python3 $SKILL_DIR/FinancialDataCollection/scripts/run_pipeline.py --output-dir $WORKSPACE/output

# 只采集 2024 年数据
python3 $SKILL_DIR/FinancialDataCollection/scripts/run_pipeline.py --start-month 2024-01 --end-month 2024-12 --output-dir $WORKSPACE/output
```

> **路径说明**：
> - `$SKILL_DIR`：skill 自身目录（`~/.openclaw/skills/financial-data-collection/`），项目代码放在 `$SKILL_DIR/FinancialDataCollection/` 内
> - `$WORKSPACE`：agent 工作区根目录（`~/.openclaw/workspace/`），采集的输出数据统一放在 `$WORKSPACE/output/` 下
> - 迁移到其他机器时，将整个 skill 目录复制过去即可，无需修改任何路径

## 输出结构

运行后在统一输出路径下按期间组织，结构如下：

```
$WORKSPACE/output/
├── YYYYMM-YYYYMM/           ← 每个统计区间一个目录
│   ├── raw_documents.xlsx   ← 原始公告层
│   └── extracted_metrics.xlsx ← 原始提取层（累计值）
└── 全量汇总/                ← 全量运行汇总（优先使用）
    └── YYYYMMDDHHMMSS/
        ├── derived_metrics_*.xlsx   ← 推导层（含单月值、赤字派生指标）
        └── monthly_summary_*.xlsx   ← 月度汇总宽表（行=指标，列=各月）
```

### 各文件说明

**各期间 extracted_metrics.xlsx**：原始提取层，每行 = 某指标在某个统计区间的累计值，字段包含 `指标（单位：亿元）`（即指标名称）、`指标值`、`同比增速`、`来源公告` 等。

**全量汇总/derived_metrics_*.xlsx**：推导层，共 3 类推导记录：
- 累计差值推导（单月值）
- 1-2月平均值拆分
- 赤字派生指标（窄口径、宽口径）

**全量汇总/monthly_summary_*.xlsx**：月度宽表，行 = 指标（共 47 项），列 = 各月（201301 起），适合直接做跨年度环比、同比分析。

### 数据文件使用优先级

> ⚠️ **优先使用全量汇总文件夹中的文件**，仅在汇总文件缺失或需要验证时再查各期间的分文件。

**何时用哪个**：
- 分析"某指标的月度趋势 / 同比 / 环比"→ 优先用 `monthly_summary_*.xlsx`
- 分析"单月推导值或赤字派生过程"→ 用 `derived_metrics_*.xlsx`
- 需要验证某条原始数据来源→ 用各期间的 `extracted_metrics_*.xlsx`

## 核心指标口径

### 财政收入类
- 全国一般公共预算收入 / 全国税收收入 / 非税收入
- 中央 / 地方一般公共预算收入
- 主要税种：国内增值税、消费税、企业所得税、个人所得税、证券交易印花税等

### 财政支出类
- 全国一般公共预算支出 / 中央本级支出 / 地方支出
- 主要支出科目：教育、社保就业、卫生健康、节能环保、交通运输、债务付息等

### 派生指标
- **窄口径财政赤字** = 当月一般公共预算支出 − 当月一般公共预算收入
- **宽口径财政赤字** = (当月一般公共预算支出 + 当月政府性基金支出) − (当月一般公共预算收入 + 当月政府性基金收入)

### 累计值转单月值规则
- 1 月：累计值即为当月值
- 2 月及以后：单月值 = 本期累计值 − 上期累计值（上期 = 同年上一统计区间）
- 例：1-10月累计 − 1-9月累计 = 10月单月值

## 爬取异常处理

运行日志中 `[WARN]` 开头的行为异常记录，格式为：

```
[WARN] YYYY-MM 指标名称 - 异常原因
```

常见异常类型及修复方向：

| 异常类型 | 异常原因 | 修复方向 |
|---------|---------|---------|
| 缺少上一期间数据 | 上期公告未抓取或解析失败 | 补充抓取上期数据后重跑 pipeline |
| 解析失败 | 网页结构变化或指标格式不匹配 | 检查 src/fiscal_parser.py 的解析正则，定位变化点，更新正则或添加新指标映射规则 |
| 重复数据 | 同一指标在同一期间有多条记录 | 检查去重逻辑，清理 output 缓存后重跑 |
| 单位不一致 | 原文使用万元等非亿元单位 | 在 fiscal_transform.py 中检查单位转换逻辑 |

**修复流程**：
1. 定位异常指标和期间
2. 查看原始公告内容（raw_documents.xlsx 或财政部官网对应页面）
3. 判断是解析规则问题还是数据本身问题
4. 更新 src/fiscal_parser.py 或 fiscal_transform.py 中的对应规则
5. 删除异常期间的缓存目录后重跑

## 数据分析指引

### 分析思路

1. **优先读 monthly_summary_*.xlsx**：该文件已将所有推导值整理为宽表格式，行 = 47 项指标，列 = 各月（201301 起），适合直接做跨年度同比、环比分析，无需额外计算
2. **若需单月推导细节或赤字派生过程**：读 derived_metrics_*.xlsx
3. **若需验证原始数据**：读各期间的 extracted_metrics.xlsx

### 数据粒度说明

- monthly_summary：直接是单月值（由原始累计值推导得出）
- derived_metrics：记录了推导过程，包含计算公式

### 生成文件输出路径

> ⚠️ 本 skill 生成的所有图表、数据文件（如 .png、.csv 等）一律保存到以下目录，不放在 workspace 根目录：

```
$WORKSPACE/output/artifacts/
```

输出文件名应包含分析主题和日期，便于识别，例如：`tax_revenue_yoy_20260327.png`。

### 分析示例

**示例 1：分析 2024 年各月财政赤字趋势**

1. 读取 extracted_metrics.xlsx，过滤 2024 年相关期间（如 2024-01、2024-03、2024-06、2024-09、2024-12）
2. 对每个指标计算单月值
3. 财政收入 = 全国一般公共预算收入（单月值）
4. 财政支出 = 全国一般公共预算支出（单月值）
5. 财政赤字 = 财政支出 − 财政收入
6. 绘图或输出表格

**示例 2：对比 2024 年和 2025 年同期税收收入**

1. 提取目标年度对应期间（如两者均有 1-2 月、1-6 月等累计值）
2. 计算同期单月值或使用累计值直接对比（注意：累计值不能跨年直接对比，需同口径）
3. 计算同比增速

**示例 3：识别异常指标**

1. 对各指标计算同比增速
2. 标出增速异常（如增幅 > 50% 或降幅 < -30%）的指标
3. 结合政策背景判断是否为数据异常或口径调整

### 读取 Excel 的参考代码

```python
import pandas as pd

# 各期间分文件
df = pd.read_excel("$WORKSPACE/output/202401-202412/extracted_metrics.xlsx")

# 全量汇总月度宽表（优先使用）
df_summary = pd.read_excel("$WORKSPACE/output/全量汇总/<最新时间戳>/monthly_summary_<时间戳>.xlsx")
```

## 触发规则

- **抓取数据**：优先确认目标月份范围，优先使用 `--start-month` / `--end-month` 限制范围减少重复抓取
- **分析数据**：优先确认用户需求的时间范围和指标范围，再决定是否需要先运行抓取
