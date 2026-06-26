# 🚀 Quick Publishing Guide (5 Steps)

**Get SystemDesign Skill published to GitHub and NPM in under 1 hour.**

---

## Step 1: Prepare Your GitHub Repository (10 min)

### 1.1 On GitHub.com

1. Go to **github.com** → **+** → **New repository**
2. Name: `systemdesign-skill`
3. Description: "CTO-level architectural skill for Claude Code"
4. License: MIT
5. Click **Create repository**

### 1.2 Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/systemdesign-skill.git
cd systemdesign-skill

# Copy all files from /mnt/user-data/outputs/ to this directory
# (README.md, SKILL.md, spec_template.md, DESIGN_template.md, code_review_checklist.md, etc.)

# Initial commit
git add .
git commit -m "Initial commit: SystemDesign Skill v1.0.0"
git branch -M main
git push -u origin main
```

---

## Step 2: Add Essential Files (15 min)

Run the packager script:

```bash
bash /mnt/user-data/outputs/package-skill.sh
```

This creates:
- ✅ package.json
- ✅ LICENSE (MIT)
- ✅ CONTRIBUTING.md
- ✅ CHANGELOG.md
- ✅ examples/
- ✅ docs/
- ✅ .github/ templates

Then push:

```bash
git add .
git commit -m "Add: package.json, documentation, examples"
git push
```

---

## Step 3: Create GitHub Release (5 min)

```bash
# Tag the release
git tag -a v1.0.0 -m "Release SystemDesign Skill v1.0.0"
git push origin v1.0.0
```

On GitHub:
1. Go to **Releases** → **Draft a new release**
2. Select tag **v1.0.0**
3. Title: "SystemDesign Skill v1.0.0"
4. Description:
   ```markdown
   # 🎉 SystemDesign Skill v1.0.0

   A production-grade CTO-level architectural skill for Claude Code.

   ## What's New
   - The Three Pillars framework (state, feedback, blast radius)
   - Architectural spec template
   - Google DESIGN.md integration
   - Code review checklist (594 items)
   - Real-world examples
   - Comprehensive documentation

   ## Quick Start
   See [README.md](README.md) to get started.

   ## Installation
   ```bash
   npm install @udit/systemdesign-skill
   ```
   ```
5. Click **Publish release**

---

## Step 4: Publish to NPM (10 min)

### 4.1 Create NPM Account

```bash
# Go to https://www.npmjs.com/signup and create account
# Verify email

# Login locally
npm login
# Enter username, password, email
```

### 4.2 Publish

```bash
cd systemdesign-skill

# Verify version in package.json is "1.0.0"
npm publish

# Verify
npm view @udit/systemdesign-skill
```

✅ Published! View at: https://npmjs.com/package/@udit/systemdesign-skill

---

## Step 5: Register with Registries (20 min)

### 5.1 Update Awesome Lists

Submit PR to skill registries:

1. **Awesome Claude Skills** (GitHub)
   - Fork: https://github.com/YOUR_LINK/awesome-claude-skills
   - Add to list:
     ```markdown
     - [SystemDesign](https://github.com/YOUR_USERNAME/systemdesign-skill) 
       — CTO-level architectural skill for Claude Code. 
       Design before code, think systems-first.
     ```
   - Submit PR

2. **Awesome AI Tools** (GitHub)
   - Same process

### 5.2 Announce

**Social Media** (pick 1-3):

```
🚀 Just released: SystemDesign Skill for Claude Code

A CTO-level architectural skill that forces design-before-code thinking.

Key features:
• The Three Pillars framework (state, feedback, blast radius)
• Architectural spec templates
• Google DESIGN.md integration
• Code review checklist

GitHub: https://github.com/YOUR_USERNAME/systemdesign-skill
NPM: https://npmjs.com/package/@udit/systemdesign-skill

Move from "coding faster" to "architecting better."
```

Post on:
- Twitter/X
- Dev.to (write full article)
- LinkedIn
- Hacker News: "Show HN: SystemDesign — CTO-level skill for Claude Code"
- Reddit: r/claude, r/programming

---

## Complete Checklist

**Before Publishing:**
- [ ] All files copied from /mnt/user-data/outputs/
- [ ] package.json updated (author, repo URL)
- [ ] LICENSE file present
- [ ] README.md complete
- [ ] SKILL.md in place
- [ ] references/ folder with templates
- [ ] examples/ folder with real specs
- [ ] .gitignore configured

**GitHub:**
- [ ] Repository created
- [ ] Files committed and pushed
- [ ] v1.0.0 tag created
- [ ] Release published on GitHub

**NPM:**
- [ ] npm account created and verified
- [ ] npm publish successful
- [ ] Package visible on npmjs.com

**Marketing:**
- [ ] Announced on social media
- [ ] Submitted to awesome lists
- [ ] Wrote blog post or dev.to article (optional)

---

## Verify It's Live

### Check GitHub

```bash
# Visit repository
https://github.com/YOUR_USERNAME/systemdesign-skill

# Check release
https://github.com/YOUR_USERNAME/systemdesign-skill/releases/tag/v1.0.0
```

### Check NPM

```bash
# Search
npm search systemdesign-skill

# View package
npm view @udit/systemdesign-skill

# Install (test)
npm install @udit/systemdesign-skill --save-dev
```

### Check Online

Visit:
- https://npmjs.com/package/@udit/systemdesign-skill
- https://github.com/YOUR_USERNAME/systemdesign-skill

---

## Post-Launch (Day 2+)

### Engagement

- [ ] Monitor GitHub issues (respond within 24h)
- [ ] Track NPM downloads
- [ ] Watch social media mentions
- [ ] Engage with community questions

### Improvements

- [ ] Add more examples based on feedback
- [ ] Expand documentation
- [ ] Create video walkthrough
- [ ] Write follow-up articles

### Releases (Future)

For v1.1, v1.2, etc.:

```bash
# Make changes, commit

# Bump version
npm version minor  # 1.0.0 → 1.1.0

# Publish
npm publish

# Push tags
git push origin --tags

# Create GitHub release with changelog
```

---

## Files You Need

All in `/mnt/user-data/outputs/`:

```
START_HERE.md                    ← Read first
README.md                        ← GitHub repo README
SKILL.md                         ← Main skill
spec_template.md                 ← For specs
DESIGN_template.md              ← For design systems
code_review_checklist.md        ← For code reviews
INTEGRATION_GUIDE.md            ← Setup instructions
PACKAGE_SUMMARY.md              ← Complete guide
GITHUB_PUBLISHING_GUIDE.md      ← Detailed publishing
package-skill.sh                ← Packaging script
FILES_MANIFEST.txt              ← File reference
```

---

## Commands Reference

```bash
# GitHub
git clone https://github.com/YOUR_USERNAME/systemdesign-skill.git
cd systemdesign-skill
git add .
git commit -m "message"
git push
git tag -a v1.0.0 -m "Release"
git push origin v1.0.0

# NPM
npm login
npm publish
npm view @udit/systemdesign-skill
npm search systemdesign-skill

# Updates
npm version patch   # 1.0.0 → 1.0.1
npm version minor   # 1.0.0 → 1.1.0
npm publish
git push origin --tags
```

---

## Success Indicators

After 1 week:
- ✅ 50+ GitHub stars
- ✅ 100+ NPM downloads
- ✅ 5+ issues/questions

After 1 month:
- ✅ 200+ GitHub stars
- ✅ 500+ NPM downloads
- ✅ Community contributions

---

## Need Help?

**Lost?** → Start with START_HERE.md  
**GitHub questions?** → GITHUB_PUBLISHING_GUIDE.md  
**Integration questions?** → INTEGRATION_GUIDE.md  
**Skill details?** → SKILL.md  

---

## You're Ready! 🚀

Everything is prepared. You have:
- ✅ Complete skill documentation
- ✅ Templates and examples
- ✅ Publishing guide
- ✅ Packaging script
- ✅ Marketing strategy

**Next action**: Run the packaging script, customize package.json, push to GitHub, publish to NPM.

**Estimated time**: 1-2 hours total.

**Result**: Your CTO-level architectural skill is live and discoverable.

Good luck! 🎉
