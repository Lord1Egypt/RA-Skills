---
name: agentbox
description: >
  Do web research and data work with the `agentbox` CLI: web search, fetch and
  read pages, look up facts with source URLs, compare prices and products,
  extract prices/tables/dates/people from pages, get stock, index, FX and
  crypto quotes (incl. Taiwan .TW), check Polymarket odds, do arithmetic, get
  today's date, keep notes with sources, write a sourced Markdown report that
  passes a template check, and edit text files safely. Use when a task needs
  facts from the web, current numbers, citations, a report file, or a file
  edit. Do not use for small talk, opinions, or answers that need no source,
  and not for trivial math that does not go into an answer.
compatibility: Requires the `agentbox` binary (v0.2.0+) on PATH. Prebuilt for Linux and Windows x86_64; build from source on macOS. Needs network access for search, fetch, quote and market. Optional TAVILY_API_KEY gives better search; without it agentbox uses keyless DuckDuckGo/Bing.
metadata:
  author: alex-ht
  version: "0.2.0"
  standard: agentskills.io
  homepage: https://github.com/alex-ht/agentbox
  openclaw:
    emoji: "🧰"
    homepage: https://github.com/alex-ht/agentbox
    requires:
      bins:
        - agentbox
    os:
      - linux
      - darwin
      - win32
    envVars:
      - name: TAVILY_API_KEY
        required: false
        description: Optional Tavily API key for better web search (needs a Tavily account; Tavily has a free monthly quota and paid plans). Without it agentbox uses keyless DuckDuckGo/Bing. Set by the human, never by the agent.
      - name: STOOQ_API_KEY
        required: false
        description: Optional Stooq key, only for `quote --backend stooq` price history. Not needed by default.
      - name: AGENTBOX_HOME
        required: false
        description: Optional state directory for saved pages, notes, tables and config. Default ~/.agentbox.
    install:
      - id: download-linux
        kind: download
        label: Download agentbox v0.2.0 (Linux x86_64, static musl) from GitHub Releases
        url: https://github.com/alex-ht/agentbox/releases/download/v0.2.0/agentbox-v0.2.0-x86_64-unknown-linux-musl.tar.gz
        sha256: 904b3ece7c90b65679dd7fb40eb3ae1b4b6cef2f9164f280ac57b697d6b75694
        archive: tar.gz
        extract: true
        stripComponents: 1
        targetDir: bin
        bins:
          - agentbox
        os:
          - linux
      - id: download-windows
        kind: download
        label: Download agentbox v0.2.0 (Windows x86_64) from GitHub Releases
        url: https://github.com/alex-ht/agentbox/releases/download/v0.2.0/agentbox-v0.2.0-x86_64-pc-windows-msvc.zip
        sha256: 841996ce7ac761f48e0c11005c7702e75db26a1786aa59650fc05117e54289a8
        archive: zip
        extract: true
        stripComponents: 1
        targetDir: bin
        bins:
          - agentbox
        os:
          - win32
---

# agentbox

`agentbox` is one command-line tool for research tasks. Run it with your shell/exec tool.
Every command prints exactly one JSON line.

## When to use

- The task needs facts from the web, with source URLs.
- The task needs current numbers: prices, stock quotes, FX rates, Polymarket odds.
- The task asks for a report or answer file with citations.
- The task asks you to edit a text file.

Do not use it for small talk or for answers that need no source.

## Read every result

Success: `{"ok":true,"data":{...},"hint":"..."}`
Failure: `{"ok":false,"error":{"code":"...","message":"..."},"hint":"..."}`

1. Check `ok` first.
2. If `ok` is true, take facts only from `data`. The `hint` names a good next command.
3. If `ok` is false, read `error.code` and do what `hint` says.
4. Exit code 2 means a bad flag. Run `agentbox search --help` (use your command name) and fix the flag.
5. Retry an identical failing command at most once. Then change the keyword, flag or URL, or follow the hint.

## Golden research workflow

```bash
agentbox now
agentbox note list --limit 5
agentbox note clear --apply     # only if note list shows notes from an older task
agentbox search "EU AI Act general-purpose AI obligations" --max-results 5 --save 3
agentbox read doc:1 --grep obligations
agentbox read doc:1 --section 3
agentbox note add 'GPAI model obligations apply from 2 August 2025' --source https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai --tag findings
agentbox report build "EU AI Act: GPAI obligations" --template brief --out report.md --apply
agentbox file replace report.md --todo 1 --replace 'Providers of general-purpose AI models must meet transparency and copyright duties from 2 August 2025.' --apply
agentbox report check report.md --template brief
```

1. `now`: get today's date. Use it for "latest", "this week", and in the report.
   At the start of a new task, `note list`; if it shows notes from an older task, `note clear --apply`. Never clear notes in the middle of a task.
2. `search --save N`: find pages and store the top N as `doc:1`, `doc:2`, ...
3. `read doc:N --grep WORD` or `--section N`: read only the part you need. Never dump a whole doc.
4. `note add`: save each fact with its `--source` URL. Tag notes with a section word (`summary`, `findings`) or `item1`, `item2`, ... for numbered reports (top-n, market-brief).
5. `extract` / `table`: pull prices, dates, tables or people from docs, then sort or filter them.
6. `report build --template T --out FILE --apply`: write a skeleton with exact headings, numbered `<!-- TODO(N) -->` placeholders, your notes and a Sources list.
7. `file replace FILE --todo N --replace TEXT --apply`: fill each TODO.
8. `report check FILE --template T`: read `data.pass` and `data.issues`. Each issue has a `fix` command. Run it (put your text where it says YOUR TEXT).
9. Repeat step 8 until `pass` is true. Then stop.

## Command cheat-sheet

```bash
agentbox now --tz Asia/Taipei                         # date, time, weekday
agentbox calc "round(1299 * 0.85, 2)"                 # all arithmetic
agentbox search "best open source Notion alternative" --max-results 5 --save 2
agentbox search "Nvidia earnings" --news --time week  # recent news
agentbox fetch https://example.com/pricing            # one known URL -> doc:N + outline
agentbox read doc:2 --grep price                      # snippets around a word
agentbox read doc:2 --section 3                       # one section from the outline
agentbox read doc:2 --offset 4000                     # continue after truncated:true
agentbox note add 'Pro plan is $20/user/month' --source https://example.com/pricing --tag pricing
agentbox note list --tag pricing                      # notes and their sources
agentbox note clear --apply                           # only at the start of a new task
agentbox extract doc:1 doc:2 --kind prices --save-table
agentbox extract doc:3 --kind people --grep CEO
agentbox table show tbl:1
agentbox table query tbl:1 --where "value < 50" --sort value --select value,raw,url
agentbox table import prices.csv
agentbox table export tbl:1 --out prices.csv --apply
agentbox quote get NVDA 2330.TW ^TWII USDTWD=X
agentbox quote history 2330.TW --range 6mo
agentbox quote search "Taiwan Semiconductor"
agentbox market trending --limit 10
agentbox market search election --limit 10
agentbox market get balance-of-power-2026-midterms
agentbox market history 2026-balance-of-power-d-senate-d-house-949 --interval 1m
agentbox report templates
agentbox report template show top-n
agentbox report build "Top 3 Rust Web Frameworks" --template top-n --n 3 --out report.md --apply
agentbox report check report.md --template top-n --n 3
agentbox file read report.md --lines 1:40
agentbox file write answer.md --content '# Answer' --apply
agentbox file replace report.md --find "old text" --replace "new text" --apply
agentbox config get                                   # which search backend/key is active (masked)
```

## What to take from the output

- `search`: `data.results[]` with `title`, `url`, `snippet`, and `doc` when saved. `data.backend` tells you the engine.
- `fetch`: `data.doc` and `data.outline[]` (`section`, `heading`). Then use `read`.
- `read`: `data.content`. If `data.truncated` is true, continue with `--offset` set to `data.next_offset`. With `--grep`: `data.snippets[]` (`section`, `text`).
- `note list`: `data.notes[]` (`text`, `source`, `tag`) and `data.sources[]`.
- `extract`: `data.items[]`, each with `context` and `url` (prices, dates, numbers also have `raw`). `data.table` when you used `--save-table`.
- `table query`: `data.rows[]` and `data.row_count`.
- `quote get`: `data.quotes[]` (`price`, `change_pct`, `currency`, `time`, `market_state`), `data.errors[]`, `data.note`.
- `market search` / `trending`: `data.events[]` (`title`, `url`, `volume_24h`, `end_date`, `markets[]` with `question`, `odds`, `yes_pct` or `leader` and `leader_pct`).
- `report check`: `data.pass`, `data.score`, `data.issues[]` (`message`, `fix`).
- `file write` / `file replace`: `data.applied` and `data.diff`.

## Which reference to open

Open a reference file (relative to this skill folder) only when you need it:

| You need to... | Open |
|---|---|
| search better, read long pages, handle weak keyless results | `references/research.md` |
| get prices, tables, dates or people out of pages; filter or sort | `references/data.md` |
| write a report file, pick a template, fix `report check` issues | `references/reports.md` |
| get stock/FX/crypto quotes or Polymarket odds | `references/finance-markets.md` |
| edit files, write multi-line text, quote `$` safely, use notes | `references/files.md` |
| do a known task type (stock briefing, executive lookup, pricing, Polymarket briefing, EU regulation, OSS alternatives, IT procurement, competitive or deep research, BYOK) | `references/task-playbooks.md` |

## Hard rules

1. Run `agentbox` directly. Do not prefix it with `python3`, `bash -c` or a guessed path.
2. Use agentbox instead of `curl`, `wget`, `python`, `jq` or `grep` on web pages.
3. Do not reimplement agentbox features in Python or shell scripts.
4. Use `agentbox calc` for every number you compute (sums, percentages, averages, conversions).
5. Use `agentbox now` for today's date. Never guess the date or year.
6. Cite only URLs that appeared in agentbox output in this task (search results, fetch, notes, quote, market). Never invent a URL.
7. Do not paste raw page content into your answer. Summarize in your own words; quote at most one short sentence.
8. Read with `--grep` or `--section`. Do not read a whole doc page by page unless you must.
9. Writes need `--apply`. Without it nothing is written; you only get a diff preview. Preview first when you change a file you did not create.
10. Put text in single quotes when it contains `$`, a backtick or `!`: `'Pro costs $20/month'`. In double quotes the shell eats `$20`.
11. Do not type `\n` inside quotes; it stays a literal backslash-n. For multi-line text use `--replace -` with a heredoc (see `references/files.md`).
12. Keep `--max-results` at 3-8 and `--limit` small. For `market search` and `market trending` use `--limit 10` or more.
13. Never ask for, print or set API keys. Do not run `agentbox config set`.
14. If `data.backend` is `ddg` or `bing`, results are weaker: check that each result fits the question, add `--site`, and say so if the evidence is thin.
15. Do not re-run a command in a loop. If two different tries fail, report what failed and move on.
16. Quotes may be about 15 minutes delayed. Polymarket percentages are market prices, not forecasts. Say so in the answer.
17. Stop when `report check` returns `pass: true`. Do not keep polishing.

## Done criteria

- [ ] Every fact came from agentbox output in this task.
- [ ] Every claim has a source URL that agentbox returned.
- [ ] Every computed number came from `agentbox calc`.
- [ ] Time-sensitive data states the date from `agentbox now`.
- [ ] The requested file exists at the requested path (check with `agentbox file read report.md --lines 1:20`).
- [ ] If you wrote a report: `report check` returned `pass: true` and no `<!-- TODO` or `<!-- NOTES` blocks remain.
- [ ] The final answer is short, in your own words, and lists its sources.

## Setup and safety (for the human operator)

- Install: the OpenClaw download installer fetches the v0.2.0 release archive from
  GitHub Releases, checks its pinned sha256, and extracts it to `~/.openclaw/tools/agentbox/bin/`.
  OpenClaw only finds binaries on PATH, so add that folder to PATH
  (Linux: `export PATH="$HOME/.openclaw/tools/agentbox/bin:$PATH"`;
  Windows: add `%USERPROFILE%\.openclaw\tools\agentbox\bin` to the user Path), then start a new session.
- macOS has no prebuilt binary. Build from source (Rust 1.85+):
  `cargo install --git https://github.com/alex-ht/agentbox --tag v0.2.0 --locked`.
- Network: `search` calls api.tavily.com (only with a key), html.duckduckgo.com or bing.com;
  `quote` calls finance.yahoo.com or stooq.com; `market` calls polymarket.com;
  `fetch`/`extract` read only the URLs the agent passes.
- Keys are optional and set by the human (env `TAVILY_API_KEY`, or `agentbox config set` run by the human).
  agentbox never prints a key; `config get` shows it masked.
- Local writes: state goes to `~/.agentbox` (or `AGENTBOX_HOME`). `file` edits and `report build`
  only preview until `--apply` is given. No scripts run; this skill folder holds Markdown and one TOML sample.
