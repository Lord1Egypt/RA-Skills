# ClawhHub Publication Guide

**Complete step-by-step guide for publishing ClawText-Ingest to ClawhHub.**

---

## Overview

ClawhHub is the OpenClaw skill marketplace. Publishing ClawText-Ingest there makes it discoverable and installable by the community.

**Current Status:**
- ✅ Code ready (Phase 1 + Phase 2 complete)
- ✅ Tests passing (22/22)
- ✅ Documentation complete
- ✅ Ready for publication

---

## Before Publishing

### Checklist

- [ ] **All tests passing**
  ```bash
  npm test && npm run test:discord && npm run test:discord-cli
  ```

- [ ] **Version updated** in `package.json` (should be 1.3.0)
  ```json
  "version": "1.3.0"
  ```

- [ ] **README.md is current** (includes Discord section)

- [ ] **SKILL.md is valid YAML** (frontmatter correct)

- [ ] **Git working directory clean**
  ```bash
  git status  # Should show "nothing to commit"
  ```

- [ ] **GitHub repository public** (https://github.com/ragesaq/clawtext-ingest)

- [ ] **clawhub.json exists** in repository root

---

## Step 1: Verify Git Status

```bash
cd ~/.openclaw/workspace/skills/clawtext-ingest

# Check working directory is clean
git status

# Check latest commits
git log --oneline -5

# Verify tag exists (or create if needed)
git tag v1.3.0
git push origin v1.3.0
```

Expected output:
```
[main 50a15d1] docs: add quick reference guide
On branch main
nothing to commit, working tree clean
```

---

## Step 2: Verify Files

ClawhHub requires these files in the repository root:

```bash
# Check required files
ls -l README.md SKILL.md clawhub.json LICENSE package.json

# Expected output:
# README.md         <- Main documentation
# SKILL.md          <- Skill metadata (YAML frontmatter)
# clawhub.json      <- ClawhHub manifest
# LICENSE           <- MIT or compatible
# package.json      <- Node.js manifest
```

### File Content Verification

**README.md** — Should start with title and description:
```bash
head -20 README.md
# Expected: # ClawText Ingest
#           Version: 1.3.0
#           Convert multi-source data...
```

**SKILL.md** — Should have YAML frontmatter:
```bash
head -10 SKILL.md
# Expected: ---
#           name: ClawText Ingest
#           description: Multi-source memory ingestion...
#           ---
```

**clawhub.json** — Should be valid JSON:
```bash
cat clawhub.json | jq .
# Expected: JSON output, no errors
```

**package.json** — Should have bin entry:
```bash
cat package.json | jq '.bin'
# Expected: {
#             "clawtext-ingest": "bin/ingest.js",
#             "clawtext-ingest-discord": "bin/discord.js"
#           }
```

---

## Step 3: Go to ClawhHub

1. **Visit:** https://clawhub.com
2. **Sign in:** Click "Sign in with GitHub" → Authorize
   - Use GitHub account: `ragesaq`
   - Authorize ClawhHub to access repositories

---

## Step 4: Submit ClawText-Ingest

### Option A: If ClawhHub Has "Publish" Button

1. Click **"Publish Skill"** or **"Submit New Skill"**
2. Fill in:
   - **Repository URL:** `https://github.com/ragesaq/clawtext-ingest`
   - **Version:** `1.3.0`
   - **Category:** "Memory & Knowledge Management" (or "Data Processing")
   - **License:** MIT
3. Click **"Validate"** (ClawhHub will check files)
4. Click **"Publish"**

### Option B: If ClawhHub Requires Repository Link

1. Click **"Add Repository"**
2. Paste: `https://github.com/ragesaq/clawtext-ingest`
3. ClawhHub auto-fetches:
   - README.md (main documentation)
   - SKILL.md (metadata + formatting)
   - clawhub.json (custom settings)
   - package.json (dependencies, binaries)
   - LICENSE (MIT)

---

## Step 5: Verify Submission

After publishing, ClawhHub will:

1. **Validate files** — Check README, SKILL.md, package.json
2. **Extract metadata** — Name, description, version, author, keywords
3. **Index for search** — Make skill discoverable by keywords
4. **Link related skills** — Auto-detect ClawText link via `peerDependencies`

---

## Step 6: Test Installation

After ClawhHub lists the skill, verify installation works:

```bash
# Option 1: Using openclaw CLI
openclaw install clawtext-ingest

# Option 2: Using npm (if you have ClawhHub as npm registry)
npm install @clawhub/clawtext-ingest

# Verify binaries work
clawtext-ingest help
clawtext-ingest-discord help
```

Expected output:
```
$ clawtext-ingest help

ClawText Ingest - Multi-source memory ingestion

Commands:
  help              Show this help message
  ingest-files      Ingest files matching patterns
  ...
```

---

## Step 7: Verify on ClawhHub

On ClawhHub skill page, verify:

- ✅ **Title:** "ClawText Ingest"
- ✅ **Version:** 1.3.0
- ✅ **Description:** "Multi-source data ingestion with Discord support"
- ✅ **Author:** ragesaq
- ✅ **Category:** Memory & Knowledge Management
- ✅ **Keywords:** openclaw, memory, rag, ingestion, discord
- ✅ **Installation:** `openclaw install clawtext-ingest`
- ✅ **Related Skills:** ClawText (linked)
- ✅ **Documentation:** README, SKILL.md accessible

---

## Cross-Linking with ClawText

Both skills reference each other for discoverability:

### ClawText-Ingest's clawhub.json

```json
{
  "peerDependencies": {
    "clawtext": ">=1.2.0"
  },
  "relatedSkills": ["clawtext"],
  "description": "Multi-source data ingestion (Discord, files, JSON) for ClawText RAG layer"
}
```

**Effect:** When users view ClawText-Ingest on ClawhHub, they see:
> "Requires: ClawText >=1.2.0"
> "Related skills: ClawText"

### ClawText's clawhub.json

```json
{
  "relatedSkills": ["clawtext-ingest"],
  "companion_tools": {
    "clawtext-ingest": "Multi-source data ingestion for populating memory"
  }
}
```

**Effect:** When users view ClawText on ClawhHub, they see:
> "Related skills: ClawText-Ingest"
> "Use with: ClawText-Ingest for multi-source ingestion"

**Result:** Users installing one skill automatically discover the other. ✅

---

## Updating After Publication

When you make updates and want to bump version:

### 1. Update Version

```bash
# In package.json
"version": "1.3.1"

# Commit
git add package.json
git commit -m "bump version to 1.3.1"
```

### 2. Create Tag

```bash
git tag v1.3.1
git push origin v1.3.1
```

### 3. Re-submit to ClawhHub

1. Go to ClawhHub
2. Click on ClawText-Ingest skill
3. Click **"Update"** or **"Edit"**
4. Set version to `1.3.1`
5. Click **"Publish"**

ClawhHub will fetch the new tag and update the listing.

---

## Troubleshooting

### "Repository not found"

- [ ] Verify GitHub URL is correct: `https://github.com/ragesaq/clawtext-ingest`
- [ ] Verify repository is **public** (not private)
- [ ] Verify you're signed in with GitHub account that has access

### "README.md not found"

- [ ] Verify file exists in repository root
- [ ] Verify filename is exactly `README.md` (case-sensitive)
- [ ] Verify file is not in subdirectory

### "SKILL.md validation failed"

- [ ] Check YAML frontmatter is valid:
  ```bash
  head -15 SKILL.md | cat -A  # Check for hidden characters
  ```
- [ ] Verify quotes are balanced
- [ ] Verify dashes are exactly `---` (three dashes)

### "clawhub.json not valid JSON"

```bash
cat clawhub.json | jq .  # Should output valid JSON
```

If invalid:
- [ ] Check for trailing commas
- [ ] Verify all quotes are matching
- [ ] Verify no comments (JSON doesn't allow them)

### "Installation fails after publishing"

```bash
# Test locally first
npm install -g .

clawtext-ingest help
```

If that works, issue is likely temporary (ClawhHub CDN cache). Try again in 5 minutes.

---

## Success Checklist

After publishing, verify:

- ✅ Skill appears in ClawhHub search for "clawtext"
- ✅ Skill page shows correct version (1.3.0)
- ✅ README displays properly on ClawhHub
- ✅ Installation command works: `openclaw install clawtext-ingest`
- ✅ Binaries are available: `clawtext-ingest`, `clawtext-ingest-discord`
- ✅ ClawText is linked as related skill
- ✅ Keywords are searchable (memory, rag, discord, ingestion)

---

## Post-Publication Tasks

### 1. Announce (Optional)

Share on OpenClaw community:
- Discord: #skills-showcase
- GitHub Discussions
- Email (if applicable)

**Announcement Template:**

```
🎉 ClawText-Ingest v1.3.0 Published!

Multi-source memory ingestion for OpenClaw agents.

✨ New Features:
- Direct Discord forum ingestion
- Real-time progress tracking
- Auto-batch mode for large forums
- Full agent autonomy support

📦 Install: `openclaw install clawtext-ingest`

📖 Docs: https://github.com/ragesaq/clawtext-ingest

Works with: ClawText RAG layer
```

### 2. Monitor

Check ClawhHub regularly:
- Installation count
- User feedback
- Issues or bug reports
- Feature requests

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-03-03 | Initial release (Phase 1) |
| 1.3.0 | 2026-03-05 | Discord integration (Phase 2) + Agent guides |

---

## See Also

- [ClawhHub](https://clawhub.com) — Skill marketplace
- [OpenClaw Docs](https://docs.openclaw.ai) — Platform documentation
- [ClawText README](https://github.com/ragesaq/clawtext) — Companion skill
- [AGENT_GUIDE.md](./AGENT_GUIDE.md) — Agent integration examples
