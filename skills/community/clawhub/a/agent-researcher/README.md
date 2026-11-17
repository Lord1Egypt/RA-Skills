# Research Assistant 🔬

**Knowledge builder that extracts entities, relationships, and key facts from web pages, documents, and files. Builds a searchable knowledge base with entity resolution and auto-summarization.**

> **Read the "Security & Privacy" section before using.** This tool makes outbound HTTP requests to user-supplied URLs and writes all extracted content to persistent local files. These behaviors cannot be disabled.

## Why Research Assistant?

Information is everywhere — web pages, documents, code files, emails. Research Assistant makes it *usable*:

- **Entity extraction** — Automatically finds proper names, dates, URLs, and key concepts
- **Searchable knowledge base** — Queries across everything you've processed
- **Knowledge graph** — Visualize entity relationships and connections
- **Domain filtering** — Focus on specific topics or sources
- **Auto-summarization** — Key entities and sources at a glance
- **Pure Node.js** — No npm runtime dependencies

## ⚠️ What This Tool Does (Honest Description)

- **Outbound HTTP**: `--extract <url>` fetches remote URLs. No allowlist, no rate limit, no proxy, no SSRF protection. Treat this as remote network exposure — only point it at URLs you would type into a browser.
- **Persistent local storage**: Every extraction (URL or local file) is written to `memory/research/` and kept forever. There is no automatic retention or deletion.
- **Email extraction is disabled** at the code level (see `extractEntities()` line 90), but emails can still appear inside fetched HTML or in source text — they are stored in the `summary` field.
- **No shell execution, no system calls, no subprocess spawning.** The only network I/O is `--extract <url>` via Node's built-in `http`/`https` modules.

---

## Installation

```bash
# Already included in OpenClaw workspace at skills/research-assistant/
# No npm install needed — pure Node.js
```

---

## Quick Start

```bash
# Extract entities from text
node skills/research-assistant/research-assistant.js --extract "John Doe joined the project on 2026-06-15"

# Search existing knowledge base
node skills/research-assistant/research-assistant.js --search "John Doe"

# Add to knowledge base
node skills/research-assistant/research-assistant.js --add "document-id" --source "report.md"

# Show knowledge graph
node skills/research-assistant/research-assistant.js --graph

# Summarize knowledge base
node skills/research-assistant/research-assistant.js --summarize
```

---

## Commands Reference

### Entity Extraction

```bash
node skills/research-assistant/research-assistant.js --extract <text>
```

Extracts from unstructured text:
- **Proper nouns** — Names, places, organizations
- **Dates** — ISO dates, partial dates, date ranges
- **URLs** — http/https links
- **Numbers** — Counts, IDs, versions
- **Key phrases** — Multi-word concepts (via NLP-like heuristics)

Email address extraction is **disabled** in code. Emails may still appear in the stored `summary` field (first 200 chars of source).

```
[research-assistant] Extracted 3 entities:
  John Doe (proper_noun) × 2
  2026-06-15 (number)
  https://example.com (url)
```

---

### Knowledge Base Operations

```bash
# Search
node skills/research-assistant/research-assistant.js --search "query"

# Add content to KB
node skills/research-assistant/research-assistant.js --add <id> --source <source>

# List KB entries
node skills/research-assistant/research-assistant.js --list
```

The knowledge base is stored as JSON in `memory/research/` under your workspace root.

---

### Knowledge Graph

```bash
# Show full graph
node skills/research-assistant/research-assistant.js --graph

# Filter by domain
node skills/research-assistant/research-assistant.js --graph --domain "example.com"
```

Displays:
- **Sources** — Total entries in KB
- **Entities** — Unique entities with occurrence counts
- **Relations** — Connections between entities
- **Domain filter** — Restrict to specific source domains

---

### Summarization

```bash
node skills/research-assistant/research-assistant.js --summarize
```

Returns a summary of the knowledge base:
```
[research-assistant] Summary:
  Total entries: 5
  Total entities: 12
  Total relations: 3
  Key entities:
    John Doe (3 occurrences across 2 sources)
    API (2 occurrences across 2 sources)
  Sources: report.md, documentation.md
```

---

## Data Storage

All state stored in `memory/research/`:

| File | Description |
|------|-------------|
| `kb.json` | Knowledge base entries with entities, relations, summaries |
| `entity-index.json` | Quick-lookup index for entity search |

These files persist indefinitely. There is no retention limit or built-in cleanup. Delete manually if needed.

---

## Security & Privacy

| Behavior | Status |
|----------|--------|
| **Outbound HTTP on URL extract** | ⚠️ No allowlist, no SSRF protection, no proxy, 10s timeout, real IP exposed |
| **Email extraction (entities)** | ✅ Disabled in code (see `extractEntities()` line 90) |
| **Email storage (in summaries/HTML)** | ⚠️ May still appear — review before sharing |
| **No shell execution** | ✅ Pure Node.js, no exec/system calls |
| **Input validation** | ✅ All text inputs sanitized |
| **Null-safe iteration** | ✅ Defensive programming |
| **Persistent local storage** | ⚠️ Writes to `memory/research/` and keeps forever |

⚠️ **Privacy Warning**: Extracted entities (URLs, proper nouns, numbers) and full content summaries are persisted indefinitely in `memory/research/kb.json`. There is no built-in retention limit, deletion command, or redaction. Do not use this tool on confidential documents or pages containing PII.

⚠️ **URL Extraction Warning**: `--extract <url>` makes outbound HTTP requests to user-supplied destinations. **There is no SSRF protection** — internal/private network URLs are NOT blocked. The fetched content is stored locally and indexed. Only point this tool at URLs you trust.

---

## Programmatic API

```javascript
const RA = require('./skills/research-assistant/research-assistant.js');

// Extract entities from text
const entities = RA.extractEntities('John Doe at example.com since 2026');

// Search knowledge base
const results = RA.searchKB('John Doe');

// Add to knowledge base
RA.addToKB({
  id: 'doc-1',
  entities: [{ name: 'John Doe', type: 'proper_noun', count: 2 }],
  relations: [],
  summary: 'John Doe works on the API project.',
  source: 'report.md'
});

// Show summary
RA.showSummary();
```

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `RESEARCH_DIR` | Override knowledge base data directory |

### Default Paths

| Resource | Path |
|----------|------|
| Knowledge base | `<WORKSPACE>/memory/research/kb.json` |
| Entity index | `<WORKSPACE>/memory/research/entity-index.json` |

---

## Examples

### Research a Topic
```bash
node skills/research-assistant/research-assistant.js --extract "Dr. Jane Smith, PhD, joined the AI team at MIT on 2022-09-01"
# Extracts: Jane Smith (proper_noun), 2022-09-01 (number), MIT (proper_noun)
# Note: email extraction is disabled; no email entity will be created
```

### Build a Knowledge Base from Docs
```bash
# Extract from multiple sources
node skills/research-assistant/research-assistant.js --add "doc-1" --source "architecture.md"
node skills/research-assistant/research-assistant.js --add "doc-2" --source "api-spec.md"

# Search across all sources
node skills/research-assistant/research-assistant.js --search "API"
```

### Visualize Connections
```bash
node skills/research-assistant/research-assistant.js --graph --domain "docs.example.com"
```

---

## License

MIT — Part of the OpenClaw skill ecosystem.

---

## Related Skills

- **Smart Files** — Content-aware file search and organization
- **Notification Triage** — Smart filtering and classification
- **Email Manager** — Email organization and search
