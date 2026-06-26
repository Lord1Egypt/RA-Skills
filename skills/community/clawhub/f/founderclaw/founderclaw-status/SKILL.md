---
name: founderclaw-status
description: >
  Check FounderClaw installation status. Verifies skills, workspace, and
  multi-agent config are all properly set up.
  Use when: "founderclaw status", "is founderclaw working", "check founderclaw",
  "founderclaw health".
---

# FounderClaw Status Check

Run all checks and report:

## Check 1: Skills

```bash
FC_SKILLS=$(ls ~/.agents/skills/founderclaw/*/SKILL.md 2>/dev/null | wc -l)
LINKED=$(ls -la ~/.agents/skills/ 2>/dev/null | grep founderclaw | wc -l)
echo "Skills in repo: $FC_SKILLS"
echo "Symlinks pointing to founderclaw: $LINKED"
```

## Check 2: Workspace

```bash
if [ -d ~/.openclaw/founderclaw/ceo ]; then
    echo "Workspace: EXISTS"
    ls ~/.openclaw/founderclaw/ 2>/dev/null
else
    echo "Workspace: MISSING"
fi
```

## Check 3: Multi-agent config

Use `agents_list` tool to check if these agents exist:
- founderclaw-main
- fc-strategy
- fc-shipper
- fc-tester
- fc-safety
- fc-observer

Count how many are present. Report:
- "All 6 agents configured" or "Only X/6 agents configured"

## Report

```
FounderClaw Status
==================
Skills:    [X/29 installed]
Workspace: [EXISTS/MISSING]
Agents:    [X/6 configured]
Browse:    [BUILT/NOT BUILT]

Overall: [READY / PARTIAL / NOT INSTALLED]
```

If PARTIAL or NOT INSTALLED, provide specific fix instructions.
