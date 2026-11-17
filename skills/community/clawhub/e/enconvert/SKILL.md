---
name: enconvert
description: Render web pages and files into agent-ready markdown, structured data, screenshots, and PDFs via EnConvert, with a render_quality honesty score on every read.
version: 0.0.2
author: EnConvert
tags:
  - web
  - scraping
  - conversion
  - markdown
  - pdf
  - rag
metadata:
  openclaw:
    requires:
      env:
        - ENCONVERT_API_KEY
      bins:
        - curl
    primaryEnv: ENCONVERT_API_KEY
    envVars:
      - name: ENCONVERT_API_KEY
        required: true
        description: EnConvert private API key (sk_...) from https://www.enconvert.com/dashboard/api-keys. Public pk_ keys are rejected with 403.
    emoji: "🔎"
    homepage: https://www.enconvert.com/docs
---

# EnConvert

EnConvert renders web pages and files into agent-ready data: clean **markdown**,
**structured JSON**, **screenshots**, and **PDFs**. Every page read comes back with a
**`render_quality`** score (0.0-1.0) — an honesty signal for how well the page actually
rendered, so a blocked, empty, or bot-walled page is flagged rather than silently trusted.

Use this skill when the task involves: reading a URL into markdown, searching the web,
crawling a site for its URLs, extracting structured fields from pages, or converting an
uploaded/hosted file into markdown or PDF.

## Authentication

- **Base URL:** `https://api.enconvert.com`
- **Header:** `X-API-Key: <key>` on every EnConvert API call. **Never `Authorization: Bearer`.**
- **The key** is the user's **private** key (prefix `sk_`). Read it from the
  `ENCONVERT_API_KEY` secret/env. **Never hardcode it, never print it, never put it in a URL.**
  Public `pk_` keys are rejected with `403`.
- **Validate a key** before real work with `GET /v1/whoami` (header `X-API-Key`):
  `200 {"project_id":..., "plan_slug":...}` means good; `401`/`403` means missing, invalid,
  or a `pk_` key was used.

> Two fetches in this skill deliberately carry **no** `X-API-Key` header: (1) downloading a
> user-supplied source file URL before a convert, and (2) fetching a `presigned_url` /
> signed output URL. Sending the key to those would leak it to a third-party host. See below.

---

## Operations

### 1. Perceive URL

Read one URL into agent-ready outputs.

- **Method / URL:** `POST /v2/perceive`
- **Headers:** `X-API-Key`, `Content-Type: application/json`
- **Body (JSON):**
  - `url` (string, required)
  - `outputs` (string[], optional) — default `["markdown","structured"]`. Allowed:
    `markdown`, `html_cleaned`, `html_raw`, `screenshot`, `screenshot_full_page`, `pdf`,
    `links`, `images`, `structured`.
  - `only_main_content` (bool, optional) — strip nav/footer/boilerplate.
- **Response:** `{ "render_quality": 0.0-1.0, "outputs": { "<name>": { "url", "object_key", "size_bytes", "content_type", "expires_in" } }, "structured": {...}, "status", ... }`
  - **Every artifact under `outputs` is a 15-minute signed URL, markdown included** — never
    inline text. `outputs.markdown.url` is a URL you must `GET` (with **no** `X-API-Key`) to
    read the page. Same for `html_cleaned`, `html_raw`, `screenshot`, `screenshot_full_page`,
    `pdf`, `links`, `images`.
  - `structured` is the exception: it comes back **inline at the top level** of the response,
    not under `outputs`.
  - **Always read `render_quality`.** A low score means the render is degraded (bot wall,
    empty body, JS that never settled) — surface it, don't present the content as reliable.
    **Below 0.40 is not content**: report the score and `deductions` (e.g. `anti_bot_challenge`,
    `http_error`, `login_wall`) instead of quoting the page.
  - **A detected block is a normal `200`** with `"is_blocked": true`, `"outputs": {}` and
    `"billed": false` — there is nothing to fetch and the read was not charged. Say the page
    was blocked; do not retry the same URL expecting a different answer. `billed` is also
    `false` when `deductions` contain `http_error` or `login_wall`.

### 2. Web Search

- **Method / URL:** `POST /v2/lookup`
- **Headers:** `X-API-Key`, `Content-Type: application/json`
- **Body (JSON):**
  - `query` (string, required)
  - `category` (optional) — `web` (default) | `news` | `images` | `scholar` | `patents` | `maps`
  - `num_results` (int, optional, default 10), `page` (int, optional)
  - `country`, `locale`, `location` (strings, optional)
  - `time_filter` (optional) — `hour` | `day` | `week` | `month` | `year`
  - `autocorrect` (bool, optional)
- **Response:** `{ "results": [ { "title", "url", "snippet", "position" }, ... ], ... }`

### 3. Discover URLs

Enumerate the URLs of a site (for a follow-up perceive/distill).

- **Method / URL:** `POST /v2/discover`
- **Headers:** `X-API-Key`, `Content-Type: application/json`
- **Body (JSON):**
  - `url` (string, required)
  - `mode` (optional) — `sitemap` | `crawl` | `hybrid` (default)
  - `max_urls` (int, optional, default 100), `max_depth` (int, optional, default 2)
  - `include_patterns` / `exclude_patterns` (string[], optional)
  - `same_domain_only` (bool, optional, default `true`)
  - `respect_robots` (bool, optional, default `false`)
- **Response:** `{ "urls": [ ... ], "total", ... }`

### 4. Extract Structured (Distill)

Pull typed fields off one or many pages against a schema.

- **Method / URL:** `POST /v2/distill`
- **Headers:** `X-API-Key`, `Content-Type: application/json`
- **Body (JSON):**
  - `schema` (object, required) — a JSON-Schema `{"type":"object","properties":{...}}`
    **or** a flat `{ "field": "description" }` map.
  - **Provide exactly one source:**
    - `urls` (string[], max 50), **or**
    - `discover_from` (object) — `{ "url", "max_pages"?, "mode"? }` to crawl then extract.
  - `css_schema`, `wait_for` (optional)
- **Response:** `{ "operation_id", "total", "completed", "failed", "total_cost_cents",
  "results": [ { "url", "status", "data", "extraction_tier", "render_quality", ... } ] }`
  — the extracted fields are **per URL**, in `results[].data`. There is no top-level `data`
  or `extraction_tier`.

### 5. Convert File to Markdown

Convert any uploaded/hosted file (PDF, DOCX, PPTX, XLSX, HTML, ...) into markdown.

- **Method / URL:** `POST /v1/convert/anything-to-markdown`
- **Headers:** `X-API-Key` (do **not** set `Content-Type` yourself — the multipart
  boundary sets it)
- **Body:** `multipart/form-data` with a single field named **`file`** (the file bytes).
- **Response:** `{ "presigned_url": "...", ... }` — the markdown output. **Fetch
  `presigned_url` with a plain GET and no `X-API-Key` header.**

**When the user gives a URL, not a local path** (the normal case on an agent platform):
1. `GET` the source URL to get the bytes — **no `X-API-Key` header** (it is a third-party host).
2. `POST` those bytes as multipart field `file` to the endpoint above **with `X-API-Key`**.
3. Read `presigned_url` from the JSON, then `GET` it **without `X-API-Key`** for the result.

The bundled `scripts/convert.sh` does exactly this end to end (see Examples).

### 6. Convert File to PDF

Same contract as #5, different endpoint and output.

- **Method / URL:** `POST /v1/convert/anything-to-pdf`
- **Headers / Body:** identical to #5 — multipart field **`file`**, `X-API-Key`, no manual
  `Content-Type`.
- **Response:** `{ "presigned_url": "...", ... }` — the PDF. Fetch it with no `X-API-Key`.
- **URL-in flow:** identical to #5 (download source with no key → multipart post with key →
  fetch presigned result with no key).

---

## Fetching signed / presigned URLs

All output URLs — perceive's `screenshot`/`pdf`/`html_*` (15-minute signed) and convert's
`presigned_url` — are pre-authenticated. **Fetch them with a plain GET and NO `X-API-Key`
header.** Adding the key leaks your credential to the storage host and is unnecessary; the
signature in the URL is the auth.

## Usage examples

**Perceive a URL to markdown:**
```bash
curl -sS -X POST https://api.enconvert.com/v2/perceive \
  -H "X-API-Key: $ENCONVERT_API_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","outputs":["markdown"],"only_main_content":true}'
# -> read .render_quality first, then GET .outputs.markdown.url (no X-API-Key)
```

**Convert a PDF URL to markdown** (download-then-multipart, key never touches the source host):
```bash
scripts/convert.sh markdown "https://example.com/whitepaper.pdf"
# prints the presigned_url of the markdown result; GET it without the key
```

**Search, then perceive the top result:**
```bash
TOP=$(curl -sS -X POST https://api.enconvert.com/v2/lookup \
  -H "X-API-Key: $ENCONVERT_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"open source vector database","num_results":5}' \
  | grep -o '"url":"[^"]*"' | head -n1 | cut -d'"' -f4)
curl -sS -X POST https://api.enconvert.com/v2/perceive \
  -H "X-API-Key: $ENCONVERT_API_KEY" -H "Content-Type: application/json" \
  -d "{\"url\":\"$TOP\",\"outputs\":[\"markdown\"]}"
```

## Errors

- `401` / `403` — key missing, invalid, or a public `pk_` key was used. Use a private
  `sk_` key from https://www.enconvert.com/dashboard/api-keys.
- `422` — bad body (e.g. distill given both `urls` and `discover_from`, or neither).
- Low `render_quality` is **not** an HTTP error — it is a content-quality warning inside a
  `200`. Check it on every perceive; under 0.40 is not content.
- A blocked page is also a `200`: `is_blocked: true`, empty `outputs`, `billed: false`.
- `429` — rate limited. Wait for the `Retry-After` header's seconds before retrying.

Docs: https://www.enconvert.com/docs
