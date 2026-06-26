# Data Analysis Assistant

**AI-powered data analysis using EvoLink API**

Powered by [Evolink.ai](https://evolink.ai?utm_source=github&utm_medium=skill&utm_campaign=data-analysis)

Analyze CSV, Excel, and JSON files with decision-first methodology and statistical rigor.

## 🚀 Quick Start

```bash
bash scripts/analyze.sh sales_data.csv "What are the top revenue drivers?"
```

## 🔑 Configuration

Set your API key:

```bash
export EVOLINK_API_KEY="your-key"
```

👉 [Get free API key](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=data-analysis)

## 📖 Usage

### Basic Analysis

```bash
bash scripts/analyze.sh <file_path> "<analysis_question>"
```

**Supported formats:**
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)

### Example Questions

```bash
# Trend analysis
bash scripts/analyze.sh sales.csv "What's the monthly revenue trend?"

# Comparison
bash scripts/analyze.sh experiment.csv "Is variant A significantly better than B?"

# Segmentation
bash scripts/analyze.sh users.csv "Which user segments have highest retention?"

# Anomaly detection
bash scripts/analyze.sh metrics.csv "Are there any unusual patterns in the last 30 days?"
```

## 🎯 Core Principle

**Analysis without a decision is just arithmetic.**

This skill emphasizes:
- Decision-first methodology
- Statistical rigor (sample size, confidence intervals, effect size)
- Clear output standards (insight-first, quantified uncertainty)
- Explicit limitations and caveats

## 📊 What It Does

1. **Reads your data file** (CSV/Excel/JSON)
2. **Sends to EvoLink API** with your analysis question
3. **Returns structured insights** with:
   - Key findings
   - Statistical confidence
   - Caveats and limitations
   - Recommended next steps

## 🔒 Security

**Credentials & Network**

Requires `EVOLINK_API_KEY` to call EvoLink API. Your data file content and analysis question are sent to `api.evolink.ai` for processing. EvoLink processes the data and returns analysis results. No data is stored after processing.

**File Access**

Reads the specified data file from your local filesystem. Files must be within `~/.openclaw/workspace` by default. The script validates file paths and rejects symlinks for security.

**Network Access**

- **EvoLink API** (`api.evolink.ai`) - Sends data and receives analysis

All network calls use curl and can be audited in the script source.

**Persistence & Privilege**

This skill does not modify other skills or system settings. Does not request elevated or persistent permissions.

## 📄 License

MIT

## 🔗 Links

- [API Reference](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=github&utm_medium=skill&utm_campaign=data-analysis)
- [Community](https://discord.com/invite/5mGHfA24kn)
- [Support](mailto:support@evolink.ai)
