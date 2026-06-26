---
name: apophenia-guard
version: 1.0.0
description: >
  A cognitive bias interceptor for debugging sessions. Detects when you're
  seeing patterns that aren't there, chasing red herrings, or letting
  confirmation bias steer your investigation. Named after apophenia — the
  human tendency to perceive meaningful connections between unrelated things.
  The antibody to "I'm sure it's a race condition" when it's actually a typo.
author: J. DeVere Cooley
category: cognitive-defense
tags:
  - debugging
  - cognitive-bias
  - reasoning
  - anti-pattern
metadata:
  openclaw:
    emoji: "🛡️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - debugging
---

# Apophenia Guard

> "Apophenia: the spontaneous perception of connections and meaningfulness of unrelated phenomena. In debugging, it's the voice that says 'this must be related' when it absolutely isn't."

## What It Does

You've been debugging for an hour. You've formed a theory. Every new piece of evidence *seems* to confirm it. You're deep in the code, cross-referencing logs, following a trail that feels inevitable —

And you're wrong. You've been wrong since minute twelve. Everything after that was confirmation bias wearing a lab coat.

Apophenia Guard is a **cognitive bias interceptor** that monitors debugging reasoning for the twelve most common cognitive traps that waste developer time, and intervenes before you spend three hours proving a hypothesis that a fresh pair of eyes would dismiss in three minutes.

## The Twelve Cognitive Traps

### 1. Confirmation Bias
**The trap:** Seeking evidence that supports your theory while ignoring evidence that contradicts it.

```
DETECTION SIGNALS:
├── "That proves it!" appears more than "That's weird..."
├── Contradictory evidence is dismissed as "noise" or "unrelated"
├── Investigation narrows instead of widening after the first hypothesis
└── You haven't tried to disprove your theory — only to prove it
```

**Intervention:** Force an inversion. State the opposite hypothesis and spend 5 minutes looking for evidence that supports *it*.

### 2. Recency Bias
**The trap:** Assuming the bug was introduced by a recent change because it was recently discovered.

```
DETECTION SIGNALS:
├── "It was working yesterday" → investigating only today's commits
├── Ignoring the possibility that the bug always existed
├── Conflating "when we noticed" with "when it started"
└── Not checking if the bug exists in older versions
```

**Intervention:** Check the last known good state. Binary search through history. The bug's discovery date is not its birth date.

### 3. Narrative Fallacy
**The trap:** Constructing a story that explains the symptoms, then treating the story as fact.

```
DETECTION SIGNALS:
├── "What must have happened is..."
├── The explanation is coherent, detailed, and untested
├── You can describe the bug's lifecycle without having verified any step
└── The story is more compelling than the evidence
```

**Intervention:** Strip the narrative. List only what you've **observed** (not inferred). If the observation list is shorter than the theory, you're writing fiction.

### 4. Availability Heuristic
**The trap:** Assuming the cause is something you've seen before, because it's easily recalled.

```
DETECTION SIGNALS:
├── "I've seen this before — it's definitely a race condition"
├── Jumping to a diagnosis before examining symptoms
├── The first tool you reach for is specific to your assumed cause
└── Pattern-matching from a different project/language/context
```

**Intervention:** Pretend you've never seen this type of bug before. What would a first-principles investigation look like?

### 5. Anchoring
**The trap:** The first piece of evidence disproportionately shapes all subsequent reasoning.

```
DETECTION SIGNALS:
├── Your entire investigation traces back to the first anomaly you noticed
├── You haven't questioned whether the first clue is even relevant
├── "It all started when I saw..." drives the narrative
└── Alternative starting points haven't been explored
```

**Intervention:** Deliberately start from a different symptom. If you started from the error log, start from the user report. If you started from the code, start from the data.

### 6. Sunk Cost Trap
**The trap:** Continuing down a debugging path because you've already invested time, not because it's productive.

```
DETECTION SIGNALS:
├── "I've been at this for two hours, I must be close"
├── Reluctance to abandon a theory you've invested in
├── The investigation is getting more complex, not more focused
├── New evidence requires increasingly elaborate explanations to fit the theory
└── You're adding epicycles to save the model
```

**Intervention:** Time check. If you've been on the same theory for > 30 minutes without new supporting evidence, the theory is probably wrong. Start over. The time is already spent.

### 7. Fundamental Attribution Error
**The trap:** Blaming the system (framework, OS, compiler, hardware) when the bug is in your code.

```
DETECTION SIGNALS:
├── "It must be a bug in [library/framework/OS]"
├── Elaborate theories about runtime behavior before checking your logic
├── "This shouldn't be possible" → implies the platform is broken
└── You're reading framework source code before re-reading your own
```

**Intervention:** 99.9% of bugs are in your code. Check your code first. Check it again. Then check the framework.

### 8. Clustering Illusion
**The trap:** Seeing a pattern in random or coincidental events.

```
DETECTION SIGNALS:
├── "It always fails on Tuesdays" (sample size: 2 Tuesdays)
├── "It only happens with user IDs ending in 7"
├── Correlation treated as causation without mechanism
└── Small sample sizes interpreted as trends
```

**Intervention:** Calculate the actual base rate. How many Tuesdays didn't have failures? What's the expected distribution? Random events cluster naturally — it doesn't mean anything.

### 9. Einstellung Effect
**The trap:** A known solution prevents you from seeing a better one (or the actual one).

```
DETECTION SIGNALS:
├── You immediately reached for a familiar fix pattern
├── The fix "should work" but doesn't, yet you keep refining it
├── You haven't considered that this might be a fundamentally different problem
└── Your solution vocabulary is from a previous project/language
```

**Intervention:** Describe the problem to someone (or rubber duck) without mentioning your solution. Let the problem define the solution space, not the other way around.

### 10. Survivorship Bias
**The trap:** Only examining the cases that failed while ignoring the cases that succeeded.

```
DETECTION SIGNALS:
├── Investigating only failed requests, not successful ones
├── "What's different about the broken ones?" without asking
│   "What's the same about the working ones?"
├── No control group in your investigation
└── Assuming the failure case is representative
```

**Intervention:** Compare a failing case with a succeeding case side by side. The difference is more informative than either case alone.

### 11. Occam's Broom
**The trap:** Sweeping inconvenient evidence under the rug (Occam's Razor in reverse).

```
DETECTION SIGNALS:
├── "That log entry is probably unrelated"
├── "Ignore that — it's a known issue" (is it though?)
├── Evidence that doesn't fit is labeled as noise without verification
└── The explanation requires you to ignore some of the data
```

**Intervention:** Make a list of EVERYTHING you've dismissed. Revisit each item. If your theory requires ignoring more than one data point, it's probably incomplete.

### 12. The XY Problem
**The trap:** Debugging your attempted solution instead of the original problem.

```
DETECTION SIGNALS:
├── You can no longer articulate the original symptom
├── The investigation has shifted from "why does X fail?"
│   to "why doesn't my fix for X work?"
├── You're several abstraction layers away from the user-visible issue
└── "If I can just get this regex right..." (the problem isn't regex-shaped)
```

**Intervention:** Stop. State the original problem in one sentence. If you can't, you've drifted. Return to the symptom. Start fresh from there.

## The Guard Process

```
CONTINUOUS MONITORING:
├── Track how long each hypothesis has been active
├── Count evidence for vs. evidence against current theory
├── Monitor investigation breadth (narrowing too fast = bias)
├── Flag when investigation depth exceeds evidence depth
└── Check for trap signatures at every reasoning step

INTERVENTION TRIGGERS:
├── Hypothesis active > 30 min with no new supporting evidence
├── Evidence-against count > 0 with no theory adjustment
├── Investigation breadth < 2 alternatives at any point
├── Theory complexity growing faster than evidence base
└── Any trap signature detected with confidence > 70%

INTERVENTION FORMAT:
├── Name the trap
├── Show the evidence that triggered detection
├── Suggest a specific counter-action
└── Offer to restart from a different entry point
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║              ⚠ APOPHENIA GUARD: INTERVENTION ⚠              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  TRAP DETECTED: Confirmation Bias + Sunk Cost               ║
║                                                              ║
║  EVIDENCE:                                                   ║
║  ├── Current hypothesis active for 47 minutes                ║
║  ├── 3 observations supporting theory                        ║
║  ├── 2 observations contradicting theory (dismissed as noise)║
║  ├── Investigation has narrowed to 1 file (started at 12)    ║
║  └── Theory complexity has increased twice without new data  ║
║                                                              ║
║  RECOMMENDED ACTION:                                         ║
║  ├── PAUSE: State what you've actually proven (not assumed)  ║
║  ├── INVERT: Spend 5 min trying to disprove your theory     ║
║  ├── COMPARE: Find a working case and diff against failure   ║
║  └── RESTART: If inversion finds counter-evidence, pivot     ║
║                                                              ║
║  REMINDER: The average bug is simpler than the average       ║
║  debugging theory. Complexity is usually in the              ║
║  investigator, not the code.                                 ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- At the start of any debugging session (set the guard before bias sets in)
- When you catch yourself saying "I'm sure it's..."
- When debugging has exceeded 30 minutes without resolution
- When the explanation is getting *more* complex instead of *more* clear
- When you feel frustrated (frustration amplifies every cognitive bias)

## Why It Matters

The hardest bugs aren't hard because the code is complex. They're hard because the **debugging is biased**. A developer with perfect reasoning and a simple set of tools will outperform a developer with every debugging tool and a biased mind.

Apophenia Guard doesn't help you find bugs. It helps you stop finding bugs that aren't there.

Zero external dependencies. Zero API calls. Pure cognitive bias detection.
