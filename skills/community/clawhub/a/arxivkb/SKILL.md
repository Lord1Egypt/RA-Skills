---
name: arxivkb
description: "Local arXiv paper manager with semantic search. Crawls arXiv categories, downloads PDFs, chunks content, and indexes with FAISS + Ollama embeddings. No cloud API keys required — everything runs locally."
metadata: {"openclaw":{"requires":{"bins":["python3","ollama"]}}}
---

# ArXivKB — Science Knowledge Base

## Why This Skill?

🏠 **100% local** — crawls arXiv's free API, embeds with Ollama (nomic-embed-text), indexes in FAISS + SQLite. No cloud cost.

🔍 **Semantic search on paper content** — FAISS indexes PDF chunks (not just abstracts), so you find papers by what they contain.

📂 **arXiv category-based** — tracks official arXiv categories (155 available, 8 groups). No free-text queries.

🧹 **Auto-cleanup** — configurable expiry deletes old papers, PDFs, and chunks.

## Install

```bash
python3 scripts/install.py
```

Works on **macOS and Linux**. Installs Python deps (`faiss-cpu`, `pdfplumber`, `tiktoken`, `arxiv`, `numpy`), pulls `nomic-embed-text` via Ollama, creates data directories and DB.

### Prerequisites

- **Ollama** — must be installed and running (`ollama serve`)
- **Python 3.10+**

## Quick Start

```bash
# 1. Add arXiv categories to track
akb categories add cs.AI cs.CV cs.LG

# 2. Browse all available categories
akb categories browse

# 3. Ingest recent papers (last 7 days)
akb ingest

# 4. Check stats
akb stats
```

## Categories

```bash
akb categories list                    # Show enabled categories
akb categories browse                  # Browse all 155 arXiv categories
akb categories browse robotics         # Filter by keyword
akb categories add cs.AI cs.RO         # Enable categories
akb categories delete cs.AI            # Disable a category
```

Categories are official arXiv codes (e.g. `cs.AI`, `eess.IV`, `q-fin.ST`). The full taxonomy is built in.

## Ingestion

```bash
akb ingest                    # Crawl, download PDFs, chunk, embed
akb ingest --days 14          # Look back 14 days
akb ingest --dry-run          # Preview only
akb ingest --no-pdf           # Index abstracts only (faster)
```

Pipeline: arXiv API → PDF download → text extraction (pdfplumber) → chunking (tiktoken, 500 tokens, 50 overlap) → embedding (Ollama nomic-embed-text) → FAISS + SQLite.

## Paper Details

```bash
akb paper 2401.12345    # Show title, abstract, categories, PDF status
```

## Statistics

```bash
akb stats   # Papers, chunks, categories, DB size
```

## Expiry & Cleanup

```bash
akb expire               # Delete papers older than 90 days (default)
akb expire --days 30     # Override: delete papers older than 30 days
akb expire --days 30 -y  # Skip confirmation
```

## Configuration

No config file needed. Defaults:

| Setting | Default | Override |
|---------|---------|----------|
| Data directory | `~/workspace/arxivkb` | `ARXIVKB_DATA_DIR` env or `--data-dir` |
| Ollama endpoint | `http://localhost:11434` | — (hardcoded) |
| Embedding model | `nomic-embed-text` (768d) | — (hardcoded) |
| Chunk size | 500 tokens, 50 overlap | — |
| Expiry | 90 days | `--days` flag |

## Data Layout

```
~/workspace/arxivkb/
├── arxivkb.db           # SQLite: papers, chunks, translations, categories
├── pdfs/                  # Downloaded PDF files ({arxiv_id}.pdf)
└── faiss/
    └── arxivkb.faiss    # FAISS IndexFlatIP (chunk embeddings)
```

## DB Schema

- **papers**: id, arxiv_id, title, abstract, categories, published, status, created_at
- **chunks**: id, paper_id, section, chunk_index, text, faiss_id, created_at
- **translations**: paper_id, language, abstract, created_at (PK: paper_id+language)
- **categories**: code, description, group_name, enabled, added_at (155 entries)

## 💬 Chat Commands (OpenClaw Agent)

When this skill is installed, the agent recognizes `/akb` as a shortcut:

| Command | Action |
|---------|--------|
| `/akb list` | Show enabled categories |
| `/akb add cs.AI cs.RO` | Enable categories for crawling |
| `/akb remove cs.AI` | Disable a category |
| `/akb browse` | Browse all 155 arXiv categories |
| `/akb browse robotics` | Filter categories by keyword |
| `/akb stats` | Show paper/chunk/category counts |
| `/akb help` | Show available commands |

The agent runs these via the `akb` CLI internally.

## 📱 PrivateApp Dashboard

A companion PWA dashboard is available. Provides:
- Semantic search across paper content
- Paper detail with abstract translation (on-demand via LLM)
- Inline PDF viewing
- Category browser
- Stats (papers, chunks, categories)

## Architecture

```
scripts/
├── cli.py             # CLI — categories, ingest, paper, stats, expire
├── db.py              # SQLite schema + CRUD
├── arxiv_crawler.py   # arXiv API search + PDF download
├── arxiv_taxonomy.py  # Full arXiv category taxonomy (155 categories)
├── pdf_processor.py   # PDF text extraction + tiktoken chunking
├── embed.py           # Ollama nomic-embed-text (768d, normalized)
├── faiss_index.py     # FAISS IndexFlatIP manager
├── search.py          # Semantic search: query → FAISS → group by paper
└── install.py         # One-command installer
```
