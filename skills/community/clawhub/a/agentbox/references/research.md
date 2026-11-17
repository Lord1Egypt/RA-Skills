# Research: search, fetch, read, notes

Use this when you need better search results, must read long pages, or get weak keyless results.

## Search

```bash
agentbox search "EU AI Act general-purpose AI obligations" --max-results 5 --save 3
agentbox search "AI Act GPAI code of practice" --site europa.eu --save 2
agentbox search "Notion alternative self-hosted" --exclude-site reddit.com --max-results 8
agentbox search "Nvidia earnings" --news --time week
agentbox search "Jensen Huang compensation 2025" --days 30
agentbox search "Who is the CEO of Nvidia" --answer --max-results 3
agentbox search "zero trust architecture vendor comparison" --deep --max-results 5
```

| Flag | Use it for |
|---|---|
| `--max-results N` | 3-8 is enough. Max 20. |
| `--save N` | Store the top N results as docs (max 5). Each saved result gets a `doc` field. |
| `--site D` | Only one domain, e.g. `europa.eu`, `sec.gov`, `github.com`. Repeat for several. |
| `--exclude-site D` | Drop noisy domains. Repeatable. |
| `--time day\|week\|month\|year`, `--days N` | Recent results only. |
| `--news` | News sources only (Tavily). |
| `--answer` | Adds a short generated `data.answer` (Tavily). It is a lead, not a source. Confirm it in a page and cite the page. |
| `--deep` | Better ranking, costs more (Tavily). Use for hard questions only. |

Query tips:

- Use the words the source would use: "pricing", "per user per month", "annual report", "press release", "regulation (EU) 2024/1689".
- Put names and products in the query: `"Asana pricing per user per month"`, not `"project tool costs"`.
- One topic per search. Run 2-4 focused searches instead of one vague one.
- For official facts, search the official domain with `--site` (company site, `europa.eu`, `sec.gov`, `gov.tw`).

## Keyless backends (ddg, bing)

Without a Tavily key, `data.backend` is `ddg` or `bing`, and `data.notes` may explain a fallback.
These results can be loosely matched. Do this:

1. Check each title and URL against the question. Ignore off-topic results.
2. Retry once with more specific words or with `--site`.
3. If you know the official URL, `fetch` it directly.
4. If evidence stays thin, say so in the answer. Do not fill gaps from memory.

`--news`, `--answer` and `--deep` only work with Tavily. Without a key, leave them out.

## Fetch and read

```bash
agentbox fetch https://www.anthropic.com/pricing
agentbox read doc:4 --grep "per month"
agentbox read doc:4 --section 2
agentbox read doc:4 --offset 4000 --max-chars 3000
```

- `fetch` returns `data.doc` and `data.outline[]` (`section`, `heading`, `chars`). Pick sections from the outline.
- `read --grep WORD` returns `data.snippets[]` with `section` and `text`, plus `data.total_matches`. Grep is case-insensitive. One word or a short phrase works best.
- `read --section N` returns one section in `data.content`.
- If `data.truncated` is true, continue with `--offset` set to `data.next_offset`.
- Error `no_match`: try a synonym or a shorter word, or read `--section 1` to see the page start.
- Error `http_error` with 403/404: the site blocks the fetch or the page moved. Try another result or the site's homepage.

## Notes

Save every fact you plan to use, with its source, as soon as you read it.

```bash
agentbox note add 'Nvidia CEO is Jensen Huang, co-founder, CEO since 1993' --source https://nvidianews.nvidia.com/bios/jensen-huang --tag item1
agentbox note list
agentbox note list --tag item1
agentbox note list --grep CEO
```

- `--source` takes the page URL (best) or a doc handle like `doc:2`.
- Tags decide where `report build` puts a note: `item1`, `item2`, ... for numbered items, or a section word such as `summary`, `findings`, `pricing`, `recommendation`.
- `note list` returns `data.notes[]` and `data.sources[]`. Use `data.sources` for the Sources section.

## Dates and math

```bash
agentbox now
agentbox now --tz America/New_York
agentbox calc "(182.5 - 170) / 170 * 100"
agentbox calc "avg(12, 15, 20)"
```

`now` returns `data.date`, `data.time`, `data.weekday`, `data.timezone`. `calc` returns `data.result`.
