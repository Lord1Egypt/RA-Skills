# civil-judgment-taiwan-vectorstore

An [OpenClaw](https://openclaw.dev) skill that ingests **Taiwan civil court judgment** (民事判決) HTML/PDF files into [Qdrant](https://qdrant.tech) using [Ollama](https://ollama.com) embeddings, enabling semantic RAG search over legal documents.

> **Scope**: This skill is exclusively designed for Taiwan civil judgments sourced from the Judicial Yuan's FJUD/FINT systems. It is not intended for criminal, administrative, or non-Taiwan judgments.

## What it does

- Parses HTML and PDF Taiwan civil judgment files deterministically (BeautifulSoup / pypdf)
- Splits documents into section-aware chunks based on Taiwan civil judgment structure (主文, 事實, 理由, etc.)
- Extracts rich metadata: court, tier, date, case number, cited legal norms (民法/民事訴訟法 citations), reasoning snippets, candidate issues (爭點)
- Embeds chunks via Ollama (`bge-m3:latest`, 1024 dims)
- Upserts into Qdrant with deterministic UUIDs — safe to re-run on the same folder

## Collections

| Collection | Granularity |
|---|---|
| `civil_case_doc` | 1 point per judgment document |
| `civil_case_chunk` | Many section-aware chunks per document |

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) with `bge-m3:latest` pulled
- [Qdrant](https://qdrant.tech) running (default: `http://localhost:6333`)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 pypdf qdrant-client
```

## Usage

```bash
source .venv/bin/activate

python3 scripts/ingest.py \
  --run-folder /path/to/judicialyuan-search/output/<RUN_FOLDER>
```

Override service endpoints via flags or environment variables:

```bash
OLLAMA_URL=http://localhost:11434 QDRANT_URL=http://localhost:6333 \
  python3 scripts/ingest.py --run-folder <RUN_FOLDER>
```

See [SKILL.md](SKILL.md) for the full usage guide including troubleshooting, CLI reference, and output descriptions.

## Key design principles

- **Taiwan civil judgments only**: metadata schema, section headings, and extraction rules are tuned specifically for Taiwan civil court document structure
- **Deterministic**: same input → same SHA-256 → same Qdrant point IDs; re-runs are safe (upsert = overwrite)
- **Traceable**: every point carries `doc_url` and `local_path`
- **Immutable source**: raw HTML/PDF is never modified; it is the source of truth
- **Parser versioned**: `parser_version` field in every point's metadata; bump on any parsing rule change

## License

MIT — see [LICENSE](LICENSE).
