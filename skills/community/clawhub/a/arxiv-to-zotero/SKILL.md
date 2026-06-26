---
name: arxiv-to-zotero
description: Find recent arXiv papers, skip what is already in Zotero, and save new imports with parent-item tagging and PDF attachments into a dedicated collection.
version: 1.0.2
user-invocable: true
always: false
homepage: https://github.com/ucaspyx/arxiv-to-zotero
metadata: {"openclaw":{"emoji":"📚","skillKey":"arxiv-to-zotero","requires":{"env":["ZOTERO_API_KEY"],"bins":["python3","curl"]},"primaryEnv":"ZOTERO_API_KEY","compatibilities":["openclaw"]}}
---
# arXiv to Zotero

Use this skill when the user wants **recent arXiv papers found and written into Zotero directly**.

## Best-fit use cases

- find papers by topic + time range
- skip papers already in Zotero
- attach PDFs when possible
- keep imports organized with a fixed tag and a dedicated collection

## Setup

On first use, if `~/.openclaw/config/skills/arxiv-to-zotero.setup.json` is missing, read `{baseDir}/setup.md`, collect the required Zotero values, tell the user to put `ZOTERO_API_KEY` in `~/.openclaw/.env`, create the setup-state file, and resume the original request exactly once.

## Flow

1. If the user has not already provided them, ask for:
   - topic keywords or phrases
   - a time range
2. Do not ask the user to write an arXiv query.
3. If the user gives keywords in Chinese, translate them into concise, technically accurate English search phrases before building the arXiv query.
4. Build **one** valid arXiv API `search_query` yourself.
5. Run the script once:

```bash
python3 {baseDir}/scripts/main.py --config {baseDir}/config.json --query '<arXiv search_query>'
```

6. After the script finishes, use `result.user_message` as the final user-facing notification.

## Query rules

- Use official arXiv fielded search syntax.
- The final arXiv query must be written in English.
- Use double quotes for multi-word phrases.
- Combine alternative keywords with `OR` when appropriate.
- Add the requested time range with `submittedDate:[YYYYMMDDTTTT TO YYYYMMDDTTTT]`.
- Pass the query as normal text. Do not URL-encode it yourself.

## Guarantees

- Existing Zotero items are not modified.
- New parent items are tagged with `arxiv-to-zotero` by default.
- New imports are placed into the `arxiv-to-zotero` collection by default. If that collection does not exist, the script creates it.
- If Zotero file upload hits HTTP 413, the script falls back to `linked_url` for that paper and keeps later attachments in link mode for the same run.

## When not to use

Do not use this skill for discussion-only requests, browsing help, or any task that should not write to Zotero.

## Network / Privacy

- Contacts: arXiv Atom API, arXiv PDF URLs, Zotero Web API
- Secret used: `ZOTERO_API_KEY`
- Writes: new Zotero parent items and child attachments only
- Does not modify existing Zotero items

## Natural-language trigger examples

- 帮我找近三年来 mamba 或者多模态用于股票预测的 arXiv 论文，并导入 Zotero。
- 帮我查最近两年 test-time adaptation 或 active search 用于组合优化的 arXiv 论文，去重后导入 Zotero。
- 帮我找近半年的 graph neural network 用于 TSP 或 vehicle routing 的 arXiv 论文，导入 Zotero。
