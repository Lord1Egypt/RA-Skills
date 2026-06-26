# CLAWHUB SKILL

**Name:** clawhub  
**Description:** ClawHub registry integration for OpenClaw skills publishing and distribution  
**Version:** 1.0.0  
**Status:** ACTIVE  

---

## 🎯 MISIÓN

Enable seamless publishing, distribution, and management of OpenClaw skills through ClawHub registry.

---

## 🔧 CONFIGURACIÓN

### Authentication

```bash
# Login to ClawHub (opens browser)
clawhub login

# Verify authentication
clawhub whoami

# Logout
clawhub logout
```

### Environment Variables

```bash
export CLAWHUB_SITE="https://clawhub.ai"
export CLAWHUB_REGISTRY="https://clawhub.ai"
export CLAWHUB_WORKDIR="$HOME/.openclaw"
```

---

## 📦 PUBLISHING WORKFLOW

### Quick Publish

```bash
# Single skill
clawhub publish ~/.openclaw/skills/my-skill \
  --slug "my-skill" \
  --version "1.0.0" \
  --changelog "Initial release" \
  --tags "latest,openclaw,automation"

# Using publish script
~/.openclaw/workspace/scripts/publish-to-clawhub.sh publish \
  ~/.openclaw/skills/my-skill
```

### Batch Sync

```bash
# Publish all valid skills
~/.openclaw/workspace/scripts/publish-to-clawhub.sh sync \
  ~/.openclaw/skills
```

### Validation Requirements

Before publishing, ensure:
- ✅ `SKILL.md` exists with Name and Description
- ✅ No sensitive data (API keys, credentials)
- ✅ Version follows semver (e.g., 1.0.0)
- ✅ Unique slug (check existing: `clawhub search <slug>`)

---

## 📊 METADATA STRUCTURE

### _meta.json (Auto-generated)

```json
{
  "ownerId": "<auto-assigned>",
  "slug": "skill-slug",
  "version": "1.0.0",
  "publishedAt": 1774384644739
}
```

### .clawhub/origin.json (After publish)

```json
{
  "version": 1,
  "registry": "https://clawhub.ai",
  "slug": "skill-slug",
  "installedVersion": "1.0.0",
  "installedAt": 1774384644739
}
```

---

## 🛠️ CLI COMMANDS

### Search & Discover

```bash
# Search skills
clawhub search "crypto trading"

# Explore latest
clawhub explore

# Inspect without install
clawhub inspect deep-scraper
```

### Install & Update

```bash
# Install skill
clawhub install <slug>

# Update installed skills
clawhub update [slug]

# List installed
clawhub list

# Uninstall
clawhub uninstall <slug>
```

### Publish & Manage

```bash
# Publish new skill
clawhub publish <path> [options]

# Update existing
clawhub publish <path> --version "1.1.0" --changelog "Bug fixes"

# Delete (moderator only)
clawhub delete <slug>

# Hide/Unhide
clawhub hide <slug>
clawhub unhide <slug>
```

---

## 📋 CATALOG MANAGEMENT

### Skill Discovery Pipeline

1. **Browse** → `clawhub explore` (latest updates)
2. **Search** → `clawhub search <query>` (vector search)
3. **Inspect** → `clawhub inspect <slug>` (preview metadata)
4. **Install** → `clawhub install <slug>` (download + configure)
5. **Update** → `clawhub update` (sync latest versions)

### Quality Standards

Published skills must:
- ✅ Have clear purpose and trigger conditions
- ✅ Include usage examples
- ✅ Document dependencies
- ✅ Follow naming conventions (kebab-case slugs)
- ✅ Be tested and functional

---

## 🔗 INTEGRATION POINTS

### With OpenClaw

```bash
# Skills auto-discovered from ~/.openclaw/skills/
# Published skills available via:
openclaw skill run <slug> "<task>"
```

### With Publishing Script

```bash
# Full workflow automation
./publish-to-clawhub.sh validate <path>   # Check structure
./publish-to-clawhub.sh package <path>    # Create tarball
./publish-to-clawhub.sh publish <path>    # Upload to registry
./publish-to-clawhub.sh sync <dir>        # Batch publish
```

---

## 📁 FILES

- `~/.openclaw/skills/clawhub/SKILL.md` (this file)
- `~/.openclaw/workspace/scripts/publish-to-clawhub.sh` (publishing automation)
- `~/.openclaw/workspace/docs/clawhub-publishing-guide.md` (documentation)
- `~/.config/clawhub/token` (authentication token)

---

## ✅ VERIFICATION

```bash
# Check CLI installed
which clawhub
clawhub --version

# Verify auth
clawhub whoami

# Test search
clawhub search "openclaw" | head -10

# List published skills (your account)
clawhub list --mine 2>/dev/null || echo "Check web dashboard"
```

---

## 🐛 TROUBLESHOOTING

### Common Errors

**"Not logged in"**
```bash
clawhub login
```

**"Slug already exists"**
```bash
# Increment version
clawhub publish <path> --version "1.1.0"
```

**"Missing SKILL.md"**
```bash
# Ensure skill has required files
ls -la <skill-path>/SKILL.md
```

**"Validation failed"**
```bash
# Run validation first
./publish-to-clawhub.sh validate <skill-path>
```

---

## 📈 METRICS

| Metric | Target | Status |
|--------|--------|--------|
| Skills Published | 5+ (test batch) | IN PROGRESS |
| Publishing Time | <2 min/skill | ✅ Automated |
| Validation Rate | 100% | ✅ Pre-check enabled |

---

**Version:** 1.0.0  
**Created:** 2026-03-31  
**Registry:** https://clawhub.ai  
**Owner:** Hybrid Labs
