---
name: skill-optimizer
description: Auto-improve any OpenClaw skill using Karpathy's autoresearch loop. Runs skill repeatedly against test inputs, scores against a yes/no checklist, makes one targeted change, keeps if better, reverts if worse. Also audits skill structure against Anthropic's best practices (progressive disclosure, gotchas section, trigger-phrase description). Use when asked to "optimize this skill", "improve my skill", "run autoresearch on", "audit this skill", or before running any skill at scale (e.g., cold outreach). Based on Ole Lehmann's autoresearch method + Anthropic internal skill patterns (@trq212).
---

# Skill Optimizer (Autoresearch Loop + Anthropic Structure Audit)

Two-phase improvement system: (1) structural audit against Anthropic best practices, (2) iterative output quality loop.

---

## Phase 1: Structure Audit (run first, always)

Before optimizing output quality, audit the skill's architecture. Score against these 5 structural checks:

**Structural Checklist:**
1. **Gotchas section** — Does SKILL.md have a `## Gotchas` section with at least one real failure case? (Highest-signal content per Anthropic)
2. **Trigger-phrase description** — Does the YAML `description` field say *when* to use the skill, not just *what* it does? Must include "Use when..." or equivalent trigger condition.
3. **Progressive disclosure** — Does the skill use the file system (references/, scripts/, assets/, config.json) instead of inline-dumping everything into SKILL.md?
4. **Single focus** — Does the skill fit cleanly into one type (Library Reference, Verification, Automation, Scaffolding, Runbook, etc.) without straddling multiple?
5. **No railroading** — Does the skill give Claude information + flexibility, rather than over-specifying *how* it must execute?

Score each: ✅ pass | ❌ fail | ⚠️ partial

For each failure: propose a concrete fix and apply if approved.

**Quick wins to apply immediately:**
- If no Gotchas section → add `## Gotchas\n- [Placeholder: add real failures here as they're discovered]`
- If description is a summary → rewrite as trigger condition
- If all content is inline → propose a `references/` folder structure

---

## Phase 2: Output Quality Loop (autoresearch)

After structure audit, run the iterative improvement loop on the skill's actual outputs.

### Setup
1. **Which skill?** — User specifies, or infer from context.
2. **Test inputs** — Get 2-3 representative inputs. If the user doesn't provide them:
   - Check the skill's own docs for example usage
   - Use recent real invocations from memory/session history
   - For extraction skills: use known-good URLs/files. For generation skills: use the skill's own example prompts.
3. **Scoring checklist** — Build 3-6 scoring items. Start from the examples below, then customize:
   - What's the #1 thing that makes this skill's output *bad*? (That's checklist item 1)
   - What would make a user say "that's exactly what I wanted"? (That's the positive framing)
   - Add 1-2 items from the "Universal structural quality" list below

### Scoring Checklist Examples
See `references/checklist-examples.md` for starter checklists by skill type (cold outreach, content, research, extraction, process/meta-skills).

### Scoring Modes

**Binary mode (default for simple skills):** Yes/no per checklist item. Pass rate = total yes / (items × runs).

**Dimensional mode (use for complex skills or when binary plateaus):** Score each dimension 0-10. Identify the weakest dimension (lowest average across runs). Target that dimension for revision — do NOT rewrite everything.

Use dimensional mode when:
- Binary scoring hits 100% but output still feels mediocre
- The skill has qualitative dimensions (tone, depth, relevance) that binary can't capture
- You want to improve from "good" to "excellent" rather than from "broken" to "working"

### The Loop

```
Round N:
1. Run skill against each test input
2. Score each output (binary: 1 per yes | dimensional: 0-10 per dimension)
3. Calculate score:
   - Binary: pass rate = (total yes) / (items × runs)
   - Dimensional: avg score per dimension across runs
4. Identify the weakest item/dimension (most failures or lowest avg score)
5. Make ONE targeted change to SKILL.md addressing ONLY that weakness
6. Re-run and re-score
7. If new score > old score: KEEP. Else: REVERT.
8. Log: score before/after, change made, dimension targeted, kept/reverted
```

Stop when: binary ≥ 95% (3 consecutive rounds) OR dimensional weakest ≥ 8/10 (3 consecutive) OR 20 rounds reached.

### Output Files
- `skills/{skill-name}/SKILL-optimized.md` — improved version (original untouched)
- `skills/{skill-name}/optimization-changelog.md` — full round log

### Changelog Format
```markdown
## Structural Audit
- Gotchas section: ❌ → Added placeholder
- Description: ❌ → Rewritten as trigger condition
- Progressive disclosure: ⚠️ → Noted, deferred

## Round 1 (binary mode)
- Score: 4/10 (40%)
- Weakest item: "Does it mention business name?"
- Change: Added rule "Always open with [Business Name],"
- New score: 7/10 (70%)
- Decision: KEPT

## Round 2 (dimensional mode)
- Scores: Accuracy 8/10 | Tone 5/10 | Brevity 9/10 | Relevance 7/10
- Weakest dimension: Tone (5/10)
- Change: Added "Match prospect's industry language, not generic sales speak"
- New scores: Accuracy 8/10 | Tone 7/10 | Brevity 9/10 | Relevance 7/10
- Decision: KEPT (Tone +2)
```

---

## Optimizing Meta-Skills (Process Skills)

Some skills don't produce text — they drive a process (e.g., this skill itself, planning workflows, research pipelines). For these:

**What to score:** Score the *experience of following the process*, not a text artifact.
- Did the process produce a clear result?
- Were there moments of confusion where the instructions were ambiguous?
- Did any step feel unnecessary or redundant?
- Could someone follow this without prior context?

**How to test:** Run the skill on 2-3 real tasks (not hypothetical). Score after each real use. The test inputs ARE the tasks you're applying the skill to.

**Dimensional scoring for process skills:**
- **Clarity** — Can I follow each step without re-reading?
- **Completeness** — Does the process cover the full workflow?
- **Actionability** — Do I know exactly what to do at each step, or do I have to infer?
- **Efficiency** — Are there wasted/redundant steps?
- **Self-applicability** — Can this process improve itself? (Meta-test)

## Checklist Sweet Spot
- **3-6 questions** = optimal
- Too few: not granular enough to guide changes
- Too many: skill starts gaming the checklist (like a student memorizing answers without understanding)

## When to Use
- Before running any skill at scale (cold outreach, content generation, scraping)
- After a new model upgrade — re-validate existing skills
- When a skill has inconsistent output quality
- Monthly maintenance pass on high-use skills
- Immediately after creating a new skill (structural audit only takes 5 min)

## When to Run Which Phase

- **Any new skill** → Structure audit (5 min, catches issues early)
- **Before scale use** → Output loop (validate quality before mass runs)
- **After model upgrade** → Output loop (re-validate existing skills)
- **Inconsistent output** → Output loop (find the failing item/dimension)
- **High-revenue skills** → Both phases (cold outreach, content gen — quality variance = revenue impact)

## Gotchas
- Output loop requires skills that produce **scoreable text outputs** — scripts/tools that produce side effects need a different verification approach (use a Product Verification skill type instead)
- Don't run output loop on skills that call expensive APIs without rate limit awareness — each round runs the skill multiple times
- Phase 1 (structure audit) should always run before Phase 2 — fixing structure first makes the output loop more effective
- 3-6 checklist questions is the sweet spot — more than 6 and the skill starts gaming individual checks rather than improving overall quality
