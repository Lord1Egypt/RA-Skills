---
name: autoresearch-pro
description: "Automatically improve OpenClaw skills, prompts, or articles through iterative mutation-testing loops. Inspired by Karpathy's autoresearch. Use when user says 'optimize [skill]', 'autoresearch [skill]', 'improve my skill', 'optimize this prompt', 'improve my prompt', 'polish this article', 'improve this article', or explicitly requests quality improvement for any text-based content. Supports three modes: skill (SKILL.md files), prompt (any prompt text), and article (any document)."
---

# autoresearch-pro

## Overview

Automatically improve any OpenClaw skill, prompt, or article through iterative mutation-testing: small edits → run test cases → score with checklist → keep improvements, discard regressions.

**Inspired by [Karpathy/autoresearch](https://github.com/karpathy/autoresearch).**

Supports three optimization modes:

| Mode | Input | Output |
|------|-------|--------|
| **Skill** | Path to a skill directory | Improved SKILL.md |
| **Prompt** | A prompt text string | Improved prompt |
| **Article** | An article/document text | Improved article |

---

## Workflow

### Step 1 — Identify Mode and Input

Ask the user to confirm:

- **Mode 1 — Skill**: User says "optimize [skill-name]" or provides a skill path
- **Mode 2 — Prompt**: User says "optimize this prompt" or pastes a prompt
- **Mode 3 — Article**: User says "improve this article" or pastes article text

For **Skill mode**, resolve the skill path to `~/.openclaw/skills/<skill-name>/SKILL.md`.
For **Prompt/Article mode**, keep the text in context (do not write to disk unless needed).

### Step 2 — Generate Checklist (10 Questions)

Read the target content first. Then generate 10 diverse, specific yes/no checklist questions relevant to the content type:

**For Skill mode (same as before):**

| # | Dimension | What to Check |
|---|----------|---------------|
| 1 | Description clarity | Is the frontmatter description precise and actionable? |
| 2 | Trigger coverage | Does it cover the main real-world use cases? |
| 3 | Workflow structure | Are steps clearly sequenced and unambiguous? |
| 4 | Error guidance | Does it handle error states and edge cases? |
| 5 | Tool usage accuracy | Are tool names and parameters correct for OpenClaw? |
| 6 | Example quality | Do examples reflect real usage patterns? |
| 7 | Conciseness | Is content free of redundant repetition? |
| 8 | Freedom calibration | Is instruction specificity appropriate? |
| 9 | Reference quality | Are references and links accurate? |
| 10 | Completeness | Are all sections filled with real content? |

**For Prompt mode (10 tailored questions):**

| # | Dimension | What to Check |
|---|----------|---------------|
| 1 | Goal clarity | Does the prompt state a clear, specific goal? |
| 2 | Role/tone | Is the desired role or tone specified? |
| 3 | Input format | Is the input format clearly described? |
| 4 | Output format | Is the expected output format specified? |
| 5 | Constraints | Are key constraints and boundaries stated? |
| 6 | Context sufficiency | Is enough context provided to avoid hallucination? |
| 7 | Edge cases | Does it handle ambiguous or edge case inputs? |
| 8 | Conciseness | Is it free of redundant or contradictory instructions? |
| 9 | Actionability | Are instructions concrete and actionable vs. vague? |
| 10 | Completeness | Are all necessary elements for the task present? |

**For Article mode (10 tailored questions):**

| # | Dimension | What to Check |
|---|----------|---------------|
| 1 | Title quality | Does the title clearly convey the main value? |
| 2 | Opening hook | Does the opening grab attention and set expectations? |
| 3 | Logical structure | Are ideas logically organized (not random)? |
| 4 | Argument clarity | Are claims supported with evidence or reasoning? |
| 5 | Conciseness | Is unnecessary padding or repetition removed? |
| 6 | Transition flow | Do paragraphs/sections flow smoothly? |
| 7 | Closing strength | Does the conclusion summarize and inspire action? |
| 8 | Tone consistency | Is the tone consistent throughout? |
| 9 | Readability | Is sentence/paragraph length varied appropriately? |
| 10 | Audience match | Does language match the target audience level? |

**Present the 10 questions**, numbered 1-10. Ask the user to select which ones to activate (e.g., "use questions 1, 3, 5, 7"). Default: use all 10 if user doesn't specify.

### Step 3 — Prepare Test Cases

- **Skill mode**: Generate 3-5 realistic prompts a user would send when using the skill
- **Prompt mode**: Generate 3-5 test inputs that the prompt would process
- **Article mode**: Generate 3-5 ways the article might be read or consumed

Store test cases in context — do not write to disk.

### Step 4 — Run Autoresearch Loop

**Loop configuration:**
- **Rounds per batch**: 30
- **Max total rounds**: 100
- **Pause**: After every 30 rounds, show summary and ask user to continue or stop
- **Stop conditions**: User says stop, OR 100 rounds completed

**Per-round procedure:**

1. **Mutate**: Make ONE small edit to the target content:
   - Skill mode: edit SKILL.md
   - Prompt mode: edit the prompt string
   - Article mode: edit the article text

2. **Test**: For each test case, simulate what output the content would produce.

3. **Score**: Apply each active checklist question (0 or 1 per question). Score = (passed / total) × 100.

4. **Decide**: If new score ≥ best score → keep the mutation. If lower → revert.

5. **Log**: Round number, mutation type, score, keep/revert decision.

**Mutation types (pick one per round):**

| Type | Description |
|------|-------------|
| A | Add a constraint rule |
| B | Strengthen trigger/coverage |
| C | Add a concrete example |
| D | Tighten vague language |
| E | Improve error/edge case handling |
| F | Remove redundant content |
| G | Improve transitions |
| H | Expand a thin section |
| I | Add cross-reference |
| J | Adjust degree-of-freedom |

### Step 5 — Report Results

**After each batch (30 rounds):**
```
Batch N (rounds X-Y):
  Best score: XX%
  Mutations kept: N  |  Reverted: N
  Most effective types: [list top 2-3]
Accumulated improvements: [summary]
Continue? (yes/stop)
```

**After full completion:**
- Original score vs. final score
- Top 3 most impactful mutations
- Final improved content (inline or diff)
- File path (skill mode only)

---

## Mutation Strategy Reference

**High-impact, low-risk changes:**
- Adding explicit constraints where the content is vague
- Expanding coverage to cover edge cases
- Adding concrete examples to abstract instructions
- Tightening soft language ("try to" → "must")

**Avoid in one round:**
- Large rewrites of entire sections
- Multiple unrelated changes at once
- Changing fundamental scope or purpose

See `references/mutation_strategies.md` for the full strategy guide.

---

## Mode Selection Quick Reference

| User says | Mode |
|-----------|------|
| "optimize [skill]" / "autoresearch [skill]" | Skill |
| "optimize this prompt" / "improve my prompt" | Prompt |
| "polish this article" / "improve this article" | Article |
| "optimize this document" | Article |

Default to **Prompt mode** if the input is a text string without a skill path.
