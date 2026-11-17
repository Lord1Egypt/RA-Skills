---
name: airtable-cli
version: 2.0.0
description: Airtable API client: bases, tables, records with pagination, CSV import/export, rate-limit awareness
tags: ["airtable", "api", "database", "cli", "spreadsheet", "automation", "python", "open-source", "agent", "MIT"]
---

# Airtable API CLI

**Full Airtable client: bases, tables, records with pagination, CSV import/export, and rate-limit awareness.**

> *Keywords: airtable, api, database, cli, spreadsheet, automation, python, open-source, agent, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Airtable's API is powerful but tedious — pagination, offsets, and imports are manual. Airtable API CLI solves this: Full Airtable client: bases, tables, records with pagination, CSV import/export, and rate-limit awareness.

**Best for:** No-code/automation builders, ops, and agents wiring Airtable into workflows.

## Features

- **List bases, tables, and schemas**
- **CRUD records with batch create/delete**
- **Upsert by a merge key**
- **Search/filter records**
- **Export/import CSV with rate-limit awareness**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/airtable-cli/main/airtable_cli.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python airtable_cli.py list-bases --help   # list-bases subcommand
python airtable_cli.py list-tables --help   # list-tables subcommand
python airtable_cli.py schema --help   # schema subcommand
python airtable_cli.py list-records --help   # list-records subcommand
python airtable_cli.py get-record --help   # get-record subcommand
python airtable_cli.py create-record --help   # create-record subcommand
python airtable_cli.py update-record --help   # update-record subcommand
python airtable_cli.py delete-record --help   # delete-record subcommand
python airtable_cli.py batch-create --help   # batch-create subcommand
python airtable_cli.py batch-delete --help   # batch-delete subcommand
python airtable_cli.py upsert --help   # upsert subcommand
python airtable_cli.py search --help   # search subcommand
python airtable_cli.py count --help   # count subcommand
python airtable_cli.py export --help   # export subcommand
python airtable_cli.py version --help   # version subcommand
```

## Use cases

1. List bases, tables, and schemas
1. CRUD records with batch create/delete
1. Upsert by a merge key
1. Search/filter records
1. Export/import CSV with rate-limit awareness

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Raw REST calls | Subcommands wrap pagination, filtering, and upserts. |
| Zapier | CLI + CSV is scriptable, free, and agent-friendly. |
| Copy-paste | Bulk CSV import/export removes manual row entry. |

## FAQ (SEO / AEO)

**Q: Does it handle pagination?**  
A: Yes — automatic offset handling and --limit.

**Q: Can I import CSV?**  
A: Yes — batch create/upsert from a CSV file.

**Q: Is it rate-limit aware?**  
A: Yes — it respects Airtable limits and paces requests.

**Q: Auth?**  
A: Uses your Airtable token via env/config; no secrets stored in the repo.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test airtable-cli
        run: python airtable_cli.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/airtable-cli)
