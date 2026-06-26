---
name: skill-distiller
description: "Distill successful workflows into reusable skills with quality gates. Use after completing multi-step tasks to evaluate if the workflow should be saved. Triggers: 'distill this', 'save as skill', 'make this reusable', or automatically at end of complex tasks. Evaluates novelty, success, reuse potential AND grounding (≥10 real samples) before generating SKILL.md. Includes IP boundary check (private vs shared classification), trigger keyword discipline, and pre-publish vet for skills going to public registries. Prevents skill bloat through 4-question quality gates and the 'sycophancy of completeness' anti-pattern."
version: 2.0.1
---

# Skill Distiller

Turn successful workflows into reusable skills — with discipline, not enthusiasm.

> Built on agentic learning-loop patterns. Hardened by 30+ skill-creation incidents (some real, some embarrassing).

## When to Distill — 4-Question Gate

**All four must be YES to proceed.** This is stricter than v1's 3-question gate (Novel + Successful + Reusable) because we learned the hard way that "looks reusable" without grounding produces hallucinated skills.

1. **Novel?** — Is this a workflow you haven't done before? (If similar skill exists, UPDATE it instead of creating new)
2. **Successful?** — Did the task complete with verified results? (Failed tasks → write to lessons-learned.md, not a skill)
3. **Reusable?** — Will this exact workflow likely be needed again? (One-off → memory note, not skill)
4. **Grounded?** 🆕 — Do you have ≥10 real samples to back up the workflow? (Without grounding = LLM hallucination dressed as a skill — see Anti-Pattern: "Sycophancy of Completeness")

**Quick scoring:**

```
4/4 YES = CREATE SKILL
Novel + Successful + Reusable, but only 1 sample = STAGE THE SKILL but mark "needs more samples" — don't publish/install yet
Novel + Successful + One-off = MEMORY NOTE
Failed = LESSONS-LEARNED entry
Not Novel = UPDATE EXISTING SKILL
```

## Distillation Process

### Step 1: Extract the Workflow

Look back at what you just did. Identify:

- **Trigger**: What kind of request started this? (the *pattern*, not the specific instance)
- **Steps**: The key steps in order
- **Tools**: Which tools used and how
- **Decisions**: Non-obvious choices and why
- **Gotchas**: What almost went wrong, what required retry

🆕 **Grounding requirement**: Before extracting, list the real instances this skill is based on. <3 instances = mark "experimental, do not publish"; 3-9 = "beta, single-user only"; ≥10 = ready for public publish.

### Step 2: Generalize

Transform the specific instance into a reusable pattern.

❌ Bad (too specific):
```
1. Read ch10-multi-agent-comm-patterns.md
2. Convert markdown to docx using python-docx
3. Upload to <internal-folder-token>
```

✅ Good (generalized):
```
1. Read source markdown file(s)
2. Convert to docx (see references/docx-patterns.md)
3. Upload to target output destination
```

### Step 3: Write SKILL.md

Standard format:

```markdown
---
name: <slug>
description: "<when to trigger — be specific>"
version: <semver>
---

# <Skill Name>

## When to Use
<1-2 sentences on the trigger pattern>

## Workflow
<Numbered steps>

## Key Decisions
<Non-obvious choices and rationale>

## Gotchas
<Specific failure modes and handling>

## References
<Links to detailed docs if needed>
```

**Size targets:**
- SKILL.md body: under 200 lines
- description: under 1024 chars (some registries enforce this)
- Long-form content → references/ subdirectory

🆕 **Trigger keyword discipline**: Description's "Triggers:" or "Use when:" section must list 5-15 concrete phrases users actually type. Mix English + native language if your audience is bilingual. Vague triggers ("when needed", "for general use") = skill won't fire.

### Step 4: 4-Layer Quality Check

Before saving, verify:

**Layer A — Format**
- [ ] description states *when* to trigger (not just what it does)
- [ ] Each step has a clear, atomic action
- [ ] No hardcoded values that should be parameters
- [ ] Gotchas are specific (not "handle errors properly")

**Layer B — Grounding**
- [ ] Workflow backed by ≥10 real instances (or marked "experimental")
- [ ] Examples in references/ are real, not invented
- [ ] No claim made without source

**Layer C — IP Boundary** 🆕
- [ ] No private user identifiers (real names, account IDs, internal codenames)
- [ ] No internal project names or customer info
- [ ] No absolute paths revealing user identity (`/home/<user>/...`)
- [ ] No references to private memory files
- [ ] Description reads like a generic tool, not a personal note

**Layer D — Discoverability**
- [ ] Triggers list 5-15 concrete user phrases
- [ ] Skill name doesn't collide with existing slugs
- [ ] No near-duplicate skill exists (run `ls ~/.openclaw/skills/ | grep -i <keyword>`)

### Step 5: Save and Register

Save to `~/.openclaw/skills/<slug>/SKILL.md` (or workspace skills dir).

Reference materials → `~/.openclaw/skills/<slug>/references/`.

Verify it loads:
```bash
ls ~/.openclaw/skills/<slug>/SKILL.md
```

🆕 **For skills destined for a public registry** (e.g., ClawHub):
1. Run IP grep on whole skill directory before publish
2. Track in a SSOT file (e.g., `skills/SKILL-REGISTRY.md`) — slug, version, owner, publish date
3. After publish, update SSOT immediately. "Already published" memory across sessions is unreliable.

## Skill Classification

🆕 Before saving, decide which class:

| Class | Naming | Goes to | Public? |
|---|---|---|---|
| 🔴 **Internal** | `<owner-prefix>-<name>` | Owner's private skills dir | Never share |
| 🟡 **Preparing** | no prefix | Workspace skills dir | Polished but not vetted yet |
| 🟢 **Shared** | no prefix | Workspace skills dir | Ready for public registry |
| 🔵 **External** | original name | Skills dir | Installed from registry, don't modify |

**The rule:** if the skill references private state (memory files, personal config, user identity), it's Internal — even if the workflow itself is generic.

## Automatic Distillation Mode

When integrated with a harness skill's Compound phase (e.g., `trinity-harness` Layer 3), distillation can happen automatically:

1. Task completes → Compound phase triggers
2. Run 4-question gate
3. If all YES → run distillation process
4. If NO → write lesson to memory
5. **Always announce** what was created (never silent)

🆕 **Automatic ≠ silent.** Even auto-distilled skills must surface to the user with a one-line summary, so they can review/edit/reject before the skill is used in earnest.

## Skill Maintenance

### Update vs. Create

Before creating new, check related ones:
```bash
ls ~/.openclaw/skills/ ~/.openclaw/workspace/skills/ 2>/dev/null | grep -i <keyword>
```

Similar exists → **update it** (add as variant), don't create near-duplicate.

### Pruning (during periodic review)

- Unused 30+ days → archival candidate
- Overlapping triggers → merge
- Superseded → mark deprecated

🆕 **Skill hash drift detection**: For installed external skills, periodically diff the local file against the registry version. Hash change without an explicit update = possible upstream poisoning. Alert the user.

## Anti-Patterns

| Don't | Why | Do Instead |
|---|---|---|
| Distill every task | Skill bloat, noise drowns signal | Apply the 4-question gate |
| Include conversation history | Wastes tokens, not reusable | Extract only the workflow pattern |
| Write vague gotchas | "Be careful" helps no one | Specific: "API X returns 429 after 3 concurrent requests" |
| Hardcode user-specific paths/names | Not portable, leaks identity | Use `<parameter>` placeholders |
| Skip quality check | Garbage skills waste future context | Always verify all 4 layers |
| 🆕 **Sycophancy of Completeness** | Skill looks polished but invented | Require ≥10 real samples before publishing |
| 🆕 Auto-publish without IP grep | Real production leak risk | Always grep private identifiers before pushing to public registry |
| 🆕 Trust "I already published this" memory | Cross-session memory is lossy | Maintain a SSOT file with slug + version + date |

## Integration with Memory System

| Output | Goes to | When |
|---|---|---|
| Reusable workflow (4/4 gate passes) | Skills dir / SKILL.md | Novel + Successful + Reusable + Grounded |
| Lesson learned | `memory/lessons-learned.md` | Successful but one-off, or failed |
| Quick note | `memory/YYYY-MM-DD.md` | Routine observations |
| Core insight (changes how you work) | Persistent memory file | Fundamental principle change |
| Skill in progress | Skills dir, marked "experimental" | Novel + Successful + Reusable but <10 samples |

## Pre-Publish Vet (for public registries) 🆕

Before pushing to ClawHub or similar:

1. **IP grep** — search the whole skill dir for private identifiers, internal codenames, absolute paths
2. **Anti-injection scan** — check description and references for prompt-injection vectors (`ignore previous`, `system:`, `admin:`, etc.)
3. **Self-vet via skill-vetter** (or equivalent) — independent reading checks for hallucinated commands, dangerous shell patterns
4. **SSOT update** — record slug + version + publish date + owner BEFORE the publish call (so you don't forget afterward)

## Quick Reference

```
Distill?     → 4-question gate (Novel + Successful + Reusable + Grounded)
Classify?    → Internal / Preparing / Shared / External
Quality?     → 4 layers (Format / Grounding / IP / Discoverability)
Publish?     → IP grep → vet → SSOT update → push
Always:      Announce auto-distilled skills, never silent.
```
