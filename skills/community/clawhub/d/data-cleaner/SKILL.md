---
name: multi-source-data-cleaner
label: Multi-Source Data Cleanser
version: 1.0.0
language: Python
runtime: subprocess (scripts/main.py)
trigger_words:
  - data cleaning
  - deduplication
  - spreadsheet cleanup
  - data merge
  - format standardization
  - CRM data cleanup
  - Excel cleaning
  - clean data
  - remove duplicates
  - merge data
---

# Multi-Source Data Cleanser

Upload messy data — get clean, structured output. Supports multi-format parsing, AI field identification, intelligent dedup/fill/formatting, multi-source join, and Feishu-native output (Bitable + quality report doc).

**Use cases:** E-commerce order cleanup, CRM customer data cleansing, bank statement reconciliation, roster cleanup, multi-system data merge.

---

## Capabilities

### F1 · Multi-Format Parsing
- Excel (.xlsx / .xls)
- CSV / TSV
- JSON (semi-structured)
- Clipboard paste text

### F2 · Smart Field Identification
- AI auto-detects: name, phone, email, address, amount, date, SKU, order ID, ID number, gender, etc.
- Supports user-defined field mapping override

### F3 · Data Cleaning
- **Deduplication**: Exact match + fuzzy dedup (FuzzyWuzzy, threshold 88%)
- **Missing value fill**: Mean / mode / semantic inference / leave blank
- **Format standardization**:
  - Phone → `1xx-xxxx-xxxx`
  - Date → `YYYY-MM-DD`
  - Amount → 2 decimal places
  - Address → Province/City/District/Street standardization

### F4 · Data Classification / Tagging (Pro)
- 8 built-in business rules (high-value customer, dormant user, VIP, enterprise, etc.)
- Supports custom JSON rules
- AI auto-tagging (requires Pro + AI API Key)

### F5 · Multi-Source Join / Merge (Pro)
- Cross-file relational join on key fields
- Fuzzy join when exact key not available (FuzzyWuzzy)
- Conflicted field resolution: priority by source order or latest timestamp

### F6 · Feishu Native Output
- Excel / CSV export
- Feishu Bitable (multi-dimensional table) write-back
- Data quality report auto-generated as Feishu Doc (Markdown)

---

## Tier Feature Matrix

| Feature | Free | Basic | Standard | Pro |
|---------|:----:|:-----:|:--------:|:---:|
| Multi-format parsing | ✅ | ✅ | ✅ | ✅ |
| Basic dedup | ✅ | ✅ | ✅ | ✅ |
| Monthly rows | 50 | 500 | 3,000 | Unlimited |
| Data sources | 1 | 3 | Unlimited | Unlimited |
| Smart fill | ❌ | ❌ | ✅ | ✅ |
| Format standardization | ❌ | ❌ | ✅ | ✅ |
| Fuzzy dedup | ❌ | ❌ | ✅ | ✅ |
| Multi-source merge | ❌ | ❌ | ❌ | ✅ |
| AI classification | ❌ | ❌ | ❌ | ✅ |
| Data quality report | ❌ | ❌ | ❌ | ✅ |
| Feishu Bitable output | ❌ | ❌ | ❌ | ✅ |

---

## Pricing

| Tier | Price | Monthly Rows | Sources |
|------|-------|:------------:|:-------:|
| Free | ¥0 | 50 | 1 |
| Basic | ¥29/mo | 500 | 3 |
| Standard | ¥99/mo | 3,000 | Unlimited |
| Pro | ¥299/mo | Unlimited | Unlimited |

---

## Usage

### Feishu Trigger
```
data cleaning
deduplication
spreadsheet cleanup
CRM data cleanup
Excel cleaning
```

### CLI
```bash
python scripts/main.py clean -i data.xlsx -o cleaned.xlsx
python scripts/main.py clean -t "name,phone\nJohn,13800138000" -f csv -o cleaned.csv
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
```

---

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DATA_CLEANER_API_KEY` | For AI features | MiniMax or DeepSeek API Key |
| `DATA_CLEANER_TIER` | Recommended | Subscription tier (free/basic/std/pro) |

---

## Directory Structure

```
multi-source-data-cleaner/
├── SKILL.md
├── README.md
├── scripts/
│   ├── main.py              # Entry: run_clean_pipeline / run_merge_pipeline
│   ├── parser.py            # F1: Multi-format parsing
│   ├── field_identifier.py # F2: AI field identification
│   ├── cleaner.py           # F3: Cleaning engine
│   ├── classifier.py        # F4: Classification / tagging
│   ├── merger.py            # F5: Multi-source join
│   ├── reporter.py          # F6: Quality report generation
│   ├── output.py            # F6: Output (Excel/CSV/Bitable/Feishu Doc)
│   └── tier_limits.py       # Tier access control + API key verification
└── tests/
    ├── test_parser.py
    ├── test_cleaner.py
    └── test_field_identifier.py
```

---

## License

MIT

> For paid plans, visit [YK-Global.com](https://yk-global.com)
