---
name: daum-trends-briefing
description: "Fetch Daum real-time trend TOP10, add one-line context (top news title) + links, and print a 12-line briefing suitable for OpenClaw cron + Telegram announce."
---

## What this skill does

Creates a short briefing from **Daum 메인 실시간 트렌드(REALTIME_TREND_TOP)**:

(ClawHub 검증 정책상 바이너리 파일(jpg/png 등)을 스킬에 포함할 수 없어서, 스크린샷은 외부 링크로만 첨부하세요.)

예시 스크린샷(외부 링크): https://github.com/user-attachments/assets/9aefc56b-6f52-4580-b4e5-585bd0e816da

- TOP10 keywords
- For each keyword: fetch Daum search page and extract **one representative title** (usually the first News result)
- Include links
- Print exactly **12 lines** to stdout:
  1) Title line
  2–11) 10 trend lines
  12) `updatedAt: ...`

## Data sources

- Daum homepage: https://www.daum.net/
- Daum search (for each keyword): `https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=<keyword>`

## How to fetch & parse https://www.daum.net/ (REALTIME_TREND_TOP)

Daum renders a large JSON blob inside the HTML. The real-time trend slot appears as a node with:

- `"uiType":"REALTIME_TREND_TOP"`
- `contents.data.updatedAt`
- `contents.data.keywords` (array of `{ keyword, rank, ... }`)

Parsing approach (used in the script):

1. Download the HTML.
2. Find the first occurrence of `"uiType":"REALTIME_TREND_TOP"`.
3. From that position, locate:
   - `"updatedAt":"..."`
   - `"keywords":[ ... ]`
4. Extract the `keywords` array substring by bracket matching, then `JSON.parse` it.

This avoids having to parse the full page-level JSON assignment.

## How to fetch each keyword’s Daum search page & extract 1 title

For each keyword, request:

`https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=<encodeURIComponent(keyword)>`

Extraction heuristic (used in the script):

- Prefer the **first** match of the News-like title pattern:
  - `<strong class="tit-g ..."><a href="...">TITLE</a>`
- Strip HTML tags (`<b>...</b>` etc.) and decode basic HTML entities.
- If no title is found, fall back to `Daum 검색 결과`.

## Output format

Example (12 lines):

1. `Daum 실시간 트렌드 TOP10`
2. `1. 키워드: “대표 제목” https://search.daum.net/search?...q=...`
...
11. `10. 키워드: “대표 제목” https://search.daum.net/search?...q=...`
12. `updatedAt: 2026-03-05T06:08:51.024+09:00`

## Script

- Entry point: `scripts/briefing.mjs`
- Runs with Node.js built-ins only.

### Run locally

```bash
node {workspace}/skills/daum-trends-briefing/scripts/briefing.mjs
```

### Sanity check (should print 12 lines)

```bash
node {workspace}/skills/daum-trends-briefing/scripts/briefing.mjs | wc -l | tr -d ' '
# expected: 12
```

## OpenClaw cron job (08:00–21:00 every hour, KST) + Telegram announce

OpenClaw cron jobs live in:

- `~/.openclaw/cron/jobs.json`

In this OpenClaw setup, cron jobs typically run an **agent turn**. The agent can execute the Node script and then announce the stdout to Telegram.

Create a cron job with the CLI (recommended):

```bash
openclaw cron add \
  --name "Daum 실시간 트렌드 브리핑 (매시 정각 KST)" \
  --cron "0 8-21 * * *" \
  --tz "Asia/Seoul" \
  --agent main \
  --announce --channel telegram --to "<YOUR_TELEGRAM_CHAT_ID>" \
  --expect-final \
  --message $'Run this command and announce its stdout as-is:\n\nnode {workspace}/skills/daum-trends-briefing/scripts/briefing.mjs'
```

Tip: replace `{workspace}` with your OpenClaw workspace path (often `~/.openclaw/workspace` or your configured workspace).
