---
name: publish-skill
version: 1.0.1
description: Prepare and publish an OpenClaw skill to ClawHub. Handles PII/secret auditing, generalization, env var extraction, directory scaffolding, git init, and the clawhub publish command. Use when publishing a new skill or updating an existing one on ClawHub.

---

# Publish Skill

Prepare and publish an OpenClaw skill to ClawHub. This skill codifies the audit → generalize → publish workflow.

## When To Use

- Publishing a new skill to ClawHub
- Updating an existing published skill
- When the user says "publish this skill", "prepare for publishing", "make a publishable copy"
- NOT for installing skills from ClawHub (that's `npx clawhub@latest install`)

## Workflow

### Step 1: Audit the Live Skill

Before creating any copy, audit the source skill for secrets and PII:

1. Read every file in the skill directory recursively
2. Check for these categories of sensitive content:

| Category | Examples | Action |
|----------|----------|--------|
| **Secrets** | API keys, tokens, passwords, private keys | Must remove |
| **Paths** | Absolute paths (`/home/username/...`, `/Users/...`) | Replace with env var or `~` relative |
| **Discord IDs** | Channel IDs, user IDs, guild IDs, message IDs | Remove or replace with env var |
| **Timezones** | Hardcoded IANA timezone strings | Replace with env var |
| **Personal data** | Real names, emails, phone numbers, medication names | Remove or generalize |
| **Network info** | IP addresses, internal URLs, port numbers | Remove or replace with placeholders |
| **Custom identifiers** | User-specific labels, internal project names | Generalize |

3. Report findings to the user before proceeding — do not silently modify

### Step 2: Create Publishable Copy

Create a separate directory (never modify the live skill):

```
$CLAWHUB_DEFAULT_DIR/<skill-name>-skill/
```

Default base: `~/projects/skills` (override via `CLAWHUB_DEFAULT_DIR` env var).

Directory structure:
```
<skill-name>-skill/
├── SKILL.md           # Manifest (generalized)
├── README.md          # User-facing docs
├── .gitignore         # Standard ignores
├── scripts/           # Script files (generalized)
├── references/        # Optional reference docs
└── ...                # Any other skill-specific files
```

### Step 3: Generalize Content

For each file in the skill:

**SKILL.md frontmatter:**
- Add `env:` block declaring all extracted env vars with descriptions and required/optional
- Remove any personal identifiers from `description`

**Scripts (Python, Shell, etc.):**
- Replace hardcoded paths with `os.environ.get("VAR", fallback)` / env var reads
- Replace hardcoded timezones with env var (UTC fallback)
- Remove `now()`/`utc_now()` fallbacks that bypass source timestamps — raise errors instead
- Remove personal data (medication names become empty lists with edit instructions, etc.)
- Remove dead code and unused imports

**Documentation (Markdown):**
- Remove Discord IDs, channel names, user IDs
- Replace personal examples with generic ones
- Keep timezone/ID references only as example values (e.g. "e.g. America/Los_Angeles")
- Remove internal URLs/IPs

**Shell wrappers:**
- Use relative path resolution: `SCRIPT="$(cd "$(dirname "$0")" && pwd)/tracker.py"`
- Remove hardcoded absolute paths

### Step 4: Verify Clean State

Run a final grep across all files:
```bash
grep -rn "hardcoded_pattern1\|hardcoded_pattern2\|..." --include="*.py" --include="*.md" --include="*.sh" .
```

Verify:
- No secrets or tokens remain
- No absolute paths containing usernames
- No Discord/user IDs
- No personal data (real names, specific medication names, etc.)
- Timezone strings only in examples/comments, never as runtime defaults
- All config via env vars with sensible defaults

### Step 5: Git Init and Commit

```bash
git init
git add -A
git commit -m "Initial publishable copy — no PII, no secrets"
```

### Step 6: Publish (with user confirmation)

**Always confirm with the user before publishing.**

```bash
npx clawhub@latest publish --slug <skill-name> --version <version> --name "<display name>" /absolute/path/to/skill-dir
```

**Gotchas:**
- **Use absolute paths**, not `.` — cwd may not propagate through exec/shell layers
- `--slug` is required — without it, the CLI picks up the directory name
- **Slug naming is competitive** — every generic name (`publish-skill`, `skill-publisher`, etc.) is likely taken. Pick something unique or namespaced (e.g. `myname-publish-helper`)
- Rate limited — if you get slug collisions repeatedly, wait 50s between retries

Common version bumps:
- New skill: `1.0.0`
- Bug fix: patch bump (e.g. `1.0.0` → `1.0.1`)
- New feature: minor bump (e.g. `1.0.0` → `1.1.0`)

After publishing, report the slug, version, and install command to the user.

## Common Patterns

### Extracting env vars from hardcoded values

Before:
```python
TIMEZONE = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/home/user/.openclaw/workspace"
```

After:
```python
TZ_STR = os.environ.get("MEDICATION_TIMEZONE", "UTC")
TIMEZONE = ZoneInfo(TZ_STR)
WORKSPACE = os.environ.get("WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
```

### Replacing personal config with user-editable sections

Before:
```python
MORNING_MEDS = ["RealMedA", "RealMedB"]
KNOWN_MEDS = ["RealMedA", "RealMedB", "RealMedC"]
```

After:
```python
# Edit these lists to match your regimen
MORNING_MEDS: list[str] = []  # e.g. ["MedA", "MedB"]
KNOWN_MEDS: list[str] = []   # e.g. ["MedA", "MedB", "MedC"]
```

### Removing timestamp fallbacks

Before:
```python
dt_utc = datetime.fromisoformat(ts) if ts else datetime.now(timezone.utc)
```

After:
```python
if not ts:
    raise ValueError("timestamp_utc is required — source message timestamp must be provided")
dt_utc = datetime.fromisoformat(ts.replace("Z", "+00:00"))
```

### Changelog

Add `--changelog <text>` to the publish command for release notes. Example:
```bash
npx clawhub@latest publish --slug my-skill --version 1.1.0 --changelog "Added env var support, fixed timestamp handling" .
```

## ClawHub CLI Reference

| Command | Purpose |
|---------|---------|
| `npx clawhub@latest login` | Authenticate (browser callback) |
| `npx clawhub@latest whoami` | Verify auth |
| `npx clawhub@latest publish --slug X --version Y .` | Publish from current dir |
| `npx clawhub@latest inspect <slug>` | View published metadata |
| `npx clawhub@latest search <query>` | Search registry |

Publish must run from inside the skill directory (requires SKILL.md in cwd).

## Required Files

- `SKILL.md` — this file
- `references/checklist.md` — quick audit checklist

## Notes

- Never modify the live skill — always create a separate copy
- The publishable copy should work for anyone who installs it with minimal config
- If a skill can't be fully generalized (e.g. deeply personal workflows), document what the user needs to configure
- ClawHub registry may not display `env:` frontmatter — that's a registry display issue, not a skill issue
