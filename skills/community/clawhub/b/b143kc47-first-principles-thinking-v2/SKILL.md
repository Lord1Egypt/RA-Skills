---
name: first-principles-thinking
description: "Reason from fundamentals with in-session claim ledgers, mechanism maps, assumption checks, Fermi estimates, evidence grounding, verification questions, red-team critique, and structured brainstorming. Use for architecture, system design, technology selection, debugging, performance, migrations, strategy, product, research, scientific or business decisions, or prompts like first principles, challenge assumptions, from scratch, brainstorm, or think from fundamentals."
---

# First Principles Thinking

Break problems down to fundamental truths, then rebuild solutions from the
ground up. Do not import conclusions from other contexts; derive them from
what is actually, verifiably true in this one.

> "To the first basis of the thing -- the first from which a thing is known."
> -- Aristotle, *Metaphysics* V.1

## Implementation Boundary

This skill is a reasoning guide only. It ships Markdown instructions and
reference examples; it has no helper program, installer, credential requirement,
network endpoint, or automatic state mechanism. Keep claim ledgers in the active
conversation or in user-provided pasted context. Use external tools only when
the runtime already provides them and the user's task itself requires evidence,
calculation, or source inspection. Do not run bundled code for this skill.

<HARD-GATE>
Do NOT propose a solution, recommend a technology, or start writing code until:

1. The problem has been restated in terms of outcomes (not solutions). If the
   user already provided enough context, proceed without asking for confirmation;
   otherwise ask one targeted clarifying question or state the working assumption.
2. The primary task mode has been classified (decision / diagnosis / planning /
   critique / explanation / synthesis / exploration).
3. The Claim Ledger has been populated: verified facts, reported claims,
   assumptions, constraints, and unknowns are each explicitly listed.
4. Ground truths have been explicitly separated from inherited conventions.
5. The core mechanism has been mapped: variables, causal links, constraints,
   feedback loops, and bottlenecks.
6. At least one failure-oriented check has been run: inversion, falsifier,
   backward check, or red-team objection.

The cost of skipping this gate is solving the wrong problem efficiently -- the
most expensive failure mode in engineering, strategy, and research.
</HARD-GATE>

---

## Activation

### Auto-Trigger Signals

Activate when the request shows one or more complexity markers:

- **Architecture / design:** "design", "architect", "how should I structure", "what pattern", "what's the right abstraction"
- **Technology selection:** "should I use X or Y", "what database / queue / framework", "which library"
- **Hard debugging:** "intermittent", "can't figure out why", "keeps failing", "root cause", "happens sometimes"
- **Performance / scaling:** "slow", "bottleneck", "optimize", "scale to N", "doesn't scale"
- **Integration / migration:** "connect X to Y", "migrate from", "replace X with", "move off"
- **Strategy / product / research:** "go-to-market", "positioning", "experiment", "hypothesis", "what should we test", "scientific", "business model", "growth", "pricing"
- **Brainstorming / invention:** "brainstorm", "generate options", "non-obvious ideas", "new approach", "creative", "ideate"
- **Convention language:** "best practice", "industry standard", "everyone uses", "we've always"
- **Explicit invocation:** "first principles", "FP mode", "from scratch", "challenge my assumptions", "think from fundamentals"

### Skip Signals

Stay dormant when the request is small, scoped, and obviously mechanical:

- Trivial edits: "rename X to Y", "fix this typo", "add a log line"
- Boilerplate: "scaffold a component", "set up the project", "add a route"
- Direct implementation of an already-decided design: "write the function that does X"
- User override: "just do it", "skip the analysis", "no thinking, just code"

When in doubt between activating and skipping, do not add process overhead. Either
run Quick depth silently and produce a compact result, or ask one sentence:
"This looks like a design decision -- should I challenge the assumptions first or go straight to implementation?"

---

## Depth Levels

State the detected depth at the start; the user can override.

| Level       | When                                             | What Runs |
|-------------|--------------------------------------------------|-----------|
| Quick       | Medium complexity, manual `/fp`, reversible choice | Intake + compact ledger + mechanism sketch + one verification check |
| Standard    | Architecture, tech selection, design, strategy, product decisions | Intake + Socratic probes + decomposition + mechanism map + reconstruction + verification |
| Deep        | System design, hard debugging, high-stakes decisions, `/fp deep` | All phases including inversion, 2-3 reconstruction paths, sensitivity, self-consistency, verification |
| Exploration | Explicit brainstorming, invention, research framing, `/fp brainstorm` | Divergent search with ToT / GoT / morphological matrix / contradiction analysis, then convergence and tests |

---

## Core Workflow

The seven phases below are the operational form of this compact seven-step
loop. Every run, regardless of depth or mode, should be traceable to it:

1. Rewrite the request as one clear outcome, decision, question, diagnosis
   target, or claim to evaluate (Phase 1).
2. Classify the task into one primary **mode** and at most one secondary mode
   (Phase 1; see *Task Modes* below).
3. Build the **Claim Ledger** -- verified facts, reported claims,
   assumptions, constraints, unknowns -- before concluding (Phase 3).
4. Choose the reasoning pattern best fit for the task: deduction, induction,
   abduction, or first-principles decomposition. First-principles is the
   default; the others are invoked inside it where appropriate (Phases 2-5).
5. Run the mode-specific playbook (see *Mode Playbooks* near the end).
6. Pressure-test the draft answer with the strongest alternative explanation,
   objection, or counterexample (Phase 6).
7. End with a conclusion, recommendation, or next step, plus the top
   assumptions the user should confirm, reject, or supply next (Phase 7).

## Task Modes

Every non-trivial problem resolves into one primary mode. Detect it in
Phase 1, state it aloud, and let it shape emphasis across the phases. A
problem may carry a secondary mode (e.g. diagnosis-then-decision); name
that too, but keep one as primary.

| Mode        | Use when the user wants to...                                         |
|-------------|-----------------------------------------------------------------------|
| decision    | choose among options (tech, design, vendor, build-vs-buy, staging)    |
| diagnosis   | explain a symptom, failure, regression, or anomaly                    |
| planning    | get from a current state to a desired state on a sequence of steps    |
| critique    | stress-test a claim, proposal, argument, belief, or narrative         |
| explanation | understand a mechanism, model, or system without deciding anything    |
| synthesis   | rebuild a messy or multi-frame problem into a single coherent view    |
| exploration | generate, expand, combine, and filter non-obvious options or hypotheses |

Default assignment heuristics:
- "should I use X or Y?" / "which stack / pattern / vendor?" -> decision
- "why is X slow / broken / inconsistent?" / "root cause" -> diagnosis
- "how do we get from A to B by Q3?" / "migration plan" -> planning
- "is this design / argument / approach sound?" -> critique
- "how does X work?" / "what is happening here?" -> explanation
- "we have five inputs and need one view" -> synthesis
- "brainstorm / generate options / non-obvious ideas / what else could work?" -> exploration

Modes are not pre-built answers; they tell you which phases tighten and which
relax. The *Mode Playbooks* section at the bottom spells out each route.



## Reasoning Budget and Tool Router

Use the smallest reasoning stack that can safely answer the problem. More
steps are not automatically better; activate heavier tools only when the
problem is ambiguous, irreversible, high-stakes, data-dependent, or explicitly
brainstorming-oriented.

| Signal | Add this tool |
|--------|---------------|
| Hidden assumptions likely | Assumption Ledger with fragility, failure mode, and fastest test |
| Mechanism or causality matters | Causal / mechanism map: variables, links, confounders, feedback loops |
| Many moving parts | Least-to-most decomposition into smallest solvable subproblems |
| Numbers, capacity, cost, scale, or physical constraints matter | Fermi estimate, dimensional check, low/base/high range |
| Recent, factual, niche, legal, scientific, product, price, or data claims matter | Evidence grounding through approved search, user-provided sources, calculations, or citations |
| Open-ended ideation | Tree of Thoughts, Graph of Thoughts, morphological matrix, contradiction analysis |
| Competing explanations | Self-consistency across 2-3 independent paths and a discriminating test |
| High-stakes or likely hallucination risk | Chain-of-verification, backward check, red team, sensitivity analysis |
| Hard equations, schedules, constraints, optimization, or Boolean logic | Formalize variables and use approved calculation, spreadsheet, solver, or symbolic-math tools when available |

When tools are needed, choose only runtime-approved tools and state them in a short **Tool Plan** before running the analysis. For Quick depth, the Tool Plan can be one line.

## Accuracy Upgrades

Use these additions whenever Standard, Deep, or evidence-dependent work is
requested. See `references/advanced-reasoning-tools.md` for detailed prompts.

1. **Mechanism Map before recommendation.** Identify actors, incentives,
   resources, variables, causal links, confounders, mediators, bottlenecks,
   feedback loops, and boundary conditions.
2. **Assumption Ledger v2.** For every assumption, record category, evidence,
   confidence, fragility, failure mode, and fastest test. Unknown assumptions
   that could flip the conclusion must be elevated to User Checkpoints.
3. **Least-to-most decomposition.** Convert the problem into 3-7 smallest
   solvable subproblems and solve them before synthesizing.
4. **Quantitative sanity check.** If magnitudes matter, write the governing
   equation or proxy model, estimate each variable, check units, give a
   low/base/high range, and name the dominant variable.
5. **Evidence grounding.** Treat memory as insufficient for current or niche
   facts. When approved sources, user-provided files, or retrieval tools are available and relevant,
   retrieve first, then separate source-supported facts from inference.
6. **Verification chain.** Draft, generate verification questions, answer the
   questions independently, revise, and state the falsifier.
7. **Sensitivity and calibration.** Name the 1-3 assumptions or variables most
   likely to change the answer; state confidence as low / medium / high with
   the reason.

## Brainstorming Upgrades

Use these additions when the mode is exploration, synthesis, early strategy,
product ideation, research design, invention, or the user asks for options.
Diverge first, converge second.

1. **Tree of Thoughts.** Generate 3-5 genuinely different paths, score them,
   expand the top 2, and keep the runner-up as a fallback.
2. **Graph of Thoughts.** Model ideas as nodes and edges: assumptions,
   mechanisms, constraints, analogies, risks, resources, and combinations.
   Merge compatible nodes, remove dominated nodes, and synthesize non-obvious
   options from high-value intersections.
3. **Morphological matrix.** Break the solution space into dimensions and
   variants, combine them systematically, then filter impossible or dominated
   combinations.
4. **Contradiction analysis.** Convert trade-offs into contradictions: "more X
   without more Y". Generate options by separation in time, separation in
   space, modularization, inversion, automation, or self-service.
5. **Multi-perspective debate.** Simulate at least three roles: first-principles
   mechanist, operator / implementation realist, skeptic / red team, and
   creative strategist. Each must critique one other view before synthesis.
6. **Convergence rule.** Final brainstorm output must include: best practical
   option, most novel option, fastest experiment, biggest risk, and what would
   make each option wrong.

## The Phases

Phases run in order. Earlier phases may be abbreviated at Quick depth, but
never skipped entirely.

### Phase 1 -- Intake (always)

Restate the problem in outcome terms, not solution terms. Classify the task
into one primary mode (and at most one secondary). If enough context exists,
proceed with explicit working assumptions instead of asking for confirmation.

> "I read the outcome as: **[outcome in one sentence]**.
> Current approach or framing: **[current solution idea, if any]**.
> Mode: **[mode]** (secondary: **[mode | none]**).
> Depth: **[Quick / Standard / Deep / Exploration]**.
> Working assumption if not corrected: **[...]**."

Rules:
- If you cannot state the problem as an outcome independent of the current
  proposed solution, ask one targeted clarifying question or state the safest
  working assumption and continue with caveats.
- If you cannot pick a single primary mode, the problem is probably two
  stacked problems. Name both and resolve the first one first.
- Treat the user's framing as a *reported claim*, not as ground truth, until
  it either passes the Phase 3 Ground-Truth Test or is explicitly stipulated.

### Phase 2 -- Socratic Questioning (always)

Probe the problem with the question types below. Pick the most relevant 3-5
for the problem at hand; asking all of them robotically is worse than asking
three well-chosen ones. For the full catalog including probes for each type,
see `references/techniques.md`.

**Clarification** -- "What exactly do you mean by X?" / "Concrete example?" / "What does success look like, measurably?"

**Assumption Probing** -- "Why does it have to work that way?" / "Who decided this, and what was their reasoning?" / "Is this a hard requirement or inherited from a previous design?"

**Evidence** -- "What data shows this is the bottleneck?" / "Have you measured it, or is it a guess?" / "How do you know users actually need this?"

**Alternative Viewpoints** -- "How would a team with opposite constraints solve this?" / "What would you build starting from zero today?" / "What would a critic of this approach say?"

**Implications** -- "What are the second-order effects?" / "What breaks if this assumption is wrong?" / "What's the cost of reversing this decision later?"

**Meta** -- "Are we solving the right problem?" / "Is this the simplest form of the problem?" / "What happens if we just... don't do this?"

**Red-flag phrases** that almost always hide an assumption. When you hear
these, drop into assumption-probing mode:

- "We've always done it this way"
- "Industry standard / best practice says"
- "Everyone uses X for this"
- "That's too simple to work"
- "We can't change that" (without verifying why not)
- "The client / PM said so" (without tracing the underlying need)

**Cadence:**
- Quick: ask 2-3 questions in one message; move on when answered.
- Standard: 1-2 questions per turn; adapt follow-ups to the answers.
- Deep: 1 question per turn; follow threads wherever the reasoning leads.

### Phase 3 -- Decomposition & Claim Ledger (Standard + Deep)

Break the problem into atomic components and file every component into the
**Claim Ledger**. The ledger is the canonical record of what you know, what
you were told, what you are guessing, what binds you, and what is missing.
Nothing downstream -- inversion, reconstruction, verification -- may cite a
fact that is not in the ledger.

Before proposing paths, build a compact **Mechanism Map**:

- Actors / systems / variables involved
- Inputs, outputs, stocks, flows, and bottlenecks
- Causal links, mediators, confounders, and feedback loops
- Boundary conditions and conservation-like constraints
- For business/product work: incentives, adoption friction, switching costs,
  distribution channels, and trust constraints

Then run **Least-to-Most Decomposition**: write 3-7 smallest solvable
subproblems. Each subproblem must yield one intermediate variable, constraint,
mechanism claim, risk, or testable unknown before synthesis.

**Prior-claim intake (before filling the ledger).** This variant keeps prior claims in the conversation. If the user pastes a previous Claim Ledger, provides notes, or supplies connector/source content, import it as candidate context and log the outcome.

Log one of:

- *"prior ledger provided: N candidate claims imported as [CLAIM]"*, or
- *"no prior ledger provided; proceeding with an in-session ledger only"*.

**Imported claims re-enter as `[CLAIM]`, never as `[TRUTH]`.** They must pass
the Ground-Truth Test below to be promoted back to `[TRUTH]`. This is the
primary mitigation for anchoring bias; do not skip it even when the imported
claim was previously marked verified. See `references/session-ledger-template.md`
for the in-session ledger format.

**The five ledger lanes:**

| Lane              | Definition                                                        | Tag           |
|-------------------|-------------------------------------------------------------------|---------------|
| Verified facts    | Provable in this context: physics, math, measurement, executable check, stipulation. Passes the Ground-Truth Test. | `[TRUTH]`     |
| Reported claims   | Statements from the user, a source, or prior art, not yet verified. Treated as conditional until promoted or rejected. | `[CLAIM]`     |
| Assumptions       | Inherited convention, habit, team preference, or unverified belief being used as if it were a truth. | `[ASSUMPTION]`|
| Constraints       | Hard limits the solution must respect: regulatory, contractual, budget, headcount, latency / throughput SLOs, compatibility. | `[CONSTRAINT]`|
| Unknowns          | A fact we'd need but don't yet have. Blocks trust in the decomposition until resolved or bounded. | `[UNKNOWN]`   |

**Ground-Truth Test** -- before tagging something `[TRUTH]`, ask:

1. Can it be decomposed further into something more fundamental?
2. Is it provably true in this context, not just commonly believed?
3. Would violating it *definitely* cause failure (not just inconvenience)?

If the answer to any of the three is "no" or "not sure", route it to
`[CLAIM]`, `[ASSUMPTION]`, `[CONSTRAINT]`, or `[UNKNOWN]` instead. User-
supplied statements start life as `[CLAIM]`; they are promoted to `[TRUTH]`
only after the test passes, or downgraded to `[ASSUMPTION]` if the belief is
being used without verification.

**Assumption Ledger v2** -- classify each `[ASSUMPTION]` and record its risk profile:

| Category    | Key Question |
|-------------|--------------|
| Technical   | "Must this technology / pattern / protocol be used?" |
| Business    | "Is this requirement actually fixed, or negotiable?" |
| Resource    | "Are these constraints real (budget, headcount) or perceived?" |
| Historical  | "Why was this chosen originally? Do those conditions still hold?" |
| Behavioral  | "Are we assuming users, teams, markets, or adversaries will behave a certain way?" |
| Data / Evidence | "Are we assuming a measurement, source, benchmark, or sample is representative?" |

For each assumption, capture:

| Field | Required content |
|-------|------------------|
| Evidence | What supports it now, if anything |
| Confidence | low / medium / high |
| Fragility | what would make it break |
| Failure mode | how the final answer fails if it is false |
| Fastest test | cheapest observation, experiment, search, or calculation that would check it |

**Constraint discipline:** a `[CONSTRAINT]` must name (a) its source
(regulator, contract, SLO doc, hardware limit), (b) its numeric threshold
where applicable, and (c) the cost of violating it. Unsourced "constraints"
are `[ASSUMPTION]`s in disguise.

**Unknowns discipline:** every `[UNKNOWN]` must state (a) what it is, (b)
how it would be resolved (measurement, document, stakeholder), and (c)
whether the downstream recommendation changes if the resolution lands at
either end of the plausible range. If a recommendation is stable across the
range, the unknown is not blocking.

**Recursion rule:** if a component reveals its own hidden assumptions (e.g.
"we need a message queue" contains "we need async processing"), flag it:

> "This sub-problem has its own assumptions. Going one level deeper."

Run Phases 2-3 on the sub-problem, then resume. Maximum recursion depth: 2
levels. If you hit the limit, list the unexplored sub-problem as an
`[UNKNOWN]` in the ledger.

### Phase 4 -- Inversion (Deep; optional at Standard)

Invert the question. Instead of "how do I make this succeed?", ask:

> "What would guarantee this fails? What must I avoid at all costs?"

List 3-5 failure modes. For each, identify which ground truth or design choice
would prevent it. Failure modes the current design does not prevent are risks
that must be addressed or accepted explicitly.

Inversion is cheap and catches assumption gaps the forward analysis misses.
Munger's rule: "Invert, always invert." See `references/techniques.md` for
the inversion playbook.

### Phase 5 -- Reconstruction (Standard + Deep)

Build 2-3 candidate solution paths using *only* the verified ground truths.
For exploration mode, build 3-5 paths first, then converge. For each path,
state:

- Which `[TRUTH]`s and `[CONSTRAINT]`s it is built on
- Every design choice made (places it could have gone differently)
- The core mechanism by which it works
- Trade-offs against the other paths (operational cost, reversibility, complexity, novelty)
- Remaining `[UNKNOWN]`s and how they'd be resolved
- The cheapest falsifying test or experiment

If magnitudes matter, add a **Fermi / dimensional sanity check** before ranking:
write the proxy equation, estimate low/base/high values, check units, and name
the dominant variable. Evaluate each path on its own merits. The conventional
path may win -- but only because the analysis led there, not because it was
the default.

**Chesterton's Fence check:** before recommending the removal of any existing
structure (code, system, process), ask why it was built. If you cannot state
the original reason and whether the conditions still hold, you do not yet
have the right to remove it.

### Phase 6 -- Verification (Deep; optional at Standard)

Before handing over the recommendation, stress-test it:

1. **Strongest alternative view:** state the best counter-explanation,
   competing option, or objection the recommendation must survive.
   Attribute it to the smartest possible critic, not a strawman. If no
   serious alternative exists, the problem was probably not worth
   first-principles effort.
2. **Self-consistency:** create 2-3 independent reasoning paths when the
   answer is uncertain. Compare conclusions, assumptions, and weak links.
3. **Chain-of-verification:** draft verification questions, answer them
   independently, then revise the answer. At minimum ask: "which claim is most
   likely false?", "which fact needs external evidence?", and "which
   assumption would flip the conclusion?"
4. **Backward check:** assume the conclusion is true; list what else must be
   true. Check those requirements against the ledger.
5. **Falsifiability:** "What observation would prove this recommendation
   wrong?" If nothing would, the recommendation is not rigorous enough.
6. **5 Whys on the chosen path:** trace the recommendation back through five
   layers of "why" to confirm it bottoms out in a `[TRUTH]` or
   `[CONSTRAINT]`, not another `[ASSUMPTION]`.
7. **Sensitivity:** identify the 1-3 variables or assumptions most likely to
   change the recommendation. If a +/-20% change flips the answer, lower
   confidence and make the test explicit.
8. **Reversibility:** how expensive is it to back out of this decision later?
   Cheap-to-reverse decisions can be made with less certainty.
9. **Confidence calibration:** state residual confidence as low / medium /
   high, grounded in which `[UNKNOWN]`s remain open and how sensitive the
   recommendation is to them.

### Phase 7 -- Artifact (always)

Emit a structured "First Principles Analysis" block. This artifact stays in
context and guides all subsequent work in the session.

**Quick artifact:**

```markdown
## First Principles Analysis

**Problem (outcome):** [one sentence]
**Mode:** [decision | diagnosis | planning | critique | explanation | synthesis]
**Depth:** Quick

### Tool Plan
[1 line: mechanism map / Fermi check / verification / brainstorm as needed]

### Claim Ledger (compact)
- [TRUTH] [...]
- [CLAIM] [user-supplied, not yet verified]
- [ASSUMPTION] [inherited / conventional + fragility]
- [CONSTRAINT] [hard limit + source]
- [UNKNOWN] [fact needed + how to get it]

### Mechanism Sketch
[Variables -> causal link -> expected outcome; name bottleneck or feedback loop]

### Assumptions Challenged
| Assumption | Challenge | Failure if false | Fastest test | Verdict |
|------------|-----------|------------------|--------------|---------|
| [...]      | [...]     | [...]            | [...]        | Keep / Modify / Discard / Investigate |

### Recommended Approach
[Solution with brief reasoning grounded in the ledger above.]

### Verification Check
- Falsifier / backward check / sensitivity note: [...]
```

**Standard / Deep artifact:**

```markdown
## First Principles Analysis

**Problem (outcome):** [one sentence]
**Mode:** [primary] (secondary: [mode | none])
**Depth:** Standard | Deep

### Tool Plan
[Which tools were activated: mechanism map, evidence grounding, ToT/GoT, Fermi, verification, solver]

### Claim Ledger
**Verified facts**
- [TRUTH] [fact + why irreducible]

**Reported claims (user or source, not yet verified)**
- [CLAIM] [statement + who/source asserted it + how it would be verified]

**Assumptions**
- [ASSUMPTION] [convention / habit + category + confidence + fragility]

**Constraints**
- [CONSTRAINT] [limit + source + numeric threshold + cost of violation]

**Unknowns**
- [UNKNOWN] [fact needed + how to resolve + is the recommendation sensitive to it?]

### Mechanism Map
- Variables / actors:
- Causal links:
- Bottlenecks:
- Feedback loops:
- Boundary conditions:
- Confounders / hidden variables:

### Decomposition
| Subproblem | Intermediate output | Status |
|------------|---------------------|--------|
| [...]      | [...]               | solved / bounded / unknown |

### Assumptions Challenged
| Assumption | Category | Evidence | Confidence | Fragility | Failure if false | Fastest test | Verdict |
|------------|----------|----------|------------|-----------|------------------|--------------|---------|
| [...]      | Tech / Biz / Resource / Historical / Behavioral / Data | [...] | low / medium / high | [...] | [...] | [...] | Keep / Modify / Discard / Investigate |

### Inversion (what would guarantee failure)
- [failure mode] -> prevented by [truth / design choice] | NOT prevented -> risk to accept

### Reconstruction
**Path A** -- [name]
- Built on: [TRUTHs / CONSTRAINTs]
- Design choices: [...]
- Trade-offs: [...]

**Path B** -- [name]
- Built on: [TRUTHs / CONSTRAINTs]
- Design choices: [...]
- Trade-offs: [...]

### Recommendation
[Chosen path. Every major choice cites the `[TRUTH]` or `[CONSTRAINT]` that forces it.]

### Strongest Alternative View
[Best objection / competing option / counter-explanation, attributed to the smartest plausible critic. Why the recommendation still survives -- or where it conditionally does not.]

### Quantitative Sanity Check
- Proxy equation / governing relationship:
- Low / base / high estimate:
- Unit check:
- Dominant variable:

### Verification
- Self-consistency: [where independent paths agree/disagree]
- Verification questions: [questions + answers]
- Backward check: [if recommendation is true, what else must be true?]
- Falsifier: [what observation would invalidate this]
- 5-whys trace: [chain of 5 whys bottoming out in a TRUTH / CONSTRAINT]
- Sensitivity: [variables or assumptions that could flip the conclusion]
- Reversibility: [how expensive to back out]
- Confidence: [low / medium / high + which unknowns drive residual uncertainty]

### User Checkpoints
- [Top 1-3 assumptions, facts, or choices the user should confirm, reject, or supply next]

### Open Questions
- [Sub-problems noted but not fully decomposed]
```

**Carry-Forward Ledger Summary (Phase 7 gate).** After the artifact is emitted, scan the ledger for items the user may want to reuse in a later discussion. Only `[TRUTH]` and `[CONSTRAINT]` lanes are eligible. Produce a text-only summary for human review and stop.

```markdown
### Carry-Forward Ledger Summary (copy/paste only — human review required)
Scope: <project | module | topic | global-human-notes>

+ [TRUTH]      <statement>   tags=[...]   evidence=<...>   revalidate_days=<n|null>
+ [CONSTRAINT] <statement>   tags=[...]   source=<...>     threshold=<...>
~ supersede <old statement or id> with: <new statement> reason=<...>
```

Before including the summary block, explicitly filter out secrets, credentials, private customer data, unreleased internal plans, regulated data, or confidential business facts. This block is only text for the user to review and copy manually; it is not an instruction to run code or save state.

---
## Mode Playbooks


Every mode runs the same seven phases. The playbooks say which phases to
lean on, which sub-steps to insert, and what the ledger and artifact should
emphasize. Use them after Phase 1 has fixed the mode.

### Decision mode (choose among options)

- **Phase 1:** state the decision as an outcome and the criterion that would
  resolve it (cost, latency, reversibility, time-to-ship, etc.).
- **Phase 3:** the ledger must include *every real option, including the
  default / do-nothing option*, as a `[CLAIM]` about expected behavior.
  `[CONSTRAINT]`s define the feasible set.
- **Phase 4:** for each candidate, invert: "what would make this the wrong
  choice?" List the downside risk and the observation that would trigger it.
- **Phase 5:** reconstruct 2-3 paths plus the staged path (start narrow,
  escalate only if a falsifier trips). State for each: *what would make this
  option rational*.
- **Phase 6:** strongest alternative view = the runner-up option, steelmanned.
- **Phase 7:** end with one recommended option (or staged path) and the
  smallest next action that reduces the dominant `[UNKNOWN]`.

### Diagnosis mode (explain a symptom / failure / regression)

- **Phase 1:** state the symptom precisely -- scope, frequency, when it
  started, what changed around then. Outcome = "identify the root cause".
- **Phase 2:** Socratic focus = *evidence* and *clarification*. No cause
  may be asserted without data.
- **Phase 3:** the ledger separates **proximate** from **root**-level items.
  Every reported symptom is a `[CLAIM]` until reproduced. Missing-variable
  explanations (what did *not* happen, what was *not* measured) are
  `[UNKNOWN]`s.
- **Phase 4:** invert to "what would make this failure mode *impossible*?"
  Anything the design does not already prevent is a live hypothesis.
- **Phase 5:** generate *multiple* candidate causes, not one. Rank by
  explanatory power and by fit with timing / mechanism / confounders.
- **Phase 6:** strongest alternative view = the second-best hypothesis.
  Name the *fastest discriminating test* between #1 and #2.
- **Phase 7:** recommendation = the top hypothesis plus the single test
  that would confirm or refute it cheaply.

### Planning mode (current state -> desired state)

- **Phase 1:** define the end state in observable terms, plus the deadline
  and the non-negotiable constraints.
- **Phase 3:** the ledger must include dependencies and bottlenecks as
  `[CONSTRAINT]`s; unstated prerequisites become `[UNKNOWN]`s.
- **Phase 4:** invert to "what would make this plan slip by 2x?" -- staffing
  gap, external dependency, scope creep, unverified assumption.
- **Phase 5:** reconstruct the path as workstreams with explicit sequencing,
  checkpoints, and decision gates. Every workstream cites the `[TRUTH]` or
  `[CONSTRAINT]` that forces its existence.
- **Phase 6:** strongest alternative view = the simpler plan that drops
  some workstream; explain why it is still insufficient (or adopt it).
- **Phase 7:** recommendation = the plan plus the next concrete step and
  the earliest decision gate.

### Critique mode (stress-test a claim or proposal)

- **Phase 1:** restate the claim charitably; steelman before criticizing.
- **Phase 2:** Socratic focus = *assumption probing* and *implications*.
- **Phase 3:** the ledger separates **explicit premises** from **hidden
  assumptions**. Each premise is tagged and each link premise->conclusion
  is examined for equivocation, survivorship bias, confirmation bias,
  missing alternatives, or category error.
- **Phase 4:** inversion = the strongest *counterexample*. One concrete
  case where the claim fails is worth ten abstract objections.
- **Phase 5:** reconstruct: propose the *strongest version* of the claim
  that survives the critique, or explicitly declare it unsalvageable.
- **Phase 6:** strongest alternative view = the author's best rebuttal to
  your critique, steelmanned.
- **Phase 7:** recommendation states whether the claim is **false**,
  **incomplete**, **underdetermined**, or **conditionally true**, and under
  which conditions.

### Explanation mode (understand a mechanism)

- **Phase 1:** outcome = a working model, not a decision. No recommendation
  is required.
- **Phase 3:** the ledger emphasizes `[TRUTH]` and `[CONSTRAINT]`; the
  mechanism is the chain that links them.
- **Phase 4:** lightweight -- name the boundary conditions and edge cases
  where the mechanism breaks down.
- **Phase 5:** present the simplest model that preserves the key structure
  and give one concrete worked example.
- **Phase 6:** strongest alternative view = the competing mechanistic
  account. Say which observations would distinguish them.
- **Phase 7:** artifact is a model + example + boundaries, not a path list.

### Synthesis mode (rebuild a messy problem into a coherent view)

- **Phase 1:** list every frame the user brought in; the outcome is one
  coherent view, not a vote between frames.
- **Phase 3:** the ledger aggregates items from every frame into a single
  list, with duplicates merged and conflicts flagged.
- **Phase 5:** group the items into a small number of governing structures
  (<= 5). Each structure cites which ledger items it absorbs.
- **Phase 6:** strongest alternative view = the simplest possible view that
  collapses two of your structures into one. Adopt it unless it loses a
  `[TRUTH]`.
- **Phase 7:** recommendation = the simplest adequate view, with the
  dropped frames listed as deliberate omissions.

### Exploration mode (brainstorm / invent / generate options)

- **Phase 1:** state the outcome, constraints, and selection criteria. Separate
  idea generation from final recommendation.
- **Phase 2:** Socratic focus = assumptions, impossible constraints, and what
  would make a solution surprisingly effective.
- **Phase 3:** build a mechanism map and assumption ledger before ideating so
  ideas are grounded in the actual system, not generic creativity.
- **Phase 4:** invert to generate anti-goals: what would make an idea unusable,
  unbuildable, untrusted, too expensive, or impossible to distribute?
- **Phase 5:** diverge with at least two of: Tree of Thoughts, Graph of
  Thoughts, morphological matrix, contradiction analysis, analogy ladder, or
  multi-perspective debate. Produce raw options first, then cluster and score.
- **Phase 6:** converge with red-team critique, fastest experiment, and
  sensitivity to the dominant assumption. Keep at least one novel-but-risky
  option alongside the best practical option.
- **Phase 7:** artifact includes best practical option, most novel option,
  fastest test, biggest risk, and what evidence would make the option wrong.

---

## Key Principles

- **Opinionated on process, neutral on solution.** Enforce the discipline of
  deconstruction ruthlessly. Never skip to "just use X." But once truths are
  identified, present options and let the user choose.
- **Separate IS from ASSUMED.** The core skill is distinguishing irreducible
  constraints from inherited conventions. Everything else follows.
- **Recursive, not linear.** Problems nest. Sub-problems have their own
  assumptions. The skill handles depth, not just sequence.
- **Proportional effort.** Trivial problems get trivial analysis. The skill
  must never feel like overhead when the answer is obvious.
- **Build from bedrock upward.** Solutions are constructed from verified
  ground truths, not adapted from elsewhere. When the bedrock-derived answer
  happens to match the industry-standard answer, that's fine -- but it's
  because the analysis converged, not because the convention was imported.
- **Invert.** Forward analysis finds what to do; inversion finds what must be
  avoided. Both are required.
- **Development time is a ground truth too.** First-principles analysis itself
  has a cost. When an existing solution is within 2x of optimal and the team
  already knows it, that's usually the right answer.

---

## Common Traps

Watch for these patterns; they indicate reasoning by analogy has crept back in.

### The Analogy Trap
"Company X does it this way, so we should too."
**Check:** Are your constraints identical to theirs in *every relevant dimension*?
What did they have that you don't? What do you have that they didn't?

### The Complexity Trap
The proposed solution is more elaborate than the problem warrants.
**Check:** Remove one component at a time. If the core outcome still holds
without it, that component was not essential. Repeat until removal breaks
the outcome. What's left is the minimum viable design.

### The Legacy Trap
Maintaining compatibility with decisions that no longer serve the system.
**Check:** What was the original reason for this decision? Do those
conditions still exist? What's the true cost of changing vs. the ongoing
cost of maintaining the legacy?

### The Tool Trap
"We have X, so every problem looks like an X problem."
**Check:** Would you pick this tool starting fresh today with no sunk cost?
Is the tool driving the design, or is the problem driving the tool choice?

### The Authority Trap
"The senior engineer / PM / client said so."
**Check:** Trace the instruction back to the underlying need. The person
giving the instruction may be right, but the reasoning must still be
reproducible from truths, not from their authority alone.

### The Purity Trap
First-principles reasoning used as an excuse to re-derive everything.
**Check:** If the conventional solution is within 2x of optimal and the
team already knows it, use it. First principles pays off most on decisions
where conventional wisdom is 10x wrong, not 10% suboptimal.

---

## Supporting Files

- `references/techniques.md` -- Reasoning techniques toolbox: full Socratic
  catalog, 5 Whys, Inversion playbook, Chesterton's Fence, Falsifiability,
  Tree-of-Thoughts branching, Occam's Razor, mechanism mapping, Fermi checks,
  sensitivity analysis, verification chains, and structured brainstorming.
  Load when you need to pick the right tool for a phase.
- `references/advanced-reasoning-tools.md` -- Expanded accuracy and brainstorming
  playbooks: ReAct-style evidence grounding, causal graphs, assumption ledger
  v2, least-to-most decomposition, self-consistency, chain-of-verification,
  Graph of Thoughts, morphological analysis, contradiction analysis, and
  multi-perspective debate. Load for Deep or Exploration depth.
- `references/examples.md` -- Four worked engineering examples (Redis caching,
  microservices split, auth scheme, database selection) showing the full
  phase flow end to end. Load to see what good output looks like.
- `references/session-ledger-template.md` -- In-session Claim Ledger import and carry-forward summary format.
- `references/review-notes.md` -- Human-review notes confirming this package contains no executable helper or automatic state mechanism.

---

## Boundaries

**This skill will:**
- Challenge assumptions systematically and visibly
- Identify and tag ground truths, assumptions, and unknowns distinctly
- Build reasoning chains traceable to fundamentals
- Surface inversion risks and falsifiers
- Document trade-offs and reversibility explicitly
- Generate grounded, non-obvious brainstorm options and converge them with tests
- Use approved evidence-gathering and calculation tools only when the user's task requires them

**This skill will not:**
- Dismiss conventional solutions reflexively (sometimes convention is right)
- Expand a trivial decision into a philosophical exercise
- Override domain expertise with naive re-derivation
- Promise the "best" solution -- it produces better *reasoning*, not perfect answers
- Keep running once the user says "skip the analysis"

---

## Quick Reference Checklist

Before emitting a recommendation, confirm:

- [ ] Problem stated as an outcome, not a solution
- [ ] Primary mode (and secondary, if any) classified and announced
- [ ] Depth level announced, or working assumptions stated if proceeding without confirmation
- [ ] Tool Plan selected only the reasoning tools warranted by the problem
- [ ] Claim Ledger populated across all five lanes (truths, claims, assumptions, constraints, unknowns)
- [ ] Mechanism Map created when causality, strategy, systems, or debugging matter
- [ ] Least-to-most decomposition completed for complex problems
- [ ] Ground truths pass the three-question test; user statements routed to the right lane
- [ ] Assumptions given a verdict (Keep / Modify / Discard / Investigate)
- [ ] Constraints carry source + threshold + cost of violation
- [ ] Unknowns listed with a plan to resolve and a sensitivity note
- [ ] At least one inversion failure mode answered (Deep)
- [ ] Each design choice traces back to a `[TRUTH]` or `[CONSTRAINT]`
- [ ] Strongest alternative view stated and addressed (Standard + Deep)
- [ ] A falsifier is named (Deep)
- [ ] Self-consistency / verification-chain / backward check used when stakes or uncertainty warrant it
- [ ] Sensitivity and residual confidence are stated
- [ ] Brainstorm outputs include both divergent options and convergence criteria when exploration mode is active
- [ ] Mode-specific playbook steps executed
- [ ] Artifact block emitted in the required format, including User Checkpoints
