# Prompt: Source Evaluation

## Purpose
Judge the reliability of Exa results before relying on them — using similarity `score`, domain authority, recency, and corroboration — so weak or biased sources are demoted or dropped.

## Reusable prompt template
```
You are evaluating sources for reliability.

Question/topic: {{topic}}
Recency requirement: {{recency}}   # e.g. "must be within 6 months", "any"
Candidate sources (from Exa results):
{{sources}}   # each: {title, url, publishedDate, author, score}

For each source, output:
{
  "url": "...",
  "score": <0-1 from Exa>,
  "domain_authority": "high|medium|low|unknown",
  "recency": "fresh|acceptable|stale|unknown",
  "independence": "primary|independent|derivative|same-network",
  "keep": true|false,
  "reason": "<one line>"
}

Then output:
{
  "kept": [...urls...],
  "corroboration_ok": true|false,   # >=2 independent kept sources for key claims
  "notes": "<gaps, single-source risks, conflicts>"
}

Rules:
- Higher Exa score = more relevant, NOT automatically more trustworthy. Combine with domain/recency.
- Prefer primary and independent sources; flag when all sources share one owner/network.
- Mark stale sources against the recency requirement.
- Never keep a source just because it agrees with the others if it is not independent.
- Use "unknown" honestly when metadata is missing; do not guess authority.
```

## Variables
| Variable | Meaning |
|----------|---------|
| `{{topic}}` | The question/topic the sources must support. |
| `{{recency}}` | Freshness requirement. |
| `{{sources}}` | List of candidate results with metadata. |

## Example use
`{{topic}}` = "Company X's latest funding round", `{{recency}}` = "within 12 months", `{{sources}}` = 5 Exa results.

## Bad example
```
Kept all 5 sources because they all say the same $50M figure.
```
Why bad: ignores that all five may republish one press release (no independence), ignores recency, treats agreement as corroboration without checking origin.

## Good example
```json
{
  "evaluations": [
    {"url":"https://sec.gov/filing","score":0.74,"domain_authority":"high","recency":"fresh","independence":"primary","keep":true,"reason":"Primary regulatory filing."},
    {"url":"https://techblog.example/funding","score":0.88,"domain_authority":"medium","recency":"fresh","independence":"derivative","keep":false,"reason":"Restates the same press release; not independent."},
    {"url":"https://oldnews.example/2019","score":0.80,"domain_authority":"high","recency":"stale","independence":"independent","keep":false,"reason":"Outside 12-month window."}
  ],
  "kept": ["https://sec.gov/filing","https://reuters.example/round"],
  "corroboration_ok": true,
  "notes": "Two independent sources confirm $50M; several blogs merely echo the PR and were dropped."
}
```

> Verification needed: confirm score semantics with https://docs.exa.ai
