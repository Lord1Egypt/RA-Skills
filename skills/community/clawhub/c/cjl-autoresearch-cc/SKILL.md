# cjl-autoresearch-cc

## Overview

Improve skills, prompts, articles, workflows, and systems via iterative mutation-testing.

**Core principle:** One small verifiable change per round. Large rewrites are unverifiable and will be reverted.

**Workflow:** small edits → test → score → keep improvements, discard regressions.

Inspired by Karpathy/autoresearch and 0xcjl/openclaw-autoresearch-pro.

## Trigger Keywords

**English:** `autoresearch`

**Chinese:** `自动优化`, `自动研究`

## Semantic Triggers (No Keywords Needed)

This skill activates when the user's intent matches, even without explicit keywords:

- User wants to improve any skill, prompt, article, workflow, or system
- User asks to polish, refine, enhance, or upgrade content
- User wants iterative testing and improvement
- User says '帮我改进一下这个prompt', 'optimize this'
- User says '迭代优化', '循环改进', '反复打磨'
- User asks '能不能更好', '如何提升质量'
- User uses "打磨", "精炼", "完善", "升级" in context of content improvement

## Supported Optimization Targets

| Mode | Input | Example |
|------|-------|---------|
| **Skill** | Skill name or path | `coding-standards`, `~/.claude/skills/tdd-workflow` |
| **Plugin** | Path to a plugin directory | `~/.claude/plugins/everything-claude-code` |
| **Prompt** | A prompt text string | Inline or file path |
| **Article** | An article/document text | Inline or file path |
| **Workflow** | A process or workflow description | Inline or file path |
| **System** | A mechanism or system design | Inline or file path |

## Workflow

### Step 1 — Identify Mode and Target

Before proceeding, confirm with user:
> "Optimize [target] in [mode] mode? (yes/no)"

If no, ask for clarification. If yes, proceed to Step 2.

Parse the user's request to determine mode. Check for:

**Keyword triggers:**
- `autoresearch [target]` / `自动优化 [target]` / `自动研究 [target]`
- `optimize [target]` / `improve [target]` / `优化 [target]` / `改进 [target]`
- `refine [target]` / `enhance [target]` / `精炼 [target]` / `增强 [target]`

**Semantic triggers (intent-based):**
- User wants to improve any skill, prompt, article, workflow, or system
- User asks to polish, refine, enhance, or upgrade content
- User describes wanting iterative testing and improvement

**Mode detection from intent:**

| User Intent | Mode |
|-------------|------|
| Optimize a skill/SKILL.md file | Skill |
| Optimize an agent configuration | Skill |
| Improve a custom command | Skill |
| Optimize a plugin | Plugin |
| Improve hooks configuration | Plugin |
| Improve a prompt text | Prompt |
| Polish an article/document | Article |
| Optimize a workflow/process | Workflow |
| Improve a system mechanism | System |

For Skill/Plugin mode, resolve the path:
- Skill: `~/.claude/skills/<skill-name>/SKILL.md`
- Plugin: `~/.claude/plugins/<plugin-name>/`

If path doesn't exist, search in order: ~/.claude/skills/ → current dir → ask user.

**Examples of semantic triggers (no keywords):**
- "帮我优化一下这个skill" → Skill mode
- "这个prompt不够好，帮我改进" → Prompt mode
- "我想让这篇文章更通顺" → Article mode
- "优化一下部署流程" → Workflow mode

### Step 2 — Generate Checklist (10 Questions)

Read the target content first. Then generate 10 diverse, specific yes/no checklist questions relevant to the content type:

**For Skill/Plugin mode:**

| # | Dimension | What to Check |
|---|----------|---------------|
| 1 | Description clarity | Is the description precise, actionable, and clear? Does it state what the skill does and when to use it? |
| 2 | Trigger coverage | Does it cover main real-world use cases? |
| 3 | Workflow structure | Are steps clearly sequenced and unambiguous? |
| 4 | Error guidance | Does it handle error states and edge cases? |
| 5 | Tool usage accuracy | Are tool names and parameters correct for Claude Code? |
| 6 | Example quality | Do examples reflect real usage patterns? |
| 7 | Conciseness | Is content free of redundant repetition? |
| 8 | Freedom calibration | Is instruction specificity appropriate? |
| 9 | Reference quality | Are references and links accurate? |
| 10 | Completeness | Are all sections filled with real content? |

**For Prompt mode:**

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

**For Article/Documentation mode:**

| # | Dimension | What to Check |
|---|----------|---------------|
| 1 | Title quality | Does the title clearly convey the main value? Is it specific enough? |
| 2 | Opening hook | Does the opening grab attention? Does it set clear expectations? |
| 3 | Logical structure | Are ideas logically organized (not random)? |
| 4 | Argument clarity | Are claims supported with evidence or reasoning? |
| 5 | Conciseness | Is unnecessary padding or repetition removed? |
| 6 | Transition flow | Do paragraphs/sections flow smoothly? |
| 7 | Closing strength | Does the conclusion summarize and inspire action? |
| 8 | Tone consistency | Is the tone consistent throughout? |
| 9 | Readability | Is sentence/paragraph length varied appropriately? |
| 10 | Audience match | Does language match the target audience level? |

**For Workflow/System mode:**

| # | Dimension | What to Check |
|---|----------|---------------|
| 1 | Goal clarity | Is the objective clearly stated? |
| 2 | Step sequencing | Are steps in logical, efficient order? |
| 3 | Completeness | Are all necessary steps present? |
| 4 | Error handling | Are failure modes addressed (timeout, auth, network, resource exhaustion)? |
| 5 | Edge cases | Are corner cases considered (empty input, large files)? |
| 6 | Simplicity | Is the workflow/system as simple as possible? Can steps be combined or eliminated? |
| 7 | Observability | Can progress/status be tracked? |
| 8 | Reversibility | Can steps be undone if errors occur? |
| 9 | Automation potential | Which steps could be automated? |
| 10 | Maintainability | Is it easy to modify and extend? |

Present the 10 questions, numbered 1-10. Ask the user to select which ones to activate.

> **Rule:** Must use at least 5 questions. Using fewer makes scoring unreliable.

After presenting, ask: "Ready to start the optimization loop? (yes/start)"

### Step 3 — Prepare Test Cases

Test cases validate that mutations improve, not harm, the content. Generate realistic user scenarios.

- **Skill/Plugin mode**: Generate 3-5 realistic prompts a user would send when using the skill/plugin
- **Prompt mode**: Generate 3-5 test inputs that the prompt would process
- **Article mode**: Generate 3-5 ways the article might be read or consumed
- **Workflow mode**: Generate 3-5 scenarios the workflow would handle
- **System mode**: Generate 3-5 conditions the system would encounter

Store test cases in context — do not write to disk unless needed.

### Step 4 — Run Autoresearch Loop

> **Tip:** For mutation strategies, see [Mutation Strategy Reference](#mutation-strategy-reference) below.

**Loop configuration:**
- Rounds per batch: 30
- Max total rounds: 100
- Pause: After every 30 rounds, show summary and ask user to continue or stop
- Stop conditions:
  - User says stop
  - 100 rounds completed
  - Score reaches 100%
  - No improvement for 10 consecutive rounds

**Per-round procedure:**

Track progress: Round N/100 | Best: XX% | Last: +/-YY

> **Constraint:** ONE mutation per round. Multiple changes = unverifiable = will be reverted.

1. **Mutate**: Make ONE small edit (see [Mutation types](#mutation-types-pick-one-per-round))
2. **Test**: For each test case, simulate what output the content would produce

   > **Constraint:** Be honest. If the output would disappoint a user, the mutation failed.

3. **Score**: Apply each active checklist question (0 or 1 per question). Score = (passed / total_questions) × 100

   Scoring scale:
   - 10/10 = 100% (perfect)
   - 7/10 = 70% (good)
   - 5/10 = 50% (minimum viable)

4. **Decide**: If new score ≥ best score → keep the mutation. If lower → revert

   Example: Best=85%, New=87% → Keep. Best=85%, New=83% → Revert.

   > Trust the score. Don't rationalize a bad mutation.

5. **Log**: Round number, mutation type, score, keep/revert decision

**Mutation types (pick ONE per round):**

| Type | Name | When to Use |
|------|------|-------------|
| A | Add constraint | When content is too vague |
| B | Strengthen coverage | When trigger cases are missing |
| C | Add example | When steps are too abstract |
| D | Tighten language | When words are soft ("try to") |
| E | Error handling | When failure modes missing |
| F | Remove redundancy | When content is verbose |
| G | Improve transitions | When flow is choppy |
| H | Expand thin section | When content is sparse |
| I | Add cross-ref | When sections are isolated |
| J | Adjust freedom | When balance is off |

### Step 5 — Report Results (after each batch)

See [Quick Reference](#quick-reference) below for output format examples.

**After each batch (30 rounds):**

Example:
```
Batch 1 (rounds 1-30):
  Best score: 85%
  Mutations kept: 23  |  Reverted: 7
  Most effective types: A, C, D
```

**After full completion:**

```
Optimized: [filename/path]
Score: XX% → YY% (+ZZ%)
Rounds: N (kept: K, reverted: R)
Top mutations: [type, type, type]
---
Final content:
[diff or inline]
```

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
- Formatting-only changes (no testable value)
- Adding content the user didn't request
- Removing more than 10% of content

## Quick Reference

### Keywords Reference

**Auto-detect:** `autoresearch`, `自动优化`, `自动研究`
**Skill:** `autoresearch ~/.claude/skills/tdd`
**Prompt:** `optimize this prompt: [text]`
**Workflow:** `optimize the deployment workflow`
**System:** `improve the error handling system`

### Semantic Triggers (No Keywords)
```
"帮我优化一下这个skill"           # → Skill mode
"这个prompt不太行"               # → Prompt mode
"我想让文章更通顺"               # → Article mode
"优化一下部署流程"               # → Workflow mode
"改进一下这个系统"               # → System mode
"improve this code review"         # → Prompt/Skill mode
"polish this documentation"       # → Article mode
```

### Mode Detection
| Situation | Action |
|-----------|--------|
| Path detected | Skill/Plugin mode |
| Keyword present | Keyword-specified mode |
| Short text | Prompt mode |
| Long document | Article mode |
| Uncertain | Prompt mode (default) |

**Edge cases:** Empty → ask. Invalid path → fallback to ~/.claude/skills/. Ambiguous → ask.
