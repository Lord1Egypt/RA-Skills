---
name: fn-portrait
description: "Financial report footnote extraction and analysis tool for Chinese A-share listed companies. Use when: (1) User wants to extract financial note data from annual reports (附注), (2) User wants to analyze financial statement footnotes, (3) User mentions 'Portrait', '财报附注', '年报分析', 'financial notes extraction', (4) User wants to download annual reports from CNINFO (巨潮资讯网), (5) User wants to visualize financial data from Chinese stock reports. Supports Shanghai/Shenzhen stock exchanges, STAR Market (科创板), ChiNext (创业板), and main boards."
license: MIT
---

# FN Portrait Toolkit

Financial report footnote extraction and analysis tool for Chinese A-share listed companies.

## Quick Start

### Prerequisites

Install Python dependencies:
```bash
uv pip install pandas openpyxl requests matplotlib numpy pillow pdfplumber filelock
```

### Configure LLM (Choose one)

**Option A: DeepSeek (Recommended for China)**
```bash
export DEEPSEEK_API_KEY=sk-...
```

**Option B: Moonshot**
```bash
export KIMI_API_KEY=sk-...
```

**Option C: Ollama (Local, no API key needed)**
```bash
# Install and start Ollama
ollama pull gemma3:1b
ollama serve
```

### Run Analysis

```bash
# Basic usage
python ~/.openclaw/skills/fn-portrait/scripts/fn_pipeline.py <stock_code> <company_name>

# Full example
python ~/.openclaw/skills/fn-portrait/scripts/fn_pipeline.py 688018 乐鑫科技 2023-2025 科创板
```

**Parameters:**
- `stock_code`: 6-digit stock code (e.g., 688018)
- `company_name`: Chinese company name (e.g., 乐鑫科技)
- `years`: Year range (default: 2023-2025, format: YYYY or YYYY-YYYY)
- `plate`: Stock exchange plate (default: 科创板, options: 科创板/创业板/沪主板/深主板)

## Pipeline Steps

1. **Download PDFs** - Fetch annual reports from CNINFO (巨潮资讯网)
2. **Extract Data** - Parse financial footnotes using pdfplumber
3. **LLM Analysis** - Semantic analysis of financial data
4. **Generate Portrait** - Create visualization charts

## Output Files

- `portraits/Portrait_<code>_<name>.png` - Final visualization chart
- `output2/<code>_<name>/` - Extracted Excel data
- `output2/<code>_<name>/<code>_<name>_LLM分析结果.xlsx` - LLM analysis results
- `RAWPDF/<name>PDF/` - Downloaded PDF files

## Supported Financial Items

### Balance Sheet Notes
- Current Assets: 货币资金, 交易性金融资产, 应收票据, 应收账款, 存货分类
- Non-current Assets: 固定资产情况, 在建工程, 商誉

### Income Statement Notes
- Revenue: 营业收入, 营业成本, 境内外毛利率
- Expenses: 管理费用, 销售费用, 财务费用, 研发费用

### Cash Flow Notes
- Operating activities
- Investing activities
- Financing activities

## Advanced Usage

### Skip Steps
```bash
python fn_pipeline.py 688018 乐鑫科技 --skip-download  # Use existing PDFs
python fn_pipeline.py 688018 乐鑫科技 --skip-extract   # Use existing extracted data
python fn_pipeline.py 688018 乐鑫科技 --skip-llm       # Skip LLM analysis
python fn_pipeline.py 688018 乐鑫科技 --skip-portrait  # Skip chart generation
```

### Custom Directories
```bash
python fn_pipeline.py 688018 乐鑫科技 --rawpdf-dir /path/to/pdfs --output-dir /path/to/output
```

## Troubleshooting

### Ollama Connection Error
Ensure Ollama is running: `ollama serve`

### PDF Download Fails
Check internet connection and CNINFO website accessibility

### Missing Fonts
Fonts are bundled in `assets/fonts/`. If display issues occur, install Noto CJK fonts system-wide.

## References

- See [references/financial-items.md](references/financial-items.md) for complete list of extractable financial items
- See [references/api-integration.md](references/api-integration.md) for API integration details
