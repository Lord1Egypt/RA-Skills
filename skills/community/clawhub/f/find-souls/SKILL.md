---
name: find-souls
description: >-
  Search and install AI persona prompts from Agent Souls library. Use when user wants to roleplay as a historical figure, fictional character, or expert persona; find a SOUL.md prompt; browse AI character prompts.
version: 0.2.0
---

# Find Souls

Search the [Agent Souls](https://agent-souls.com/) library (332+ AI persona prompts) and install a SOUL.md into the current project.

## Workflow

### Step 1: Search

Load the soul index with local caching (cache file: `~/.cache/agent-souls/search.json`):

1. Check if `~/.cache/agent-souls/search.json` exists and its modification time is less than 1 day old.
   - Use `stat` to check the file's modification time.
2. If the cache is **fresh** (< 1 day old): read the local file directly with the `Read` tool.
3. If the cache is **stale** (>= 1 day old) or **missing**:
   - `WebFetch https://agent-souls.com/search.json` to download it.
   - Create directory `~/.cache/agent-souls/` if it doesn't exist.
   - Write the downloaded JSON to `~/.cache/agent-souls/search.json`.

The JSON is an array of objects with these fields:
- `name_en` — English display name
- `name_zh` — Chinese display name
- `url` — path like `/real_world/confucius/`
- `category_en` — "Real World", "Virtual World", or "Expert Personas"
- `category_zh` — Chinese category
- `tags` / `tags_en` / `tags_zh` — keyword arrays

Match the user's query against `name_en`, `name_zh`, `tags`, `tags_en`, `tags_zh`, and `category_en` / `category_zh`. Show the top matches (up to 10) in a numbered list with name, category, and tags. Ask the user to pick one.

**If no matches are found:**

1. If using a cached `search.json`, tell the user the cache may be outdated and offer to refresh it (delete the cache and re-download). If after refresh there are still no results, go to step 2.
2. Tell the user this soul doesn't exist yet, and suggest they submit a request at: https://github.com/wklken/souls/issues

### Step 2: Determine Language

- If the user's conversation is in Chinese, use `SOUL.md` (Chinese version).
- If the user's conversation is in English or unknown, use `SOUL.en.md` (English version).
- The user can explicitly request a language.

### Step 3: Download

Construct the download URL:

```
https://agent-souls.com{url}SOUL.md       # Chinese
https://agent-souls.com{url}SOUL.en.md    # English
```

Where `{url}` is the `url` field from search.json (e.g. `/real_world/confucius/`).

Use `WebFetch` to download the raw content of the chosen SOUL file.

### Step 4: Backup & Install

Before replacing, always back up the existing SOUL.md:

1. Check if `SOUL.md` exists in the current working directory.
2. If it exists, create `.soul_backups/` directory if it doesn't exist, then:
   - **First time only**: if `.soul_backups/SOUL.md.original` does **not** exist, copy SOUL.md to `.soul_backups/SOUL.md.original`. This preserves the user's original persona and is never overwritten.
   - **Every time**: copy SOUL.md to `.soul_backups/SOUL.md.<slug>` where `<slug>` is the soul's unique identifier extracted from the `url` field (the last non-empty path segment, e.g. `/virtual_world/sun_wukong/` → `sun_wukong`, so the backup file is `SOUL.md.sun_wukong`). If a backup with the same slug already exists, overwrite it (only the latest version of each soul needs to be kept).
3. Write the downloaded content to `SOUL.md` in the current working directory.
4. Tell the user:
   - Which soul was installed (name + category).
   - That they should **reset the conversation** (e.g. `/clear` or start a new session) to load the new persona.
   - That the previous SOUL.md was backed up and can be restored with this skill.
   - (First time only) That the original SOUL.md has been saved and can be restored at any time.

### Step 5: Rollback (if requested)

When the user asks to revert / rollback / restore the previous SOUL.md:

1. List all files in `.soul_backups/` sorted alphabetically.
2. Show them to the user with a numbered list. Each backup is named `SOUL.md.<slug>` (e.g. `SOUL.md.sun_wukong`, `SOUL.md.confucius`), making it easy to identify which soul each backup contains. Highlight `SOUL.md.original` as **"[Original]"** if it exists — this is the user's initial persona before any soul was installed.
3. Ask the user which one to restore (the user can specify by slug name; if user says "original" / "最初" / "初始", use `SOUL.md.original`).
4. Back up the **current** SOUL.md the same way (so rollback is also reversible).
5. Copy the selected backup to `SOUL.md`.
6. Tell the user to reset the conversation to reload.

## Notes

- The `.soul_backups/` directory keeps a full history. The user can manually delete old backups.
- If no SOUL.md exists and no backup exists, skip the backup step.
- Always confirm with the user before overwriting SOUL.md.
