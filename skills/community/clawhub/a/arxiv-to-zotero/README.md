# arxiv-to-zotero

[中文说明 / Chinese version](README.zh-CN.md)

Find recent arXiv papers, skip what is already in Zotero, and save new imports into Zotero with PDF attachments, a fixed `arxiv-to-zotero` tag on parent items, and a dedicated `arxiv-to-zotero` collection.

## Why this skill is useful

This skill is built for a narrow workflow that many research users repeat all the time:

- search recent papers on arXiv
- deduplicate against Zotero before writing
- attach PDFs automatically when possible
- keep imports organized with a fixed tag and a dedicated collection
- avoid touching existing Zotero items

In one line: **find recent arXiv papers and push only the genuinely new ones into a clean Zotero inbox.**

## What it does

The agent will:

1. collect topic keywords or phrases and a time range
2. build one valid arXiv `search_query` internally
3. search arXiv for recent papers
4. deduplicate against Zotero
5. import only new papers
6. tag new parent items with `arxiv-to-zotero`
7. place imports into the `arxiv-to-zotero` collection, creating it automatically if needed
8. return one final summary

## Typical requests

- Find papers from the last three years on Mamba for stock prediction and import only the new ones into Zotero.
- Search recent papers on multimodal methods for stock prediction, deduplicate them against Zotero, and save the rest.
- Find recent arXiv papers on test-time adaptation and active search, then import only the ones I do not already have in Zotero.

## Runtime requirements

- Python 3.10+
- `curl`
- Zotero Web API access via `ZOTERO_API_KEY`
- OpenClaw skill runtime

## First run

If the setup-state file is missing, the skill will:

1. read [`setup.md`](setup.md)
2. collect the required Zotero settings
3. write non-secret updates back into `config.json`
4. create the setup-state file
5. resume the original request once

## How the agent should use this skill

The intended interaction pattern is:

1. collect topic keywords or phrases
2. collect a time range
3. translate Chinese keywords into concise technical English when needed
4. build one valid English arXiv `search_query`
5. call the script once

Example:

```bash
python3 scripts/main.py --config ./config.json --query '(all:"Mamba" OR all:"state space model") AND (all:"stock prediction" OR all:"financial prediction" OR all:"market prediction" OR all:"price forecasting") AND submittedDate:[202304010000 TO 202604092359]'
```

## Key behavior

### Discovery source

This skill uses **arXiv only** as the paper discovery source.

### Deduplication

The script builds a temporary Zotero cache from three scopes:

- query-derived Zotero quick-search terms
- the fixed skill tag `arxiv-to-zotero`
- the dedicated target collection when it already exists

It then checks duplicates using:

- normalized exact title matching
- strict normalized title-prefix matching
- arXiv ID matching when available

Existing Zotero items are skipped and never modified.

### PDF attachments

For each new parent item, the script derives one or more candidate PDF URLs from the saved paper URL.

It first tries to upload the PDF as a real Zotero file attachment. If Zotero returns `413 Request Entity Too Large`, the script deletes the unfinished upload, falls back to `linked_url` for that paper, and keeps the rest of the current run in link mode.

### Organization rules

By default, the script writes imports with these fixed organization rules:

- parent items get the tag `arxiv-to-zotero`
- - parent items go to the collection `arxiv-to-zotero`
- if the collection does not exist, the script creates it automatically

### Import cap

The script stops creating new Zotero parent items after `import_policy.max_new_items` is reached. The default cap is 50 new items per run.

## Runtime paths

- Default non-secret config: `./config.json` in the skill root directory
- Setup state: `~/.openclaw/config/skills/arxiv-to-zotero.setup.json`
- Secrets / environment: `~/.openclaw/.env`

## Repository structure

- [`SKILL.md`](SKILL.md): skill definition and runtime instructions
- [`setup.md`](setup.md): first-run setup guidance
- [`SECURITY.md`](SECURITY.md): security, boundary, and risk notes
- [`scripts/main.py`](scripts/main.py): main script implementation
- [`config.json`](config.json): default non-secret configuration

## Security and privacy

This skill contacts:

- arXiv Atom API
- arXiv PDF URLs
- Zotero Web API

This skill:

- creates new Zotero items and attachments
- does not modify existing Zotero items
- uses `ZOTERO_API_KEY` for Zotero API access

For more detail, see [`SECURITY.md`](SECURITY.md).

## Notes

- The script expects one direct program invocation only.
- Do not use shell composition such as `&&`, `;`, pipes, or chained `cd` commands.
- The script URL-encodes the query parameter itself. Do not pre-encode spaces, quotes, or parentheses.
