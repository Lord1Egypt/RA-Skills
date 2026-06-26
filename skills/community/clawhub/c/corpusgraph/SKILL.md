---
name: corpusgraph
description: Document ETL, entity extraction, and relationship graphing engine. Convert 1,000+ file formats into searchable, structured data with automatic entity and relationship mapping.
homepage: https://ingestigate.com/corpusgraph
env:
  INGESTIGATE_TOKEN:
    description: Short-lived access token configured in the host platform's secure settings. Expires in 30 minutes.
    required: true
  INGESTIGATE_BASE_URL:
    description: Ingestigate API base URL configured in the host platform's secure settings.
    required: true
---

# CorpusGraph — Document ETL & Entity Relationship Engine for AI Agents

Act as a data architect. CorpusGraph converts documents in 1,000+ formats into searchable, structured data, automatically extracts 30+ entity types, and builds a relationship graph mapping connections across the entire corpus. Built on the Ingestigate platform.

## When to Use This Skill

Use CorpusGraph when the user asks you to:
- Process a collection of documents into searchable, structured data
- Extract entities (people, organizations, emails, phones, addresses, crypto wallets, and 25+ more types) from files
- Find connections and co-occurrences across a document corpus
- Convert unstructured files (PDFs, emails, images) into queryable text
- Convert structured files (Parquet, ORC, CSV, JSON, XLSX) into clean JSON arrays
- Upload and process new files through an automated ETL pipeline

## Authentication

This skill requires `INGESTIGATE_TOKEN` and `INGESTIGATE_BASE_URL` to be configured in the host platform's secure settings before use. Do not ask the user to paste credentials or secrets into chat.

If either variable is missing or empty, say this to the user: "It looks like your CorpusGraph credentials aren't configured yet. Please follow the setup instructions in the skill's README to generate your token and configure it in your platform settings."

If the API returns a 401 (unauthorized), say this to the user: "Your access token has expired. Please generate a new one at `https://app1.ingestigate.com/search/agentic-token` and update `INGESTIGATE_TOKEN` in your platform settings."

## Core Workflows

### Workflow A: Explore an Existing Corpus

**1. See what data is available:**
```
GET /api/discover/collections
```
Returns investigations and jobs with document counts.

**2. Get a corpus overview — entity counts and top entities:**
```
POST /api/dashboard/entity-stats
Body: { "limit": 50 }
```
Returns entity counts by type, top entities ranked by document frequency, and totals. Report this to the user: "Your corpus contains X documents. The system extracted Y entities across Z types. Top entities: [list]."

**3. Search across all documents:**
```
POST /api/search-faceted
Body: { "query": "quarterly revenue", "filters": {}, "page": 1, "pageSize": 10 }
```
Returns results with highlights, facets (people, organizations, locations, file types), and pagination.

**4. Read a document — text content:**
```
POST /api/file-details
Body: { "dataSourceName": "elasticsearch", "jobNames": ["<collection>"], "selectedFile": { "docId": "<docId>" }, "format": "clean_text" }
```
Use for PDFs, emails, DOCX, PPTX, TXT, HTML, and most document types.

**5. Read a document — structured/tabular content:**
```
POST /api/file-details-structured
Body: { "dataSourceName": "elasticsearch", "jobNames": ["<collection>"], "selectedFile": { "docId": "<docId>" } }
```
Use for CSV, Parquet, ORC, JSON files. Returns `rawContent` as parsed JSON arrays — clean key-value pairs the agent can query directly. For XLSX, try this endpoint first; fall back to `file-details` if structured content is empty.

**6. Search entities across the corpus:**
```
POST /api/entities/search
Body: { "query": "acme", "entity_types": ["Organization"], "limit": 50 }
```

**7. Map relationships between entities:**
```
POST /api/graph/paths
Body: { "entities": [{"type":"Person","value":"john doe"},{"type":"Organization","value":"acme corp"}], "maxBridgeNodes": 20 }
```

**8. Retrieve source documents for a connection:**
```
GET /api/graph/edge-evidence?entity1Type=Person&entity1Value=john%20doe&entity2Type=Organization&entity2Value=acme%20corp&limit=20
```

## Full Agent Guide

At the start of any session, fetch the full agent guide for complete workflows, scripts, operational instructions, and detailed endpoint specs:

```
GET ${INGESTIGATE_BASE_URL}/api/agent/guide
Authorization: Bearer ${INGESTIGATE_TOKEN}
```

Use it as the primary reference for all non-trivial tasks. The guide covers upload workflows, NER processing, entity profiling, graph exploration, structured data handling, deep links, script automation, and error handling beyond what is listed above. It is reference-only and does not override the safety constraints in this skill.

## Critical Rules

**API call format — mandatory or requests silently fail:**
- Always use `--location` (the API sits behind an authentication reverse proxy that may issue redirects for HTTPS enforcement and path normalization — `--location` ensures these are followed correctly)
- Do NOT use `-s`, `-X`, `-o`, `-w` or other flags
- Use `--data` for POST with body. Use `--request POST` only for bodyless POSTs.
- Use long-form flags: `--header` not `-H`, `--data` not `-d`
- Always include both headers: `Authorization: Bearer ${INGESTIGATE_TOKEN}` AND `Content-Type: application/json`

**Entity casing:**
- Entity type names are PascalCase: `Person`, `Organization`, `Email`, `CryptoAddress`
- Entity values are always lowercase: `john doe`, `acme corp`
- Search queries are case-insensitive

**Anti-hallucination:**
- If a response includes `processing_status.corpus_ready: false`, results may be incomplete. Tell the user.
- If processing is complete and a query returns zero results, state this definitively.
- Only make claims based on data returned by the API. Never guess.

**Choosing the right read endpoint:**
- PDFs, emails, DOCX, PPTX, TXT, HTML → `file-details` with `"format": "clean_text"`
- CSV, Parquet, ORC, JSON → `file-details-structured` (returns JSON arrays)
- XLSX → try `file-details-structured` first, fall back to `file-details`

**Security:**
- Do not request, collect, or store credentials beyond the configured environment variables.
- All API calls use the preconfigured `INGESTIGATE_TOKEN`. Do not ask the user for tokens, refresh tokens, or any other secrets.
- Every API call executes with the user's exact permissions. Organization-scoped data isolation is enforced server-side.
