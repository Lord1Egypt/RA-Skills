---
name: 3gpp-scout
description: Semantic search over 3,200+ 3GPP technical specifications (TS/TR series, Rel-15 and Rel-19). Search text, diagrams, and figures across 904K+ vectors.
version: 1.0.2
homepage: https://3gppscout.com
metadata:
  openclaw:
    requires:
      env:
        - SCOUT_API_KEY
    primaryEnv: SCOUT_API_KEY
---

# 3GPP Scout API — Agent Skill Guide

You have access to the 3GPP Scout API, a semantic search engine over
3GPP technical specifications. Use it to find specific information
in 3GPP standards documents (TS and TR series).

## Provider & Pricing

**Provider:** [Carrot Labs](https://carrotlabs.ai)
**Homepage:** [3gppscout.com](https://3gppscout.com)
**Dashboard:** [dashboard.3gppscout.com](https://dashboard.3gppscout.com)
**API Docs:** [api.3gppscout.com/docs](https://api.3gppscout.com/docs)
**Terms of Service:** [3gppscout.com/terms](https://3gppscout.com/terms)
**Privacy Policy:** [3gppscout.com/privacy](https://3gppscout.com/privacy)

This is a **paid API service**. Each API call costs a small amount against
your account's credit balance. New accounts receive free starter credits
(worth a few hundred API calls) so you can evaluate the service before
purchasing additional credits. You can view your balance, usage history,
and buy additional credits at [dashboard.3gppscout.com](https://dashboard.3gppscout.com).

## Base URL

```
https://api.3gppscout.com
```

## Authentication

All search and document endpoints require a Bearer token (API key).

**How to get an API key:**
1. Sign up or log in at [dashboard.3gppscout.com](https://dashboard.3gppscout.com)
2. Go to the **API Keys** page
3. Create a new key — it will start with `sk-`

**Set your API key** via environment variable:
```
export SCOUT_API_KEY="sk-your-key-here"
```
Or set `skills."3gpp-scout".apiKey` / `skills."3gpp-scout".env.SCOUT_API_KEY` in `~/.openclaw/openclaw.json`.

The key is included in every request as a Bearer token:
```
Authorization: Bearer $SCOUT_API_KEY
```

## Available Endpoints

### POST /search/text

Semantic search over specification text. This is your primary tool.

**Request body (JSON):**

| Parameter              | Type   | Default | Description                                     |
|------------------------|--------|---------|-------------------------------------------------|
| query                  | string | —       | **Required.** Natural language search query      |
| match_count            | int    | 30      | Candidate matches before reranking (1–200)       |
| match_threshold        | float  | 0.0     | Minimum similarity score (0–1)                   |
| rerank                 | bool   | true    | Rerank results for higher precision              |
| rerank_top_k           | int    | 10      | Results to keep after reranking (1–50)           |
| include_section_text   | bool   | true    | Include the full parent section text             |
| filter_release         | string | null    | e.g. "Rel-19", "Rel-15"                         |
| filter_doc_type        | string | null    | "TS" or "TR"                                     |
| filter_doc_number      | string | null    | e.g. "38.331", "23.501"                          |
| filter_series          | string | null    | e.g. "38" (NR/5G), "23" (system architecture)   |
| filter_section_number  | string | null    | e.g. "5.3.3"                                     |

**Response fields:**

| Field           | Type          | Description                                |
|-----------------|---------------|--------------------------------------------|
| query           | string        | Echo of the search query                   |
| results         | TextResult[]  | Matching text chunks                       |
| total           | int           | Number of results returned                 |
| reranked        | bool          | Whether reranking was applied              |
| elapsed_ms      | float         | Server processing time in ms               |

Each **TextResult** contains:
- `doc_number`, `doc_type`, `version`, `release` — document metadata
- `section_number`, `section_title` — which section the chunk is from
- `content` — the matched text chunk
- `similarity` — semantic similarity score (0–1)
- `relevance_score` — reranker score (0–1), present when reranked
- `section_text` — full parent section text (when include_section_text=true)
- `section_token_count` — token count of the parent section

### POST /search/images

Semantic search over figures, diagrams, and tables in specifications.

**Request body (JSON):**

| Parameter          | Type   | Default | Description                            |
|--------------------|--------|---------|----------------------------------------|
| query              | string | —       | **Required.** Natural language query   |
| match_count        | int    | 10      | Number of results (1–50)               |
| match_threshold    | float  | 0.3     | Minimum similarity (0–1)               |
| filter_release     | string | null    | e.g. "Rel-19"                          |
| filter_doc_number  | string | null    | e.g. "38.300"                          |
| filter_series      | string | null    | e.g. "38"                              |

Each **ImageResult** contains:
- `doc_number`, `doc_type`, `version`, `release` — document metadata
- `section_number` — which section the image is in
- `caption` — figure/table caption
- `context_before`, `context_after` — surrounding text
- `image_path` — path to the image file
- `similarity` — semantic similarity score

### POST /search/combined

Text + image search in a single request. Useful for broad questions where
both text passages and diagrams are relevant.

**Request body (JSON):**

| Parameter              | Type   | Default | Description                               |
|------------------------|--------|---------|-------------------------------------------|
| query                  | string | —       | **Required.** Natural language query       |
| text_match_count       | int    | 30      | Text candidates before reranking (1–200)   |
| text_match_threshold   | float  | 0.0     | Text similarity threshold (0–1)            |
| rerank                 | bool   | true    | Rerank text results                        |
| rerank_top_k           | int    | 10      | Text results after reranking (1–50)        |
| include_section_text   | bool   | true    | Include full parent section text           |
| image_match_count      | int    | 5       | Image results to return (1–50)             |
| image_match_threshold  | float  | 0.0     | Image similarity threshold (0–1)           |
| filter_release         | string | null    | Filter both searches by release            |
| filter_doc_type        | string | null    | Filter text search by doc type             |
| filter_doc_number      | string | null    | Filter both searches by document           |
| filter_series          | string | null    | Filter both searches by series             |
| filter_section_number  | string | null    | Filter text search by section              |

**Response** has `text_results` (TextResult[]) and `image_results` (ImageResult[]).

### GET /documents

List available 3GPP documents with metadata. Use filters to check if a specific
document or release is indexed — this is fast (1-2 lookups). Without filters
returns all ~3,200 documents which is slower.

**Query parameters:**

| Parameter   | Type   | Default | Description                                        |
|-------------|--------|---------|----------------------------------------------------|
| doc_number  | string | null    | Filter by document number, e.g. "38.811". **Recommended.** |
| release     | string | null    | Filter by release, e.g. "Rel-19"                   |
| series      | string | null    | Filter by series, e.g. "38"                         |
| doc_type    | string | null    | Filter by type: "TS" or "TR"                        |

**Example:** Check if TR 38.811 has a Rel-19 version:
```
GET /documents?doc_number=38.811&release=Rel-19
```

### GET /documents/{document_id}

Get a single document by its numeric ID.

### GET /sections

Fetch full section text by section number.

**Query parameters:**

| Parameter       | Type   | Default | Description                                      |
|-----------------|--------|---------|--------------------------------------------------|
| section_number  | string | —       | **Required.** e.g. "5.3.3"                        |
| doc_number      | string | null    | Document number — always provide this              |
| version         | string | null    | e.g. "19.1.0"                                     |
| release         | string | null    | e.g. "Rel-19"                                     |
| prefix          | bool   | false   | Match sub-sections too (e.g. "5.4" gets "5.4.1") |

### GET /sections/toc

Table of contents for a document — section numbers and titles without full text.

**Query parameters:**

| Parameter   | Type   | Default | Description                      |
|-------------|--------|---------|----------------------------------|
| doc_number  | string | —       | **Required.** e.g. "38.321"      |
| version     | string | null    | e.g. "19.1.0"                    |

### GET /images/{doc_number}/{version}/{image_index}

Fetch an extracted image (PNG) from a specification. No authentication required.

The `image_path` field in image search results (e.g. `/images/38.300/19.1.0/5`)
maps directly to this endpoint. Construct the full URL as:

```
https://api.3gppscout.com/images/{doc_number}/{version}/{image_index}
```

Returns `image/png` on success, 404 if the image doesn't exist.

## Corpus Coverage

The index currently covers:
- **Rel-15** — 1,493 documents, 195K sections
- **Rel-19** — 1,789 documents, 291K sections
- **Total** — 3,282 documents, 486K sections

Series 38 = NR/5G, 23 = system architecture, 24 = signaling protocols,
36 = LTE, 33 = security, 29 = core network protocols.

## Recommended Workflows

### Finding specific technical details

1. Use `POST /search/text` with a focused query and `rerank_top_k: 5`
2. Read the `content` field for the matched chunk
3. Read `section_text` for the full section context
4. If you need the broader document structure, call `GET /sections/toc`
   with the `doc_number` from the result

### Exploring a specific document

1. Get the table of contents: `GET /sections/toc?doc_number=38.331`
2. Fetch a specific section: `GET /sections?section_number=5.3.3&doc_number=38.331`
3. Use `prefix=true` to get a section and all its sub-sections

### Broad topic research

1. Use `POST /search/combined` to get both text and diagrams
2. Use `filter_series` to narrow to a domain (e.g. "38" for NR)
3. Increase `rerank_top_k` to 15–20 for more diverse results

### Comparing across releases

1. Search with `filter_release: "Rel-15"` for the original version
2. Search again with `filter_release: "Rel-19"` for the latest
3. Compare the section text to see what changed

## Tips for Best Results

- **Always use reranking** (enabled by default). The `relevance_score` from
  the reranker is a much better quality signal than raw `similarity`.
- **Use filters to narrow scope.** If you know which spec you're looking for,
  `filter_doc_number` dramatically improves result quality.
- **Use `include_section_text: true`** (the default) to get the full parent
  section. The `content` field is a chunk (~400-800 tokens), while
  `section_text` gives the complete section for full context.
- **Cite results precisely.** When presenting results to users, always include
  the document number, section number, and release. For example:
  "According to TS 38.331 Section 5.3.3 (Rel-19)..."
- **Use the TOC endpoint** before diving deep into a document. It helps you
  understand the document structure and find the right section numbers.
- **Prefer `/search/text` over `/search/combined`** when you only need text.
  Combined search is slower because it queries both indexes.
- **Don't set `match_threshold` too high.** The default of 0.0 with reranking
  gives the best results. The reranker handles quality filtering.
- **Render images from search results.** Image search results include
  `image_path` (e.g. `/images/38.300/19.1.0/5`). Construct the full URL:
  `https://api.3gppscout.com{image_path}`. No authentication required.

## Data & Privacy

Queries you send to this API are processed by the 3GPP Scout service to
perform vector search. The API does not store your queries beyond transient
usage logs for billing. The corpus consists entirely of publicly available
3GPP specifications — no proprietary or user-supplied data is stored in the
search index. See [3gppscout.com/privacy](https://3gppscout.com/privacy)
for the full privacy policy.
