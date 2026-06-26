---
name: cognitive-self-training
description: Daily cognitive training, dream review, dream-scene narration, and self-improvement loop for OpenClaw, Hermes, Codex, Claude Code, and other AI agents. Use when the user wants a bot to review today's learning, consolidate knowledge, run spaced repetition or active recall, connect concepts across domains, reason with tian-dao style deduction, generate a human-readable dream description of the reasoning process, configure random dream styles, learn from corrections/errors, update agent memory, schedule daily dream reviews, or generate a next-step improvement strategy.
---

# Cognitive Self Training

Use this skill to turn an agent's daily work into durable learning. The goal is not to claim a biological brain, but to approximate useful brain-like behavior through external memory, retrieval practice, error correction, concept linking, dream-like recombination, human-readable dream description, and strategic review.

When the `tian-dao` reasoning skill is available, use it as the deduction engine for dream review: eight-dimensional deduction, probability branches, causal chains, butterfly effects, terminal states, contradiction analysis, inversion, and calibration.

## Core Model

Run the loop as:

1. **Capture**: Record new knowledge, corrections, tool failures, decisions, user preferences, and surprising insights.
2. **Distill**: Convert raw events into small cards: concept, procedure, error, preference, principle, or strategy.
3. **Retrieve**: Re-answer due cards from memory before looking at the source note.
4. **Compare**: Identify gaps, false assumptions, missing context, and weak reasoning.
5. **Connect**: Link today's ideas to prior ideas, adjacent domains, counterexamples, and concrete future tasks.
6. **Dream**: Run abductive, counterfactual, and tian-dao style deduction over today's material.
7. **Describe**: Render the reasoning process as a styled dream scene that a human can inspect.
8. **Consolidate**: Update the local training store, promote stable lessons, and schedule the next review.
9. **Strategize**: Choose the next 1-3 improvements that will most increase future performance.

## Pre-Install Time Handshake

Before installing, enabling, or copying this skill for a bot, ask the user for a daily dream review time. Do not silently choose a schedule.

Ask:

```text
What time should this bot run its daily dream review and cognitive consolidation? Please include timezone if different from the current environment.
```

If the user declines, install the skill but mark dream automation as `manual`. If they answer, write the schedule with:

```bash
bash cognitive-self-training/scripts/configure_dream_schedule.sh . "23:30" "Asia/Shanghai"
```

Then create the host automation using the current platform's automation system. For Codex Desktop, create a thread heartbeat if the user wants the review in the current conversation; create a cron automation only if they want a separate recurring job.

## Setup

Prefer a project-local store so learning remains scoped and inspectable:

```bash
bash cognitive-self-training/scripts/init_cognitive_training.sh .
```

If the skill is installed elsewhere, run the script from that installed skill path. If scripts are unavailable, create the structure in [references/storage-schema.md](references/storage-schema.md). For dream scheduling details, read [references/dream-protocol.md](references/dream-protocol.md) and [references/automation.md](references/automation.md). For dream description style configuration, read [references/dream-styles.md](references/dream-styles.md).

Use this root selection:

1. If an OpenClaw workspace exists for the current task, use `~/.openclaw/workspace/.cognitive-training/`.
2. Else use the current project/workspace root: `.cognitive-training/`.
3. Ask before writing to a global home directory, sharing across sessions, or modifying `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `MEMORY.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`.

Never record secrets, tokens, private keys, raw environment dumps, full private transcripts, health data, or third-party personal data. Store short redacted summaries instead.

## Start Of Session

When this skill activates:

1. Locate `.cognitive-training/`.
2. Read `principles.md`, `strategy.md`, `cards.md`, `graph.md`, and today's `daily/YYYY-MM-DD.md` if present.
3. Search for due cards with `Due: <= today`.
4. Load only relevant detail files. Keep the hot context small.
5. If the store is missing, initialize it or offer the exact command to initialize it.

Use source transparency when acting from stored learning: cite the file and entry id, such as `Using CT-20260422-003 from .cognitive-training/cards.md`.

## Capture Triggers

Log a training event when any of these happen:

- The user corrects the agent or says a previous answer was wrong.
- A command, tool, API, workflow, or integration fails unexpectedly.
- The agent discovers knowledge was outdated or incomplete.
- The user teaches a domain fact, preference, workflow, or style rule.
- A recurring problem appears for the second time.
- A task produces a non-obvious best practice.
- The user asks the bot to remember, review, train, practice, improve, or prepare for tomorrow.

Ignore one-off instructions unless they reveal a reusable preference or principle.

## Daily Review

At the end of a work session or when the user asks for a daily review:

1. Collect today's raw notes from `.cognitive-training/inbox/`, `.learnings/` if present, command failures, user corrections, and completed task summaries.
2. Distill them into cards using [references/templates.md](references/templates.md).
3. Run active recall on due cards before reading their answers.
4. Score each card with the rubric in [references/training-protocols.md](references/training-protocols.md).
5. Update `cards.md` with the next due date and `graph.md` with new links.
6. Promote repeated high-value lessons to `principles.md`.
7. Produce `daily/YYYY-MM-DD.md` with:
   - what was learned
   - what was misunderstood
   - what connected to older knowledge
   - what should be practiced next
   - what strategy should change tomorrow

## Dream Review

Run dream review during the scheduled time, or whenever the user asks the bot to "dream", "nightly review", "sleep on it", "deeply consolidate", or "research today's lessons".

Use the full protocol in [references/dream-protocol.md](references/dream-protocol.md). The short version:

1. Gather today's daily review, inbox, cards, mistakes, graph links, and unresolved questions.
2. Select 3-7 important fragments that deserve recombination.
3. Run tian-dao style deduction:
   - causal chain
   - stakeholders or forces
   - variables
   - branch points
   - probabilities and confidence
   - timeline
   - butterfly effects
   - terminal states
4. Add academic discipline:
   - distinguish observation, inference, hypothesis, and speculation
   - generate falsifiable questions
   - mark confidence and missing evidence
   - propose next experiments or reading
5. Select a dream description style from `.cognitive-training/dream-style-config.md`.
6. Write a "Dream Description" scene that maps the reasoning process to visible actions, places, characters, and tensions.
7. Write `dreams/YYYY-MM-DD.md`.
8. Convert only tested or high-value results into cards, graph links, mistakes, or strategy.

The dream description is not decorative filler. It must preserve traceability:

- Every major image must correspond to an input, card, mistake, hypothesis, branch, or strategy.
- Do not introduce unsupported facts as if they were evidence.
- Mark dream-only metaphors as metaphors when needed.
- Keep the rigorous deduction and hypothesis sections separate from the narrative.

## Retrieval Practice

For each due card, ask or self-run three forms of recall:

1. **Plain recall**: Explain the concept or procedure without looking.
2. **Diagnostic recall**: Explain when this knowledge fails, what confusion it prevents, or which mistake it corrects.
3. **Transfer recall**: Apply the idea to a new project, domain, user need, or tool.

After answering, compare against the stored source. Update the card only after comparison. If the answer was vague, score it low even if the direction was correct.

## Connection And Transfer

For each important new idea, add at least three links:

- **Causal link**: What caused it, enables it, or blocks it?
- **Analogy link**: What older concept has the same structure?
- **Application link**: Where can it be used next?

For complex learning, build a mini transfer matrix:

| Source Idea | Near Transfer | Far Transfer | Counterexample | Next Experiment |
| --- | --- | --- | --- | --- |

Prefer concrete task links over abstract associations. A useful connection changes future behavior.

## Strategic Review

After consolidation, write or update `strategy.md`:

1. Identify the highest-leverage weakness exposed today.
2. Pick one deliberate practice target for tomorrow.
3. Pick one prevention rule for recurring mistakes.
4. Pick one exploration thread if the knowledge graph reveals a gap.
5. Keep the plan short enough to load at the start of the next session.

Use this wording:

```markdown
## Strategy YYYY-MM-DD
- Focus:
- Why it matters:
- Practice:
- Prevention rule:
- Next evidence to seek:
```

## Promotion Rules

Promote a lesson from cards into `principles.md` when any are true:

- It was recalled correctly with score 4-5 on three separate days.
- It prevented a repeated mistake.
- It applies across multiple projects or domains.
- The user explicitly says it is important or asks to keep it.

For OpenClaw workspaces, promotion targets are:

- `SOUL.md`: behavioral style, principles, communication norms.
- `AGENTS.md`: workflows, delegation, planning, review loops.
- `TOOLS.md`: tool gotchas, command patterns, integration constraints.
- `MEMORY.md`: durable facts and preferences for the main session.

For generic coding agents, use `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` only with user approval or explicit project convention.

## Output Format

When the user asks for a review or training cycle, respond with:

```markdown
## Daily Cognitive Review

### Learned Today
- ...

### Recall Drills
- Card:
  - Prompt:
  - Answer:
  - Score:
  - Next due:

### Connections
- ...

### Mistakes Or Gaps
- ...

### Tomorrow's Strategy
- Focus:
- Practice:
- Prevention rule:

### Memory Updates
- Created:
- Updated:
- Promoted:
- Deferred:
```

Keep the final user-facing summary concise. Put detailed logs in `.cognitive-training/`.

When the user asks for dream review, use exactly these top-level sections and do not add extra top-level sections:

```markdown
## Dream Review
- Selected style:
- Dream scene:
- Reasoning map:

## Dream Recurrence Statement
- Why this dream scene recurs today:
- What learning pattern it rehearses:

## Tian-Dao Deduction
- Causal chain:
- Branches:
- Butterfly points:
- Terminal states:

## Research Hypotheses
- Hypothesis:
- Evidence needed:
- Confidence:

## Tomorrow's Practice
- 

## Store Updates
- 

## Summary Narrative
- Write one novel-like concluding paragraph in Chinese, no more than 300 Chinese characters.
- Fully describe the dream details, the review experience, and how the knowledge understanding improved.
```

## Failure Handling

If the agent cannot find prior memory, initialize the store and run only today's capture. If sources conflict, prefer the most specific and most recent source, then ask the user when the conflict affects behavior. If a card becomes stale or wrong, mark it `Status: retired` and add the replacement entry instead of deleting history.
