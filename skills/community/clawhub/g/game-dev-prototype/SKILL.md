---
name: game-dev-prototype
description: >
  Throwaway prototype workflow for rapid validation. Conduct 1-3 day
  hypothesis-driven sprints with clear exit criteria, playtest goals, and
  a decision framework (proceed / pivot / kill).
triggers:
  - "prototype an idea"
  - "validate game mechanic"
  - "rapid prototyping"
  - "test a game idea"
  - "prototype sprint"
  - "game jam"
---

# Game Dev Prototype — Rapid Validation Sprint

## 🎯 Purpose

Validate risky game mechanics or concepts quickly with throwaway code.
1-3 day sprints focused on answering exactly ONE question. Disciplined exit
criteria prevent scope creep and sunk-cost fallacy.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Can create prototype plan, track progress, and write results. Best for structured prototyping docs. |
| **Claude Code** | Can write prototype code directly. Best for actual implementation support. |
| **Cursor/Windsurf** | Excellent for coding the prototype. Can scaffold a minimal project quickly. |
| **GitHub Copilot** | Can help write prototype code inline. Great for quick implementations. |
| **Generic LLM Chat** | Guide the user through the process and provide code snippets. |
| **Any AI** | All can do the planning phase. Coding-capable AIs can help implement. |

**Key principle:** A throwaway prototype should be THROWN AWAY. Do not let
prototype code become production code unless you're doing a game jam.

---

## 📋 Phase 1: Hypothesis Definition

### Step 1.1 — The One Question

Ask:

> **"What is the ONE thing we need to validate?"**
>
> Good questions:
> - "Does this control scheme feel good?"
> - "Is this core loop fun for more than 5 minutes?"
> - "Can we render 1000 entities at 60fps?"
> - "Does the procedural generation produce interesting levels?"
>
> Bad questions (too broad):
> - "Is the game fun?" (too vague)
> - "Will people buy it?" (can't test in 3 days)

### Step 1.2 — Hypothesis Statement

Write as:

> **"We believe that [mechanic/concept] will [outcome] for [player type]."**
>
> Example: *"We believe that magnetic polarity switching will create satisfying
> traversal puzzles for puzzle-platformer fans."*

### Step 1.3 — Success Criteria (Exit Criteria)

Define measurable criteria:

```markdown
## Success Criteria (3 = pass, ≥2 = consider, <2 = fail)

| # | Criterion | Measure |
|---|-----------|---------|
| 1 | Player can complete the loop without instructions | ≥ 3 of 3 playtesters |
| 2 | Average time to first "fun" moment | < 30 seconds |
| 3 | Players attempt to repeat the action unprompted | Observed in ≥ 2 testers |
| 4 | Framerate stays above 60fps | With target entity count |
| 5 | [Custom criterion] | [Measure] |
```

---

## 🎯 Phase 2: Scope

### Step 2.1 — The Minimum Viable Prototype

Ask:
> **"What is the smallest thing we can build to test our hypothesis?"**

Examples:
- For "does this control feel good?" → one scene, one object, the control
- For "is this loop fun?" → the loop with placeholder art, no menu
- For "performance?" → stress test scene, no gameplay

### Step 2.2 — What We WON'T Build

List explicitly:

```
WILL NOT:
- Menu screens
- Sound effects
- Tutorial
- Save/load
- Polish
- Art (placeholder only)
- UI
- Analytics
```

### Step 2.3 — Constraints

| Dimension | Limit |
|-----------|-------|
| **Time** | 1-3 days (fixed, non-negotiable) |
| **Engine** | Whatever gets it done fastest |
| **Art** | Primitives / placeholders / free assets |
| **Code quality** | "Working" not "clean" — it will be thrown away |

---

## 🛠️ Phase 3: Build Sprint

### Day 1: Core

- Set up minimal project
- Implement the ONE mechanic
- No polish, no extra features
- End of day: it should run and be testable

### Day 2: Playability

- Add simple inputs
- Add a goal/objective so there's a "loop"
- Add minimal feedback (visual indicator of success)
- End of day: someone who isn't you can play it

### Day 3: Playtest & Decision

- Don't add new features
- Polish only what's needed to remove blockers
- Run playtest (see Phase 4)
- Make decision (see Phase 5)

### Daily Check-Ins

Each day, ask:
> **"What did you build today? Did anything surprise you? Are we still on track?"**

If something surprising (good or bad) changes the hypothesis, adjust.

---

## 🎮 Phase 4: Playtest

### Step 4.1 — Tester Selection

Ask:
> **"Who will test?"**
>
> ```
> 1) Yourself (better than nothing, biased)
> 2) Friend/family (honest but kind)
> 3) Fellow dev (technically knowledgeable)
> 4) Target audience member (ideal)
> ```

### Step 4.2 — Test Protocol

Provide testers the prototype and observe WITHOUT giving instructions.

**Observe:**
- Do they figure it out without help?
- Where do they get stuck?
- Do they smile / curse / lean in?
- Do they want to keep playing after the test?
- What do they try that you didn't expect?

**Ask after:**
- "What was confusing?"
- "What was the moment it 'clicked'?"
- "What would make this more fun?"
- "What's one thing you'd change?"

**Do NOT ask:**
- "Did you like it?" (they'll be polite)
- "Is this a good idea?" (they don't know)

### Step 4.3 — Score Against Criteria

Rate 1-5 for each criterion. Collect data below.

---

## 🚦 Phase 5: Decision

### Step 5.1 — The Three Doors

| Outcome | Criteria | Action |
|---------|----------|--------|
| **PROCEED** 🟢 | Most criteria met; data supports hypothesis | Move to production. Archive the prototype. Start fresh with real code. |
| **PIVOT** 🟡 | Mixed results; interesting but needs change | Document what didn't work. Modify hypothesis. Run another prototype sprint (1 day max). |
| **KILL** 🔴 | Hypothesis disproven or not worth pursuing | Celebrate the learning. Document findings. Move to next concept. NO sunk-cost. |

### Step 5.2 — Decision Document

Write `prototype-result.md`:

```markdown
# Prototype Results

## Hypothesis
[Original hypothesis statement]

## What We Built
[One-paragraph summary]

## Duration
[Start date] — [End date] ([X] days)

## Results

| Criterion | Score | Notes |
|-----------|-------|-------|
| Criterion 1 | X/5 | [notes] |
| Criterion 2 | X/5 | [notes] |
| ... | ... | ... |

## Playtest Feedback
- **What worked:** [list]
- **What didn't:** [list]
- **Surprises:** [list]

## Decision: [PROCEED / PIVOT / KILL]

**Rationale:** [Why this decision]

## Lessons Learned
- [Lesson 1]
- [Lesson 2]

## Next Steps
- [If PROCEED] → Write/update GDD, start `architecture` design
- [If PIVOT] → Adjust hypothesis, plan next sprint
- [If KILL] → Return to `brainstorm` for next concept
```

### Step 5.3 — Archive or Delete

**If PROCEED:** Archive the prototype in a `_prototypes/` folder. Do not
reuse code. Write fresh production code based on lessons learned.

**If PIVOT:** Keep the prototype. Fork or modify for the next sprint.
Set a 1-day time limit on the pivot sprint.

**If KILL:** Delete or archive. Move on quickly.

---

## ⚡ Game Jam Variant

For game jams (48-72 hours), the prototype IS the game. Adapt:

1. **Hour 0-4:** Concept + core loop (Phase 1-2 compressed)
2. **Hour 4-24:** Core mechanic working (Phase 3 day 1 + 2)
3. **Hour 24-48:** Content + polish (Phase 3 day 3 extended)
4. **Final hours:** Playtest + ship (no kill option)

In a jam, the prototype becomes the release. Code quality is secondary.
**Shipping > Perfect.**
