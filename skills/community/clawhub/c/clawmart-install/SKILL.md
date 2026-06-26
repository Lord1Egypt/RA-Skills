---
name: clawmart-install
description: Search and install an OpenClaw configuration pack from ClawMart
version: 1.2.0
triggers:
  - "install from clawmart"
  - "install pack"
  - "clawmart install"
  - "search clawmart"
---

# ClawMart Install Skill

You are helping the user find and install an OpenClaw configuration pack from ClawMart. Follow these steps exactly and in order.

## Configuration

- ClawMart API base URL: `https://clawmart-gray.vercel.app`
- Config file: `~/.openclaw/clawmart-config.json`
- Install target: `~/.openclaw/workspace/` (non-skill files)
- Skills target: `~/.openclaw/workspace/skills/` (skill folders)
- Backup directory: `~/.openclaw/backups/`

---

## Step 1: Check API Token

Read `~/.openclaw/clawmart-config.json`. If the file does not exist or `token` is empty:

Tell the user:
> You need a ClawMart API Token to download packs. Please visit https://clawmart-gray.vercel.app/dashboard/tokens to generate one, then paste it here.

Once the user provides a token (format: `cm_` followed by hex characters), save it:

```json
{
  "token": "<user_provided_token>",
  "base_url": "https://clawmart-gray.vercel.app"
}
```

Write this to `~/.openclaw/clawmart-config.json`.

---

## Step 2: Determine Search Query

Extract the pack name from the user's message. If the user said something like "install Deep Research Analyst", the search query is "Deep Research Analyst".

If no specific name was mentioned, ask:
> Which pack would you like to install? Enter a search keyword.

---

## Step 3: Search ClawMart

Call:
```
GET {base_url}/api/packs/search?q={query}&limit=8
```

Parse the `packs` array from the response. If empty, tell the user:
> No packs found matching "{query}". Please try different keywords.

Then stop.

If results exist, display them as a numbered list:

```
Found the following packs:

1. <Pack Title A>
   By: @username · ⭐ 4.8 · ↓ 1.2K
   Contains: SOUL, AGENTS, MEMORY, SKILLS ×3
   "Pack description..."

2. <Pack Title B>
   By: @username · ⭐ 4.5 · ↓ 856
   Contains: SOUL, AGENTS
   "Pack description..."

Select a pack to install (enter number, or 0 to cancel):
```

Wait for user input.

---

## Step 4: Show Pack Details

Use the data already returned from the search response (no extra API call needed). Display:

```
Pack Details:
─────────────────────────────
Title:       <pack.title>
By:          @<pack.creator.username>
Rating:      ⭐ <pack.avg_rating> · ↓ <pack.download_count>

Description:
<pack.description>
─────────────────────────────

Confirm install? (y/n)
```

Note the `id` from the search result — it is used in Step 6 to call the download endpoint.

---

## Step 5: Check for Conflicts

Before downloading, check what files exist in `~/.openclaw/workspace/` and `~/.openclaw/skills/`.

Compare with the pack's file list. If any files would be overwritten, list them:

```
The following files will be overwritten (originals will be backed up to ~/.openclaw/backups/2026-03-28-143022/):

  · claude.soul.md  (existing file will be backed up)
  · research.agents.md  (new file)

Continue? (y/n)
```

---

## Step 6: Download Pack

Call the download endpoint:

```
POST {base_url}/api/packs/{id}/download
Authorization: Bearer {token}
Content-Type: application/json
```

The response is JSON — **no signed URL, no ZIP file**:

```json
{
  "version": "1.0.0",
  "files": [
    { "name": "SOUL.md",               "type": "SOUL",   "size": 4200, "content": "..." },
    { "name": "skills/my.skill.md",    "type": "SKILLS", "size": 980,  "content": "..." },
    { "name": "skills-manifest.json",  "type": "OTHER",  "size": 180,  "content": "{\"clawhub_skills\":[...]}" }
  ]
}
```

Store this response in memory for Step 8.

---

## Step 7: Backup Conflicting Files

If any conflicting files were found in Step 5:

1. Create backup directory: `~/.openclaw/backups/{YYYY-MM-DD-HHmmss}/`
2. Copy each conflicting file to the backup directory
3. Tell the user: `Backed up {n} file(s) to ~/.openclaw/backups/{timestamp}/`

---

## Step 8: Install Files

Write each entry from the `files` array in the download response:

- `type == "SKILLS"` → write `content` to `~/.openclaw/workspace/skills/{name without skills/ prefix}/SKILL.md`
- `name == "skills-manifest.json"` → **do not write to disk**; parse the JSON and display the `clawhub_skills` list (see below)
- All other files → write `content` to `~/.openclaw/workspace/{name}`

Create directories if they don't exist.

**External skills handling:** If the response includes a `skills-manifest.json` file, parse its `clawhub_skills` array and inform the user:

```
This pack references external skills that are not installed automatically:

  - <skill-slug-1>  (v1.0.0)
  - <skill-slug-2>  (v2.0.0)

To install them, run the appropriate plugin install command for each source.
```

---

## Step 9: Confirm Installation

Tell the user:

```
Installation complete!

Installed to ~/.openclaw/workspace/:
  · claude.soul.md
  · research.agents.md
  · deep_analysis.boot.md
  · memory_projects.json

Installed to ~/.openclaw/skills/:
  · 3 skill files

Backup location: ~/.openclaw/backups/2026-03-28-143022/ (copy files back to restore)

Restart OpenClaw to load the new configuration.
```

---

## Notes

- Pack detail page: `{base_url}/packs/{id}`
- If token authentication fails (401), direct the user to regenerate at `{base_url}/dashboard/tokens`
- Local skill files are installed to `~/.openclaw/workspace/skills/` and visible after installation
- External skills listed in `skills-manifest.json` must be installed separately via their own source
- No restart required — OpenClaw loads new configuration on the next conversation
