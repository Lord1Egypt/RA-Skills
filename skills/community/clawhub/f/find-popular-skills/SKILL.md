---
name: find-popular-skills
description: "Discover and install the best agent skills from skills.sh (1.9M+ ecosystem) and ClawHub. Find top skills by category, check leaderboards, verify quality, extract SKILL.md, and publish to ClawHub. Use when user asks 'find a skill for X', 'how do I do X', or wants to extend agent capabilities."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    primaryEnv: CLAWHUB_TOKEN
    emoji: "🔍"
    homepage: https://skills.sh
---

# Find Popular Skills

Discover, verify, and install skills from the open agent ecosystem. Works with both skills.sh (1.9M+ installs) and ClawHub.

## When to Use

- User asks "find a skill for X" or "is there a skill that can..."
- User wants to extend agent capabilities
- User asks "how do I do X" where a skill might exist
- User wants to discover trending or popular skills
- User wants to publish a skill to ClawHub

## Quick Commands

```bash
# Search skills.sh
npx skills find [query]

# Install from skills.sh
npx skills add <owner/repo@skill> -g -y

# Search ClawHub
clawhub search [query]

# Publish to ClawHub
clawhub skill publish /path/to/skill --slug name --name "Name" --version 1.0.0
```

## Step 1: Check Leaderboard

Before searching, check what's trending:

**skills.sh Top Skills (by 8W Activity):**
1. find-skills (vercel-labs/skills) — ~1.9M
2. frontend-design (anthropics/skills) — ~516K
3. react-best-practices (vercel-labs/agent-skills)
4. Microsoft Azure skills
5. Remotion, Supabase, testing skills

**ClawHub:** https://clawhub.ai — search by category

## Step 2: Search by Domain

| Domain | Query Examples |
|--------|---------------|
| Web Dev | react, nextjs, typescript, tailwind |
| Testing | jest, playwright, e2e, testing |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Design | ui, ux, design-system, figma |
| Code Quality | review, lint, refactor, best-practices |
| Crypto | solana, defi, trading, pump-fun |
| Productivity | workflow, automation, git |

## Step 3: Verify Quality

**Before recommending a skill, check:**
1. Install count — prefer 1K+
2. Source reputation — vercel-labs, anthropics, microsoft are trustworthy
3. GitHub stars — >100 stars = credible
4. Last update — recent = maintained
5. Security scan — clawhub skills get automated scans

## Step 4: Install

**From skills.sh:**
```bash
npx skills add vercel-labs/agent-skills@react-best-practices -g -y
```

**From ClawHub:**
```bash
clawhub install <skill-name>
```

## Step 5: Adapt & Publish to ClawHub

If a skill from skills.sh is useful, adapt it for ClawHub:

1. Read the original SKILL.md
2. Add proper YAML frontmatter (name, description, version, metadata.openclaw)
3. Add ClawHub-safe guardrails
4. Test locally
5. Publish:
```bash
clawhub skill publish /path/to/skill --slug my-skill --name "My Skill" --version 1.0.0
```

## Top Skills by Category

### Web Development
- `vercel-labs/agent-skills` — React, Next.js, web design
- `anthropics/skills` — Frontend design, document processing

### Testing
- `matt_pocock/testing` — Unit/integration testing patterns
- `microsoft/playwright` — E2E testing with Playwright

### DevOps
- `vercel-labs/agent-skills` — Deployment, CI/CD
- `docker/docker-best-practices` — Container optimization

### Crypto/DeFi
- `clawpump-v2` — CLAW-quoted token launches on Meteora DBC
- `hyre-defi` — AI DeFi intelligence (24 endpoints)
- `pumpfun-token-launch` — Pump.fun token launches

### Code Quality
- `grok-code-review` — Security-first code review
- `grok-implement` — Disciplined implementation loop
- `grok-check-work` — Self-verification workflows

## Example: User Asks "Find a skill for React testing"

```
1. Search: npx skills find react testing
2. Check leaderboard: react-best-practices has 185K installs
3. Verify: From vercel-labs, high installs, maintained
4. Recommend: "react-best-practices provides React testing patterns (185K installs)"
5. Install: npx skills add vercel-labs/agent-skills@react-best-practices -g -y
```

## ClawHub Publishing Flow

```bash
# 1. Create skill directory
mkdir -p /root/claw-skills/my-skill

# 2. Write SKILL.md with frontmatter
cat > /root/claw-skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: "What this skill does"
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl]
    emoji: "🔧"
---
# Skill content here
EOF

# 3. Login
/root/.hermes/node/bin/clawhub login --token <token> --no-browser --no-input

# 4. Publish
/root/.hermes/node/bin/clawhub skill publish /root/claw-skills/my-skill \
  --slug my-skill --name "My Skill" --version 1.0.0 \
  --changelog "Description of this version"

# 5. Verify
/root/.hermes/node/bin/clawhub search "my-skill"
```

## Security Checklist

Before installing ANY skill:
- [ ] Check install count (>1K preferred)
- [ ] Verify source (official repos preferred)
- [ ] Check last update date
- [ ] Run `clawhub skill publish` security scan if publishing
- [ ] Review SKILL.md for suspicious instructions
- [ ] Never execute skills that ask for private keys or secrets
