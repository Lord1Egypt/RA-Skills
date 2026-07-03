---
name: analysis-toolkit
version: 2.0.4
author: wUwproject
license: MIT
description: 检验检测行业质量控制和数据分析工具箱。覆盖室内质控、室间比对、批次间比对、方法验证、趋势监控五大场景。方法通用，跨领域适用。
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/analysis-toolkit/
title: 分析质控工具包
summary: 检验检测行业质量控制和数据分析工具箱。覆盖室内质控、室间比对、批次间比对、方法验证、趋势监控五大场景。方法通用，跨领域适用。
trigger: ['室内质控', '精密度', '质控图', '室间比对', '批次比对', 'ANOVA', 'Z值', 'YYouden', '方法验证', '标准曲线', '检出限', '回收率', '不确定度', '趋势监控', '预测', 'Prophet', 'PCA', '主成分分析', '质控报告', '一致性评价', '总误差', '偏倚', '扩展不确定度', '合成不确定度']
trigger_negative: true
read_when: ['需要做质控分析', '需要做方法验证', '需要多组比对分析', '需要时序预测', '需要自动生成分析报告']
tags: ['qc', 'analysis', 'statistics', 'validation']
h1_position: true
trigger_quality: add_triggers
external_data_dir: true
meta_field_sync: true
antipattern_detail: add_detail
faq_quality: improve_qa
create_permissions_md: true
---
# analysis-toolkit：分析质控工具包

**触发词**：精密度、室内质控、室间比对、方法验证、标准曲线、趋势监控、Prophet 预测、PCA分析
**适用场景**：室内质控 | 室间比对 | 方法验证 | 趋势监控 | PCA分析 | 报告生成

> **场景驱动的检验检测分析工具箱** — 不是给你一堆函数，而是给你一套完整的分析工作流。

## 触发条件

**正向触发：**
- [帮我做室内质控分析 / 算一下精密度 / 画个质控图]
- [做几个实验室比对 / 算ANOVA和Z值 / 画YYouden 图]
- [做方法验证 / 算检出限定量限 / 拟合标准曲线]
- [做趋势监控 / 预测未来数据 / 跑Prophet 预测]
- [帮我生成质控报告 / 数据分析报告]
- [做PCA主成分分析 / 一致性评价]
- [做批次间比对 / 重复限性检查]
- [F值查表 / 回归分析 / 分组统计分析]

## 核心能力

→ 详见 渐进式文件索引表

| # | 功能 | 说明 |
| --- |------| ------ |
| 1 | **四层算子架构** | 细粒度算子层 + 组合层(Pipeline) + 模板场景 + 自扩展 |
| 2 | **注册表驱动** | 算子注册表 + 自动缺口检测 + 公式级自测试 |
| 3 | **模板 = 场景 + HTML 报告包** | 场景模板(分析) × 报告模板(可视化) 独立编排 |
| 4 | **置信验证体系** | 场景交叉验证 + 通用逼近验证 + 算子自测试 |
> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| ------ |------| ---------- |----------|
| `scripts/operations/` | 细粒度算子层 | 原子级统计/不确定度/总误差/回归算子（自动注册 + 缺口发现） | 无 |
| `scripts/pipeline/` | 流水线引擎 | Pipeline/Step 编排 + 模板注册表 | 无 |
| `scripts/standards/` | 标准管理 | 标准注册表 + 搜索链 + 自动注册 | 无 |
| `references/antipatterns.md` | 规范指南 | 常见错误做法与正确做法 | R-18 |
| `references/data-interface.md` | 数据接口规范 | 输入输出格式、字段约定、必填参数标注 | R-11 |
| `references/anova-analysis.md` | ANOVA方差分析 | F临界值查表、单因素ANOVA实现 | 无 |
| `references/changelog.md` | 版本管理 | 更新日志 | R-24 |
| `references/faq.md` | 常见问题 | 数据格式、错误处理等常见问答 | R-19 |
| `references/group-analysis.md` | 分组统计分析 | 分组聚合、阳性率分析、结论生成 | 无 |
| `references/LICENSE.md` | 许可协议 | MIT 许可证 | R-26 |
| `references/pca-analysis.md` | PCA主成分分析 | PCA算法实现、碎石图、散点图 | 无 |
| `references/permissions.md` | 权限说明 | 操作类型与风险等级 | R-15, R-16 |
| `references/pipeline.md` | 流水线参考 | Pipeline 架构、四种用法、模板=场景+报告 | 无 |
| `references/quickstart.md` | 快速开始 | 导入、完整示例代码 | C-17 |
| `references/regression-validation.md` | 回归分析与方法验证 | 线性/多项式回归、LOD/LOQ、不确定度 | 无 |
| `references/report-generation.md` | 报告生成 | Word 报告生成模板与配置 | 无 |
| `references/standards-interface.md` | 标准接口 | 标准注册/搜索、模板管理 | 无 |
| `references/time-series.md` | 时序分析与预测 | 趋势聚合、滚动统计、Prophet 预测 | 无 |

## 工作流程

1. **理解用户需求** → 识别分析场景和目标参数（输入：用户原始需求；输出：分析计划）
2. **规划执行步骤** → 选择算子/Pipeline 模板，确定数据要求和预期输出（输入：分析计划；输出：执行方案）
3. **调用相关工具/脚本** → 执行数据分析/质控计算/报告生成（输入：执行方案；输出：数值结果+HTML报告）
4. **返回结果给用户** → 呈现分析结论和可视化报告（输入：数值结果+HTML报告；输出：用户可读的最终输出）

## 能力边界

### 支持范围
- 本技能专注于**检验检测行业**的质量控制和数据分析
- 单次调用可处理**任意数量**的测量数据点（基于 numpy/pandas 向量化计算）

### 适用范围说明
- **通用分析引擎**：本技能专注统计分析与质控算法，方法和公式跨行业适用。
- **非专有场景**：不包含农产品/食品检测的专用判定标准，但通用算法可直接处理其数据。
- **最小数据量要求**：精密度分析每水平≥2行，质控图建议≥10个点，Prophet 预测需要≥3个聚合后的时间点。数据不足时函数会抛出 ValueError 或返回 result["warnings"] 提示。严重问题（如列名错误、斜率为0）抛出明确异常；轻度问题（如含空值、数据偏少）写入 result["warnings"] 并同步输出到控制台，避免静默返回错误结果。
- **最小数据量要求**：精密度分析每水平≥2行，质控图建议≥10个点，Prophet 预测需要≥3个聚合后的时间点。数据不足时函数会抛出 ValueError 或返回 result["warnings"] 提示。严重问题（如列名错误、斜率为0）抛出明确异常；轻度问题（如含空值、数据偏少）写入 result["warnings"] 并同步输出到控制台，避免静默返回错误结果。

### 运行环境
- 离线可用，无需网络连接
- 基于 Python 3.8+，依赖 numpy/pandas/matplotlib
- 输入格式：pandas DataFrame
- 输出格式：数值结果 + HTML 可视化报告
- 内置算子数量持续增长中，可通过测试验证确保正确性
- 计算精度受限于 IEEE 754 双精度浮点数标准

## 核心场景

### 1️⃣ 室内质控（Internal QC）

同一实验室内部，评估方法精密度和稳定性。

| 功能 | 说明 |
| ------ |------|
| **多水平精密度分析** | 每水平SD/RSD/均值/中位数，合成标准差（正规算法 + 简单算法） |
| **重复限性检查** | 平行样极差检查、相对误差、允许值分级判定 |
| **质控图** | Levey-Jennings 控制图，±1σ/±2σ/±3σ限，失控点标注 |

→ 详见 渐进式文件索引表

### 2️⃣ 室间比对（Inter-lab QC）

多家实验室/操作人员/仪器之间的结果比对。

| 功能 | 说明 |
| ------ |------|
| **ANOVA方差分析** | SST/SSB/SSW分解，F值计算 |
| **F临界值查表判定** | α=0.05，支持 df₁=1~24, df₂=1~20 |
| **Z值分析** | 基于ISO 13528的Z值计算与判定（满意/可疑/不满意） |
| **YYouden 图** | 双实验室比对可视化 |

→ 详见 渐进式文件索引表

### 3️⃣ 批次间比对（Inter-batch QC）

不同批次的检测结果一致性检验。

| 功能 | 说明 |
| ------ |------|
| **批次ANOVA** | 同室间比对的ANOVA流程，应用于批次维度 |
| **重复限性** | 批次内重复性检查 |
| **允许值判定** | 根据数量级自动查找允许偏差 |

→ 详见 渐进式文件索引表

### 4️⃣ 方法验证（Method Validation）

标准曲线、检出限、定量限、回收率、不确定度。

| 功能 | 说明 |
| ------ |------|
| **标准曲线拟合** | 线性/多项式，支持强制过零点 |
| **检出限/定量限** | 支持GB/T 27417和ICH两种标准，sigma 来源支持 curve/仪器/空白/噪声 |
| **加标回收率** | 多水平回收率计算 |
| **曲线不确定度** | EURACHEM/CITAC标准曲线分量 u_rel(curve) |
| **一致性评价** | PCA相关系数法 |

→ 详见 渐进式文件索引表

### 5️⃣ 趋势监控（Trend Monitoring）

长期数据跟踪与风险预警。

| 功能 | 说明 |
| ------ |------|
| **时序聚合分析** | 按日/周/月聚合，趋势图绘制 |
| **滚动统计** | 滚动均值、标准差、±2σ警戒线 |
| **Prophet 预测** | 多品类/整体预测，95%置信区间 |

→ 详见 渐进式文件索引表

## 快速使用

### 导入

```python
from scripts.operations import calc_mean, calc_sd, calc_rsd, calc_bias
from scripts.scenarios.internal_qc import internal_precision_analysis
```

### 示例

```python
# 完整室内精密度分析
import scripts.scenarios.internal_qc as iqc
result = iqc.internal_precision_analysis(df, "水平", "结果")
fig, stats = iqc.control_chart(df, "结果")
```

## 流水线（Pipeline）

四种用法：
- **单独用** — 单步调用算子
- **组合用** — pipeline() + step() 临时拼装
- **场景模板** — 加载内置模板跑完整场景+HTML报告
- **自扩展** — 查标准->自动补全算子->注册模板

```python
from scripts.pipeline.registry import load_template
from scripts.reporting.report_engine import render_from_template

pipe = load_template("总误差评估")
results = pipe.run(data)
html = render_from_template("总误差评估", results)
```

## 数据格式

统一接受 `pandas.DataFrame`。
关键列名参数：`value_col`(数值列), `group_col`(分组列), `date_col`(时间列)