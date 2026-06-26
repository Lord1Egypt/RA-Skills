---
name: clawhub-skill-audit
version: 1.0.2
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "requires": { "bins": ["clawhub", "python3"] },
      "network": { "outbound": true, "reason": "Fetches skill metadata from ClawHub registry via clawhub inspect." }
    }
  }
description: "Audit locally installed skills against ClawHub: detect version drift, find new publish candidates, review security flags, and triage ownership conflicts. Use when: reviewing whether published skills need updates, deciding what new local skills are ready to open-source, investigating hidden/flagged skills on ClawHub, or running the weekly skill lifecycle check."
---

# ClawHub Skill Audit

Maintain the health of your published ClawHub skills: detect drift, find new candidates, review security flags.

## When to use

- Weekly (Monday 09:00 AEST — automated via launchd)
- Any time Nissan asks "do we need to update our ClawHub skills?"
- Before a major release that ships new skills
- When a skill shows unexpected behaviour that might have been fixed in a newer ClawHub version

## Tools required

- `clawhub` CLI (npm global: `~/.npm-global/bin/clawhub`)
- `scripts/skill-lifecycle/drift-detector.py` — version comparison
- `scripts/clawhub_audit.py` — local security compliance check
- `scripts/skill-lifecycle/publish-skill.sh` — publish gate

## Full playbook

See `playbooks/clawhub-skill-lifecycle/PLAYBOOK.md` for complete step-by-step.

## Quick audit (3 commands)

### 1. Check drift (local vs published)
```bash
/Users/loki/.pyenv/versions/3.14.3/bin/python3 \
  ~/.openclaw/workspace/scripts/skill-lifecycle/drift-detector.py
```

### 2. Check for hidden / flagged skills
```bash
for skill in agent-hive llm-eval-router fastapi-studio-template observability-lgtm \
  insight-engine fact-checker agent-budget-governance demo-precacher \
  gateway-env-injector mistral-agents-orchestrator multi-agent-pipeline \
  reddi-humanizer tweet-humanizer tweet-pipeline notion-content-pipeline security-auditor; do
  result=$(clawhub inspect "$skill" 2>&1 | grep -E "Owner:|Latest:|hidden|security|flag|pending")
  echo "$skill: $result"
done
```

Look for: `hidden while security scan is pending` or any flag/warning text.

### 3. Find new candidates (never published)
```bash
for d in ~/.openclaw/workspace/skills/*/; do
  name=$(basename "$d")
  has_version=$(grep -m1 "^version:" "$d/SKILL.md" 2>/dev/null | wc -c)
  published=$(clawhub inspect "$name" 2>/dev/null | grep "Owner: nissan")
  if [ "$has_version" -gt 0 ] && [ -z "$published" ]; then
    ver=$(grep -m1 "^version:" "$d/SKILL.md" | awk '{print $2}' | tr -d "'\"")
    echo "CANDIDATE: $name @ $ver"
  fi
done
```

## Publishing a skill update

```bash
# 1. Bump version in SKILL.md frontmatter
# 2. Add CHANGELOG.md entry
# 3. Run publish gate (checks version + changelog)
bash ~/.openclaw/workspace/scripts/skill-lifecycle/publish-skill.sh <skill-name>
# 4. Publish
clawhub publish ~/.openclaw/workspace/skills/<skill-name>
```

## Fixing a security-flagged skill

1. Run local compliance check:
```bash
/Users/loki/.pyenv/versions/3.14.3/bin/python3 \
  ~/.openclaw/workspace/scripts/clawhub_audit.py <skill-name>
```

2. Fix the flagged issues (typically: undeclared env vars, missing `network.outbound`, suspicious patterns)

3. Bump patch version, add CHANGELOG entry, republish.

## Ownership conflicts

If `clawhub publish` returns `Error: Only the owner can publish updates`:
- The skill was installed from ClawHub and belongs to another account
- Do NOT try to re-publish under the same slug
- Options: fork as `reddi-<name>`, or keep local-only
- To fork: copy skill dir → rename to `reddi-<name>` → update `name:` in SKILL.md → publish new slug

## Known nissan-owned slugs (as of 2026-03-25)

```
agent-hive, llm-eval-router, fastapi-studio-template, observability-lgtm,
insight-engine, fact-checker, agent-budget-governance, demo-precacher,
gateway-env-injector, mistral-agents-orchestrator, multi-agent-pipeline,
reddi-humanizer, tweet-humanizer, tweet-pipeline, notion-content-pipeline
```

## Known community skills with local improvements

| Skill | Published owner | Recommended action |
|---|---|---|
| `reddi-humanizer` | nissan | Forked from biostartechnology/humanizer — published as reddi-humanizer |
| `self-improving-agent` | pskoett | Audit diff, then fork or local-only |

## Gotchas

- `clawhub explore` returns empty — use `clawhub inspect <slug>` per skill
- `_meta.json` in skill dir = drift tracker. Missing = drift detector can't compare. After publish, clawhub writes this file.
- Security scan is usually quick (minutes) but can take hours. Hidden ≠ failed — wait and re-check.
- Rate limit: max 5 new skill publishes per hour. Updates do not appear to count against this the same way, but new slugs must be batched across hourly windows.
- Use `clawhub sync --dry-run` as the source of truth for full registry drift; the legacy `drift-detector.py` only checks local `_meta.json` files and misses new local skills.
- ClawHub ahead of local: `fastapi-studio-template`, `insight-engine`, `fact-checker`, `demo-precacher` show higher published versions than local. Run `clawhub update <slug>` to pull those down and sync.
