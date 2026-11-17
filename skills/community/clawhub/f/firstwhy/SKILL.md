---
name: firstwhy
description: "Prefer explicit /firstwhy invocation. Without the command, activate only in three situations: a requirement too vague to act on, a design tradeoff that needs defensible justification, or the same problem returning after it was supposedly fixed. Drills down by asking why until the answer hardens into an unexamined assumption (\"that's just how it's done\"), splits that assumption into real constraints versus inherited habits, rebuilds the solution from the constraints alone, walks back up the chain to prove every layer is explained, then verifies the load-bearing assumption with the cheapest available evidence. Triggers: firstwhy, 5why, five whys, first principles, first-principles thinking, root cause, root cause analysis, why does this keep happening. Not for single reproducible crashes or test failures — route those to a debugging workflow."
argument-hint: "[the problem, the decision, or the recurring symptom]"
---

# FirstWhy · 5Why × First Principles

## Core mechanism

Ask why until the answer hardens into **"that's just how it's done" / "everyone does it this way" / "it's the convention."** That sentence is the target.

Split the target into **real constraints** and **inherited habits**, rebuild the solution from the constraints alone, walk back up the chain to account for every layer, and **finally verify the one assumption the whole solution stands on**.

Drilling locates a single target (so you don't decompose in ten directions at once). Decomposition breaks through the shell (so you don't stall at "everyone does it this way"). Ground verification turns logical coherence into factual truth. All three are load-bearing.

**The critical distinction**: walking back up proves the reasoning *holds together*. It does not prove it is *true*. Without ground verification, this whole method is just issuing itself a certificate.

## Flow

```
1 Pin down the symptom
2 Ask why ──reached something actionable──→ 5 Walk back up → 6 List assumptions → 7 Verify ground → Close
   │                                                ↑                          │
   └─hit "everyone does it this way"→ 3 Split → 4 Rebuild ┘                    │
                                                                  assumption falsified
                                                                        ↓
                                                              back to step 3, re-split
```

## When to use

**Prefer the explicit `/firstwhy` command.**

Without the command, activate only in these three situations:

- A requirement too vague to act on
- A design tradeoff that needs defensible justification
- The same problem returning after it was supposedly fixed

Natural-language triggers: 5why, first principles, root cause analysis, think from the ground up, why does this keep happening.

**Stay out of everything else** — routine Q&A, information lookups, clearly-scoped small changes. Just do the work.

## When NOT to use

| Situation | Go here instead |
|---|---|
| A reproducible error, test failure, or crash | A debugging workflow (e.g. `systematic-debugging`) — that one needs evidence and reproduction |
| Pure information lookup, one obvious small change | Just do it, don't run a process |
| User only wants the conclusion | Use the light tier, skip decomposition and rebuild |

## The process

### Step 1 — Pin down the symptom

One sentence: what is wrong, or what must be decided. **No causes allowed in this step.**
If the symptom itself is vague, ask the user one clarifying question. Do not guess.

### Step 2 — Ask why

Format each layer:

```
Why X? → Because Y (evidence: observed fact / code / data / the user's own words)
```

Rules:

- **Do not preset five rounds.** Stop when you stall or when you reach something actionable.
- Every layer needs evidence. Mark any unevidenced guess as `[assumption]`.
- Stall signals: that's just how it is / it's always been this way / everyone does it this way / it's the standard / legacy reasons / it was faster at the time / that's what upstream gave us

**Branch**:

- Reached a concrete, actionable cause → jump to Step 5 (light tier, no decomposition)
- Hit a stall signal → go to Step 3 (full tier)

### Step 3 — Split the target (only when stalled)

Split that "everyone does it this way" into two piles:

| Real constraints (these count) | Inherited habits (void, re-choosable) |
|---|---|
| Physically or mathematically unavoidable | Someone's temporary choice at the time |
| Genuine ceilings on cost, time, headcount | Carried forward, never questioned |
| Hard legal, safety, or compatibility requirements | "Industry convention" nobody can justify |

**Test**: every real constraint must state **what concretely goes wrong if it is violated**. Anything that cannot state a consequence goes in the habits pile.

### Step 4 — Rebuild

**Reuse by default. Do not rebuild casually.**

First check whether an existing solution already satisfies every real constraint from Step 3. Only when a constraint that the existing solution depends on has been *falsified* may you design from scratch — and you must name which constraint was falsified.

When rebuilding, map the solution against each constraint and state how it is satisfied.

### Step 5 — Walk back up (never skip)

Take the solution back to the chain and account for each layer:

```
Layer N's Y — how does the solution stop this from happening?
```

**If any layer cannot be accounted for, you only patched a symptom. Go back to Step 4.**
This is the only way to separate "genuinely hit the root" from "patched the symptom in a new posture."

### Step 6 — List the assumptions

Collect everything marked `[assumption]`, plus anything judged a real constraint in Step 3 but lacking measured evidence.
Give each one **the cheapest possible test**: one command, one lookup, one minimal experiment.

### Step 7 — Verify the ground (never skip)

The Step 6 list cannot just sit there. Sort the assumptions into two kinds:

| | Load-bearing | Peripheral |
|---|---|---|
| Role | Whether the solution stands at all | Only how *well* it works |
| Action | **Verify now, with the cheapest test, immediately** | Note it, watch while doing |
| If it fails | **Solution is void — back to Step 3, re-split the target** | Adjust details, keep the skeleton |
| Count | Usually one or two | Everything else |

**How to tell which is which**: ask "If this is false, does the solution still work?" No → load-bearing. Yes, just less well → peripheral.

**Why a failure sends you back to Step 3**: a falsified load-bearing assumption means you mis-classified an inherited habit as a real constraint during the split. The ground itself is wrong. You cannot keep building on it.

**Status constraint until verified**: before the load-bearing assumption has evidence, the entire analysis must be marked **pending**. It must not be treated as an established conclusion for anything consequential (writing it into a paper, committing to a plan, changing architecture, taking a large position).

### Closing condition

The analysis closes when either holds:

- Every load-bearing assumption has measured evidence
- Or the target has been re-split and the new ground is verified

**Peripheral assumptions may stay open.** Do not demand that every assumption be verified — that makes the analysis unclosable.

## Output format (two tiers)

**Light tier** — reached an actionable cause, never hit a wall:

```
Symptom: …
Chain: … → … → root cause
Solution: …
Walk-back: …
Load-bearing assumption: … (may be empty; if present, verify it now)
Verification result: …
Status: closed / pending
```

**Full tier** — hit a wall, ran decomposition and rebuild:

```
Symptom: …
Chain: … (mark which layer stalled, and the exact stalling sentence)
Target split:
  Real constraints: … (each with its violation consequence)
  Inherited habits (void): …
Rebuilt solution: … (state why existing solutions can't be reused)
Walk-back: account for every layer
Load-bearing (verify now): … → result: …
Peripheral (may stay open): … + tests
Status: closed / pending
```

## Anti-patterns (any one of these is a failure)

1. **Padding to five whys** — layers four and five are usually filler. If three rounds close it, use three.
2. **Treating a habit as a constraint** — "everyone uses X" is not a constraint. Anything with no stateable consequence goes in the habits pile.
3. **Decomposing then rebuilding everything** — that is over-engineering. Reuse by default; rebuild only on a falsified constraint.
4. **Skipping the walk-back** — without it you cannot prove the analysis reached the root.
5. **Asking why without evidence** — a chain of pure speculation is the same as not investigating. Mark `[assumption]`.
6. **Using it as a debugger** — a reproducible error belongs in a debugging workflow (e.g. `systematic-debugging`). Don't spin here.
7. **Listing assumptions then treating the output as a conclusion** — the judge is written on paper but never seated on the bench. Verify the load-bearing assumption now; if you can't, mark the output **pending**.
8. **Demanding every assumption be verified** — the analysis will never close. Verify the ground, leave the periphery open.

## Examples

See [examples.md](examples.md) — five fully worked runs:

| # | Domain | Tier |
|---|---|---|
| 1 | Project conventions re-explained every session | Light |
| 2 | A skill library nobody actually uses | Full |
| 3 | Stock investing: every trade made sense, the year lost money | Full |
| 4 | The same class of bug keeps coming back | Full |
| 5 | Experiment scores swing, unclear whether the method works | Full |

Example 4 opens by drawing the line against debugging skills: a single reproducible failure goes there, a recurring *class* of problem comes here.
