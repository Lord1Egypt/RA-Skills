# Auto Report Generator

**AI-powered automatic report generation from CSV/Excel data**

---

## 功能介绍 | Features

Auto Report Generator automates the creation of professional data reports. Upload your CSV or Excel data, and the AI will automatically analyze patterns, generate charts, and produce formatted reports with textual insights.

### English
- Upload CSV or Excel files → AI auto-analyzes → Generates professional reports with charts + text analysis
- Supports multiple chart types: line, bar, pie, scatter, area, heatmap
- Multiple report templates: Monthly Report, Financial, Sales, Comparison, Custom
- Export to Excel (multi-sheet with formatting)
- AI-powered data insights and trend analysis

### 中文
- 上传 CSV/Excel → AI自动分析 → 生成专业报表（图表+文字分析）
- 支持多种图表类型：折线图、柱状图、饼图、散点图、面积图、热力图
- 多种报表模板：月报、财务、销售、对比、自定义
- 导出为 Excel（多Sheet带格式）
- AI 驱动的数据洞察与趋势分析

---

## 支持的数据格式 | Supported Data Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| CSV | `.csv` | Comma-separated values, UTF-8 encoded |
| Excel | `.xlsx` / `.xls` | Microsoft Excel files (2007+ recommended) |

**Requirements:**
- First row must contain column headers
- Numeric columns for chart generation
- Maximum file size: 50MB

---

## 安装步骤 | Installation

```bash
# Clone or navigate to the skill directory
cd /path/to/auto-report-generator

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt contents:**
```
pandas>=1.3.0
openpyxl>=3.0.0
xlsxwriter>=3.0.0
matplotlib>=3.4.0
Pillow>=8.0.0
requests>=2.25.0
numpy>=1.20.0
```

---

## 快速开始 | Quick Start

### Python API

```python
from scripts.generator import ReportGenerator

# Initialize generator
generator = ReportGenerator(
    ai_provider="openai",
    ai_model="gpt-4",
    tier="FREE"
)

# Generate report
result = generator.generate(
    file="sales_data.csv",
    template="monthly",
    output="monthly_report.xlsx"
)

print(f"Report saved to: {result['output_path']}")
```

### CLI Usage

```bash
# Basic usage
python scripts/generator.py --file data.csv --template monthly --output report.xlsx

# With AI provider
python scripts/generator.py \
    --file data.xlsx \
    --template financial \
    --ai-provider deepseek \
    --ai-model deepseek-chat \
    --tier STD \
    --output report.xlsx

# Custom template
python scripts/generator.py \
    --file data.csv \
    --template custom \
    --output custom_report.xlsx
```

### Shell Script (Quick Report)

```bash
# Make executable (first time)
chmod +x scripts/quick_report.sh

# Run quick report
./scripts/quick_report.sh data.csv monthly
```

---

## 图表类型 | Chart Types

| Type | Chinese | Best For |
|------|---------|----------|
| `line` | 折线图 | Trends over time |
| `bar` | 柱状图 | Category comparisons |
| `pie` | 饼图 | Proportion distribution |
| `scatter` | 散点图 | Correlation analysis |
| `area` | 面积图 | Volume trends |
| `heatmap` | 热力图 | Matrix/correlation data |

---

## 模板列表 | Template List

| Template | 中文名 | Description |
|----------|--------|-------------|
| `monthly` | 月报 | Monthly business report with KPIs |
| `financial` | 财务 | Financial summary with P&L |
| `sales` | 销售 | Sales performance analysis |
| `comparison` | 对比 | Side-by-side comparison report |
| `custom` | 自定义 | User-defined template |

---

## 套餐说明 | Pricing Tiers

| Tier | Price | Monthly Uses | Charts | Features |
|------|-------|-------------|--------|----------|
| FREE | ¥0 | 5 (lifetime) | 1 per report | Basic charts |
| STD | ¥9.9/mo | 50 | 3 per report | All chart types |
| PRO | ¥29.9/mo | 200 | Unlimited | PDF export, priority AI |
| MAX | ¥99/mo | Unlimited | Unlimited | Custom templates, API access |

---

## 注意事项 | Important Notes

1. **Data Privacy**: Uploaded data is processed locally; no data is stored on external servers (unless using cloud AI providers).
2. **AI Quota**: FREE tier has a strict 5-use lifetime limit; upgrade for higher volumes.
3. **File Format**: For best compatibility, use `.xlsx` format for Excel files.
4. **Column Headers**: Ensure your data files have clear, descriptive column headers in the first row.
5. **Numeric Data**: At least one numeric column is required for chart generation.
6. **Large Files**: Files over 50MB may experience slower processing; consider splitting large datasets.
7. **AI Provider**: Requires valid API key for OpenAI-compatible endpoints; set via environment variable `OPENAI_API_KEY` or `DEEPSEEK_API_KEY`.

---

## 环境变量 | Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# DeepSeek (alternative)
export DEEPSEEK_API_KEY="sk-..."

# Optional: Custom API endpoint
export OPENAI_API_BASE="https://api.openai.com/v1"
```

---

## License

MIT License
