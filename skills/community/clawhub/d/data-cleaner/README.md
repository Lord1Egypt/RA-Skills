# Multi-Source Data Cleanser

> Upload messy data — get clean, structured output.

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](#)
[![Language](https://img.shields.io/badge/language-Python-green)](#)
[![Platform](https://img.shields.io/badge/platform-Feishu%20Miaoda-cyan)](#)

---

## 🎯 What It Does

Every day, teams deal with messy data — inconsistent Excel formats, incomplete CRM exports, duplicate customer records scattered across platforms.

**Multi-Source Data Cleanser** lets you dump raw data in, and AI automatically identifies formats, cleans, classifies, and merges — outputting ready-to-use clean datasets.

---

## ✨ Core Features

| # | Feature | Description |
|---|---------|-------------|
| F1 | Multi-format parsing | Excel / CSV / TSV / JSON / clipboard paste |
| F2 | Smart field identification | AI auto-detects name / phone / email / amount / date |
| F3 | Data cleaning | Intelligent dedup + missing value fill + format standardization |
| F4 | Data classification / tagging | Built-in rules + AI auto-tagging (Pro) |
| F5 | Multi-source join/merge | Cross-file join + Fuzzy Join (Pro) |
| F6 | Feishu native output | Excel/CSV + Bitable + data quality report doc |

---

## 📋 Pricing

| Tier | Price | Monthly Rows | Data Sources | Key Features |
|------|-------|:------------:|:------------:|--------------|
| Free | ¥0 | 50 | 1 | Basic dedup, CSV/XLSX |
| Basic | ¥29/mo | 500 | 3 | Multi-format parsing, basic dedup |
| Standard | ¥99/mo | 3000 | Unlimited | Smart fill, format unification, fuzzy dedup |
| Pro | ¥299/mo | Unlimited | Unlimited | Multi-source merge, AI classification, quality report, Feishu Bitable |

---

## 🚀 Quick Start

### Trigger via Feishu

```
data cleaning
deduplication
spreadsheet cleanup
CRM data cleanup
Excel cleaning
```

### CLI

```bash
# Install dependencies
pip install pandas openpyxl xlrd fuzzywuzzy python-Levenshtein

# Clean an Excel file
python scripts/main.py clean -i data.xlsx -o cleaned.xlsx

# Paste text data
python scripts/main.py clean -t "name,phone\nJohn,13800138000" -f csv -o cleaned.csv

# Multi-source merge
python scripts/main.py merge --sources customers.xlsx orders.csv --on phone -o merged.xlsx
```

### Python API

```python
from main import run_clean_pipeline

result = run_clean_pipeline(
    sources=["orders.xlsx"],
    output_format="xlsx",
    output_path="/tmp/cleaned.xlsx",
    dedup_strategy="auto",
    fill_strategy="auto",
    classify=True,
    ai_model="deepseek",
    generate_report=True,
)

print(f"Done! Output: {result['file_path']}")
print(f"Cleaned rows: {result['cleaned_rows']}")
print(f"Quality score: {result['report_dict']['overall_score']}")
```

---

## 📊 Data Quality Report

After cleaning, a Markdown quality report is auto-generated:

- **Overall quality score** (0-100)
- **Data scale change** (rows/columns before vs. after)
- **Duplicate / missing rate change**
- **Cleaning details** (dedup count, fill count, formatted cells)
- **Field quality detail** (missing rate, unique values, sample values per column)
- **Optimization suggestions** (AI-generated)

Report can be created as a Feishu Doc and shared with the team instantly.

---

## 🗂️ Directory Structure

```
multi-source-data-cleaner/
├── SKILL.md                    # Skill definition (trigger words, params, description)
├── README.md                   # This file
├── scripts/
│   ├── __init__.py
│   ├── main.py                 # Entry point (run_clean_pipeline / run_merge_pipeline)
│   ├── parser.py               # F1: Multi-format parsing
│   ├── field_identifier.py     # F2: AI field identification
│   ├── cleaner.py              # F3: Cleaning engine (dedup/fill/format)
│   ├── classifier.py           # F4: Data classification / tagging
│   ├── merger.py               # F5: Multi-source join/merge
│   ├── reporter.py            # F6: Data quality report generation
│   ├── output.py               # F6: Output (Excel/CSV/Bitable/Feishu Doc)
│   └── tier_limits.py         # Tier access control
└── tests/
    ├── test_parser.py
    ├── test_cleaner.py
    └── test_field_identifier.py
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATA_CLEANER_API_KEY` | For AI features | MiniMax or DeepSeek API Key |
| `DATA_CLEANER_TIER` | Recommended | Subscription tier (free/basic/std/pro) |

### AI API Key

**MiniMax:** https://platform.minimax.chat/
**DeepSeek:** https://platform.deepseek.com/

---

## 🧪 Testing

```bash
cd tests
pytest test_parser.py -v
pytest test_cleaner.py -v
```

---

## ⚠️ Notes

1. **Data security**: All processing happens locally — no upload to third-party servers
2. **Encoding**: UTF-8 preferred, GBK auto-compatible
3. **Date formats**: Supports `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYYMMDD`, Unix timestamp
4. **Phone numbers**: Auto-detects 11-digit Chinese mobile and formats as `1xx-xxxx-xxxx`
5. **Monthly quota**: Usage stored in `/tmp/data_cleaner_state.json`, manually clearable

---

## 🔄 Changelog

### v1.0.0 (2026-04-19)
- Initial release
- F1-F6 all core features implemented
- 4-tier subscription system complete

---

## 📞 Feedback & Support

Contact the skill developer for issues or feature requests.

---

> For paid plans, visit [YK-Global.com](https://yk-global.com)
