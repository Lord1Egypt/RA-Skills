# 财务报表审查工具 (Financial Statement Review Tool)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

基于中国《会计法》《企业会计准则》和《税法》体系的财务报表智能审查工具，支持主流财务软件文件解析、税务风险识别、策略化审查等功能。

[English Documentation](#english-documentation) | [中文文档](#中文文档)

---

## 中文文档

### 🌟 核心特性

- **📄 智能文件解析**：自动识别并解析金蝶、用友等主流财务软件导出的文件（Excel/Word/PDF/CSV）
- **🔍 税务风险识别**：基于税法自动识别少缴税款、限额扣除超标、关联交易等风险
- **📊 策略化审查引擎**：模块化策略设计，支持自定义审查规则
- **📈 财务异常检测**：自动发现数据异常、勾稽关系错误、趋势异常
- **📝 专业报告输出**：生成符合审计标准的审查意见书

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/financial-statement-review.git
cd financial-statement-review

# 安装依赖
pip install -r requirements.txt
```

#### 基础用法

```python
from parsers import parse_file
from strategies import StrategyManager

# 1. 解析财务文件
result = parse_file('金蝶_资产负债表.xlsx')

if result.success:
    data = result.data
    
    # 2. 准备审查数据
    review_data = {
        'financial_statements': {
            'revenue': data.income_statement.get('营业收入', 0),
            'profit': data.income_statement.get('净利润', 0),
            # ...
        },
        'tax_returns': {
            'vat_paid': 1235000,
            'cit_paid': 450000,
        }
    }
    
    # 3. 执行审查策略
    manager = StrategyManager()
    manager.load_all_strategies()
    results = manager.execute_all(review_data)
    
    # 4. 生成报告
    summary = manager.generate_summary_report(results)
    print(summary)
```

### 📁 项目结构

```
financial-statement-review/
├── parsers/              # 文件解析模块
│   ├── excel_parser.py   # Excel解析器
│   ├── pdf_parser.py     # PDF解析器
│   ├── kingdee_parser.py # 金蝶专用解析器
│   └── ufida_parser.py   # 用友专用解析器
├── strategies/           # 审查策略库
│   ├── tax_reconciliation.py    # 税款比对策略
│   ├── revenue_recognition.py   # 收入确认审查
│   ├── tax_preference.py        # 税收优惠审查
│   └── related_party.py         # 关联交易审查
├── data/                 # 法规数据
├── references/           # 参考资料
└── scripts/              # 示例脚本
```

### 📋 支持的文件格式

| 格式 | 扩展名 | 支持软件 |
|-----|--------|---------|
| Excel | .xlsx, .xls | 通用、金蝶、用友、SAP |
| Word | .docx | 通用 |
| PDF | .pdf | 通用 |
| CSV | .csv | 通用、用友 |

### 📊 内置审查策略

| 策略 | 功能 | 适用场景 |
|-----|------|---------|
| **税款比对分析** | 比对已纳税款与财务报表，识别少缴税款 | 税务自查、稽查应对 |
| **收入确认审查** | 基于 CAS 14 审查收入确认合规性 | 审计、IPO |
| **成本操纵识别** | 识别通过成本费用调节利润 | 舞弊审计 |
| **税收优惠审查** | 审查优惠政策适用条件和时效性 | 高新审计、优惠核查 |
| **关联交易审查** | 审查转让定价、资本弱化、资金占用 | 反避税调查 |

### ⚠️ 免责声明

本工具仅供专业参考，审查意见基于预设规则和法规库生成，**不构成正式审计或税务意见**。重大决策请咨询持证会计师或税务师。

---

## English Documentation

### 🌟 Features

- **📄 Intelligent File Parsing**: Auto-recognize and parse files from major financial software (Kingdee, UFIDA, etc.)
- **🔍 Tax Risk Identification**: Identify underpaid taxes, deduction limit violations, related-party transactions
- **📊 Strategy-based Review Engine**: Modular design supporting custom review rules
- **📈 Financial Anomaly Detection**: Auto-detect data anomalies and reconciliation errors
- **📝 Professional Report Generation**: Generate audit-standard review reports

### 🚀 Quick Start

```bash
pip install -r requirements.txt
```

```python
from parsers import parse_file
from strategies import StrategyManager

# Parse financial file
result = parse_file('financial_report.xlsx')

if result.success:
    # Execute review strategies
    manager = StrategyManager()
    manager.load_all_strategies()
    results = manager.execute_all({'financial_statements': result.data.to_dict()})
```

### 📋 Supported Formats

- Excel (.xlsx, .xls)
- Word (.docx)
- PDF (.pdf)
- CSV (.csv)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## 📮 Contact

- Issues: [GitHub Issues](https://github.com/yourusername/financial-statement-review/issues)
- Email: your.email@example.com

## 🙏 Acknowledgments

- 中国《企业会计准则》
- 《中华人民共和国税法》体系
- 开源社区提供的优秀工具库

---

**⭐ Star this repository if you find it helpful!**
