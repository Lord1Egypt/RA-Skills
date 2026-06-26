---
name: writing-skills
description: "Use when creating new skills, editing existing skills, or verifying skills work before deployment. Trigger when a user asks to create, improve, or test a skill. Do not trigger for general task execution or when the user is only reading an existing skill."
---

# Writing Skills

## Overview

**Writing skills is Test-Driven Development applied to process documentation.**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**Skills live in the platform's designated skills directory.**

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or workflows. Skills help future agent instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, workflows, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations agent uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify agent now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

The entire skill creation process follows RED-GREEN-REFACTOR.

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in project config)
- Mechanical constraints (if enforceable by automation, automate it — save skills for judgment calls)

## The Process

### Phase 1: RED — Establish Baseline

Before writing the skill, prove it's needed:

1. **Run baseline scenario** — Dispatch subagent with the pressure scenario, WITHOUT the skill
2. **Document violations** — Record exact rationalizations the agent uses to bypass the rule
3. **Confirm skill is needed** — Only proceed if agent fails baseline

**Baseline prompt template:**
```markdown
[Task description that will tempt the agent to skip the target behavior]

Your task: [what the agent should do]
```

Record: What did the agent do wrong? What exactly did it say to rationalize it?

### Phase 2: GREEN — Write the Skill

Write the skill to address the exact violations you documented:

1. **Address documented rationalizations** — Each violation gets a counter in the skill
2. **Include Iron Law if rigid** — "NO X WITHOUT Y FIRST"
3. **Include Red Flags section** — List the exact rationalizations from baseline
4. **Keep it minimal** — Address what failed, nothing more
5. **Run compliance test** — Dispatch subagent WITH the skill, same pressure scenario

**Success:** Agent complies with all rules.

### Phase 3: REFACTOR — Close Loopholes

After achieving GREEN:

1. **Find new rationalizations** — Run variations of the pressure scenario
2. **Document new violations** — Add to Red Flags section
3. **Plug loopholes** — Update skill, re-verify
4. **Repeat** until no new violations found in 3 consecutive runs

## Skill Structure

```markdown
---
name: skill-name
description: "Trigger description. Use when [conditions]. Do not trigger when [exclusions]."
---

# Skill Title

## Overview
[Core principle in 1-2 sentences]

## The Iron Law (if rigid)
[The non-negotiable rule]

## When to Use
[Conditions and anti-conditions]

## The Process / Pattern
[Numbered steps or phases]

## Red Flags — STOP
[Exact rationalizations to watch for]

## Common Mistakes
[Table: Mistake | Fix]

## The Bottom Line
[One-sentence summary]
```

## Description Quality

The description is the trigger mechanism. It must:

1. **State when to trigger** — specific conditions, not vague
2. **Include trigger phrases** — what users typically say when they need this
3. **State when NOT to trigger** — explicit exclusions
4. **Avoid mandatory language** — use "trigger when" not "MUST trigger after ANY"
5. **Length:** 50–200 words

**Good:**
```
"Use when creating or editing a skill file. Trigger when the user asks to create a skill, improve a skill description, or test a skill. Do not trigger when the user is only reading or viewing a skill."
```

**Bad:**
```
"MUST trigger proactively after ANY SKILL.md file is created, written, edited, modified, or optimized"
```

## Gotchas

**Writing the skill without baseline testing**
- You don't know what the agent actually does wrong
- Result: Skill addresses imagined problems, not real ones
- Fix: Always run baseline first

**Addressing the letter, not the spirit**
- Agent finds new wordings that bypass the rule
- Result: Skill passes initial test, fails in practice
- Fix: Refactor phase — find and close loopholes

**Over-specification**
- Skill becomes so long it overwhelms the agent
- Result: Agent skips parts or gets confused
- Fix: Keep it minimal — address what failed, nothing more

**Vague description**
- Agent doesn't know when to invoke the skill
- Result: Skill never triggers
- Fix: Include specific trigger phrases and explicit exclusions
