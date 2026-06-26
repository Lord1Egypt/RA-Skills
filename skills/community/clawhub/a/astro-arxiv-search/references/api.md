# API Reference

Use this reference only when the exact endpoint shape, parameters, or response fields matter.
For astronomy paper retrieval, this API is the primary source. If it is unavailable, failing, or clearly insufficient for the request, fall back to other search methods available in the environment.

## 1. List papers for one arXiv update day

Endpoint:
`https://arxiv.q-cs.cn/ai/by-date?date={YYYY-MM-DD}&only_title=true`

Parameters:
- `date`: Optional. Use `YYYY-MM-DD`. If omitted or empty, the API returns the latest indexed arXiv day.
- `only_title`: Use `true` by default. This keeps the response lightweight and still returns `title`, `arxiv_id`, `pub_date`, and `categories`.

Default response shape:

```json
{
  "after_date": "2026-03-13",
  "articles": [
    {
      "arxiv_id": "2603.10040v1",
      "categories": "astro-ph.SR, astro-ph.IM",
      "pub_date": "2026-03-12 09:54:02",
      "title": "The diagnostic temperature discrepancy as evidence for non-Maxwellian coronal electrons"
    }
  ],
  "count": 131,
  "date": "2026-03-12",
  "generate_time": "2026-03-13 23:09:30",
  "previous_date": "2026-03-11"
}
```

Important behavior:
- `after_date: null` means the queried day is already the latest indexed day.
- `previous_date` and `after_date` refer to the previous and next update day that actually has papers, not necessarily adjacent calendar dates.
- Each article now includes `categories`, which can be used to label or filter astro-ph subfields without materially increasing context size.
- If `only_title` is not `true`, each article may also include `abstract` and `creators`. This can cost roughly `50k-100k` context for a full day and should be avoided unless the user explicitly wants exhaustive detail.

Use this endpoint for:
- "What papers appeared on arXiv that day?"
- "What papers appeared on the latest update day or on today/yesterday's update?"
- Navigating to the next or previous update day

## 2. Recommend papers

The `recommend` endpoint now supports two modes:
- topic-based recommendation with `topic=...`
- similar-paper recommendation with `arxiv_id=...`

Use only one of `topic` or `arxiv_id` in a single request.
When no date restriction is intended, the maximum supported lookback window is `period=9999`.
Never send `period > 9999`. Cap larger user requests at `9999` and mention the cap in the answer when it matters.

### 2.1 Topic mode

Endpoint:
`https://arxiv.q-cs.cn/ai/recommend?topic={topic}&period={int}&date={YYYY-MM-DD}&limit={30}`

Parameters:
- `topic`: Required. Natural-language topic string. English and Chinese topic words are acceptable.
- `period`: Required. Search window in days.
- `date`: Optional. Use only when `period=0`.
- `limit`: Optional. Default `30`.

Interpretation:
- `period=30`: Recent month
- `period=7`: Recent week
- `period=365`: Recent year
- `period=0`: One specific day only. In this case, pass `date`.
- `period=9999`: No date restriction / all available dates

Typical response shape:

```json
{
  "articles": [
    {
      "abstract": "Eclipsing close double white dwarf...",
      "arxiv_id": "2603.08470v1",
      "categories": "astro-ph.SR",
      "creators": "Leandro G. Althaus, Alejandro H. Corsico, Monica Zorotovic, Maja Vuckovic, Alberto Rebassa-Mansergas, Santiago Torres",
      "date": 1773114481,
      "pub_date": "2026-03-10 11:48:01",
      "similarity": 0.7098953,
      "title": "Extreme mass loss during common envelope evolution: the origin of the double low-mass white dwarf system J2102--4145"
    }
  ],
  "message": "Found the top 30 papers related to topic \"stars\" on 2026-03-10",
  "period": "2026-03-10",
  "status": "success",
  "timestamp": 1773158400,
  "topic": "stars",
  "total_articles": 30
}
```

Use this endpoint for:
- "What papers were published in this area over the last month?"
- "What papers on galaxy mergers appeared in the last week?"
- "Were there any stellar papers on a specific day?"
- Requests that need quick subfield separation from `categories`, for example distinguishing `astro-ph.EP` from `astro-ph.HE`

Ranking rule:
- The `similarity` field is the similarity score. When presenting or narrowing `recommend` results, prefer papers with higher `similarity`.

Practical rule:
- If the user asks for "today's topic papers", first resolve the latest indexed arXiv date with `/ai/by-date`, then call `recommend` with `period=0` and that exact date.
- If the user asks for no date restriction, all available dates, or the widest possible search window, use `period=9999`.
- If the user asks for `period` above `9999`, cap it at `9999`.
- When the request uses `period=0`, the response may represent the resolved day in a date-like field or string form. Report the exact resolved date to the user rather than relying on the raw response shape alone.

### 2.2 Similar-paper mode

Endpoint:
`https://arxiv.q-cs.cn/ai/recommend?period=500&arxiv_id={bare_arxiv_id}`

Parameters:
- `period`: Use `500` for this mode by default. If the user explicitly wants no date restriction or all available dates, use `9999`.
- `arxiv_id`: Required. Must use the bare arXiv ID format `xxxx.xxxxx` and must not include a version suffix.

Normalization rule:
- Convert `2306.15611v1` to `2306.15611` before calling this endpoint.
- Do not strip the version suffix when calling `article/{arxiv_id}` for a direct paper lookup.

Typical use:
- "Find papers similar to 2306.15611"
- "Recommend papers close to 2306.15611v2"
- "What related work exists for this paper?"

Expected article fields:
- The response comes from `recommend`, so returned articles can include the same fields used in topic mode such as `title`, `arxiv_id`, `categories`, `pub_date`, `creators`, `abstract`, and similarity-related metadata when present.
- `similarity`: similarity score. Higher values should generally be treated as stronger matches.

## 3. Fetch one paper in detail

Endpoint:
`https://arxiv.q-cs.cn/ai/article/{arxiv_id}`

Typical response shape:

```json
{
  "article": {
    "abstract": "Direct imaging of exoplanets presents...",
    "announce_type": "",
    "arxiv_id": "1703.00582v2",
    "bibcode": null,
    "categories": "astro-ph.EP, astro-ph.IM",
    "created_at": "2025-04-02 10:26:44",
    "creators": "Ji Wang, Dimitri Mawet, Garreth Ruane, Renyu Hu, Bjorn Benneke",
    "doi": null,
    "id": 137829,
    "link": "https://arxiv.org/abs/1703.00582v2",
    "pub_date": "2017-03-02T01:47:10Z",
    "rating": 0,
    "rights": "",
    "title": "Observing Exoplanets with High Dispersion Coronagraphy. I. The scientific potential of current and next-generation large ground and space telescopes",
    "translation_status": 1,
    "update_time": null
  },
  "status": "success"
}
```

Useful fields:
- `title`
- `creators`
- `abstract`
- `categories`
- `link`
- `pub_date`

Use this endpoint for:
- Drilling into a shortlisted paper after a title-only daily listing
- Getting abstract, authors, categories, or source link for a specific arXiv ID

## 4. Query mapping

- User asks "What papers are on arXiv today?"
  Use `/ai/by-date` with `date` omitted and `only_title=true`.

- User asks "Were there any exoplanet papers today?"
  First resolve the latest indexed date, then use `recommend` with `topic=exoplanets`, `period=0`, and the resolved date.

- User asks "Show me the 20 most relevant dark matter papers from the last year"
  Use `recommend` with `topic=dark matter`, `period=365`, and `limit=20`.

- User asks "Show me galaxy evolution papers across all available dates"
  Use `recommend` with `topic=galaxy evolution`, `period=9999`.

- User asks "Show me stellar papers from the last 20000 days"
  Cap the request and use `recommend` with `topic=stars`, `period=9999`.

- User asks "Recommend papers similar to 2306.15611v2"
  Strip the version suffix and use `recommend` with `period=500` and `arxiv_id=2306.15611`.

- User asks "Show me 1703.00582v2"
  Use `article/1703.00582v2`.

## 5. Response discipline

- Report the exact resolved date whenever the user says "today", "latest", or "recent day".
- Avoid full-day abstract dumps unless the user explicitly asks for them.
- Use `categories` in list responses when it helps filter, group, or annotate astronomy subfields.
- When the user asks for similar papers and provides a versioned arXiv ID, report the original ID they mentioned but call the API with the bare ID.
- When the user asks for an unrestricted recommendation search, state that the query used `period=9999`.
- Unless the user explicitly asks for another language, return paper information in the same language the user is using.
- Keep source metadata such as `title`, `arxiv_id`, and `categories` in source form unless the user explicitly asks for translation or rewriting; localize the explanation and summary around them instead.
- If this API cannot be used, fall back to other available retrieval methods and clearly base the answer on the fallback source rather than this API.
- When falling back, prefer structured or official paper sources before generic web search when those options are available.
- For `recommend` output, prioritize higher `similarity` results in both ranking and recommendation emphasis unless the user asks for another ordering.
- Prefer narrowing with title-only listings first, then deepening with `article/{arxiv_id}`.
- Treat the API response as the source of truth and do not invent missing metadata.
