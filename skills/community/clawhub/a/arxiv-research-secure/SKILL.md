# ArXiv Research Assistant Secure

name: arxiv-research-secure  
description: Advanced ArXiv paper search with local caching, smart summarization, and research tracking. Secure alternative with no shell execution.

---

# ArXiv Research Assistant Secure

## Overview

Advanced research tool for ArXiv papers:
- **Smart search** — Multi-keyword, author, category filtering
- **Local caching** — Avoid repeated API calls, offline reading
- **AI summarization** — Automatic abstract extraction with LLM
- **Research tracking** — Log papers to structured markdown
- **PDF download** — Local storage with metadata
- **Zero shell** — Pure Python, no curl/wget/exec

## Security Model

### Network Isolation
```python
# Only HTTPS to export.arxiv.org
ALLOWED_HOSTS = ["export.arxiv.org", "arxiv.org"]
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
```

### Input Validation
```python
def validate_query(query: str) -> str:
    # Block injection attempts
    FORBIDDEN = [";", "|", "&", "$", "`", "\"", "'", "<", ">", "..", "//"]
    for char in FORBIDDEN:
        if char in query:
            raise ValueError(f"Invalid character in query: {char}")
    return query[:200]  # Max 200 chars
```

### Local Storage Only
```python
CACHE_DIR = WORKSPACE / ".arxiv_cache"
PAPERS_DIR = CACHE_DIR / "papers"
METADATA_DIR = CACHE_DIR / "metadata"

# No external network after download
# All operations on local files
```

## Capabilities

### 1. Search Papers
```bash
arxiv-secure search "transformer energy consumption" --max=10 --sort=relevance
arxiv-secure search "author:LeCun" --category=cs.LG
arxiv-secure search "LLM reasoning" --date-from=2024-01-01
```

### 2. Download & Cache
```bash
arxiv-secure fetch 2501.12345           # Download by ID
arxiv-secure fetch --search="query" --auto-download  # Download all results
```

### 3. Smart Summary
```bash
arxiv-secure summarize 2501.12345       # AI summary of paper
arxiv-secure summarize --file=paper.pdf # Summarize local PDF
```

### 4. Research Log
```bash
arxiv-secure log 2501.12345             # Add to research log
arxiv-secure log --search="query" --auto-log
arxiv-secure list-log                   # Show research history
arxiv-secure export-log --format=md     # Export for reports
```

### 5. Manage Cache
```bash
arxiv-secure cache-list                 # List cached papers
arxiv-secure cache-clear --older-than=30d
arxiv-secure cache-stats                # Disk usage
```

### 6. Batch Operations
```bash
arxiv-secure batch --search="volatility modeling" --max=20 --download --summarize --log
```

## Workflow Examples

### Daily Research Digest
```bash
# Morning: Check new papers on your topics
arxiv-secure search "quantitative finance volatility" --date-from=yesterday --max=5 --summarize

# Log interesting ones
arxiv-secure log 2501.12345
arxiv-secure log 2501.12346

# Export weekly report
arxiv-secure export-log --format=md --since=last-week > weekly_report.md
```

### Deep Research Session
```bash
# Search broadly
arxiv-secure search "transformer energy efficiency" --max=50

# Download all
arxiv-secure batch --search="transformer energy efficiency" --max=20 --download

# Summarize batch
arxiv-secure batch --ids=2501.12345,2501.12346,2501.12347 --summarize

# Log to research tracker
arxiv-secure batch --ids=2501.12345,2501.12346 --log
```

## Output Formats

### Console Table
```
ID          Title                          Authors        Date     Category
2501.12345  Energy-Efficient LLMs          Smith et al.   2025-01  cs.LG
2501.12346  Transformer Optimization         Chen et al.    2025-01  cs.CL
```

### Markdown Log
```markdown
## [2025-01-15] Research: Energy-Efficient LLMs
- **Paper**: Energy-Efficient Transformers for Edge Devices
- **Authors**: Smith, J., Chen, L., Kumar, R.
- **arXiv**: 2501.12345
- **Category**: cs.LG (Computation and Language)
- **Summary**: Proposes a novel pruning technique...
- **Relevance**: High - directly applicable to RTE volatility prediction models
- **Downloaded**: ✅ paper_2501.12345.pdf
```

### JSON Export
```json
{
  "query": "transformer energy",
  "date": "2025-01-15",
  "papers": [
    {"id": "2501.12345", "title": "...", "summary": "...", "relevance": 0.85}
  ]
}
```

## Resources

### scripts/
- `arxiv_client.py` — Secure API client with caching
- `paper_summarizer.py` — LLM-based summarization
- `research_logger.py` — Structured logging to markdown
- `pdf_downloader.py` — Safe PDF download and storage

### references/
- `arxiv_api_reference.md` — API documentation
- `research_templates.md` — Log templates and formats

### assets/
- `paper_template.md` — Default paper log template

