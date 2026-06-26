# Financial Report Analyzer · 财报智能解读

[English](#english) | [中文](#chinese)

---

## English

Extract, normalize and analyze key metrics from corporate financial reports (10-K, 10-Q, A-share annual/interim reports, IFRS/GAAP/CAS PDFs).

### Quick Start

```bash
python3 scripts/run_pipeline.py --input annual_report.pdf --output report.json
python3 scripts/render_report.py --input report.json --format md > analysis.md
```

### Features

- 📊 Multi-format ingestion: PDF, XBRL, Excel
- 🔢 40+ standardized financial ratios (CFA-aligned)
- 🚩 18 red-flag heuristics for earnings quality
- 📈 Peer benchmarking with industry percentiles
- 📍 Full provenance: every number → source page+table
- 🔒 No external network calls

### License

MIT-0

---

## Chinese

从企业财报（10-K、A 股年报半年报、IFRS/GAAP/CAS PDF）抽取并归一化关键指标，输出对比、比率、风险信号。

### 快速开始

```bash
python3 scripts/run_pipeline.py --input 公司2024年报.pdf --output report.json
python3 scripts/render_report.py --input report.json --format md > 分析报告.md
```

### 功能

- 📊 多格式摄入：PDF / XBRL / Excel
- 🔢 40+ 标准财务比率（按 CFA 规范）
- 🚩 18 项红旗启发式（识别盈余管理迹象）
- 📈 同行对标，给出行业分位
- 📍 完整溯源：每个数字带页码+表格定位
- 🔒 零外部网络请求

### 协议

MIT-0
