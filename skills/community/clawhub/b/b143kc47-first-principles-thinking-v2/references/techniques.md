# Reasoning Techniques Toolbox

Reference for the skill's phases. Each technique lists: *what it is*, *when
to use it*, *how to run it*, and *failure modes to watch for*.

Load only the sections relevant to the current phase; do not page through
the whole file.

---

## 1. Socratic Questioning (full catalog)

**What it is.** A disciplined sequence of questions that surfaces hidden
assumptions and forces clarity. Six question families, each with a distinct
job.

**When to use.** Phase 2 of every depth level. Pick 3-5 families most
relevant to the problem; using all six mechanically is worse than using
three well-chosen ones.

### 1.1 Clarification
- "What exactly do you mean by [term]?"
- "Can you give a concrete example of the problem, with numbers?"
- "What does success look like -- what would you measure?"
- "Is this the full problem, or part of a larger one?"

### 1.2 Assumption Probing
- "Why does it have to work that way?"
- "What if that constraint didn't exist?"
- "Is that a hard requirement or something inherited from the last design?"
- "Who decided this, and what was their reasoning?"
- "What would change if we revisited that decision today?"

### 1.3 Evidence
- "What data shows this is actually the bottleneck?"
- "Have you measured it, or is it a guess?"
- "How do you know users want this? Which users? How many?"
- "What would prove this theory wrong?"

### 1.4 Alternative Viewpoints
- "How would a team with opposite constraints (tiny / huge / different stack) solve this?"
- "What would you build starting from zero today, no sunk cost?"
- "What would a skeptic of this approach say?"
- "What are the two strongest arguments against your current plan?"

### 1.5 Implications
- "What are the second-order effects of this choice?"
- "What breaks if the core assumption turns out to be wrong?"
- "What's the cost of reversing this decision in six months?"
- "Who else is affected by this that we haven't talked to?"

### 1.6 Meta
- "Are we solving the right problem?"
- "Is this the simplest version of the problem, or have we over-specified it?"
- "What happens if we just... don't do this?"
- "Is the problem real, or are we pattern-matching to a previous project?"

**Failure modes.**
- Machine-gunning all six families: reads as interrogation, not reasoning.
- Asking questions you already know the answer to: wastes turns.
- Skipping to the next question before the answer is digested.

---

## 2. The 5 Whys

**What it is.** A root-cause technique. Ask "why" five times in succession,
each time about the previous answer, until the chain bottoms out in a
`[TRUTH]` or a process gap.

**When to use.**
- Hard debugging (Phase 2 and again in Phase 6 verification).
- Tracing a "requirement" to its real origin (Phase 2 assumption probing).
- Validating that a proposed solution in Phase 5 is grounded in truth, not
  in another assumption.

**How to run it.**

```
Symptom: "The API is slow."
Why 1: Why is it slow?          -> Database queries are slow.
Why 2: Why are the queries slow? -> Missing index on the orders table.
Why 3: Why is the index missing? -> Nobody reviewed the migration.
Why 4: Why wasn't it reviewed?   -> No required-reviewer rule for migrations.
Why 5: Why no rule?              -> Team skipped that when moving to the new repo.
                                   ^ This is the root: process, not code.
```

**Failure modes.**
- Stopping at the first plausible answer.
- Wandering off the causal chain into correlated-but-unrelated topics.
- Treating "human error" as the bottom. Humans err; the environment should
  make the right thing easy. Ask "why did the system allow this?"

---

## 3. Inversion (Munger's Rule)

**What it is.** Instead of asking "how do I succeed?", ask "what would
guarantee failure, and how do I avoid it?" The inverse problem is often
easier to reason about and catches gaps forward analysis misses.

**When to use.** Phase 4 (Deep) and any time you feel too confident.

**How to run it.**

1. State the goal.
2. List 3-5 specific failure modes -- what would make this fail catastrophically?
3. For each failure mode, ask: "does my current design prevent this? How?"
4. Failure modes without a concrete preventer become:
   - new `[TRUTH]` constraints, OR
   - explicit risks the user must accept.

**Example.**

Goal: deploy a new payment flow.

| Failure mode                                  | Current design prevents? |
|-----------------------------------------------|--------------------------|
| Double-charge the customer                    | Yes -- idempotency key   |
| Charge with no order record                   | No -- gap, need tx log   |
| PCI data leaks in logs                        | No -- gap, need scrub    |
| Retries after timeout cause duplicate orders  | Yes -- idempotency key   |

The "No" rows are what inversion uncovered. Those become required work,
not nice-to-haves.

**Failure modes.**
- Generic failure lists ("it could go wrong") -- be specific.
- Treating inversion as a blame exercise; it's a gap-finding exercise.

---

## 4. Chesterton's Fence

**What it is.** A rule against removing things you don't understand. Before
tearing down an existing component, you must first explain why it was put
there. Only then do you have the right to decide whether removing it is safe.

**When to use.**
- Any Phase 5 path that recommends removing, replacing, or deprecating
  existing code / infrastructure / process.
- Any time "legacy" is used as a reason to change something.

**How to run it.**

1. State what you propose to remove.
2. Research or ask: why was it originally built? Who built it? What did it solve?
3. Determine whether those original conditions still hold.
4. Only then decide: remove (conditions gone), keep (conditions still hold),
   or replace (conditions partially hold, new design addresses them explicitly).

**Failure modes.**
- Accepting "it's old" as sufficient justification for removal.
- Accepting "I don't know why it's there" as sufficient justification for removal.
- Over-applying: sometimes the fence really is just rotting. The rule is
  "understand before removing", not "never remove".

---

## 5. Falsifiability

**What it is.** A recommendation is rigorous only if you can state what
observation would prove it wrong. If nothing could invalidate it, it isn't
a claim about reality -- it's a preference in disguise.

**When to use.** Phase 6 (Verification), applied to the chosen Path in Phase 5.

**How to run it.**

Write a sentence of the form:

> "If we observe **[specific measurable event]** within **[timeframe]**,
> this recommendation is wrong and we should **[alternative]**."

**Examples.**

- "If P99 latency remains above 200ms one week after deploying the query
  fix, caching is not optional and we must revisit Path C (Redis)."
- "If, after 30 days, fewer than 5% of users hit the new flow, the
  feature is unneeded and should be removed rather than optimized."

**Failure modes.**
- Unfalsifiable claims ("it'll be better"). Better by what measure, by when?
- Falsifiers nobody will actually check. Assign an owner and a date.

---

## 6. Tree-of-Thoughts Branching

**What it is.** Instead of committing to one reasoning path, generate 2-3
candidate paths, evaluate each against the ground truths, and choose. Direct
generalization of Chain-of-Thought to a search tree.

**When to use.** Phase 5 (Reconstruction), always at Deep depth, optional
at Standard.

**How to run it.**

1. Generate 2-3 distinct candidate paths. They must be genuinely different
   (different ground truths emphasized, different trade-offs), not cosmetic
   variations of one idea.
2. Score each path on: fit to ground truths, operational cost, reversibility,
   team familiarity, and remaining unknowns.
3. Pick the path with the best total; state why the others lost.
4. Keep the runner-up path documented; it's the fallback if the chosen path
   hits an unknown that invalidates it.

**Failure modes.**
- Fake branches: three paths that are the same idea in different clothes.
- No elimination criteria: if every path "has trade-offs" with no verdict,
  no choice has actually been made.

---

## 7. Occam's Razor

**What it is.** Among hypotheses or designs that fit the evidence equally
well, prefer the one with fewer entities / assumptions. Not "simplest wins";
"simplest *that still fits* wins".

**When to use.** Phase 5 tie-breaker; Common-Traps check for the Complexity Trap.

**How to run it.**

Given two designs A and B that both satisfy all `[TRUTH]`s:
1. Count the entities (components, services, dependencies, concepts the
   team must hold in their head).
2. Count the assumptions each makes about future conditions.
3. The one with fewer of each, wins -- unless the extra complexity prevents
   a failure mode identified in Phase 4 inversion.

**Failure modes.**
- Using Occam to justify under-engineering. Simpler only wins among
  designs that *all* satisfy the truths.
- Counting entities inconsistently (ignoring the operational cost of the
  "simpler" option that ships five shell scripts).

---

## 8. Mechanism Mapping / Causal Graph

**What it is.** A compact model of how the system actually works: variables,
causal links, mediators, confounders, feedback loops, bottlenecks, and
boundary conditions.

**When to use.** Phase 3 for strategy, product, architecture, debugging,
scientific, business, and policy-like problems. Mandatory when the user asks
"why", "what causes", "what would happen if", or "which lever matters most".

**How to run it.**

1. List actors, variables, stocks, flows, constraints, and incentives.
2. Draw the causal chain in text: `A -> B -> C`, and mark confounders as
   `Z -> A` and `Z -> C`.
3. Name the bottleneck, feedback loop, and boundary condition.
4. Ask what observation would distinguish the proposed mechanism from a rival.

**Failure modes.**
- Treating correlation as causation.
- Leaving out confounders because they complicate the story.
- Making a mechanism so abstract it cannot be tested.

---

## 9. Assumption Ledger v2

**What it is.** A structured record of assumptions with evidence, confidence,
fragility, failure mode, and fastest test.

**When to use.** Phase 3 and anytime a conclusion depends on unstated beliefs,
team convention, market behavior, user behavior, benchmarks, or future states.

**How to run it.**

| Assumption | Evidence | Confidence | Fragility | Failure if false | Fastest test |
|------------|----------|------------|-----------|------------------|--------------|
| ...        | ...      | low/med/high | ...     | ...              | ...          |

Assumptions whose falsehood would reverse the recommendation become User
Checkpoints. Assumptions that only adjust implementation details can remain as
caveats.

**Failure modes.**
- Listing assumptions without saying how to test them.
- Marking assumptions high-confidence because they are familiar.
- Hiding key business or behavioral assumptions inside technical phrasing.

---

## 10. Least-to-Most Decomposition

**What it is.** Break a hard problem into the smallest subproblems that can be
solved independently, then synthesize.

**When to use.** Complex decisions, debugging, quantitative reasoning,
research design, and multi-constraint planning.

**How to run it.**

1. Write 3-7 subproblems.
2. For each, specify the intermediate output: variable, constraint, mechanism,
   test, or risk.
3. Solve or bound each subproblem before giving the final answer.
4. Do not let a vague subproblem pass; split it further.

**Failure modes.**
- Decomposing by document sections instead of by causal dependencies.
- Solving subproblems that do not affect the final decision.
- Synthesizing before the blocking unknowns are bounded.

---

## 11. Fermi Estimate and Dimensional Check

**What it is.** A sanity check that uses simple equations, rough estimates,
units, and ranges to prevent hand-wavy scale errors.

**When to use.** Any claim involving cost, capacity, latency, throughput,
market size, staffing, probability, physical limits, or operational scale.

**How to run it.**

1. Write the governing equation or proxy equation.
2. Estimate each variable with low/base/high ranges.
3. Check units.
4. Name the dominant variable.
5. Say whether changing the dominant variable flips the conclusion.

**Failure modes.**
- Presenting a single precise number from rough inputs.
- Forgetting units.
- Estimating only the convenient variables and hiding the hardest one.

---

## 12. Chain-of-Verification

**What it is.** Draft an answer, generate verification questions, answer those
questions independently, then revise the answer.

**When to use.** High-stakes answers, factual claims, research summaries,
current information, or any output where hallucination would be costly.

**How to run it.**

1. Draft the tentative answer.
2. Ask: which claim is most likely false? which fact needs evidence? which
   assumption would flip the answer? what would falsify this?
3. Answer the verification questions without relying on the draft phrasing.
4. Revise the final answer and lower confidence where verification is weak.

**Failure modes.**
- Asking verification questions that merely restate the draft.
- Verifying only easy claims, not load-bearing claims.
- Forgetting to revise after a failed check.

---

## 13. Self-Consistency and Backward Check

**What it is.** Generate multiple independent reasoning paths, compare them,
and check whether the final conclusion implies conditions that are actually
present.

**When to use.** Ambiguous decisions, competing explanations, math-like logic,
complex diagnosis, or any case where the first plausible path may anchor the
answer.

**How to run it.**

1. Produce 2-3 independent paths.
2. Compare conclusions, assumptions, and weak links.
3. Pick the answer that survives most paths, not the answer that sounded best
   first.
4. Backward check: if conclusion C is true, what else must be true? Verify or
   bound those prerequisites.

**Failure modes.**
- Cosmetic independence: paths differ in wording but share the same assumption.
- Majority voting when all paths rely on the same bad premise.
- Treating the backward check as proof instead of a consistency test.

---

## 14. Sensitivity Analysis

**What it is.** Identify which inputs or assumptions control the conclusion and
whether plausible variation changes the recommendation.

**When to use.** Any estimate, prioritization, strategy, forecast, product bet,
or decision with uncertain inputs.

**How to run it.**

1. Name the 1-3 dominant variables or assumptions.
2. Change each by a plausible range, such as +/-20% or low/base/high.
3. State whether the recommendation changes.
4. If the answer flips, lower confidence and propose the highest-value test.

**Failure modes.**
- Sensitivity on easy variables while ignoring the dominant variable.
- Overstating confidence when the conclusion is knife-edge.
- No next test after identifying sensitivity.

---

## 15. Structured Brainstorming: ToT, GoT, Morphological Matrix, Contradictions

**What it is.** A set of divergent-search tools for generating grounded,
non-obvious options before converging.

**When to use.** Exploration mode, early product/strategy/research work,
invention, or whenever the user asks for brainstorms or alternatives.

**How to run it.**

- **Tree of Thoughts:** generate 3-5 paths, score, expand the top 2.
- **Graph of Thoughts:** create nodes for assumptions, mechanisms,
  constraints, resources, analogies, risks, and combine useful intersections.
- **Morphological Matrix:** list dimensions and variants, combine variants,
  filter impossible combinations, keep surprising coherent combinations.
- **Contradiction Analysis:** frame trade-offs as "more X without more Y";
  use separation in time, separation in space, modularity, inversion,
  automation, or self-service to resolve them.

**Convergence rule.** End with best practical option, most novel option,
fastest experiment, biggest risk, and falsifier.

**Failure modes.**
- Brainstorming generic ideas not grounded in the mechanism map.
- Converging too early on the familiar option.
- Keeping only novel ideas and discarding practical next tests.

---

## 16. Evidence Grounding and Formalization

**What it is.** Use approved search, user-provided sources, calculations, solvers, or
symbolic representations when the answer depends on facts or constraints that
language alone should not guess.

**When to use.** Current facts, niche terms, legal/regulatory claims, prices,
scientific literature, API behavior, product specs, equations, scheduling,
optimization, Boolean logic, or hard constraints.

**How to run it.**

1. List the load-bearing facts or constraints.
2. Retrieve, calculate, or formalize before concluding.
3. Keep source-supported claims separate from inference.
4. For solvers: define variables, constraints, objective, and infeasibility
   interpretation before reporting the answer.

**Failure modes.**
- Using memory when facts may have changed.
- Citing evidence that supports a minor claim while the load-bearing claim is
  unsupported.
- Formalizing the wrong objective.

---

## Picking the right tool for each phase

| Phase             | Primary tool(s) |
|-------------------|-----------------|
| 1 Intake          | Clarification questions + Tool Plan |
| 2 Socratic        | Full Socratic catalog + 5 Whys |
| 3 Decomposition   | Ground-Truth Test + Assumption Ledger v2 + Mechanism Map + Least-to-Most |
| 4 Inversion       | Inversion playbook + contradiction framing |
| 5 Reconstruction  | ToT / GoT branching + Fermi check + Chesterton's Fence + Occam's Razor |
| 6 Verification    | Falsifiability + Chain-of-Verification + Self-Consistency + Backward Check + Sensitivity |
| 7 Artifact        | Structured synthesis + convergence criteria + user checkpoints |
