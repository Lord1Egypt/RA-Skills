# Exa Parameters Reference

All parameters across endpoints, with meaning, type, default, and when to change.
Send every request with header `x-api-key: <EXA_API_KEY>`.

> Defaults marked "—" follow Exa's server defaults. Verification needed: confirm
> exact defaults and the full `category` list with https://docs.exa.ai.

---

## search

| Parameter            | Type        | Default | Meaning / When to change |
|----------------------|-------------|---------|--------------------------|
| `query`              | string      | required | The search query. Phrase descriptively for neural; exact terms for keyword. |
| `type`               | enum        | `auto`  | `auto` (Exa picks), `neural` (meaning), `keyword` (exact terms, cheaper), `fast` (low latency/cost). Choose the cheapest that suffices. |
| `category`           | string      | —       | Narrow to a content type (e.g. `news`, `research paper`, `company`, `pdf`, `github`, `tweet`). Set when intent maps to one. |
| `numResults`         | integer     | —       | How many results to return. Start 5–10; raise only if insufficient (raises cost). |
| `includeDomains[]`   | string[]    | —       | Restrict results to these domains. Use to trust specific sources. |
| `excludeDomains[]`   | string[]    | —       | Remove these domains. Use to suppress noise/aggregators. |
| `startPublishedDate` | ISO 8601    | —       | Lower bound on publish date. Set for recency/time scoping. |
| `endPublishedDate`   | ISO 8601    | —       | Upper bound on publish date. Set to cap a time window. |
| `contents.text`      | boolean/obj | —       | Include full cleaned page text inline. Use only when reading deeply; adds cost. |
| `contents.highlights`| boolean/obj | —       | Include most-relevant snippets inline. Good for targeted citation. |
| `contents.summary`   | boolean/obj | —       | Include a short summary inline. Cheapest content option; good for triage. |
| `contents.livecrawl` | enum/bool   | —       | Force fresh crawl instead of cache. Use only when freshness is critical. |

---

## contents

| Parameter    | Type        | Default | Meaning / When to change |
|--------------|-------------|---------|--------------------------|
| `urls[]`     | string[]    | required | URLs (= result `id`s) to fetch. Batch related URLs together. |
| `text`       | boolean/obj | —       | Full cleaned text. Request only when summary/highlights are insufficient. |
| `highlights` | boolean/obj | —       | Relevant snippets. Use for targeted quotes/citation. |
| `summary`    | boolean/obj | —       | Short summary. Default first choice for triage and grounding. |
| `livecrawl`  | enum/bool   | —       | Fresh fetch vs cached. Use sparingly; adds latency/cost. |

---

## findSimilar

| Parameter            | Type     | Default | Meaning / When to change |
|----------------------|----------|---------|--------------------------|
| `url`                | string   | required | Reference URL whose neighbors you want. |
| `numResults`         | integer  | —       | Number of similar pages. Start small (5–10). |
| `includeDomains[]`   | string[] | —       | Constrain the neighborhood to these domains. |
| `excludeDomains[]`   | string[] | —       | Exclude domains from results. |
| `startPublishedDate` | ISO 8601 | —       | Recency lower bound. |
| `endPublishedDate`   | ISO 8601 | —       | Recency upper bound. |

---

## answer

| Parameter | Type    | Default | Meaning / When to change |
|-----------|---------|---------|--------------------------|
| `query`   | string  | required | The question to answer. Keep it single and well-scoped. |
| `text`    | boolean | —       | Include supporting source text in citations. Enable to verify/quote sources. |

---

## research (beta)

> Verification needed: confirm `research` parameters with https://docs.exa.ai.
> Treat as beta; do not rely on undocumented parameters.
