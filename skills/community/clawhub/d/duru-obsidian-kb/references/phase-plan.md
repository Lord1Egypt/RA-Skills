# Phase Plan

## Phase 1 — Scaffold and deterministic workflow

Goal: make the KB usable immediately with low risk.

Capabilities:

- initialize KB directories
- ingest URLs and local files into manifest
- extract normal web articles into markdown when possible
- clone and summarize GitHub repositories
- generate source pages, concept pages, backlinks, and indexes
- create markdown output scaffolds
- lint structure and metadata

Non-goals:

- full article extraction quality guarantees
- advanced concept clustering beyond tags
- semantic search
- embeddings
- autonomous deep synthesis
- graph visualization

## Phase 2 — Better acquisition and richer compilation

Possible additions:

- webpage extraction via fetch/browser pipeline
- PDF text extraction
- git repo summarization
- tag suggestion
- concept-page generation
- backlink maintenance
- duplicate detection by similarity

## Phase 3 — Research copilot mode

Possible additions:

- local search CLI
- hybrid retrieval
- periodic health checks
- issue queues for incomplete sources
- concept memo auto-refresh and synthesis
- slide/chart generation
- weekly digest generation
- filing outputs back into the wiki automatically
