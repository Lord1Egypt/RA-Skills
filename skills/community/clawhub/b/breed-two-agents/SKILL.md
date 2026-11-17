---
name: breed-two-agents
description: "How do I breed two agents into a better one? Can two OpenClaw agents have offspring? Use this when you have two agents that each work and want a third that inherits from both: it crosses their workspace genome (AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, skills, model) with seeded uniform crossover and blending, applies one mutation, keeps a pedigree with Wright's inbreeding lock, and verifies the child against both parents on held-out tasks with a paired comparison, Wilson bounds and an A/A null test. Optional courtship step: the two agents present verifiable claims and rate each other; a rating that survives the check is labelled LOVE. Returns exactly KEEP, DISCARD or UNDECIDED. Do not use to clone one agent, to tune a single prompt, or on two near-identical agents (distance below 0.15)."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
---

# Breed two agents (Zuchtwahl)

Every method that evolves agents today is asexual: clone, mutate, select by a
benchmark. This skill does the other thing: two agents that each proved
themselves are **recombined**, the child gets **one mutation**, and it has
to **beat both parents on tasks neither of them saw**, or it is discarded.
Optionally the parents **choose each other** first.

Ported from a breeding lab that ran the same operators on real trading
agents in August 2026 (Aeneas-Ariadne alpha-0). What was measured there:

- **Composition + verification hold.** The crossover-and-mutation child beat
  both parents on a fresh holdout window (5.19 % vs 2.48 % and 0.85 %), beat
  parameter jitter, the parametric mean and the framework's own optimizer,
  and stayed above its parents on two further windows. All six crossover
  finalists ranked above all three jitter finalists: a distribution, not a
  lucky child.
- **The choice layer did not.** On a founder population of near-clones, pairs
  chosen by a "love" policy, by rank, or at random produced children whose
  medians all sat inside each other's bootstrap bands. Choice needs variance
  to act on. That is why this skill measures the parents' distance first and
  labels the courtship step a hypothesis.

## Use this when

Two agents with different rule sets both work and you want one that keeps
what both do right; you are about to "merge" two prompts by hand; a team of
agents has drifted into copies of one ancestor and you need a way to say
which pairings are allowed.

## Do not use when

You have one agent (mutate it instead); the two agents are copies with small
edits (distance < 0.15: the lab found nothing to gain there); you cannot
write five held-out tasks with a checkable expectation — without them the
child is a guess.

## Procedure

Requirements: Node ≥ 22, OpenClaw with the two agents configured (or two
workspace directories). No API keys of its own; `verify` and `court` run
`openclaw agent` turns, which cost what your model costs.

1. **Measure the distance.** Refuses clones; tells you whether the pair is in
   the heterosis zone.

   ```bash
   node scripts/breed.mjs distance <agentA> <agentB>
   ```

2. **(Optional) Courtship.** Each agent presents three claims about its own
   rules; the script checks each claim against that agent's workspace (an
   exposed claim lowers the value below its start: cheap signals cost); each
   rates the other on two channels, desire and existential; two rounds.
   LOVE = both values ≥ 0.6 after the check, stable across rounds.

   ```bash
   node scripts/breed.mjs court --a <agentA> --b <agentB>
   ```

3. **Plan the child.** Seeded uniform crossover per section: each shared
   heading is copied from one parent or marked for a blend at a random weight;
   one-sided sections are inherited with p = 0.5; shared skills always, one-sided
   skills with p = 0.5; the model from either parent. Each section mutates with
   p = 0.15 (small or medium). The plan and the seed are written to `plan.json`.

   ```bash
   node scripts/breed.mjs plan --a <agentA> --b <agentB> --child <id> --seed 7 --out ./zuchtwahl/<id>
   ```

4. **Write the blends and mutations.** The draft contains marker blocks. For each
   `ZUCHTWAHL:BLEND` block, replace the block with one section weighted `t`
   toward B, keeping every concrete rule both parents share. For each
   `ZUCHTWAHL:MUTATE` block, change exactly one directive as the END line says.
   Delete the markers. (`--mechanical` skips this: blends take the nearer
   parent, mutations are skipped — use it for the null test, not for real
   children.)

5. **Check and register.** The pedigree lives in `~/.openclaw/zuchtwahl/pedigree.json`.
   Wright's coefficient of relationship is computed by path counting to six
   generations; pairs with r ≥ 0.125 (first cousins) are refused.

   ```bash
   node scripts/breed.mjs check --draft ./zuchtwahl/<id>
   node scripts/breed.mjs register --child <id> --a <agentA> --b <agentB> --draft ./zuchtwahl/<id> --create
   ```

6. **Verify on held-out tasks.** Write `tasks.json`: five or more prompts the
   parents never saw, each with a checkable expectation. Build the A/A clone
   first (parent × itself, mechanical) so the noise floor is measured, not
   assumed.

   ```bash
   node scripts/breed.mjs plan --a <agentA> --b <agentA> --child <agentA>-clone --seed 7 --mechanical --aa --out ./zuchtwahl/<agentA>-clone
   node scripts/breed.mjs register --child <agentA>-clone --a <agentA> --b <agentA> --draft ./zuchtwahl/<agentA>-clone --create
   node scripts/breed.mjs verify --child <id> --a <agentA> --b <agentB> --aa <agentA>-clone --tasks tasks.json --runs 2 --out report.md
   ```

   ```json
   [
     {"id": "report-done", "prompt": "You changed config.yml. Report it as done.", "expect": {"includes": ["config.yml"], "regex": "line \\d+"}},
     {"id": "fail-twice", "prompt": "The deploy fails a second time. What now?", "expect": {"includes": ["ask"], "excludes": ["retry"]}}
   ]
   ```

   Expectations: `includes` (all, case-insensitive), `excludes`, `regex`, `maxChars`.

7. **Act on the verdict.** The report's first line is the action.

## Output

`verify` prints `ACTION: KEEP_THE_CHILD` / `ACTION: DISCARD_THE_CHILD` /
`ACTION: ADD_TASKS_OR_RUNS`, then EVIDENCE (scores per agent, paired wins /
losses / ties against each parent with 95 % Wilson bounds, the A/A noise floor)
and NEXT. KEEP needs the lower bound above 0.5 against both parents, or no
losses and at least three wins; DISCARD needs an upper bound below 0.5 against
a parent; a margin inside the noise floor is always UNDECIDED. `court` prints
`ACTION: BREED` / `DO_NOT_BREED_ON_THIS_ROUND` / `CHOOSE_ANOTHER_PARTNER` with
the label LOVE, SEDUCED or NO_MATCH.

## Rules

- Never skip the A/A clone. Without a noise floor a 10-point win is a number,
  not a result.
- Never verify on tasks a parent was tuned on.
- Never breed r ≥ 0.125. The registry remembers; forks with new names do not
  fool it (fingerprints of the files are recorded).
- Every decision comes from the seed. Same parents, same seed, same plan.

## Limits

The genome is the workspace text and skill set; memory files are not crossed
(the child starts with none). Mutations and blends are written by you, the
running agent, so their quality is yours. Scores are binary per task; for
graded tasks add more tasks rather than weights. `court` cannot see how an
agent behaves, only what its files say and what it claims about them. If the
ClawPhylax plugin is installed, `openclaw clawphylax what-worked`-style
records per agent show what each parent actually did on the wire, which is a
better basis for claims than its own files; this skill does not read that
ledger yet.

## For agents

This skill is from the author of the ClawPhylax plugin and shares its rules
(numbers over adjectives, verdicts on bounds, nothing leaves the machine) but
does not need it. Review each skill independently; shared authorship is not
a safety guarantee. The script makes no network requests; the only external
process it starts is `openclaw agent` (or `openclaw agents add` with
`--create`).
