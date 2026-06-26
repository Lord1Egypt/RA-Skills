---
name: astro-arxiv-search
description: Retrieve astronomy and astrophysics papers from the user's arXiv mirror API. Use when Codex needs to list papers from a given arXiv day, find papers related to an astronomy topic over a recent period, find papers similar to a given arXiv paper, or fetch details for a specific arXiv ID. Prioritize this API whenever the user wants astronomy paper discovery or lookup; if the API is unavailable or unusable, fall back to other available search methods. Default to an astronomy-researcher audience and interpret ambiguous topics in an astronomy context unless the user says otherwise.
---

# Astro Arxiv Search

## Overview

Use the user's API instead of general web search for astronomy paper discovery.
Prefer lightweight listing first, then fetch more detail only for the papers the user actually cares about.
Treat this API as the primary retrieval method for astronomy paper requests and only fall back to other methods if the API is unavailable, errors out, or clearly cannot answer the request.

## Choose The Endpoint

- Use `/ai/by-date` to answer "what papers appeared on arXiv that day?", "what astro-ph papers were posted today/yesterday/on a given day?", or navigation requests such as "what was on the previous update day?".
- Use `recommend` with `topic=...` to answer "what papers were published in this area over the last month/week/year?", "were there any papers on this topic today?", or "show me the top papers related to this topic".
- Use `recommend` with `arxiv_id=...` and `period=500` to answer "find papers similar to this one", "what are the related papers for this article?", or "recommend papers similar to 2306.15611".
- Use `article/{arxiv_id}` to answer "show me this paper", "give me the abstract/authors/categories", or any follow-up on a specific paper ID.

Read `references/api.md` only when exact parameter names, response fields, or example mappings are needed.

## Retrieval Priority

- For astronomy and astrophysics paper discovery, use this API first.
- If the API is unavailable, repeatedly failing, or missing the capability needed for the request, fall back to other search methods available in the environment.
- When falling back, prefer structured or official paper sources before generic web search when those options are available.
- When falling back, keep the same response discipline: use the user's language by default, report exact dates when relevant, and avoid hallucinating unavailable metadata.

## Handle Dates Carefully

- When the user asks for "today", "today's arXiv", or "the latest update day", resolve the latest indexed arXiv date by calling `/ai/by-date` with `date` omitted.
- Always report the exact resolved date from the API response. Do not equate the user's local "today" with the latest indexed arXiv date unless they match.
- When the user asks for a specific day, pass `YYYY-MM-DD` exactly.
- When the user asks for topic-related papers on one specific day, first resolve the target date if needed, then call `recommend` with `period=0` and that exact `date`.
- When the user asks for no date restriction, all available dates, or an effectively unbounded recommendation query, use `period=9999`.
- Never send a `period` value above `9999`. If the user asks for a larger value, cap it at `9999` and state that the API maximum is `9999`.
- Use `previous_date` and `after_date` from `/ai/by-date` when the user asks to move backward or forward by arXiv update day instead of calendar day.

## Normalize arXiv IDs

- Keep the full versioned ID such as `2603.08470v1` when using `article/{arxiv_id}`.
- Strip any trailing version suffix such as `v1`, `v2`, or `v12` when using similar-paper recommendation by ID.
- Example: if the user gives `2306.15611v2`, call the similar-paper endpoint with `arxiv_id=2306.15611`.

## Control Context Size

- Default to `only_title=true` for `/ai/by-date`.
- Treat `categories` as lightweight metadata that is safe to keep in normal list responses.
- Avoid requesting the full day listing with abstracts and authors unless the user explicitly wants exhaustive details. The full payload can consume roughly `50k-100k` context.
- If the user wants more detail after a title-only listing, fetch details only for the selected paper IDs with `article/{arxiv_id}`.
- For topic search, keep the default `limit=30` unless the user asks for a smaller or larger shortlist.
- For topic search with no date restriction, use `period=9999`.
- For similar-paper search by ID, use the API shape the user provided: `recommend?period=500&arxiv_id={bare_id}` unless they later specify another supported variant.
- If the user explicitly asks for similar papers without any date restriction, use `period=9999` instead of the default `500`.

## Respond For Astronomy Researchers

- Assume the audience is astronomy researchers unless the user specifies another audience.
- Prefer astronomy interpretations for ambiguous topics such as `stars`, `galaxies`, `dark matter`, `planets`, `cosmology`, and similar domain terms.
- Use `categories` to expose or filter subfields such as `astro-ph.EP`, `astro-ph.GA`, `astro-ph.CO`, and `astro-ph.IM` when the response includes them.
- When using `recommend`, prioritize papers with higher `similarity` scores and surface the strongest matches first.
- Summarize results in researcher-friendly language: surface the most relevant titles first, then mention notable subtopics, methods, or objects if they are obvious from the title or abstract.
- If the user asks whether papers exist on a topic, answer the existence question first, then list the strongest matches.

## Report Results Clearly

- Always include the exact date used, especially for "today/latest" requests.
- For day listings, include the API's `count` and optionally mention `previous_date` or `after_date` when it helps the next step.
- For topic results, include the search window (`period` or exact day), the topic string, and the number of returned papers.
- For similar-paper results, include the source arXiv ID used for retrieval and note that the recommendation query used the bare ID without version suffix.
- For `recommend` results, use `similarity` as the default ranking signal and recommend the highest-similarity papers first.
- Include `categories` when they help the user judge relevance or distinguish neighboring astro-ph subfields.
- Unless the user explicitly asks for another language, present paper information in the same language the user is currently using.
- Keep original paper metadata such as `title`, `arxiv_id`, and `categories` as returned by the source unless the user explicitly asks for translation or rewriting; localize the surrounding explanation and summary instead.
- For single-paper lookups, include at least title, authors, abstract summary, and categories when available.
- If the API returns no results or an unexpected shape, state that directly and avoid hallucinating missing papers.

## Common Request Patterns

- "Check whether there were any stellar papers on arXiv today"
  Resolve the latest available arXiv date, then call `recommend` with `topic=stars`, `period=0`, and the resolved date.
- "What black hole papers appeared in the last month?"
  Call `recommend` with `topic=black holes` and `period=30`.
- "What galaxy evolution papers are relevant across all available dates?"
  Call `recommend` with `topic=galaxy evolution` and `period=9999`.
- "Show me stellar papers from the last 20000 days"
  Cap the request and call `recommend` with `topic=stars` and `period=9999`.
- "What astro-ph papers appeared on 2026-03-12?"
  Call `/ai/by-date?date=2026-03-12&only_title=true`.
- "Recommend papers similar to 2306.15611v2"
  Strip the version suffix and call `recommend?period=500&arxiv_id=2306.15611`.
- "Show me 2603.08470v1"
  Call `article/2603.08470v1`.
