# Publishing to ClawHub — Step-by-step

> **Important context:** This guide is assembled from web-search summaries of ClawHub's documentation, not from direct firsthand verification. Before submitting, run through the **verification checklist at the bottom** against the live official docs (https://github.com/openclaw/clawhub and https://docs.openclaw.ai). The format may have changed since this skill was written.

## Prerequisites

| Requirement | Status |
|---|---|
| GitHub account at least one week old | You handle this |
| ClawHub CLI installed | `npm install -g @openclaw/clawhub-cli` (verify package name in current docs) |
| Logged in to ClawHub via CLI | `clawhub login` (uses GitHub OAuth) |
| Skill folder ready | ✓ This folder |

## Step 1 — Verify CLI version and login

```bash
cd "indian-stock-monitor-clawhub"

# Confirm CLI is installed and check version
clawhub --cli-version

# See full command list (useful reference)
clawhub --help

# Log in if you haven't already (opens browser for GitHub OAuth)
clawhub login
clawhub whoami
```

Note: as of CLI v0.8.0 there is no separate `validate` subcommand — validation runs at publish time. To preview what `publish` accepts:

```bash
clawhub publish --help
```

Common things ClawHub will check at publish time:
- `name` must be lowercase-kebab-case
- `version` must be valid semver
- `category` must be one of ClawHub's known categories
- `license` must be in their allowlist

## Step 2 — Update author and repository fields

Open `SKILL.md` and replace the placeholders in the YAML frontmatter:

```yaml
author: your-name-here          # → your GitHub handle or display name
homepage: https://github.com/your-org/indian-stock-monitor   # → your actual repo
repository: https://github.com/your-org/indian-stock-monitor # → your actual repo
```

Do the same in `manifest.json` (`author`, `homepage`, `repository`).

## Step 3 — Push to GitHub (if not already)

ClawHub typically requires a public GitHub repo to publish from:

```bash
cd "indian-stock-monitor-clawhub"
git init
git add .
git commit -m "Initial release v1.0.0"
git branch -M main
git remote add origin https://github.com/your-org/indian-stock-monitor.git
git push -u origin main
```

Tag the release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Step 4 — Publish to ClawHub

CLI v0.8.0 takes a single positional path argument plus required flags. **Note**: even though `SKILL.md` has `version: 1.0.0` in its frontmatter, CLI v0.8.0 still requires `--version` as an explicit flag.

**Listing title on clawhub.ai:** The CLI sets the skill card title from **`--name`**, or else from **`TitleCase(folder basename)`**. It does **not** read `displayName` from `SKILL.md`. This repo folder is `indian-stock-monitor-clawhub`, so omitting `--name` produces the wrong title (“Indian Stock Monitor Clawhub”). Always pass:

`--name "AI stock watchdog"`

```bash
cd "indian-stock-monitor-clawhub"
clawhub publish "$(pwd)" \
  --slug ai-stock-watchdog \
  --name "AI stock watchdog" \
  --version 2.2.0
```

Use `$(pwd)` (absolute path) if `clawhub publish .` fails with “SKILL.md required” (known quirk with `.` in some setups).

To see all flags upfront before publishing:
```bash
clawhub publish --help
```

If `clawhub publish --help` lists optional flags you want to set, the typical pattern is:

```bash
clawhub publish . \
  --tags latest \
  --changelog "Initial release: daily NSE/BSE watchdog with conversational portfolio management"
```

(There is **no** `clawhub skill publish` or `clawhub package publish` in v0.8.0 — both were wrong in earlier drafts of this doc.)

### Bulk / sync alternative
If you have multiple skills in your workdir and want ClawHub to find new/updated ones automatically:

```bash
clawhub sync --dry-run    # preview
clawhub sync              # publish all changed skills
```

## Step 5 — Verify the listing

After publish completes, ClawHub will show a URL like `https://clawhub.ai/your-username/ai-stock-watchdog`. Visit it and check:
- Description renders correctly
- README is shown
- Examples are visible
- Install command is shown
- Tags and category are correct

## Step 6 — Anyone can now install

```bash
clawhub install your-username/ai-stock-watchdog
```

…which installs into their `./skills/` directory.

---

# Verification Checklist (read before submitting)

Run through these against the **live official ClawHub docs** before publishing. The format below is my best-effort reconstruction from web search — the live spec is authoritative.

## Frontmatter fields — verify these are real and correctly named
- [ ] `name` — required, kebab-case
- [ ] `slug` — required, kebab-case (verify if `slug` is the real field name vs `id`)
- [ ] `displayName` — verify field name (might be `display_name` or `title`)
- [ ] `description` — required
- [ ] `version` — required, semver
- [ ] `type: skill` — verify "skill" is a valid value (vs "agent", "plugin")
- [ ] `license: MIT-0` — verify accepted license values
- [ ] `category: finance` — verify "finance" is a valid category (vs "personal-finance", "investing", etc.)
- [ ] `tags` — verify array vs comma-string format
- [ ] `invocation.triggers` — verify this is the correct field name and structure
- [ ] `metadata.openclaw.requires.tools` — verify this nested structure is correct
- [ ] `compatibility.platforms` — verify platform names are valid
- [ ] `compatibility.platforms` — verify platform names

## Required files
- [ ] `SKILL.md` ✓
- [ ] `README.md` ✓
- [ ] `LICENSE` ✓ (MIT-0)
- [ ] `examples/` ✓ (3 examples included)
- [ ] `CHANGELOG.md` ✓
- [ ] `manifest.json` — verify if ClawHub uses this OR derives everything from SKILL.md frontmatter

## Optional but recommended
- [ ] Screenshots / demo GIF in README
- [ ] Test fixtures (verify if ClawHub has a test convention)
- [ ] Quality check: README explains what it does, who it's for, install steps

## File extension allowlist
ClawHub publishes only "text-based" files (per a `textFiles.ts` allowlist). Files in this skill:
- [x] `.md` — text
- [x] `.json` — text
- [x] `LICENSE` (no ext) — verify if accepted

## Security & quality
- [ ] No personal data in repo (verified — empty portfolio, empty ticker_to_sector)
- [ ] All external API calls clearly described in SKILL.md (web search only — no hardcoded API keys)
- [ ] No bundled binaries
- [ ] No network endpoints owned by you that could go down

## Things ClawHub may reject for that I'm not 100% certain about
- The skill uses `mcp__scheduled-tasks__create_scheduled_task` (declared as optional). ClawHub may reject skills that require host-specific MCP tools. The `mcp__workspace__bash` tool was removed in v1.0.1.
- The "{SKILL_DIR}" path convention I used in SKILL.md is a workaround for path portability. ClawHub may have a different convention (e.g., `${SKILL_PATH}` or relative paths).
- Examples are included as `.md` walkthroughs. ClawHub may prefer an `examples.json` schema.

**If validation fails for any of the above, the fix is usually a small frontmatter rename — not a structural change to the skill itself.**

---

# Security note

In late January 2026, ClawHub had to remove ~2,400 typosquatted skills that were distributing malware. The registry has since added VirusTotal scanning. Two implications:

1. **Be careful what you publish under your name** — your reputation is on the line.
2. **Use a clearly distinctive slug** — `ai-stock-watchdog` is fine; avoid anything that could be confused with another popular skill.
3. **Sign your commits and use 2FA on GitHub** — ClawHub's review checks GitHub account integrity.

---

# Where to verify everything in this guide

Authoritative sources:
- ClawHub repo: https://github.com/openclaw/clawhub
- Skill format spec: https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
- CLI reference: https://github.com/openclaw/clawhub/blob/main/docs/cli.md
- OpenClaw skills guide: https://docs.openclaw.ai/tools/skills
- ClawHub web: https://clawhub.ai

If any field name in this skill's `SKILL.md` frontmatter doesn't match what you find in those docs, rename in `SKILL.md` and re-run `clawhub skill validate .`.
