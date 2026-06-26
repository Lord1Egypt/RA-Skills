# Prompt: Synthesis

## Purpose
Write a grounded, cited answer using ONLY the retrieved content (Exa contents/summaries/citations) — combining multiple sources, surfacing agreement and conflict, and never adding outside knowledge.

## Reusable prompt template
```
You are synthesizing an answer strictly from retrieved sources.

Question: {{question}}
Retrieved content (per source):
{{retrieved}}   # each: {url, title, publishedDate, text/highlights/summary}

Write the answer with these rules:
- Use ONLY facts present in the retrieved content. No prior knowledge, no inference beyond the text.
- Attach [n] citations to every factual claim (numbering = first appearance).
- When sources agree, state the consensus and cite the strongest.
- When sources conflict, present both with attribution; do not silently pick one.
- If the content does not answer part of the question, say "not found in sources" — do not fill the gap.
- Preserve numbers, dates, units, and named entities exactly as written.
- Match the user's language; quote facts verbatim.

Output:
- Answer (with inline [n])
- Sources list
- "Gaps/uncertainties" section if anything is unresolved
```

## Variables
| Variable | Meaning |
|----------|---------|
| `{{question}}` | The question to answer. |
| `{{retrieved}}` | The per-source content to synthesize from. |

## Example use
`{{question}}` = "Is the company profitable?", `{{retrieved}}` = two filings/articles, one saying profitable, one not, plus one with no profit data.

## Bad example
```
The company is profitable and is the clear market leader, and will likely IPO soon.
```
Why bad: pulls in outside/speculative claims ("market leader," "IPO soon") absent from sources, no citations, ignores a conflicting source, no gaps section.

## Good example
```
Source [1] reports the company posted a net profit in FY2025 [1], while [2] describes
continued operating losses in its most recent quarter [2]; the figures cover different
periods. Revenue growth was 30% YoY [1]. No source reports IPO plans.

Sources:
[1] FY2025 results — https://example.org/a (2026-02-10)
[2] Q1 update — https://example.org/b (2026-05-01)

Gaps/uncertainties:
- Profitability differs by period across [1] and [2]; full-year vs latest quarter.
- IPO timing: not found in sources.
```

> Verification needed: confirm contents/summary fields with https://docs.exa.ai
