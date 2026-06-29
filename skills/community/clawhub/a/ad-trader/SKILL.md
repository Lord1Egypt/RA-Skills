---
name: ad-trader
description: AI广告投手全流程助手。覆盖数据导入→投放分析→预算优化→素材诊断→智能报表→异常告警6大阶段。支持多平台（腾讯广告/巨量引擎/百度推广/Meta/Google Ads）数据统一分析，自动生成交互式HTML可视化报告，提供ROI/ROAS/CTR/CVR/CPA等多维度智能诊断和优化建议。触发词：广告投手, 投放分析, 广告优化, ROI分析, 素材分析, 广告报表, 投放诊断, 预算优化, 广告数据, ad trader, 投手报告, 广告账户诊断, 转化分析, 广告素材诊断, 广告出价优化。
version: 1.0.0
agent_created: true
tags:
  - advertising
  - marketing
  - data-analysis
  - reporting
  - optimization
---

# AI广告投手 (Ad Trader)

AI驱动的广告投放全流程管理助手，帮你从"手动盯盘"进化到"AI指挥作战"。

## 能力矩阵

| 模块 | 功能 | 说明 |
|------|------|------|
| 📥 数据管理 | CSV/Excel/JSON导入 | 支持多平台数据格式自动识别和标准化 |
| 📊 投放分析 | KPI计算、异常检测、趋势分析 | CTR/CVR/CPA/ROAS/ROI多维度诊断 |
| 💰 预算优化 | 出价建议、预算分配 | 基于历史数据的智能预算优化建议 |
| 🎨 素材诊断 | 素材疲劳度、A/B分析 | 识别素材衰减、推荐优胜素材 |
| 📈 智能报表 | HTML可视化报告 | 日报/周报/月报一键生成 |
| 🚨 异常告警 | 消耗异常、效果暴跌 | 自动检测预算泄漏和效果异常 |

## 核心指标说明

- **CTR** (点击率): 点击/曝光，衡量素材吸引力
- **CVR** (转化率): 转化/点击，衡量落地页和产品力
- **CPA** (获客成本): 消耗/转化，衡量投放效率
- **ROAS** (广告支出回报): GMV/消耗，衡量直接收益
- **ROI** (投资回报): (收入-成本)/成本，衡量综合收益
- **CPM** (千次曝光成本): 衡量竞价环境
- **ECPM** (有效千次曝光成本): 衡量竞争力

## 使用流程

### 1. 数据导入
```
导入广告数据文件路径
# 支持：腾讯广告报表导出、巨量引擎数据导出、自定义CSV/Excel
```

### 2. 快速诊断
```
分析我的广告投放数据
投放诊断
账户分析
# 一键生成多维度诊断报告
```

### 3. 深度分析
```
分析最近7天ROAS趋势
对比各计划的转化成本
哪个素材表现最好
检测预算是否有泄漏
```

### 4. 生成报告
```
生成日报
生成本周投放周报
生成月度复盘报告
```

### 5. 优化建议
```
给出预算优化建议
怎么降低CPA
素材要怎么调整
```

## 支持的数据格式

### 标准格式 (CSV/Excel)
列名需包含以下字段（大小写、中英文均可自动识别）：
- 日期 (date)
- 计划/广告组 (campaign/adgroup)
- 展现/曝光 (impressions)
- 点击 (clicks)
- 消耗/花费 (cost/spend)
- 转化 (conversions)
- GMV/成交额 (revenue/gmv)
- CTR (可选，会自动计算)
- CVR (可选，会自动计算)

### 平台专属格式
- 腾讯广告 Marketing API 导出格式
- 巨量引擎 Ocean Engine 导出格式
- 百度推广 导出格式
- Meta Ads 导出格式
- Google Ads 导出格式

## 脚本说明

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/data_manager.py` | 数据导入、清洗、标准化 | `python scripts/data_manager.py <file_path>` |
| `scripts/performance.py` | KPI计算、异常检测、趋势 | `python scripts/performance.py <data_file>` |
| `scripts/optimizer.py` | 预算优化、出价建议、素材分析 | `python scripts/optimizer.py <data_file>` |
| `scripts/report.py` | HTML可视化报告生成 | `python scripts/report.py <data_file> --type daily` |
| `scripts/cli.py` | 统一CLI入口 | `python scripts/cli.py <command>` |

## 配置

可通过 `ad_trader_config.json` 自定义：
```json
{
  "platform": "auto",
  "currency": "CNY",
  "alert_thresholds": {
    "cpa_spike_pct": 50,
    "ctr_drop_pct": 30,
    "budget_burn_rate": 0.8
  },
  "report_type": "daily"
}
```

## 参考文档

- `references/metrics.md` — 广告指标体系详解
- `references/platforms.md` — 主流平台特性对比
- `references/strategies.md` — 投放优化最佳实践
