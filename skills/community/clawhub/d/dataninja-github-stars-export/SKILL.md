---
name: github-stars-notion-sync
description: Export GitHub starred repositories by category and sync them to a Notion database.
---

# GitHub Stars to Notion Sync Skill

This skill allows you to automate the process of exporting your GitHub starred repositories (grouped by custom lists/categories) and syncing them into a structured Notion database.

## Instructions

When this skill is active, you can perform the following tasks:

### 1. Export GitHub Stars
Use the shell script in `./scripts/export_stars.sh` to fetch all starred repositories and save them to `./assets/starred_lists.md`.
- **Requirement**: GitHub CLI (`gh`) must be installed and authenticated.
- **Output**: A Markdown file with tables for each category.

### 2. Sync to Notion
Use the Python script in `./scripts/sync_stars_to_notion_db.py` to parse the exported Markdown and populate a Notion database.
- **Requirement**: `NOTION_API_KEY` environment variable must be set.
- **Requirement**: `requests` library must be installed.
- **Config**: Local state is tracked in `./assets/.notion_sync_config.json`.

### 3. Workflow
1. Run `./scripts/export_stars.sh`.
2. Run `python scripts/sync_stars_to_notion_db.py`.

## Tool Definitions

- **export_stars**: Fetches GitHub stars and updates `./assets/starred_lists.md`.
- **sync_to_notion**: Syncs the contents of `./assets/starred_lists.md` to Notion.
