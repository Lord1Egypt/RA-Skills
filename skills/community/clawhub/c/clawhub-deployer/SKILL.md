---
name: clawhub-publish
description: Publish a skill to ClawHub registry. Use when user asks to publish, release, or deploy a skill to ClawHub.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Publish Skill to ClawHub

Validate, prepare, and publish a skill to the ClawHub registry.

## When to Trigger

- User asks to publish / release / deploy a skill to ClawHub
- User mentions `clawhub publish` or `publish skill`

## Workflow

### Step 1: Validate SKILL.md

Check that the target folder contains a valid `SKILL.md`:

```bash
ls TARGET_DIR/SKILL.md
head -20 TARGET_DIR/SKILL.md
```

Required frontmatter fields:
- `name` — lowercase + hyphens, must match `^[a-z0-9][a-z0-9-]*$`
- `description`
- `version` — semver format

Recommended fields for cross-platform compatibility:
- `allowed-tools` — for Claude Code
- `metadata.openclaw.requires.env` — required environment variables
- `metadata.openclaw.requires.bins` — required binaries

### Step 2: Check files

ClawHub only accepts text files: `.md`, `.py`, `.txt`, `.json`, `.yaml`, `.toml`, `.js`, `.ts`, `.svg`.

Must exclude:
- Images: `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.ico`
- Git: `.git/`, `.gitignore`
- License: `LICENSE` (ClawHub enforces MIT-0 for all skills)
- Environment: `.env`, `.DS_Store`

### Step 3: Prepare publish folder

Create a folder with only text files:

```bash
mkdir -p TARGET_DIR/clawhub-publish
cp TARGET_DIR/SKILL.md TARGET_DIR/*.py TARGET_DIR/*.md TARGET_DIR/*.txt clawhub-publish/
cp -r TARGET_DIR/docs clawhub-publish/docs 2>/dev/null || true
```

Add `clawhub-publish/` to `.gitignore` to keep the GitHub repo clean.

### Step 4: Login

```bash
npx clawhub@latest whoami 2>&1 || npx clawhub@latest login
```

### Step 5: Publish

```bash
npx clawhub@latest publish TARGET_DIR/clawhub-publish/ \
  --slug SLUG \
  --name "DISPLAY_NAME" \
  --version VERSION \
  --changelog "CHANGELOG" \
  --tags latest
```

- `SLUG`: globally unique, lowercase + hyphens
- `DISPLAY_NAME`: human-readable name, can include spaces
- `VERSION`: semver (e.g. `1.0.0`)
- `CHANGELOG`: use `Initial release.` for first publish

### Step 6: Verify

```bash
npx clawhub@latest inspect SLUG
```

## Error Handling

| Error | Fix |
|-------|-----|
| `Slug is required` | Add `--slug` parameter |
| `Taken` | Choose a different slug |
| `GitHub API rate limit` | Wait for reset (usually 10–60 seconds), then retry |
| `Remove non-text files` | Go back to Step 3, ensure only text files are included |
| `SKILL.md is required` | Confirm SKILL.md exists inside the publish folder |

## SKILL.md Template

```yaml
---
name: my-skill
description: One-line description of what this skill does.
version: 1.0.0
allowed-tools: Bash, Write, Read
metadata:
  openclaw:
    requires:
      env: [MY_API_KEY]
      bins: [python3]
    primaryEnv: MY_API_KEY
    emoji: "🔧"
    homepage: https://github.com/USER/REPO
    os: [macos, linux, windows]
---

# Skill Title

What this skill does.

## When to Trigger
- Trigger condition 1
- Trigger condition 2

## Usage
(Instructions for the AI on how to invoke the skill)

## Environment
(How to obtain and configure required API keys)

## Errors
(Common errors and fixes)
```
