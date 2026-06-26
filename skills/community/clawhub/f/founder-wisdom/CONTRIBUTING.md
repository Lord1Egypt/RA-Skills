# Contributing to Founder Wisdom

Thanks for your interest in contributing. This document covers what kinds of contributions are welcome, how the corpus is structured, and how to propose additions or changes.

## What makes a good axiom

Axioms in this corpus share a few properties. New axioms should generally have them too.

**Quotable in one sentence.** If the axiom needs three sentences to state, it's not an axiom — it's an essay. The opening line should be something a reader could remember and repeat. Examples: "Cash is oxygen." "Fire fast." "Distribution beats product." If you can't compress it, it doesn't belong.

**Pattern, not opinion.** The bar is "this has been observed across many companies." Not "this is what I believe." If the only evidence is one founder's experience, it's a war story, not an axiom. War stories are valuable but they go in the prose, not in the bolded headline.

**Carries a real consequence.** Axioms in this corpus exist because ignoring them costs founders something specific — a failed company, a co-founder breakup, a bad hire that took 18 months to fix. The body of the axiom should make the cost concrete. "It's important to communicate well" is too vague. "Bad news doesn't age well — whatever you're avoiding telling your team, tell them today" is concrete.

**Names its limit when relevant.** Most axioms have exceptions. "Fire fast — except never in anger, never on a Friday" is more useful than just "fire fast." Naming the limit makes the axiom usable rather than absolute.

**Attributed when traceable.** If a specific person originated an axiom (Paul Graham, Sam Altman, Marc Andreessen, etc.), name them. Attribution adds credibility and lets readers trace the source. Don't attribute axioms that are genuinely common knowledge — but err on the side of attribution when in doubt.

## What kinds of additions are likely to be accepted

- **New axioms in existing domains** that meet the bar above and don't substantially duplicate existing content.
- **New domains** that represent genuinely distinct territory not covered elsewhere (e.g., international expansion, M&A, IPO readiness, specific industry verticals).
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
- **Stage tags:** When an axiom only holds at a particular stage, name it: `*(Stage: Seed–Series A.)*`
- **Tone:** Direct and confident. Avoid hedging language ("perhaps," "it might be," "in some cases"). When hedging is necessary, hedge specifically — name the dependency.
- **No moralizing.** These are observed patterns, not commandments.

## Structure of the corpus

```
founder-wisdom/
├── SKILL.md                          # Routing logic for Claude
├── README.md                         # Public-facing description
├── CONTRIBUTING.md                   # This file
├── LICENSE                           # MIT
└── references/                       # The actual axioms
    ├── hiring.md
    ├── fundraising.md
    ├── product.md
    ├── sales-gtm.md
    ├── finance-ops.md
    ├── cofounders-equity.md
    ├── governance.md
    ├── time-energy.md
    ├── customers-market.md
    ├── crisis-resilience.md
    ├── culture.md
    ├── startup-mechanics.md
    ├── yc-canon.md
    └── meta.md
```

`SKILL.md` should stay under ~150 lines. Reference files should stay under ~300 lines. If a reference file is approaching that, it's a signal to split the domain rather than to keep adding.

## A note on the opinionated nature of the corpus

This corpus reflects observed patterns from a particular slice of the startup world: largely U.S., largely venture-backed, largely software, largely from the past 15 years. Many of the axioms hold beyond that slice. Some don't.

Contributors from outside that slice — bootstrap-funded businesses, non-U.S. ecosystems, deep-tech, biotech, hardware, agencies, e-commerce — are particularly welcome. The corpus will be more useful if it can name when an axiom holds and when it doesn't. But the goal is not neutrality; the goal is accurate pattern-matching.
