# Prompt: Query Planning

## Purpose
Turn a user's question into one or more well-scoped Exa queries — choosing neural vs keyword/fast phrasing and adding `type`, `category`, date range, and domain filters so the search returns relevant, cost-efficient results.

## Reusable prompt template
```
You are planning Exa search queries.

User question: {{question}}
Known constraints:
- Timeframe: {{timeframe}}            # e.g. "last 30 days", "any", "2023+"
- Source types wanted: {{categories}} # e.g. news, research paper, company, github, pdf, tweet
- Domains to include/exclude: {{domains}}
- Need conceptual discovery or exact-term lookup? {{intent}}

Produce a query plan as JSON:
{
  "queries": [
    {
      "query": "<phrased for the chosen type>",
      "type": "auto|neural|keyword|fast",
      "category": "<category or null>",
      "startPublishedDate": "<ISO date or null>",
      "endPublishedDate": "<ISO date or null>",
      "includeDomains": [],
      "excludeDomains": [],
      "numResults": <5-10>,
      "rationale": "<why this phrasing/type/scope>"
    }
  ]
}

Rules:
- Neural: write a full natural-language sentence describing the concept.
- Keyword/fast: use exact terms, names, error strings, quoted phrases — no filler words.
- Use type "auto" when unsure.
- Add category/date/domain only when they sharpen relevance.
- For freshness, set category "news" + startPublishedDate.
- Keep numResults lean to control cost.
- Split distinct sub-questions into separate queries; do not cram unrelated ideas into one query.
```

## Variables
| Variable | Meaning |
|----------|---------|
| `{{question}}` | The user's raw question. |
| `{{timeframe}}` | Recency requirement; drives date filters. |
| `{{categories}}` | Desired Exa categories (news, research paper, company, etc.). |
| `{{domains}}` | Domains to include or exclude. |
| `{{intent}}` | "conceptual" → neural; "exact-term" → keyword/fast. |

## Example use
`{{question}}` = "What are the latest FDA approvals for GLP-1 drugs?", `{{timeframe}}` = "last 90 days", `{{categories}}` = "news", `{{intent}}` = "conceptual + named entity".

## Bad example
```json
{"queries":[{"query":"GLP-1 stuff news latest 2025 FDA approvals weight loss drugs and side effects and competitors","type":"neural"}]}
```
Why bad: one bloated query mixing several questions, no date filter despite "latest," vague filler words, no category, no numResults, no rationale.

## Good example
```json
{
  "queries": [
    {
      "query": "FDA approval of GLP-1 receptor agonist drugs announced recently",
      "type": "neural",
      "category": "news",
      "startPublishedDate": "2026-03-01",
      "endPublishedDate": null,
      "includeDomains": ["fda.gov"],
      "excludeDomains": [],
      "numResults": 8,
      "rationale": "Conceptual + freshness; news category and date enforce recency; fda.gov for primary approvals."
    },
    {
      "query": "\"GLP-1\" approval list 2026",
      "type": "keyword",
      "category": "news",
      "startPublishedDate": "2026-01-01",
      "endPublishedDate": null,
      "includeDomains": [],
      "excludeDomains": [],
      "numResults": 6,
      "rationale": "Exact-term backup to catch listicles/roundups neural may miss; keyword is cheaper."
    }
  ]
}
```

> Verification needed: confirm current category enum and date field names with https://docs.exa.ai
