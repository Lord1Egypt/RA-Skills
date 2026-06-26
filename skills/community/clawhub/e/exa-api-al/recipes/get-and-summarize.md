# Recipe: Get and Summarize

## Goal
Given one or more URLs, fetch clean page text with Exa **contents** and produce a faithful, grounded summary per URL (and optionally a combined synthesis) with no claims beyond the retrieved text.

## When to use
- You already have URLs (from `search-the-web.md`, the user, or another recipe) and need their actual content distilled.
- The user says "summarize this page / these links."
- As the bridge between discovery (search) and writing (synthesis/answer).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `urls` | Yes | List of URLs (= Exa `id`s). |
| `text` | No | Request full clean text. |
| `highlights` | No | Request relevant snippets. |
| `summary` | No | Request Exa-generated summary (can take a `query` to focus it). |
| `summary.query` | No | Focus the summary on a specific question. |
| API key | Yes | Header `x-api-key`. Never hardcode. |

## Steps
1. **Collect & dedupe URLs.** Normalize (strip `utm_*`, fragments, trailing slash). Remove duplicates.
2. **Choose content mode.** For short distillation, request `highlights` or `summary` (cheaper, less text). For a faithful full read, request `text`. Use `summary.query` when you have a specific focus question.
3. **Call contents** with the URL list and chosen fields, header `x-api-key`.
4. **Validate per URL.** Some URLs may return empty/blocked content (paywall, JS-render). Mark these as "content unavailable" — do not summarize from the title alone.
5. **Summarize each URL strictly from its returned text/highlights.** No outside knowledge, no inference beyond the text. Preserve numbers, dates, named entities exactly.
6. **Attribute everything.** Keep the source URL attached to each summary so citations can be generated (`prompts/citation-generation.md`).
7. **(Optional) Combine** the per-URL summaries into one synthesis using `prompts/synthesis.md`, keeping per-claim attribution.
8. **Record `costDollars`** from the response.

## Output format
Per-URL:
```
Source: <title> — <url>  (published <date|unknown>)
Summary: <3–6 sentences, strictly from retrieved text>
Key facts:
- <fact> (from this source)
[content unavailable] if fetch failed
```
Footer:
```
Cost: $<costDollars>  | URLs fetched: <n ok>/<n total>
```

## Example
Input: `["https://example.org/paper-a"]`, request `summary` with `query:"energy density gains"`.
Output:
```
Source: Sulfide electrolyte advances — https://example.org/paper-a (published 2025-03-12)
Summary: The paper reports a sulfide-based solid electrolyte achieving X Wh/kg in lab cells,
up from Y in the prior generation, with stable cycling over N cycles...
Key facts:
- Reported energy density: X Wh/kg
- Cycle stability: N cycles at Z% retention
Cost: $0.004 | URLs fetched: 1/1
```

## Edge cases
- **Empty/blocked content:** report "content unavailable"; never summarize from URL/title.
- **Very long text:** prefer `highlights`/`summary` to cap tokens & cost, or chunk and summarize per chunk.
- **Mixed languages:** summarize in the user's language but keep quoted facts verbatim.
- **Conflicting facts across URLs:** keep both, attribute each, flag the conflict (don't silently pick one).
- **`400`:** malformed URL list — fix, don't retry blindly. **`401`:** key issue, stop. **`429`:** back off and retry.

## Production notes (incl. cost)
- Contents calls **add cost on top of** any prior search. Fetch only URLs you actually need (top-ranked winners), not every search hit.
- `summary`/`highlights` are cheaper (less text) than full `text`; choose the lightest mode that meets the need.
- Batch multiple URLs in one contents call where supported to reduce overhead.
- Track `costDollars` to the run ledger.

> Verification needed: confirm contents field names (`text`/`highlights`/`summary`), `summary.query` support, and batching limits with https://docs.exa.ai
