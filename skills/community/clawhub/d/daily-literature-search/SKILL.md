---
name: daily-literature
version: 1.0.0
description: Automated daily literature search system for academic researchers. Performs scheduled searches across PubMed, OpenAlex, and Semantic Scholar with automatic deduplication, OA download, smart categorization, and daily reports.
author: Researcher
license: MIT
tags:
  - literature
  - research
  - automation
  - academic
  - papers
  - cron
requirements:
  - python3
  - requests>=2.28.0
  - pyyaml>=6.0
env_vars:
  - USER_EMAIL: Email for API access (OpenAlex/Crossref polite pool)
  - SEMANTIC_SCHOLAR_API_KEY: Optional S2 API key for higher rate limits
  - OPENALEX_API_KEY: Optional OpenAlex API key
---

# Daily Literature Search Skill

Automated literature search system for academic researchers. Performs scheduled searches across multiple databases (PubMed, OpenAlex, Semantic Scholar), automatically deduplicates results, downloads open-access papers, and generates daily reports.

## 🎯 Use Cases

- **Daily literature monitoring** for specific research topics
- **Automated paper collection** for literature reviews
- **Stay updated** on latest publications in your field
- **Build personal paper library** with automatic categorization

## 📦 Components

### 1. Core Search Script (`daily_literature_search.py`)

Main execution script with the following features:

- **Multi-source search**: PubMed, OpenAlex, Semantic Scholar
- **Automatic deduplication**: By DOI (within batch + against local library)
- **OA detection**: Uses Unpaywall API to identify open-access papers
- **Auto-download**: Downloads OA papers from PubMed Central or publisher sites
- **Smart categorization**: Classifies papers by topic (configurable keywords)
- **Daily reports**: Generates Markdown reports with search statistics

### 2. Upload Analyzer (`analyze_uploaded.py`)

Analyzes and categorizes manually uploaded papers:

- **Filename-based classification**: Uses keyword matching
- **DOI extraction**: From filenames and metadata
- **Batch processing**: Handles multiple files at once
- **Report generation**: Creates categorization summary

## ⚙️ Configuration

### Directory Structure

```
papers/
├── B-ALL/raw/          # Category 1 (e.g., B-ALL research)
├── MM/raw/             # Category 2 (e.g., Multiple Myeloma)
├── OTHER/raw/          # Other papers
├── daily_search_logs/  # Search logs and reports
└── upload_temp/        # Temporary upload directory
```

### Search Keywords (Customizable)

Edit `SEARCH_KEYWORDS` in `daily_literature_search.py`:

```python
SEARCH_KEYWORDS = [
    '"inotuzumab ozogamicin"',
    '"Elranatamab"',
    '"Teclistamab"',
    '"Talquetamab"',
    '"Blinatumomab"',
    '("CAR-T" AND "B-ALL")',
]
```

### Classification Keywords

Edit `B_ALL_KEYWORDS` and `MM_KEYWORDS` in `analyze_uploaded.py` to match your research domains.

## 🚀 Usage

### Manual Execution

```bash
# Run daily search
python3 papers/daily_literature_search.py

# Analyze uploaded papers
python3 papers/analyze_uploaded.py
```

### Scheduled Execution (Cron)

Add to crontab for automatic daily searches:

```bash
# Daily search at 6:30 AM
30 6 * * * /usr/bin/python3 /path/to/papers/daily_literature_search.py >> /path/to/papers/daily_search_logs/cron.log 2>&1
```

### Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_RESULTS_PER_KEYWORD` | 10 | Max results per keyword per source |
| `DATE_RANGE_DAYS` | 7 | Search window (recent N days) |
| `SOURCES` | `["pm", "oa", "s2"]` | Search databases |
| `USER_EMAIL` | — | For polite API access (env var) |

## 📊 Output

### Daily Report Example

```markdown
# 📚 每日文献检索报告
**检索日期：** 2026-03-18

## 📊 检索汇总
| 分类 | 检索到 | 成功下载 | 付费墙 |
|------|--------|---------|--------|
| B-ALL | 28 | 0 | 28 |
| MM | 24 | 0 | 24 |
| 总计 | 53 | 0 | 53 |

## 🔀 去重统计
- 原始检索结果：130 篇
- 去重后文献：110 篇
- 批次内重复：2 篇
- 库中已有：18 篇
```

### File Organization

- **Reports**: `papers/daily_search_logs/daily_report_YYYY-MM-DD.md`
- **Logs**: `papers/daily_search_logs/daily_search_YYYY-MM-DD.log`
- **Papers**: `papers/{CATEGORY}/raw/{DOI}.pdf`

## 🔧 Advanced Features

### 1. Library Deduplication

Automatically checks new results against existing library:

- Scans all category directories for existing DOIs
- Extracts DOIs from filenames and historical logs
- Skips papers already in library
- Reports duplicate statistics

### 2. Open Access Detection

Uses Unpaywall API to identify OA papers:

```python
is_oa, oa_url = check_open_access(doi)
if is_oa:
    download_paper(oa_url, save_path)
```

### 3. PubMed Central Integration

Automatically tries PMC for biomedical papers:

```python
if pmid and str(pmid).isdigit():
    download_from_pubmed(pmid, save_path)
```

## 🛠️ Customization Guide

### Change Research Topics

1. Edit `SEARCH_KEYWORDS` in `daily_literature_search.py`
2. Update category names and keywords
3. Modify directory structure if needed

### Add New Categories

1. Create new directory: `papers/NEW_CATEGORY/raw/`
2. Add classification keywords in `classify_paper()` function
3. Update report generation to include new category

### Integrate with Notification Systems

Add email/Slack/Discord notifications after search completion:

```python
# At end of main()
send_notification(f"Daily search complete: {results['total']} papers found")
```

## 📋 Requirements

### Python Dependencies

```bash
pip install requests
# Most other modules are standard library
```

### API Access (Optional but Recommended)

- **Semantic Scholar API Key**: Higher rate limits
- **OpenAlex API Key**: Polite pool access
- **Unpaywall**: Free, no key needed (email required)

Set environment variables:

```bash
export SEMANTIC_SCHOLAR_API_KEY="your-key"
export OPENALEX_API_KEY="your-key"
export USER_EMAIL="your@email.com"
```

## ⚠️ Important Notes

1. **Rate Limits**: Respect API rate limits, especially without API keys
2. **Storage**: Monitor disk space for downloaded PDFs
3. **Copyright**: Only download open-access or legally available papers
4. **Email**: Set `USER_EMAIL` for polite API access

## 🔄 Version History

- **1.0.0** (2026-03-18): Initial release
  - Multi-source search (PubMed, OpenAlex, Semantic Scholar)
  - Automatic deduplication (batch + library)
  - OA detection and download
  - Smart categorization
  - Daily reports with statistics

## 🤝 Contributing

To contribute improvements:

1. Fork the skill repository
2. Test changes with your own literature search
3. Submit pull request with description of improvements

## 📄 License

This skill is provided as-is for academic research purposes. Users are responsible for compliance with publisher terms and copyright laws.
