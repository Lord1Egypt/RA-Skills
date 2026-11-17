# Worked Examples

Five complete runs: one light tier, four full tier (skill library, stock investing, recurring bugs, ML experiments).

Every full-tier example carries two things worth the most:

- A **Note** after the walk-back — *which layer stays unexplained if you only make half the changes*
- A **Step 7** at the end — *which assumption is load-bearing, how to verify it right now, and where to retreat if it fails*

---

## Example 1 · Light tier (reached an actionable cause, never hit a wall)

### Symptom

Every new session, the project conventions have to be explained all over again. Miss one and the agent falls back to its own habits.

### Chain

```
Why explain them again every time?
→ Because the conventions only exist in past chat history, which a new session can't read
  (evidence: nothing is auto-loaded at session start)

Why do the conventions only exist in chat history?
→ Because there is no conventions file for agents at the project root
  (evidence: no AGENTS.md / CLAUDE.md or equivalent exists at the root)
```

**Stop here.** Layer two is already a concrete, actionable cause. Nothing hit "everyone does it this way," so no decomposition or rebuild is needed.

### Solution

Put a conventions file at the project root covering commit format, directory responsibilities, and hard prohibitions. Have it auto-load every session.

### Walk-back

```
Layer 2 "no conventions file"     → the solution creates exactly that file. Accounted for.
Layer 1 "conventions live in chat" → once written to a file, they no longer depend on history. Accounted for.
Symptom "re-explaining every time" → auto-loaded, so no re-explaining. Accounted for.
```

All three layers accounted for. Done.

### Step 7 — Verify the ground

**Load-bearing assumption**: the file really is auto-loaded, rather than needing to be mentioned by hand.
(If false: the agent still doesn't know the conventions, and the solution is worth nothing → load-bearing.)

**Verify now**: open a brand-new session, say nothing, and ask "what is this project's commit convention?"

**Result branches**:
- It answers with what the file says → ground holds
- It can't → "dropping a file there means it gets read" was an inherited habit, not a real constraint. Back to Step 3, re-split.

**Peripheral assumptions**: none.

**Status**: closed (the test is opening a new session and asking one question — doable on the spot).

---

## Example 2 · Full tier (hit a wall, ran decomposition and rebuild)

### Symptom

The skill library has grown to hundreds of entries, but the agent actually uses very few. Most of them sit there untouched.

### Chain

```
Why are most skills never used?
→ Because the agent doesn't know they exist at the moment it needs them
  (evidence: skills are laid out flat in one big directory, with no task-oriented entry point)

Why doesn't the agent know they exist?
→ Because it's entirely on the model to go browse the directory and read the docs by itself
  (evidence: nowhere in the production runtime path is a skill force-loaded or routed)

Why was it designed to rely on the model browsing on its own?
→ "A skill is a written guide; once the model reads it, it'll naturally use it" — that's always how it was done
  (evidence: across the whole skill-generation pipeline, the "create a skill" stage has zero executable code — it's all instructions written for the model)
```

**Layer three hits the wall.** The stalling sentence is *"a skill is a written guide; once the model reads it, it'll naturally use it."* That's the target.

### Target split

**Real constraints** (each with its violation consequence):

| Real constraint | What goes wrong if violated |
|---|---|
| The context window is finite and cannot hold hundreds of full skill texts | Load them all → crowd out the current task, answer quality drops |
| A model does not proactively read files that were never put in front of it | Rely on initiative → the skills might as well not exist, which is exactly today's symptom |
| Skill content goes stale as upstream code changes | No detection → the agent follows a three-year-old procedure and the run fails outright |

**Inherited habits** (void, re-choosable):

- "A skill = one Markdown guide" — nobody can say what breaks if this is false; pure inheritance
- "Accumulate volume first, worry about usage later" — no mechanism ever checks whether anything got used
- "Writing verification into the guide counts as verification" — the runtime never checks, and nobody stops the model from skipping it

### Rebuilt solution

The falsified constraint is *"once the model reads it, it'll naturally use it"* — layers two and three already proved it false. So patching at the guide level won't do; the structure has to change:

1. **Add a routing layer** (addresses constraints 1, 2): stop laying skills out flat; index them by task type. When a task arrives, the index selects a handful, and only the selected ones get loaded — instead of hoping the model browses on its own.
2. **Add staleness detection** (addresses constraint 3): each skill records the version and file list it was based on. A script compares that against current reality and reports `same / changed / missing`. Stale skills get flagged automatically instead of staying in rotation.
3. **Turn verification into a hard gate** (eliminates inherited habit #3): the verification script must return an explicit pass/fail, and downstream steps depend on that status. Fail means no publish.

### Walk-back

```
Layer 3 "relies on the model browsing on its own" → routing selects for it. Accounted for.
Layer 2 "agent doesn't know skills exist"          → the index pushes relevant ones in front of it. Accounted for.
Layer 1 "skills go unused"                         → pushed in + stale ones flagged; usage becomes measurable. Accounted for.
Symptom "hundreds accumulated, almost none used"   → accounted for, and now there's a metric to keep watching.
```

All four layers accounted for. **Note**: if you only did item 3 (the verification gate) and skipped routing, layer two would remain unaccounted for — however qualified a skill is, the agent still can't find it. That's what the walk-back is for.

### Step 7 — Verify the ground

**Load-bearing assumption**: `[assumption]` once routing is added, the number of skills actually invoked rises noticeably.
(If false: the agent still can't find skills and the entire rebuild was wasted → load-bearing.)

**Verify now**: index just *one* high-frequency task type, run ten real tasks, count how many skills got loaded.

**Result branches**:
- It rises → ground holds, then go do the two peripheral items
- It doesn't → the constraint "a model does not proactively read files never put in front of it" was mis-judged. Back to Step 3, re-split.

**Peripheral assumptions** (leave open, watch while doing):

| Assumption | Test |
|---|---|
| Staleness detection catches real problems rather than producing only false positives | Run the comparison script on the ten oldest skills, eyeball whether the results are accurate |
| The hard gate doesn't slow down normal publishing | Take one known-good skill through the full flow and record the time |

If either of these turns out false, you only cut that one piece — the routing layer still stands → peripheral.

**Status**: pending. Until the ten runs are done, "routing works" must not be written up as a conclusion.

---

## Example 3 · Full tier · Stock investing

### Symptom

Trading on tips and hot themes. Every single trade "made sense" on its own. The year ended at a loss.

### Chain

```
Why did every trade make sense yet the whole lost money?
→ Because those reasons were stories that hold up in hindsight, with no testable expectation set beforehand
  (evidence: not one entry in the trade log ever wrote down "expected to reach X, exiting if Y happens")

Why was there no prior expectation?
→ Because the basis for buying and selling was "someone said it's good" and "feels like it'll go up"
  (evidence: the recorded reasons are news, hot themes, group chat opinions)

Why use other people's judgment as the basis?
→ "Everyone watches these same indicators and this same news — following along can't be wrong." That's always how it was done.
```

**Layer three hits the wall.** The target is *"following the information everyone watches can't be wrong."*

### Target split

**Real constraints**:

| Real constraint | What goes wrong if violated |
|---|---|
| Return = price change × position size − costs (fees, tax, slippage) | Ignore costs → the more you churn, the more gets ground away |
| Once public information is widely known, it is already reflected in the price | Believe you have an edge → you're actually taking the other side of the last trade |
| Losing 50% of capital requires a 100% gain to break even | One oversized mistake can put you out permanently |
| Time and attention are finite; you cannot track everything | You can only passively accept other people's conclusions |

**Inherited habits** (void, re-choosable):

- "Trade the hot themes and the news" — public news is already priced in; following it carries no edge
- "Average down when it drops to lower your cost basis" — your cost basis is a mental account; the market has never heard of it
- "Stopping out is admitting you were wrong; hold and it'll come back"

### Rebuilt solution

The falsified constraint is *"following the information everyone watches can't be wrong"* — layers two and three already showed public information is priced in, so following carries no edge. Therefore "find better news sources" cannot fix this; the structure has to change:

1. **No order without writing it down first**: why buy now, what price you expect, what signal means you were wrong and you exit, and the position size. Can't write it → don't place the order. (Addresses constraints 1, 2)
2. **Hard cap per position**: no single loss may damage more than a fixed fraction of capital. (Addresses constraint 3)
3. **Concede there is no information edge**: the bulk of capital goes low-cost, low-turnover, long-hold. Active trading gets one small slice, treated as an experiment. (Addresses constraints 2, 4)
4. **Reconcile monthly**: compare actual returns against "blindly holding the same index and doing nothing." Underperform it, and your active trading created no value.

### Walk-back

```
Layer 3 "watching what everyone watches"  → concede no edge, default to passive. Accounted for.
Layer 2 "using other people's judgment"   → you must write your own testable expectation first. Accounted for.
Layer 1 "only hindsight stories"          → with expectations set, outcomes become judgeable, not narrated. Accounted for.
Symptom "the year lost money"             → with a reconciliation baseline, value creation stays measurable. Accounted for.
```

**Note**: do only item 1 (write expectations) without item 4 (reconcile), and the symptom layer stays unaccounted for — you still won't know whether the whole is winning or losing. Each trade just looks more disciplined.

### Step 7 — Verify the ground

**Load-bearing assumption**: `[assumption]` your active trading underperforms blindly holding the same index over the long run.
(If false: if you genuinely do outperform consistently, then "concede there is no information edge" was mis-judged, and the whole "passive-first" plan collapses → load-bearing.)

**Verify now**: take last year's full trade log and compare it against the same-period index return. **Uses data you already have — doable right now, no waiting.**

**Result branches**:
- Underperforms → ground holds, execute the plan
- Outperforms → back to Step 3, re-split. "Public information is already priced in" has been falsified by your own records. Now go find out what you actually won on, and whether that can persist.

**Peripheral assumptions**:

| Assumption | Test |
|---|---|
| How much do costs actually eat | Sum last year's fees + slippage, divide by capital |

The cost item only affects *how low turnover should go*; it doesn't decide whether the plan stands → peripheral.

**Status**: pending. This load-bearing test is **the reconciliation you must run before taking any large position** — and it doubles as the baseline for every later judgment.

---

## Example 4 · Full tier · Debugging code (the recurring class)

> **Boundary**: if it's "this function is throwing right now" — a single reproducible failure — go to a debugging workflow (e.g. `systematic-debugging`).
> This example covers **the same class of bug returning after being fixed** — a structural problem, which is what this skill is for.

### Symptom

The same class of bug keeps recurring: unhandled nulls and boundaries. Fix one, and a while later another pops up somewhere else.

### Chain

```
Why does it come back after being fixed?
→ Because each time only the offending line was changed; nobody checked where else the same pattern appears
  (evidence: every fix record is a single-point change, not one of them ran a global search)

Why not do a global sweep?
→ Because there's no means of automatically detecting the same pattern elsewhere
  (evidence: the project's static checks don't cover this class of problem)

Why wasn't such a check added?
→ "The tests are enough; if something breaks we'll fix it then." That's always how it was done.
```

**Layer three hits the wall.** The target is *"the tests are enough; fix it when it breaks."*

### Target split

**Real constraints**:

| Real constraint | What goes wrong if violated |
|---|---|
| People miss things; repetitive checking must be handed to a machine | Rely on diligence → the same class of bug will definitely return |
| Without an automated check, every change can reintroduce the same problem | One fix covers one occurrence only |
| A fix must be locked in by a test | Regressions elsewhere go unnoticed |

**Inherited habits** (void, re-choosable):

- "Bugs are one-offs; fix it and move on" — beneath the one-off appearance, the same pattern is scattered across many places
- "High coverage means good quality" — coverage doesn't distinguish "tested" from "tested at the boundary"
- "Fixing on demand is cheaper than preventing" — the cumulative cost of repeatedly fixing the same class far exceeds adding one rule

### Rebuilt solution

The falsified constraint is *"the tests are enough"* — the recurrence of the same bug class is itself the proof that it isn't.

1. **Reuse existing tooling first**: can the language's built-in linter or type checker express this class of constraint? If yes, just turn it on — don't build anything. (The reuse-by-default brake)
2. Only if existing rules can't express it, write one custom static check and wire it into pre-commit
3. **Every bug fix starts with a global sweep** for the same pattern, cleaned up in one pass, then commit
4. **Every fixed bug gets a test that reproduces it**: make the test fail first, then make it pass

### Walk-back

```
Layer 3 "rely on tests to catch it"      → static rule + reproduction test, double coverage. Accounted for.
Layer 2 "no means of detecting it"       → rule wired into pre-commit. Accounted for.
Layer 1 "fix one line, no sweep"         → every fix requires a global sweep. Accounted for.
Symptom "same class keeps recurring"     → new ones blocked, existing ones cleared in one pass. Accounted for.
```

**Note**: do only item 4 (reproduction tests) without items 1 and 2, and layer two stays unaccounted for — a test can only guarantee "this one spot won't regress." It says nothing about the same pattern elsewhere.

### Step 7 — Verify the ground

**Load-bearing assumption**: `[assumption]` this class accounts for the bulk of all bugs.
(If false: if it's only a scattered handful, adding a project-wide static rule for it is over-engineering and shouldn't be done at all → load-bearing.)

**Verify now**: take the last 20 fix records and classify them by type. **Just read the records — no code required.**

**Result branches**:
- High share → ground holds, go add the rule
- Very low share → back to Step 4. The constraint "repetitive checking must be handed to a machine" still holds, but the target was picked wrong — swap in whatever class actually dominates

**Peripheral assumptions**:

| Assumption | Test |
|---|---|
| The static rule's false-positive rate is acceptable | Run it on changed files only, see how many findings are real problems |

If false positives are high, narrow the rule or downgrade it to a hint — no need to overturn the plan → peripheral.

**Status**: pending. Counting 20 records closes it. The cost is trivial; there's no reason to defer.

---

## Example 5 · Full tier · ML experiment design

### Symptom

Several versions of the experiment have been run. Scores swing up and down. Nobody can say whether the method actually works.

### Chain

```
Why can't anyone say whether it works?
→ Because the setup differed between runs, so the scores aren't comparable at all
  (evidence: different rounds used different data splits, different component wiring, different baseline sources)

Why did the setup differ?
→ Because there's no fixed experimental protocol; each run was wired according to whatever seemed right at the time
  (evidence: no unified config entry point — parameters are scattered across the codebase)

Why was no protocol defined?
→ "Get results first, add the protocol later." That's always how it was done.
```

**Layer three hits the wall.** The target is *"get results first, add the protocol later."*

### Target split

**Real constraints**:

| Real constraint | What goes wrong if violated |
|---|---|
| Scores are comparable only when the setup is identical | Swings come from setup differences, not method differences → wrong conclusions |
| Baselines must be produced by the same pipeline; numbers quoted from other papers don't count | Environmental differences get credited as method advantage |
| Verifying a method must run that method's own real code path — no hand-written stand-ins for its core components | The score doesn't represent the method → the conclusion is invalid |
| An experiment must be re-runnable as-is by others, and by you three months from now | Not reproducible, which means it wasn't done |

**Inherited habits** (void, re-choosable):

- "Get results first, add the protocol later" — it never gets added, and every conclusion already produced is contaminated
- "Run a simplified version to sanity-check the direction," then draw conclusions from that number — simplified wiring doesn't represent the method's intent
- "Use whichever wiring scores highest" — picking wiring by score is tuning on the test set
- "A high score means it works" — without comparison to a naive baseline, the gain may come entirely from the setup

### Rebuilt solution

The falsified constraint is *"get results first, add the protocol later"* — the incomparability of the scores has already voided every historical conclusion.

1. **Protocol first**: data splits, metrics, number of random seeds, and the baseline list all go into one unified config. Every experiment starts from it.
2. **A naive baseline is mandatory**: run the dumbest possible approach through the same pipeline. The method's incremental value = the gap against it.
3. **Method components must be wired with their real implementations** — no hand-written stand-ins. When a simplified run genuinely is needed, the result must be explicitly labeled `diagnostic proxy — does not represent the method's ceiling`.
4. **Record three things per run**: config fingerprint, code version, data checksum. Missing any one → the result is not trustworthy.
5. **Reuse an existing evaluation framework by default**; write your own only if it cannot express this protocol.

### Walk-back

```
Layer 3 "run first, protocol later"    → protocol comes first. Accounted for.
Layer 2 "setup decided ad hoc"         → unified config entry point. Accounted for.
Layer 1 "scores not comparable"        → same protocol, same pipeline. Accounted for.
Symptom "can't say whether it works"   → naive-baseline comparison + reproducible records answer it definitively. Accounted for.
```

**Note**: do only item 1 (unified config) without item 2 (naive baseline), and the symptom layer stays unaccounted for — scores become reproducible, but you still don't know where the method beats the dumb approach. Quite possibly it doesn't.

### Step 7 — Verify the ground

This example has **two load-bearing assumptions**. Both must be verified, and the order cannot be swapped.

**Ground ① (highest priority)**: what the naive baseline scores — **currently completely unknown**.
(If unavailable: the method's incremental value = the gap against the naive baseline. Without the baseline number the gap can't be computed, so the sentence "the method works" cannot even be judged true or false → load-bearing.)
**Verify now**: run the dumbest approach through the same protocol first. Everything else queues behind it.

**Ground ②**: `[assumption]` historical score swings came mainly from setup differences, not method differences.
(If false: if the swings genuinely came from the method itself, the historical conclusions are salvageable and don't all need re-running → load-bearing, because it decides whether to start over.)
**Verify now**: pick two historical conclusions, re-run each under the same protocol, and see whether the gap disappears.

**Result branches**:
- Gap disappears → confirms it was setup differences. All historical conclusions are void; redo under the new protocol.
- Gap persists → "scores are comparable only when the setup is identical" was misapplied. Back to Step 3, re-split.

**Peripheral assumptions**: none. Every unverified item here directly decides whether the conclusion is true or false; nothing can be left open.

**Status**: pending. **Until Ground ① produces a number, any claim of "my method works" is a guess** — not to be written into a paper, not to be used for decisions.

---

## The two tiers at a glance

| | Light tier | Full tier |
|---|---|---|
| Drilling hit "everyone does it this way" | No | Yes |
| Split into constraints / habits | Skipped | Required |
| May rebuild the solution | No | Possibly — but reuse is still the default |
| Walk-back | Required | Required |
| Ground verification | Required | Required |
| Typical length | A dozen lines | About a page |
| Examples here | #1 | #2, #3, #4, #5 |

**Neither tier may skip the walk-back** — it's the only proof the analysis reached the root.

## About the `status` field

Of the five examples, only #1 closes on the spot (its test is opening a new session and asking one question). The other four remain **pending** — and that is not unfinished work, it is honest labeling.

Until a load-bearing assumption has measured evidence, the output stays marked pending and must not be treated as an established conclusion for anything consequential. Example 5 is the clearest case: the naive baseline hasn't been run, so "the method works" cannot currently be called true *or* false.

Look at what the four pending ground tests actually cost: read a trade log, count 20 fix records, run ten tasks, run one dumb baseline. **Not one of them requires building a new system.** Ground verification should always be cheap — if it's expensive, you probably picked the wrong assumption.

## The same trap in every example

Each full-tier example's **Note** points at the same failure: **make only half the changes and some layer stays unaccounted for.**

| Example | Half a fix leaves this unsolved |
|---|---|
| Skill library unused | Verification gate but no routing → "the agent can't find the skill" |
| Stock investing | Prior expectations but no reconciliation → "is the whole winning or losing" |
| Recurring bugs | Reproduction tests but no static check → "the same pattern elsewhere" |
| ML experiments | Unified config but no naive baseline → "where does it beat the dumb approach" |

This is exactly why the walk-back cannot be skipped: **it exists to catch "looks like a rebuild, was actually another symptom patch."**
