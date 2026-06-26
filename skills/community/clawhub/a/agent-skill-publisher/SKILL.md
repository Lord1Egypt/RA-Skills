---
name: skill-publisher
description: >
  End-to-end workflow for publishing agent skills to GitHub, ClawdHub, and skills.sh.
  Handles repo creation, topic tagging, ClawdHub publish, skills.sh index request,
  and installation verification. Use when: "publish skill", "上架 skill", "发布技能",
  "submit to skills.sh", "submit to clawhub", "skill 上架流程".
version: 1.0.0
metadata:
  openclaw:
    emoji: "rocket"
    homepage: https://github.com/bryant24hao/skill-publisher
    os:
      - macos
      - linux
---

# Skill Publisher

End-to-end publishing workflow for agent skills. Covers GitHub, ClawdHub, and skills.sh — from pre-flight checks to installation verification.

## Language

Respond in the same language the user used to invoke this skill. Fall back to English if no language signal is found.

## Prerequisites

```bash
command -v gh >/dev/null || echo "CRITICAL: gh (GitHub CLI) not found — install with: brew install gh"
command -v git >/dev/null || echo "CRITICAL: git not found"
```

Optional (for ClawdHub publishing):
```bash
npx clawhub --help >/dev/null 2>&1 || echo "INFO: clawhub CLI not installed — needed for ClawdHub publishing"
```

## Workflow Overview

The full publishing pipeline has 6 phases:

```
1. Pre-flight Check    → Validate skill structure and content
2. GitHub Publish      → Create repo, push, add topics
3. ClawdHub Publish    → Publish to ClawdHub registry
4. skills.sh Submit    → Submit index request via GitHub issue
5. Install Verify      → Test all installation methods
6. Post-publish        → Summary with all links and install commands
```

Run phases sequentially. If the user only wants a specific phase (e.g., "just submit to skills.sh"), skip to that phase.

## Phase 1: Pre-flight Check

Validate the skill directory before publishing. Check ALL of the following:

### 1.1 Required Files

```bash
SKILL_DIR="<path-to-skill>"  # Ask user or infer from context

# Required
[ -f "$SKILL_DIR/SKILL.md" ] || echo "FAIL: SKILL.md missing"
[ -f "$SKILL_DIR/LICENSE" ]  || echo "FAIL: LICENSE missing"
[ -f "$SKILL_DIR/README.md" ] || echo "FAIL: README.md missing"
```

### 1.2 SKILL.md Frontmatter

Read `SKILL.md` and verify YAML frontmatter contains:
- `name` — required, should be kebab-case
- `description` — required, should be descriptive (used by search engines and skill discovery)
- `version` — required, valid semver

Optional but recommended:
- `metadata.openclaw.emoji`
- `metadata.openclaw.homepage`
- `metadata.openclaw.os`
- `metadata.openclaw.requires.bins` (list of required CLI tools)

### 1.3 README Quality

Check README.md for:
1. **Badges** — at least License badge. Platform badge recommended.
2. **Description** — clear one-liner explaining what the skill does.
3. **Install section** — should have placeholder install commands (will be updated after publishing).
4. **No broken links** — scan for URLs pointing to non-existent repos or placeholder orgs.
5. **No hardcoded user paths** — scan for `/Users/xxx/` or `/home/xxx/` patterns.
6. **Secret redaction** — no API keys, tokens, or passwords in plain text.

### 1.4 Bilingual README (Optional)

If the skill targets both Chinese and English users, check for:
- `README.zh-CN.md` exists
- Both READMEs have language switcher links at the top
- Both have consistent content (same sections, same install commands)

### 1.5 Report

Present findings:

```
# Pre-flight Report

## Required Files
- [x] SKILL.md
- [x] LICENSE (MIT)
- [x] README.md
- [ ] README.zh-CN.md (optional, not found)

## SKILL.md Frontmatter
- name: my-skill
- version: 1.0.0
- description: OK (127 chars)

## Issues Found
- WARNING: README contains placeholder org "nicepkg" — update before publishing
- INFO: No .gitignore found (optional but recommended)

## Ready to publish? YES / NO (with blockers listed)
```

## Phase 2: GitHub Publish

### 2.1 Initialize Git Repo

```bash
cd "$SKILL_DIR"
git init
git add -A
git status  # Review staged files
```

**Before committing**, scan staged files for:
- Secrets (API keys, tokens, passwords)
- User-specific absolute paths (`/Users/xxx/`)
- Large binary files (> 1MB)

```bash
git commit -m "Initial release: <skill-name> v<version>"
```

### 2.2 Determine Repo Name

Ask the user for their preferred GitHub repo name. Default: same as the skill's `name` field in SKILL.md frontmatter.

**Important**: Check if the name is already taken on ClawdHub before creating the GitHub repo, so they can be consistent:

```bash
npx clawhub inspect <proposed-name> 2>&1
```

If taken on ClawdHub, suggest alternatives and let the user choose a name that works on both platforms.

### 2.3 Create GitHub Repo

```bash
gh repo create <owner>/<repo-name> \
  --public \
  --description "<skill description from SKILL.md>" \
  --source . \
  --push
```

### 2.4 Add GitHub Topics

Add discoverable topics for skills.sh indexing and general discoverability:

```bash
gh repo edit <owner>/<repo-name> --add-topic agent-skill,claude-code-skill
```

Additional topic suggestions based on skill content:
- Category topics: `productivity`, `devtools`, `security`, `health-check`, etc.
- Platform topics: `macos`, `linux`, `openclaw`
- Technology topics: `eventkit`, `calendar`, etc.

### 2.5 Update References

After repo creation, update all files that reference the repo:
- `README.md` — badge links, install commands, git clone URL
- `README.zh-CN.md` — same
- `SKILL.md` — `metadata.openclaw.homepage`
- `docs/` — any user story or doc files with install commands
- `LICENSE` — copyright holder

```bash
# Verify no stale references remain
grep -r "placeholder-org\|nicepkg\|example-user" "$SKILL_DIR" --include="*.md"
```

Commit and push the updates.

## Phase 3: ClawdHub Publish

### 3.1 Login

```bash
npx clawhub whoami 2>&1 || npx clawhub login
```

### 3.2 Check Slug Availability

```bash
npx clawhub inspect <slug> 2>&1
```

If slug is taken, suggest alternatives based on the skill name.

### 3.3 Publish

```bash
npx clawhub publish "$SKILL_DIR" \
  --slug <slug> \
  --name "<display-name>" \
  --version <version> \
  --changelog "<changelog text>"
```

**Known issue (as of clawhub CLI v0.7.0)**: The server requires `acceptLicenseTerms: true` in the publish payload, but the CLI doesn't include it. If you get:

```
Error: Publish payload: acceptLicenseTerms: invalid value
```

Fix by patching the local CLI:

```bash
# Find the publish.js file
PUBLISH_JS="$(find ~/.npm/_npx -name 'publish.js' -path '*/clawhub/dist/cli/commands/*' 2>/dev/null | head -1)"

# Add acceptLicenseTerms to the payload
# In the JSON.stringify block, add: acceptLicenseTerms: true,
```

Then retry the publish command.

### 3.4 Verify

```bash
npx clawhub inspect <slug>
```

## Phase 4: skills.sh Index Request

skills.sh does **NOT** auto-index skills. You must submit a request via GitHub issue.

### 4.1 Submit Index Request

```bash
gh issue create --repo vercel-labs/skills \
  --title "Request to index skill: <owner>/<repo>" \
  --body "$(cat <<'ISSUE_EOF'
## Skill Information

- **Repository:** https://github.com/<owner>/<repo>
- **Skill name:** <skill-name>
- **Install:** \`npx skills add <owner>/<repo>\`
- **License:** MIT

## Description

<2-3 sentence description of what the skill does and its key features>
ISSUE_EOF
)"
```

### 4.2 Note to User

Explain that:
- The index request is reviewed by the vercel-labs/skills maintainers
- It may take days to be processed
- The `npx skills add <owner>/<repo>` install command works immediately (it clones from GitHub directly)
- Only the `npx skills search` / `npx skills find` discovery requires indexing

## Phase 5: Installation Verification

Test all three installation methods sequentially. Back up any existing installation first.

### 5.1 skills.sh

```bash
npx skills add <owner>/<repo> -g -y
# Verify: check installation path and file completeness
ls ~/.agents/skills/<skill-name>/ || ls ~/.claude/skills/<skill-name>/
# Cleanup
npx skills remove <skill-name> -g -y
```

### 5.2 ClawdHub

```bash
npx clawhub install <slug>
# Verify
ls ~/clawd/skills/<slug>/
# Cleanup
npx clawhub uninstall <slug> --yes
```

### 5.3 Manual Git Clone

```bash
git clone https://github.com/<owner>/<repo>.git /tmp/test-skill-install
# Verify
ls /tmp/test-skill-install/
# Cleanup
rm -rf /tmp/test-skill-install
```

### 5.4 Report

```
# Installation Verification

| Method | Command | Result |
|--------|---------|--------|
| skills.sh | npx skills add <owner>/<repo> -g -y | OK / FAIL |
| ClawdHub | clawhub install <slug> | OK / FAIL |
| Manual | git clone ... | OK / FAIL |
```

## Phase 6: Post-publish Summary

Present a final summary with all links and commands:

```
# Published: <skill-name> v<version>

## Links
- GitHub: https://github.com/<owner>/<repo>
- ClawdHub: https://clawhub.ai/<owner>/<slug> (if published)
- skills.sh: pending indexing (issue #NNN)

## Install Commands
# skills.sh (recommended)
npx skills add <owner>/<repo> -g -y

# ClawdHub
clawhub install <slug>

# Manual
git clone https://github.com/<owner>/<repo>.git ~/.claude/skills/<skill-name>

## Next Steps
- [ ] Wait for skills.sh indexing (issue #NNN)
- [ ] Share the GitHub link
- [ ] Consider creating a GitHub Release with tag v<version>
```

## Important Notes

- **Slug consistency**: Try to use the same name on GitHub and ClawdHub. If ClawdHub slug is taken, rename the GitHub repo to match the available ClawdHub slug for consistency.
- **README install commands**: Always update install commands in all README files after determining the final repo name and ClawdHub slug.
- **Bilingual docs**: If the skill has docs (e.g., user stories), create bilingual versions with language switcher links. English docs should use internationally recognizable examples (Telegram, not Feishu).
- **Pre-commit privacy check**: Before every git push, scan for real IP addresses, API keys, WiFi credentials, user-specific paths, and other PII.
- **ClawdHub CLI bug**: The `acceptLicenseTerms` patch is needed as of CLI v0.7.0. Check if newer versions fix this before patching.
