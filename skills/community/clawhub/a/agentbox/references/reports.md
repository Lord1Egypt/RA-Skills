# Reports: build, fill, check

Use this when the task asks for a report, brief, comparison or answer file.

## The loop

```bash
agentbox report templates
agentbox report build "Top 3 Rust Web Frameworks in 2026" --template top-n --n 3 --out report.md --apply
agentbox file read report.md
agentbox file replace report.md --todo 1 --replace "Axum" --apply
agentbox report check report.md --template top-n --n 3
```

1. Add notes first (`note add ... --source URL --tag item1`). `report build` places them for you.
2. `report build` writes the skeleton: exact headings, numbered `<!-- TODO(N): hint -->` placeholders, your notes, and a Sources list from note sources.
3. Read the file once (`file read`). Each TODO says what to write there and how many words.
4. Fill TODOs one at a time with `file replace FILE --todo N --replace TEXT --apply`. `--todo N` replaces the whole placeholder comment.
5. Run `report check` with the same `--template` (and `--n` or `--columns`) you used for build.
6. For each issue in `data.issues[]`, run its `fix`. Replace `YOUR TEXT` with real content.
7. Repeat until `data.pass` is true. Then stop.

## Templates

| Template | Use for | Shape |
|---|---|---|
| `brief` | fact lookup, regulation summary, deep research | Summary (30-150 words), Key Findings (60+ words, cited), Sources (2+) |
| `top-n` | "top 3", OSS alternatives, ranked lists | exactly N `## 1. Name` sections (25+ words, each cited), Sources (3+) |
| `compare` | pricing, vendors, procurement, competitors | Summary, Comparison table, Recommendation, Sources (3+) |
| `exec-lookup` | a person and their role | Summary, Role and Background (cited), Key Facts (cited), Sources (2+) |
| `market-brief` | Polymarket briefing | Overview, exactly N `## 1. Market` sections each with a `%` and a polymarket.com link, Sources (3+) |

```bash
agentbox report build "Asana vs Monday vs ClickUp pricing" --template compare --columns "Tool,Entry price (USD/user/mo),Free tier,Source" --out pricing.md --apply
agentbox report build "Polymarket politics brief" --template market-brief --n 3 --out brief.md --apply
agentbox report build "Who runs Nvidia" --template exec-lookup --out exec.md --apply
agentbox report build "Acme pricing" --template brief --tag pricing --out acme.md --apply
agentbox report template show compare
```

- `--n` sets the number of numbered sections (top-n, market-brief). Use the number the task asks for.
- `--columns` sets the table columns (compare). Pass the same `--columns` to `report check`.
- `--tag` uses only notes with that tag.
- Without `--out`, build returns the draft in `data.content` and writes nothing.
- Custom template: copy one with `report template show NAME`, edit it, save it as a `.toml` file, and pass `--template ./file.toml`. This skill ships an example in `assets/vendor-shortlist.toml`.

## Writing the content

- One fact per sentence. Put the citation right after it: `Pro costs $20 per user per month ([example.com](https://example.com/pricing)).`
- Citation style is an inline link: `([domain](URL))`. Use URLs from `agentbox note list`.
- Keep the exact heading shape: `## 1. Axum`, not `### 1. Axum` or `## 1) Axum`.
- In `compare`, put one Markdown table row per option, columns in the required order.
- Write numbers with units and dates. Compute them with `agentbox calc`.
- Delete the `<!-- NOTES ... -->` block after you move its facts into sections.

Multi-line text (bullets, tables): send it on stdin so the shell does not touch `$` or newlines.

```bash
agentbox file replace report.md --todo 2 --replace - --apply <<'EOF'
- Free plan: up to 2 users ([asana.com](https://asana.com/pricing)).
- Starter: $10.99 per user per month, billed yearly ([asana.com](https://asana.com/pricing)).
EOF
```

## Common check issues

| `rule` | What to do |
|---|---|
| `todo` | Fill the placeholder: run the `fix` (`file replace ... --todo N ...`). |
| `section_words`, `doc_words` | Add concrete facts (numbers, names, dates) with citations until the word count is met. Too long: cut. |
| `citation` | Add an inline link `([domain](URL))` in that section. |
| `heading_level`, `heading_format`, `numbering`, `title` | Run the `fix`; it rewrites the heading to the exact shape. |
| `item_count` | Add or remove numbered sections until there are exactly N. |
| `missing_section`, `order` | Add the section with the exact heading, in template order. |
| `sources_section`, `min_sources` | Add `- [Title](URL)` lines under `## Sources`. Use real URLs from your notes. |
| `must_contain` | Add the required text (market-brief: a `%` and a polymarket.com link in every item). |
| `table`, `table_columns` | Add the Markdown table or the missing column, in order. |
| `forbidden` | Remove phrases like "As an AI". |
| `notes_block` (warning) | Move useful facts up, then delete the NOTES block. |

Warnings do not block a pass; errors do. `report check` returns `ok: true` even when the report fails, so read `data.pass`.
