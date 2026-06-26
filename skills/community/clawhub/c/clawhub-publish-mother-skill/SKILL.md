# ClawHub Publish Mother Skill 🚀

**Description:** Comprehensive workflow for publishing OpenClaw skills to ClawHub - with **working token authentication** method confirmed.

**Status:** ✅ **AUTHENTICATION VERIFIED** (Version 1.2.0)

## 🎯 When to Use
- Publishing skills to ClawHub
- Updating existing published skills
- Batch publishing workflows
- Authentication troubleshooting

## 📋 Prerequisites

### Essential:
1. `npm install -g clawhub`
2. GitHub account (for ClawHub registration)
3. ClawHub API token (from https://clawhub.ai/settings/tokens)

### Token Format:
- Starts with: `clh_`
- Length: ~45 characters
- Example: `clh_aEv-hIyAS42nOClecciC_svRODF4Ug6Ema4PfaXNFoY`

## 🚀 Complete Workflow

### 1. Authentication (Token Method - CONFIRMED WORKING)
```bash
# Get token from: https://clawhub.ai/settings/tokens
# Then authenticate:
clawhub login --token "YOUR_TOKEN_HERE" --no-browser

# Verify:
clawhub whoami
# Should show: ✔ your-username
```

### 2. Skill Preparation
```bash
cd /path/to/your-skill

# Validate skill structure
./scripts/validate.sh

# Check for personal information
grep -i "C:\\\\\|/home/\|password\|token\|secret" SKILL.md || echo "Clean"
```

### 3. Publishing
```bash
# Dry run first
clawhub publish . --dry-run

# Actual publish
clawhub publish . \
  --slug "your-unique-slug" \
  --name "Skill Display Name" \
  --version "1.0.0" \
  --changelog "Initial release"

# Slug rules:
# - Lowercase, hyphens only
# - Must be globally unique
# - If taken, append "-v2" or "-backup"
```

### 4. Verification
```bash
# Check skill was published
clawhub inspect your-slug

# Test installation
clawhub install your-slug --dry-run

# Visit on web: https://clawhub.ai/s/YOUR_USERNAME/your-slug
```

## ⚠️ Pitfalls & Solutions

### Pitfall 1: Token Authentication Not Working
**Symptoms:** "Not logged in" even with token
**Solution:** Use exact command: `clawhub login --token "TOKEN" --no-browser`

### Pitfall 2: Slug Already Taken
**Symptoms:** "Only the owner can publish updates"
**Solution:** Choose different slug, check availability first

### Pitfall 3: Skill Validation Fails
**Symptoms:** Publishing rejected
**Solution:** Run validation script, fix SKILL.md structure

### Pitfall 4: Token Expired
**Symptoms:** Authentication suddenly stops working
**Solution:** Generate new token from ClawHub settings

## ✅ Verification Steps

### Authentication Test
```bash
clawhub whoami
# Should return: ✔ username
```

### Skill Test
```bash
# In skill directory
./scripts/validate.sh
clawhub publish . --dry-run
```

### Post-Publish Test
```bash
clawhub inspect your-slug
clawhub install your-slug --dry-run
```

## 🔧 Troubleshooting Commands

```bash
# Check CLI version
clawhub -V

# Check authentication
clawhub whoami

# Get help
clawhub publish --help
clawhub auth --help

# List your published skills
# Visit: https://clawhub.ai/u/YOUR_USERNAME
```

## 🐕 Brand Elements

**Canine Personas:**
- **Romeo:** "Token authentication is like a dog's nose - unique and reliable!"
- **Luna:** "A good publish workflow is like a well-trained retriever - fetches success every time!"
- **Buster:** "If your token starts with 'clh_', you're on the right scent!"
- **Thomas:** "Put that in your pipe and smoke it - this authentication actually works!"

**British Phrases:**
- "Right then, token sorted"
- "Bob's your uncle, authenticated"
- "Sorted and published"

## 🔄 Version History

- **v1.0.0:** Initial creation
- **v1.1.0:** Added bot detection awareness
- **v1.2.0:** **CONFIRMED** token authentication working

## 🤝 Community Contributions

This skill evolves with community use. Found a better way? Submit a PR!

**HELL YEAH, publishing mastered!** 🎯

*British dry humour + canine personas*
*Put that in your pipe and smoke it!*
