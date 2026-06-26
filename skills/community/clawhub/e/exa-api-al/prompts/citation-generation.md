# Prompt: Citation Generation

## Purpose
Convert Exa `results` (id/title/url) or answer `citations` into inline `[n]` markers within the answer text plus a numbered sources list, with stable, deduplicated numbering.

## Reusable prompt template
```
You are adding citations to an answer.

Answer draft (claims to cite): {{answer_draft}}
Available sources (Exa results or citations):
{{sources}}   # each: {id(=url), title, url, publishedDate, text?}

Produce:
1. The answer text with inline [n] markers placed immediately after the
   claim each source supports. Multiple sources for one claim -> [1][2].
2. A "Sources" list mapping [n] -> "title — url (published date)".

Rules:
- Number sources in order of first appearance in the text.
- Deduplicate: one URL = one number, even if cited many times.
- Every factual claim must have at least one [n].
- Do NOT cite a source for a claim its text does not support.
- Do not invent sources or URLs; only use the provided list.
- If a drafted claim has no supporting source, mark it (unsupported) and do not assign a number.
```

## Variables
| Variable | Meaning |
|----------|---------|
| `{{answer_draft}}` | The drafted answer needing citations. |
| `{{sources}}` | The Exa results/citations available to cite. |

## Example use
`{{answer_draft}}` = a two-sentence answer about marathon records; `{{sources}}` = two Exa citations.

## Bad example
```
The record is 2:00:35, the fastest ever and likely unbeatable for decades.

Sources:
[1] https://example.org/a
[2] https://example.org/b
[3] https://wikipedia.org/marathon   <- not used in text
```
Why bad: no inline markers on the claims, an editorializing claim ("unbeatable for decades") with no support, a listed source never cited, sources lack titles/dates.

## Good example
```
The men's marathon world record is 2:00:35 [1], set at the 2023 Chicago Marathon [1][2].

Sources:
[1] World record results — https://example.org/a (2023-10-08)
[2] Race report — https://example.org/b (2023-10-08)
```

> Verification needed: confirm citation object fields (`id`, `title`, `url`, `text`) with https://docs.exa.ai
