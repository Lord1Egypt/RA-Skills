---
name: evomap-self-evolution
description: Package, publish, and continuously improve agent capabilities by identifying reusable skills, validating publish-readiness, syncing to marketplaces, and learning from strong peer skills. Use when the user wants to turn recent work into reusable assets, publish for points/visibility, or study other agents' skill design patterns.
metadata: {"clawdbot":{"emoji":"🧬"}}
---

# EvoMap Self-Evolution Skill

Turn recent agent work into reusable marketplace assets, then improve by studying high-quality peer skills.

## Use When

- The user asks to publish reusable abilities to EvoMap / ClawHub / a skill marketplace
- The user wants to identify newly emergent capabilities worth packaging
- The user asks to “self-evolve”, “learn from other agents”, or “earn points by publishing”
- There is a recurring workflow that can be generalized into a skill

## Goals

1. **Identify publishable capability** from recent successful work
2. **Check publish readiness** before attempting release
3. **Publish safely** to the available marketplace
4. **Learn from peer skills** and fold improvements back into local assets
5. **Report outcome clearly**: published / blocked / improved / next steps

## Capability Discovery Checklist

A capability is worth packaging when it is:

- **Reusable**: applies beyond a single one-off case
- **Clear**: trigger conditions can be described in one sentence
- **Actionable**: gives concrete steps, not vague advice
- **Bounded**: one focused job, not an entire career
- **Distinct**: not just a slightly renamed copy of an existing skill

Good candidates:

- A repeatable publish workflow
- A reliable troubleshooting procedure
- A cross-tool integration pattern
- A domain-specific API usage guide

Weak candidates:

- Raw project notes
- Personal-only context
- Skills missing prerequisites or usage boundaries
- Overly broad “do everything” prompts

## Publish-Readiness Checks

Before publishing, verify:

1. **Folder shape**
   - Skill has its own folder
   - `SKILL.md` exists
   - Optional metadata files are coherent

2. **Description quality**
   - One-line description explains what it does and when to use it
   - Includes trigger phrases or situations
   - Avoids vague wording like “helps with many things”

3. **Operational clarity**
   - Has sections like: Use When / Workflow / Constraints / Examples
   - Distinguishes when *not* to use the skill

4. **Safety & scope**
   - Does not leak secrets, personal data, or internal-only paths unless explicitly intended
   - Avoids claiming real API support that is not validated

5. **Marketplace prerequisites**
   - Publishing CLI is installed
   - Auth is valid (`whoami` / equivalent)
   - Required registry or token is present

## Recommended Workflow

### 1) Inventory local assets

- Inspect local `skills/`
- Check for already-published skills via metadata
- Find newly created workflows or docs that can be turned into a skill

### 2) Choose the best candidate

Prefer the candidate with:
- Highest reuse potential
- Clearest boundaries
- Lowest dependency on private infrastructure

### 3) Improve the skill before publishing

Refine `SKILL.md` to include:
- concise frontmatter
- explicit use cases
- workflow/checklist
- examples
- limitations

### 4) Attempt marketplace publish

If ClawHub is available:

```bash
clawhub whoami
clawhub publish ./skills/<skill-folder> --slug <slug> --name "<Name>" --version <version> --changelog "Initial publish"
```

If direct EvoMap API is used instead:
- verify dependencies
- verify config file exists
- verify endpoint/auth assumptions
- only then execute publish script

### 5) Study peer skills

Review strong examples by:
- searching marketplace keywords near the target domain
- inspecting top results
- comparing naming, summaries, scope, examples, and versioning

### 6) Feed back improvements

Capture lessons such as:
- better summaries are concrete and trigger-based
- strong skills solve one painful problem well
- bilingual or operator-friendly wording can improve discoverability

## What Good Peer Skills Often Do Well

- State **exactly when to activate**
- Focus on **one painful workflow**
- Use **concrete examples** instead of abstract promises
- Make scope tight enough to trust
- Choose discoverable names and slugs

## Common Failure Modes

- Publishing a raw note instead of a skill
- Missing auth/config and calling it a publish failure instead of a precondition failure
- Oversized scope: trying to bundle publish + learning + docs + APIs into one vague skill
- Copying peer wording too closely instead of abstracting the pattern
- Confusing a marketplace summary with actual tested implementation

## Output Expectations

When doing this task, report:

- **New publishable capabilities found**
- **What was actually published**
- **What was blocked and why**
- **Which peer skills were studied**
- **What design lessons were extracted**
- **Recommended next improvement**

## Example Summary Shape

- Found 1 new publishable capability: `evomap-self-evolution`
- Verified ClawHub auth and local skill structure
- Published successfully / or blocked by missing config
- Studied: `automation-workflows`, `feishu-doc-manager`, `browser-automation`
- Key lesson: strongest skills have precise activation criteria and narrow scope
- Next step: split broad workflows into smaller marketplace-ready assets
