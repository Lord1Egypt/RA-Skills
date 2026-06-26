# arXiv Paper Downloader

Download 47+ essential AI/ML papers from arXiv with pre-curated collections.

## Features

- 47+ pre-curated papers across 3 categories
- Direct PDF download (no API rate limits)
- Batch download with metadata export

## Quick Start

```python
# Download by category
download_papers("agent_testing")  # 19 papers
download_papers("agents")         # 12 papers
download_papers("llm")            # 15 papers
download_papers("all")            # 47 papers total

# Download specific papers
download_by_arxiv_ids(["2310.06129", "2402.01031"])

# List categories
list_categories()
```

## Requirements

- Python 3.9+
- requests>=2.28.0

## License

MIT
