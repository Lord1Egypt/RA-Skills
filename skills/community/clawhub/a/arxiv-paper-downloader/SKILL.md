---
name: arxiv-paper-downloader
description: Download 47+ essential AI/ML papers from arXiv with pre-curated collections for agent testing, autonomous agents, and large language models
version: 1.0.7
author: geekbin
license: MIT
tags:
  - arxiv
  - paper
  - download
  - ai
  - machine-learning
  - llm
  - agents
  - research
  - latest
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python
    install:
      - kind: uv
        package: requests
---

# arXiv Paper Downloader

Download AI/ML papers from arXiv with pre-curated collections.

## Features

- 47+ pre-curated papers across 3 categories
- Direct PDF download (no API rate limits)
- Batch download with metadata export

## Categories

| Category | Papers |
|----------|--------|
| `agent_testing` | 19 |
| `agents` | 12 |
| `llm` | 15 |

## Usage

```python
# Download by category
download_papers("agent_testing")
download_papers("all")

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
