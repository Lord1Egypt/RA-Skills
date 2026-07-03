---
name: anomaly-detection
description: AI时序异常检测技能。基于Amazon Chronos-2零样本时序大模型，对用户提供的数据（CSV/Excel/JSON/粘贴）或API接口数据，进行多方法融合异常检测（Z-Score/MAD/IQR/移动平均偏离），自动分类异常类型（点异常/上下文异常/集体异常/水平偏移）并评定严重度（P0-P2），生成包含时序标注图、残差分析、异常分布、热力图、详细列表的交互式HTML可视化报告。触发词：异常检测、异常分析、时序异常、数据异常、检测异常、anomaly detection、找异常点、异常报告。
agent_created: true
---

# AI 时序异常检测技能

基于 Amazon Chronos-2 (120M参数) 零样本时序大模型 + 4种检测方法融合，对时序数据自动发现异常点，生成专业分析报告。

## 功能概述

1. **数据接收**：CSV/Excel/JSON 文件、用户粘贴数据、或 API 接口数据
2. **时序预测**：Chronos-2 逐点回测预测，无需训练，零样本推理
3. **多方法融合检测**：Z-Score + 改进Z-Score(MAD) + IQR + 移动平均偏离，4选2多数投票
4. **异常分类**：点异常 / 上下文异常 / 集体异常 / 水平偏移
5. **严重度评定**：P0严重 / P1警告 / P2轻微
6. **报告生成**：交互式 HTML (Plotly) + CSV 异常明细导出

## 适用场景

- IT运维：服务器 CPU/内存/QPS 异常检测
- 电商：销量/流量/转化率异常波动
- 金融：交易量/价格异常检测
- IoT：传感器数据异常
- 业务监控：任何时序指标的异常告警

## 输入数据格式

至少包含两列：时间戳 和 数值指标。

```
timestamp,value
2024-01-01 00:00,120.5
2024-01-01 01:00,118.3
2024-01-01 02:00,135.7
...
```

支持多列数据，会自动识别时间列和数值列。也支持：
- Excel (.xlsx/.xls)
- JSON (.json)
- Parquet (.parquet)

## 工作流

### Step 1: 接收数据

若用户提供文件路径 → 直接使用。若用户粘贴数据 → 保存为临时 CSV。若用户描述数据来源（如 API）→ 帮助实现数据获取。若用户未提供 → 引导用户提供数据。

数据要求：
- 最少 20 个时间点
- 时间频率需一致（秒/分/时/日/周/月）
- 数值列需为数字类型

### Step 2: 确认检测参数

向用户确认（或使用默认值）：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `zscore_threshold` | 2.5 | Z-score 阈值，超过即标记 |
| `mad_threshold` | 3.0 | 改进Z-score(MAD) 阈值 |
| `iqr_multiplier` | 1.5 | IQR 乘数 |
| `context_length` | 2048 | Chronos-2 上下文窗口长度 |

大多数情况下默认值即可满足需求。若用户数据波动较大，可适当提高阈值减少误报。

### Step 3: 运行异常检测

调用核心脚本 `scripts/anomaly_detect.py`：

```bash
python scripts/anomaly_detect.py --input <data.csv> --output <results_dir>
```

可选参数：
```bash
python scripts/anomaly_detect.py \
  --input data.csv \
  --output results/ \
  --zscore-threshold 2.5 \
  --mad-threshold 3.0 \
  --iqr-multiplier 1.5 \
  --context-length 2048
```

脚本执行流程：
1. 创建 Python 虚拟环境并安装依赖（chronos-forecasting, pandas, numpy, scipy, plotly）
2. 加载数据并自动校验（时间格式、缺失值、频率推断）
3. 加载 Chronos-2 模型（首次需从 HuggingFace 下载 ~500MB）
4. 逐点回测预测（用历史数据预测当前点）
5. 4种方法分别检测异常
6. 投票融合（至少2种方法确认才标记为异常）
7. 异常分类和严重度评定
8. 输出 `anomaly_data.json`、`anomalies.csv`、`time_series_with_detection.csv`

### Step 4: 生成 HTML 报告

调用 `scripts/report_gen.py`：

```bash
python scripts/report_gen.py --data <results_dir>/anomaly_data.json --output <report.html>
```

报告包含：
- 异常概览面板（总数/严重度/异常率）
- 主时序图（Plotly交互式，异常点分级标注）
- 残差分析图（时序 + 直方图 + σ区间）
- 异常类型分布（饼图 + 柱状图）
- 异常时段热力图（日期×时段）
- 异常明细表格（时间/值/偏离度/Z-Score/严重度/类型）
- 检测方法说明

### Step 5: 展示结果

用 `preview_url` 打开 HTML 报告，并梳理关键发现：
- 异常总数和占比
- 最严重的异常点（按 Z-Score 排序 TOP 5）
- 异常集中时段
- 异常类型分布（点异常 vs 集体异常 vs 水平偏移）
- 可能的业务原因分析
- 建议后续行动

## 异常检测方法说明

### 1. Z-Score 检测
计算每个残差的 Z-Score = |残差 - 均值| / 标准差。适用于正态分布数据。

### 2. 改进 Z-Score (MAD)
使用中位数和 MAD（中位数绝对偏差）代替均值和标准差，对离群值更鲁棒。

### 3. IQR 四分位距
基于 Q1 - 1.5×IQR 到 Q3 + 1.5×IQR 的区间判断。

### 4. 移动平均偏离
对比实际值与局部移动平均的偏离程度，检测趋势突变和水平偏移。

### 融合策略
需要至少 **2 种方法** 同时标记才确认为异常点，有效降低误报率。

## 异常类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `point` 点异常 | 单个时间点异常 | CPU 瞬时飙升至 100% |
| `contextual` 上下文异常 | 在特定上下文中异常 | 凌晨 3 点的正常流量在工作时间就异常 |
| `collective` 集体异常 | 连续多个点异常 | 连续 1 小时的服务降级 |
| `level_shift` 水平偏移 | 数值整体水平变化 | 系统升级后 QPS 永久下降 30% |

## 严重度等级

| 等级 | 条件 | 含义 |
|------|------|------|
| P0 严重 | Z-Score > 3.5 或 IQR 比率 > 3.0 | 极端异常，需立即处理 |
| P1 警告 | Z-Score > 2.5 或 IQR 比率 > 1.5 | 明显异常，需关注 |
| P2 轻微 | 其他确认异常 | 轻微异常，可观察 |

## 依赖管理

首次运行自动安装：
- chronos-forecasting >= 0.1.0
- pandas >= 2.0
- numpy >= 1.24
- scipy >= 1.10
- plotly >= 5.0
- openpyxl >= 3.0

## 注意事项

- Chronos-2 模型约 500MB，首次下载需要时间（使用 hf-mirror 镜像加速）
- CPU 推理：每个数据点约 1-3 秒（回测预测），数据量越大时间越长
- 数据量 < 20 个点会给出警告，但仍会尝试检测
- 默认使用 4选2 多数投票融合策略，减少误报
- 用户本地没有 GPU，默认 CPU 模式
- 仅作数据分析用途，发现异常后需人工判断和处理
- HuggingFace 下载慢时自动使用 `HF_ENDPOINT=https://hf-mirror.com`
- 若数据量 > 500 点，回测预测会每隔几个点进行一次以提高效率
