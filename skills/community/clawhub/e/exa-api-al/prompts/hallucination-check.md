# Prompt: Hallucination Check

## Purpose
Audit a drafted answer claim-by-claim against the cited sources, confirming each factual claim is supported by source text and flagging or removing any that are not.

## Reusable prompt template
```
You are fact-checking an answer against its sources.

Answer to check: {{answer}}
Sources with text (Exa contents/citations):
{{sources}}   # each: {n, url, title, text/highlights}

Steps:
1. Extract every distinct factual claim from the answer.
2. For each claim, find the cited source(s) and check whether their text supports it.
3. Classify: SUPPORTED | PARTIALLY-SUPPORTED | UNSUPPORTED | MISCITED.

Output JSON:
{
  "claims": [
    {"claim":"...", "cited":[n...], "verdict":"SUPPORTED|PARTIAL|UNSUPPORTED|MISCITED",
     "evidence":"<quote from source text or 'none'>"}
  ],
  "action": "<what to fix: remove/relabel/recite unsupported claims>",
  "clean": true|false   # true only if all claims SUPPORTED
}

Rules:
- A claim is SUPPORTED only if the cited source's text actually states it.
- MISCITED = the cited source exists but does not contain the claim.
- Do not use outside knowledge to validate a claim; only the provided source text counts.
- Numbers/dates/units must match the source exactly, else PARTIAL or UNSUPPORTED.
- Recommend removing or labeling (unverified) any non-SUPPORTED claim.
```

## Variables
| Variable | Meaning |
|----------|---------|
| `{{answer}}` | The drafted answer to audit. |
| `{{sources}}` | Cited sources with their text for verification. |

## Example use
`{{answer}}` = "Revenue was $4B (+30%), and the CEO resigned in April [1].", `{{sources}}` = `[1]` text mentions revenue and growth but not a CEO resignation.

## Bad example
```
Looks fine — all claims have a [1] next to them, so it's verified.
```
Why bad: confuses "has a citation marker" with "is supported by the cited text"; never checked the source text; misses the unsupported CEO-resignation claim.

## Good example
```json
{
  "claims": [
    {"claim":"Revenue was $4B","cited":[1],"verdict":"SUPPORTED","evidence":"\"revenue reached $4.0 billion\""},
    {"claim":"Revenue grew 30%","cited":[1],"verdict":"SUPPORTED","evidence":"\"up 30% year over year\""},
    {"claim":"The CEO resigned in April","cited":[1],"verdict":"MISCITED","evidence":"none — source [1] has no mention of CEO or resignation"}
  ],
  "action": "Remove the CEO-resignation claim or find a source that supports it before publishing.",
  "clean": false
}
```

> Verification needed: confirm citation `text` availability for verification with https://docs.exa.ai
