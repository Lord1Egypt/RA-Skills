# Publishing ENS Manager to GitHub and ClawHub

**Repository ready!** Follow these steps to publish.

---

## Step 1: Authenticate GitHub (Manual)

Run on the **server** (SSH'd into VPS):

```bash
gh auth login
```

**Prompts:**
1. **What account?** → GitHub.com
2. **Protocol?** → HTTPS
3. **How to authenticate?** → Login with a web browser
4. **Continue?** → Press Enter
5. Browser opens → Paste the code shown in terminal
6. Authorize in browser
7. Done! ✅

**Verify:**
```bash
gh auth status
# Should show: ✓ Logged in to github.com
```

---

## Step 2: Create GitHub Repository

After authentication:

```bash
cd /root/.openclaw/workspace/skills/ens-manager

# Create repo and push
gh repo create ens-manager \
  --public \
  --description "Complete ENS workflow - register names, create subdomains, publish IPFS content" \
  --source=. \
  --push

# Verify
gh repo view
```

**Result:** https://github.com/YOUR-USERNAME/ens-manager

---

## Step 3: Authenticate ClawHub (Manual)

```bash
clawdhub login
```

**What happens:**
1. Browser opens to ClawHub
2. Sign in with GitHub
3. Authorize ClawHub
4. Token saved automatically
5. Done! ✅

**Verify:**
```bash
clawdhub whoami
# Should show your ClawHub username
```

---

## Step 4: Publish to ClawHub

```bash
cd /root/.openclaw/workspace/skills/ens-manager

# Publish skill
clawdhub publish .

# Follow prompts:
# - Skill name: ens-manager (auto-detected)
# - Version: 1.1.0 (from VERSION file)
# - Confirm: yes
```

**Result:** Skill published to https://clawhub.com/skills/YOUR-USERNAME/ens-manager

---

## Step 5: Verify Publishing

**GitHub:**
```bash
gh repo view --web
# Opens in browser
```

**ClawHub:**
```bash
clawdhub explore --limit 5
# Should show ens-manager in recent skills
```

**Test install:**
```bash
# Try installing your own skill
clawdhub install YOUR-USERNAME/ens-manager
```

---

## Alternative: Quick Commands (Copy-Paste)

If you're comfortable with automation:

```bash
cd /root/.openclaw/workspace/skills/ens-manager

# GitHub (after gh auth login)
gh repo create ens-manager --public \
  --description "Complete ENS workflow - register names, create subdomains, publish IPFS content" \
  --source=. --push && \
gh repo view --web

# ClawHub (after clawdhub login)
clawdhub publish . && \
echo "✅ Published to GitHub and ClawHub!"
```

---

## Troubleshooting

### "gh: command not found"
Already installed. Try: `which gh`

### "Repository already exists"
```bash
# Check if it's yours
gh repo view ens-manager

# Delete and recreate if needed
gh repo delete ens-manager --yes
gh repo create ens-manager --public --source=. --push
```

### "ClawHub publish failed"
```bash
# Check authentication
clawdhub whoami

# Re-login
clawdhub logout
clawdhub login
clawdhub publish .
```

### "Push failed - remote exists"
```bash
cd /root/.openclaw/workspace/skills/ens-manager

# Check remotes
git remote -v

# Update remote URL
git remote set-url origin https://github.com/YOUR-USERNAME/ens-manager.git

# Push again
git push -u origin master
```

---

## What Gets Published

**GitHub:**
- All source code (scripts/)
- Documentation (README.md, SKILL.md, COSTS.md)
- Examples and references
- Git history

**ClawHub:**
- SKILL.md (skill description)
- VERSION (1.1.0)
- scripts/ (executable code)
- README.md (displayed on skill page)
- Indexed for search

**Not published:**
- node_modules/ (gitignored)
- .env files (gitignored)
- Local testing files

---

## After Publishing

**Share with others:**
```bash
# GitHub
https://github.com/YOUR-USERNAME/ens-manager

# ClawHub
https://clawhub.com/skills/YOUR-USERNAME/ens-manager

# Install command
clawdhub install YOUR-USERNAME/ens-manager
```

**Update skill README:**
Add install instructions at top:

```markdown
## Installation

Via ClawHub:
\`\`\`bash
clawdhub install YOUR-USERNAME/ens-manager
\`\`\`

Via GitHub:
\`\`\`bash
git clone https://github.com/YOUR-USERNAME/ens-manager.git
cd ens-manager/scripts && npm install
\`\`\`
```

---

**Ready to publish!** Start with Step 1 (gh auth login) 🚀
