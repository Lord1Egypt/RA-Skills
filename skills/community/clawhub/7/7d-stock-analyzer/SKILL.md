---
name: 7d-stock-analyzer
description: 七维分析框架 - 深度股票分析 Agent，整合多数据源进行全方位股票分析
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"],"env":["QVERIS_API_KEY"]},"install":[{"id":"python-deps","kind":"pip","package":"efinance akshare pandas numpy","label":"Install Python dependencies"}]}}
---

# 七维分析框架深度股票分析 Agent

基于七维分析框架的深度股票分析系统，整合 efinance、akshare、qveris 多数据源，提供全方位的股票投资分析。

## 核心能力

**七维分析框架：**
1. 数据收集与验证
2. 基本面分析（盈利能力、资产负债、现金流）
3. 估值分析（相对估值、估值风险）
4. 行业与竞争分析（生命周期、竞争格局、护城河）
5. 技术面分析（趋势、支撑压力、资金流向）
6. 风险识别（财务风险、行业风险、估值风险）
7. 结论输出（评分卡、投资建议矩阵）

## 快速开始

### 基础使用

```bash
python scripts/analyze.py 600519
```

### 完整分析（所有维度）

```bash
python scripts/analyze.py 600519 --full
```

### 指定维度分析

```bash
# 只分析基本面
python scripts/analyze.py 600519 --dimensions fundamental

# 分析多个维度
python scripts/analyze.py 600519 --dimensions fundamental,valuation,technical
```

### 指定数据源

```bash
# 仅使用 efinance
python scripts/analyze.py 600519 --sources efinance

# 使用多数据源交叉验证
python scripts/analyze.py 600519 --sources efinance,akshare,qveris
```

## 可用维度

| 维度标识 | 维度名称 | 说明 |
|---------|---------|------|
| `data` | 数据收集与验证 | 获取并验证核心数据 |
| `fundamental` | 基本面分析 | 盈利能力、资产负债、现金流 |
| `valuation` | 估值分析 | 相对估值、估值风险 |
| `industry` | 行业与竞争分析 | 行业周期、竞争格局、护城河 |
| `technical` | 技术面分析 | 趋势、支撑压力、资金流向 |
| `risk` | 风险识别 | 财务风险、行业风险、估值风险 |
| `conclusion` | 结论输出 | 评分卡、投资建议矩阵 |

## 输出格式

- **Markdown**：详细的分析报告，包含表格和评分
- **JSON**：结构化数据，便于程序化处理
- **简报**：简要摘要，适合快速浏览

```bash
# 输出 JSON
python scripts/analyze.py 600519 --output json

# 输出简报
python scripts/analyze.py 600519 --output brief
```

## 评分系统

**综合评分（0-100分）：**

| 分数区间 | 评级 | 含义 | 建议 |
|---------|------|------|------|
| 85-100 | ⭐⭐⭐⭐⭐ | 强烈推荐 | 重仓买入，长期持有 |
| 70-84 | ⭐⭐⭐⭐ | 推荐 | 适量买入，中期持有 |
| 55-69 | ⭐⭐⭐ | 中性 | 观望，等待更好买点 |
| 40-54 | ⭐⭐ | 谨慎 | 减仓，或短线博弈 |
| <40 | ⭐ | 回避 | 远离，或做空 |

## 数据源说明

| 数据源 | 主要功能 | 优势 | 成本 |
|--------|---------|------|------|
| efinance | 实时行情、基础数据 | 免费、开源、A股全面 | 低 |
| akshare | 深度财务数据 | 数据全面、更新及时 | 低 |
| qveris | 动态API调用 | 可扩展、多源验证 | 中 |

## 技术特性

- **并行分析**：多个维度并行执行，提高效率
- **数据缓存**：复用数据接口，降低成本
- **交叉验证**：多数据源验证，提高准确性
- **模块化设计**：每个维度独立，易于扩展

## 使用场景

1. **个股深度分析**：全面了解一只股票的投资价值
2. **投资决策支持**：为买入/卖出/持有提供数据支撑
3. **投资组合管理**：定期分析持仓股票
4. **股票筛选**：快速排除不符合要求的股票

## 依赖项

```bash
pip install efinance akshare pandas numpy
```

## 环境变量

```bash
export QVERIS_API_KEY=your_qveris_api_key
```

## 注意事项

- ⚠️ 本系统仅供参考，不构成投资建议
- ⚠️ 投资有风险，入市需谨慎
- ⚠️ 请结合市场情况和自身判断做出决策
- ⚠️ 数据可能存在延迟，请以实时数据为准
