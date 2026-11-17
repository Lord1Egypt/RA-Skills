# Contributing to Founder Wisdom

Thanks for your interest in contributing. This document covers what kinds of contributions are welcome, how the corpus is structured, and how to propose additions or changes.

## What makes a good axiom

Axioms in this corpus share a few properties. New axioms should generally have them too.

**Quotable in one sentence.** If the axiom needs three sentences to state, it's not an axiom — it's an essay. The opening line should be something a reader could remember and repeat. Examples: "Cash is oxygen." "Fire fast." "Distribution beats product." If you can't compress it, it doesn't belong.

**Pattern, not opinion.** The bar is "this has been observed across many companies." Not "this is what I believe." If the only evidence is one founder's experience, it's a war story, not an axiom. War stories are valuable but they go in the prose, not in the bolded headline.

**Carries a real consequence.** Axioms in this corpus exist because ignoring them costs founders something specific — a failed company, a co-founder breakup, a bad hire that took 18 months to fix. The body of the axiom should make the cost concrete. "It's important to communicate well" is too vague. "Bad news doesn't age well — whatever you're avoiding telling your team, tell them today" is concrete.

**Names its limit when relevant.** Most axioms have exceptions. "Fire fast — except never in anger, never on a Friday" is more useful than just "fire fast." Naming the limit makes the axiom usable rather than absolute.

**Benchmark numbers carry a vintage.** Any threshold that depends on the funding market — burn multiples, CAC payback bands, Rule of 40 medians, dilution norms, ARR multiples, prepay discounts — must be tagged *[bench YYYY-MM]* and, where practical, sourced. The mechanic is the axiom; the number is a snapshot. Untagged market figures will be asked for a date before merge.

**Attributed when traceable.** If a specific person originated an axiom (Paul Graham, Sam Altman, Marc Andreessen, etc.), name them. Attribution adds credibility and lets readers trace the source. Don't attribute axioms that are genuinely common knowledge — but err on the side of attribution when in doubt.

## What kinds of additions are likely to be accepted

- **New axioms in existing domains** that meet the bar above and don't substantially duplicate existing content.
- **New domains** that represent genuinely distinct territory not covered elsewhere (e.g., international expansion, IPO readiness, specific industry verticals).
- **Sharpenings** of existing axioms — better one-liners, sharper examples, clearer explanations of the limit.
- **Attributions** for axioms currently uncredited where you can trace the source.
- **Counter-axioms** that genuinely contradict existing content and are defensible as observed pattern.
- **Stage-specific tagging** improvements where an axiom only holds at a particular stage.
- **Skill machinery improvements** — better Socratic translations, better routing logic in `SKILL.md`, better organization of the references.

## What kinds of additions are likely to be rejected

- **Both-sidesism.** Adding a "but on the other hand…" to every axiom dilutes the corpus. The corpus is opinionated by design. If you have a genuine counter-axiom, propose it as a peer — not as a hedge on an existing one.
- **War stories without a pattern.** "When I was at Company X, we did Y and it worked" is not an axiom. It might be evidence for an axiom, but the axiom has to generalize.
- **Generic management advice.** This is a startup wisdom corpus. "Communicate clearly" applies to every job and belongs in a different book.
- **Industry-specific operational knowledge.** FDA approval pathways, ad-tech mechanics, real-estate development — important, but out of scope.
- **Personal opinions phrased as axioms.** The corpus already contains the writer's voice; new content should match the existing pattern-matched register, not introduce a different rhetorical mode.
- **Padding for completeness.** "We should have at least 10 axioms in every file" is not a goal. Brevity is a feature.

## How to propose changes

1. **Open an issue first** for larger changes — new domains, structural reorganization, controversial counter-axioms. This is cheaper than writing the change and having it rejected.
2. **Small additions can come straight as PRs.** New axioms in existing files, attribution improvements, sharpenings — these are easier to evaluate in PR form.
3. **One axiom per PR**, ideally. Easier to discuss and accept/reject individually.
4. **Show your sources** in the PR description if the axiom comes from a specific essay, book, or talk. Especially for attributed material.
5. **Be willing to be edited.** Maintainers may suggest tightening, rephrasing, or reorganizing. The bar for the corpus is high and consistency matters.

## Style guide

- **Headings:** Domain files use `#` for the title, `##` for major sections, and bolded one-liners for axioms (not headings).
- **Axiom format:** `**Axiom in one sentence.** Reasoning, context, and limit in 2–4 sentences.`
- **Attribution:** Inline parenthetical: `(Paul Graham)` or `(Sam Altman, "The Post-YC Slump")`.
- **Stage tags:** When an axiom only holds at a particular stage, name it: `*(Stage: Seed–Series A.)*`. Ranges and open-ended forms are fine (`*(Stage: Series A+.)*`, `*(Stage: Pre-PMF.)*`). A tag is owed when acting on the axiom takes organizational machinery a founder may not have yet — a management layer, an executive bench, a team too large for one conversation — or when the headline claim actively inverts later; naming a pattern or prescribing a solo ritual doesn't earn one, and neither does an axiom whose job is deflating a claim founders make *before* they have the thing, because the tag would route it away from the reader it corrects. An axiom whose only barrier is process or finance mechanics — a cadence, a forecast, a written definition — stays untagged; SKILL.md's stage-matching fallback cuts it down to the company in front of the reader at the point of use. Never write `*(Stage: all.)*` and don't tag an axiom that plainly holds everywhere — but **an untagged axiom is the default, not an assertion that anyone checked it at every stage**.
- **Tone:** Direct and confident. Avoid hedging language ("perhaps," "it might be," "in some cases"). When hedging is necessary, hedge specifically — name the dependency.
- **No moralizing.** These are observed patterns, not commandments.

## Canonical homes

Duplication across files is deliberate — routing sends Claude to one file at a time, so each domain file has to stand alone. Full restatements, though, drift: the Tesla path-dependency example diverged between `yc-canon.md` and `customers-market.md`, and both copies independently carried the same factual error, which is what a twice-maintained axiom looks like right before it becomes two different axioms.

So: **every axiom has exactly one canonical home**, where the full treatment lives. Other files carry at most a bolded one-liner, two lines of context, and a pointer — "See `yc-canon.md` for the full treatment." Examples, statistics, named cases, and worked frameworks live only in the canonical home. When an axiom is traceable to a specific source, `yc-canon.md` is usually the canonical home; otherwise it's the domain file where the axiom does the most work. Don't resolve a duplicate by deleting one side — routing depends on the axiom being findable in both.

`references/socratic-technique.md` applies the same rule as a column. Its translation table restates axioms in their most compressed form — one question each — so every row names the canonical home it came from, which keeps a compressed question traceable to the treatment behind it and makes a missing home visible at a glance. A new row owes that column an entry.

## Structure of the corpus

```
founder-wisdom/
├── SKILL.md                          # Routing logic for Claude
├── README.md                         # Public-facing description
├── CONTRIBUTING.md                   # This file
├── LICENSE                           # MIT
├── evals/                            # Behavioral scenarios for SKILL.md
│   ├── scenarios.yaml
│   ├── check_scenarios.py
│   ├── run_scenarios.py
│   ├── results/                      # Committed judged-run output
│   └── README.md
└── references/                       # The actual axioms
    ├── hiring.md
    ├── fundraising.md
    ├── product.md
    ├── sales-gtm.md
    ├── finance-ops.md
    ├── capital-valuation.md
    ├── bootstrapping.md
    ├── exits-ma.md
    ├── cofounders-equity.md
    ├── governance.md
    ├── time-energy.md
    ├── customers-market.md
    ├── crisis-resilience.md
    ├── culture.md
    ├── startup-mechanics.md
    ├── strategy-moats.md
    ├── management-execution.md
    ├── socratic-technique.md
    ├── yc-canon.md
    ├── yc-canon-product.md
    └── meta.md
```

`SKILL.md` should stay under ~150 lines. Reference files should stay under ~300 lines. If a reference file is approaching that, it's a signal to split the domain rather than to keep adding.

## Changing SKILL.md routing prose

`SKILL.md` is prose that steers a model, so a wording change is a behavior change. `evals/scenarios.yaml` pins down what that behavior is supposed to be: when the skill triggers, which reference files it reads, which mode it picks, and what the output looks like.

If your PR touches the description, the mode triggers, the domain list, the stage note, or the output-style rules, check it against `evals/`:

1. Run `python3 evals/check_scenarios.py` — it validates the scenario file, prints it, and fails if the description has grown past its 950-character budget. No dependencies, no model call.
2. Run `python3 evals/run_scenarios.py` to check the change by actually running the scenarios against a model — it reports triggering, file routing, and axiom counts per scenario, and `--judge` also grades the mode and the prose assertions. It needs the `anthropic` SDK and an `ANTHROPIC_API_KEY` and a full pass costs real API calls, so `--id` on the affected scenarios is usually the right size; CI runs it on PRs where a key is available.
3. Read the scenarios whose `rationale` cites the prose you changed and confirm they still describe the behavior you want.
4. If a scenario is now wrong, update it in the same PR and say why. If your change makes a new behavior load-bearing, add a scenario for it.

The description is the most contended prose in the repo — every domain added wants a word in it — and it has a hard runtime ceiling of 1024 characters, under which `check_scenarios.py` enforces a 950-character budget. Past the ceiling the description is truncated or the skill is rejected, and the symptom (it stops triggering on some questions) is a long way from the cause. When it gets tight, buy the characters back by deleting enumeration the routing bullets already carry — `exits-ma.md` names LOIs and earn-outs, `capital-valuation.md` names venture debt and dilution — rather than by raising the budget. The description's job is to name the *shapes* of question that should trigger the skill; enumerating sub-topics is the routing list's job.

Adding a domain file means adding it to the structure trees here and in `README.md`, and usually adding a routing scenario. See `evals/README.md` for the schema.

## A note on the opinionated nature of the corpus

This corpus reflects observed patterns from a particular slice of the startup world: largely U.S., largely venture-backed, largely software, largely from the past 15 years. Many of the axioms hold beyond that slice. Some don't.

Contributors from outside that slice — bootstrap-funded businesses, non-U.S. ecosystems, deep-tech, biotech, hardware, agencies, e-commerce — are particularly welcome. The corpus will be more useful if it can name when an axiom holds and when it doesn't. But the goal is not neutrality; the goal is accurate pattern-matching.
