# 📊 finance-analysis - 财务分析 CLI

> **你只管 do it，财务分析交给滚滚**

[![ClawHub](https://img.shields.io/badge/ClawHub-finance--analysis-orange)](https://clawhub.com/skills/finance-analysis)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/alsoforever/gungun-life/tree/gh-pages/skills/finance-analysis)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 📋 技能介绍

**finance-analysis** 是一个专业的财务分析 CLI 工具，帮助财务人和投资者快速分析公司财务状况。

**核心功能：**
- 📊 财报分析（规模/成长/盈利指标）
- 💰 股票估值（DCF/相对估值）
- ⚠️ 风险评估（偿债/盈利/成长能力）
- 📈 行业对比（同行业多公司对比）

**适用场景：**
- 投资决策前分析
- 月度财务分析
- 竞争对手分析
- 行业研究

---

## 🚀 快速开始

### 安装

```bash
# 使用 clawhub CLI 安装
clawhub install finance-analysis
```

### 使用

**1. 财报分析**
```bash
python scripts/finance_analysis.py analyze --stock 000001.SZ
```

**2. 股票估值**
```bash
python scripts/finance_analysis.py valuation --stock 600519.SH --method dcf
python scripts/finance_analysis.py valuation --stock 600519.SH --method relative
```

**3. 风险评估**
```bash
python scripts/finance_analysis.py risk --stock 000001.SZ
```

---

## 📋 输出示例

### 财报分析

```
📊 财报分析 - 平安银行 (000001.SZ)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【规模指标】
总资产：¥5.59 万亿
总收入：¥1,799 亿
净利润：¥465 亿

【成长指标】
收入增长率：8.2%
利润增长率：12.5%

【盈利指标】
毛利率：N/A（银行业）
净利率：25.8%
ROE：11.2%
ROA：0.85%

【综合评价】
⭐⭐⭐☆☆ 盈利能力中等
```

### 股票估值

```
💰 DCF 估值 - 贵州茅台 (600519.SH)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【假设条件】
最新收入：¥100,000 百万
收入增长率：15.0%
净利润率：50.0%
WACC：8.0%
永续增长率：2.0%

【估值结果】
公司价值：¥1,881,487 百万
每股价值：¥1,498 元
```

---

## ⚙️ 配置

### 环境变量

| 变量 | 描述 | 必需 |
|------|------|------|
| `TUSHARE_TOKEN` | Tushare API Token | 否（使用基础接口） |

### 依赖安装

```bash
pip install tushare pandas numpy
```

---

## 💡 使用案例

### 案例 1：投资决策前分析

```bash
# 分析目标公司
python scripts/finance_analysis.py analyze --stock 600519.SH

# 估值
python scripts/finance_analysis.py valuation --stock 600519.SH --method dcf

# 风险评估
python scripts/finance_analysis.py risk --stock 600519.SH
```

### 案例 2：行业对比

```bash
# 对比白酒行业
python scripts/finance_analysis.py analyze --stocks 600519.SH,000858.SZ,002304.SZ
```

---

## 📚 技能结构

```
finance-analysis/
├── SKILL.md           # 技能说明
├── README.md          # 使用文档
├── scripts/
│   └── finance_analysis.py  # 主脚本
└── package.json       # 发布信息
```

---

## 🌪️ 滚滚的话

**"你只管 do it，财务分析交给滚滚！"**

**这个技能是滚滚家族为财务人打造的分析利器，**
**希望能帮助你更高效地完成财务分析工作！**

**如有问题或建议，欢迎反馈！**

**翻滚的地球人，一直在！** 🌪️💚

---

**作者：** 滚滚家族 🌪️  
**版本：** 1.0.0  
**创建时间：** 2026-03-28  
**许可：** MIT
