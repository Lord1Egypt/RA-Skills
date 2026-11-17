# Founder Wisdom

A [Claude Skill](https://www.anthropic.com/news/skills) that surfaces hard-won axioms from experienced startup founders and operators — the pattern-matched wisdom that first-timers usually learn by running into walls.

## What it does

Founders face decisions where the right answer isn't obvious from first principles — it's obvious from pattern. This skill gives Claude access to a curated corpus of those patterns, organized by domain, with the context that makes each one useful.

When you ask Claude a founder-stage question — hiring, fundraising, product, sales, finance, co-founders, governance, crisis, or any of the surrounding territory — Claude consults this corpus and responds with the relevant axioms rather than working from generic priors.

The skill operates in two modes:

- **Direct mode** (default): Surfaces relevant axioms with reasoning and qualifiers. Useful when you want a quick read on a decision.
- **Socratic mode**: Asks the question the axiom answers, rather than handing you the answer. Useful for working through ambivalence, for coaching/mentoring conversations, and for processing live decisions.

## Domains covered

- Hiring, firing, comp, equity grants, the keeper test, and the AI-era talent shift toward systems thinkers
- Fundraising, terms, runway, investor relations
- Product, product-market fit, pivots, and where startup ideas come from — Paul Graham on noticing rather than inventing, and on schlep blindness
- Sales, pricing, GTM, the founder-as-seller, what a visionary customer is actually buying, and selling in the AI era — building the motion like a product, automating in order of workflow legibility
- Finance, cash, burn, CFO timing, ramen profitability, AI-pilot revenue and ERR, the operating metrics that matter (cohorts, NRR, Rule of 40, CAC payback, gross margin), and how to build the two models the axioms keep pointing at — the 13-week cash flow forecast and the Default Alive calculation
- Capital and valuation — cost of capital, dilution math, venture debt, ARR multiples, the liquidation waterfall, 409A, down rounds, secondaries, plus the procedures: computing your own waterfall off the charter, and running a down round
- Bootstrapping and the non-venture path — whether to raise at all, self-financeable growth, overtrading, annual prepay, revenue-based financing, SBIR grants, profit share and phantom equity, the plateau
- Exits and M&A — running a sale process, bankers, LOIs and exclusivity, diligence, earn-outs, escrow, retention packages, acqui-hires, headline price vs. actual payout
- Co-founder dynamics, splits, vesting, titles, and Noam Wasserman's rich-versus-king trade
- Boards and governance — board design, running the board like a team you lead, and why success is what gets founder-CEOs replaced
- Founder time, energy, sustainability, and where founder attention goes — the maker's schedule, the one top idea in your mind
- Customers and market dynamics, and Geoffrey Moore's chasm — why early adopters can't reference you to the mainstream
- Strategy, moats, and defensibility — Helmer's 7 Powers (including the math), Rumelt's kernel, Thiel, Greenwald, Christensen, Porter
- Management and execution — the IC-to-manager transition, delegation, 1:1s, meetings, org design, reorgs, the AI-era operating axioms, and the founder-mode counter-canon (Brian Chesky, Paul Graham)
- Crisis, layoffs, resilience, not dying as most of the strategy, and how to wind down when the answer is to stop — creditor priority, payroll withholding as trust money, dissolution vs. an assignment for the benefit of creditors vs. Chapter 7, the reserve that buys an orderly shutdown, and who you owe in what order
- Culture, vision, the cultural DNA of the first 20 employees, and talent density as the input every other freedom depends on
- Startup mechanics: incorporation, founder stock, IP assignment, vesting, and the founder exposures outside the corporate veil — personal guarantees, veil-piercing, trust-fund payroll taxes, claims-made D&O and tail coverage, sponsored immigration status, director duties near insolvency
- The YC canon, in two files — the essays (Paul Graham, Sam Altman, Jessica Livingston, Geoff Ralston, Paul Buchheit, Aaron Harris, Michael Seibel on fundraising) and the product/PMF material (Michael Seibel, Gustaf Alströmer, Eric Migicovsky, Dalton Caldwell, Peter Reinhardt)
- The Harvard Innovation Labs canon — talks hosted at the i-lab from Michael Skok's *Startup Secrets* series, Underscore VC partners (Lily Lyman, Chris Gardner), Alphabet X (Helen Riley), Megan Smith (3rd U.S. CTO), Phil Green, and Rebekah Emanuel
- Meta-wisdom: how to take advice, contextuality, founder peer groups

## Installation

Skills work in Claude.ai, Claude Code, and the Claude API. For other LLMs, see [Using with other LLMs](#using-with-other-llms) below.

- **Claude Code**: clone this repository (or copy `SKILL.md` and `references/`) into `~/.claude/skills/founder-wisdom/` for personal use, or `.claude/skills/founder-wisdom/` inside a project.
- **Claude.ai and the Claude API**: zip the repository contents (with `SKILL.md` at the root of the zip) and upload it through your client's skill settings.

For more on Claude Skills, see [Anthropic's skills documentation](https://docs.claude.com).

## Using with other LLMs

The corpus itself is plain provider-neutral markdown; only the skill packaging (frontmatter triggering, file-based progressive disclosure) is Claude-specific. The `dist/` directory carries generated artifacts for everything else:

- **`dist/founder-wisdom-full.md`** — the entire skill (routing guidance plus all twenty-one reference files) as one self-contained document, with file cross-links rewritten as section references. At roughly 75–80k tokens it fits in current large context windows: paste it into a Gemini Gem's instructions, a ChatGPT Project, or any long-context model's system prompt.
- **`dist/system-prompt.md`** — a short system prompt for platforms where the corpus lives in a retrieval store rather than in context (e.g. a ChatGPT Custom GPT with the reference files uploaded as knowledge). It carries the trigger conditions, the two modes, the section roster with routing notes, the stage-matching rules, and the output-style rules, plus an instruction to retrieve whole topic sections by name to compensate for chunk-based retrieval.

Both files are generated — never edit them by hand. The sources (`SKILL.md` and `references/`) remain the single source of truth; after changing them, regenerate with:

```bash
python3 scripts/build_bundle.py
```

The script is deterministic and fails loudly if the sources drift out of sync with its rewrites (e.g. a reference file missing from SKILL.md's routing list). To verify without writing anything — a build in memory, compared against the committed files, exiting non-zero when they differ:

```bash
python3 scripts/build_bundle.py --check
```

That is the command CI runs on every pull request. CI runs it against the committed tree while a local run reads your working copy, so commit the regenerated `dist/` alongside the sources it came from — a `--check` that passes on artifacts you rebuilt but never staged will still fail in CI.

## Use cases

The skill is designed to be useful for several distinct audiences:

- **Founders** wrestling with a specific decision or just trying to pattern-match where they are
- **Operators** (CEOs, COOs, VPs) who didn't found the company but face the same operating questions
- **Investors and advisors** who want to ground their guidance in the canonical wisdom
- **Executive coaches, mentors, and peer-advisors** working with founder-stage clients (Socratic mode is particularly designed for this)
- **Aspiring founders** learning the landscape before they start

## Philosophy

The corpus is **opinionated and pattern-matched, not neutral or comprehensive**. Every axiom in it has counter-examples. The value is in the encounter with the pattern, not in obedience to it.

The corpus is also **biased toward observed patterns from a particular slice of the startup world**: largely U.S., largely venture-backed, largely software. Geographic, sectoral, and structural exceptions exist and should be named when relevant.

The corpus is **sampled on outcome**: almost everything in it comes from founders and companies that worked. An axiom earns its place by how consistently the pattern shows up among survivors, not by how reliably it produces survival — the companies that ran the same play and died mostly didn't write essays. That is a different bias from the slice above and compounds with it, so where an axiom rests on a single company's practice the skill names the condition that practice ran on rather than presenting the result as a general law.

The skill is **not a substitute for qualified legal, financial, or specialized professional advice**. It's a thinking partner that knows the canonical wisdom, not an oracle.

## Attribution

The YC canon section attributes axioms to their sources: Paul Graham, Sam Altman, Jessica Livingston, Michael Seibel, Geoff Ralston, Paul Buchheit, and Aaron Harris, drawn from essays linked in [YC's Essential Startup Advice](https://www.ycombinator.com/blog/ycs-essential-startup-advice). The original essays remain the property of their authors. This skill paraphrases and synthesizes — it does not reproduce them.

Paul Graham's essays also supply material in the domain files outside the two canon files: "The Equity Equation," "Maker's Schedule, Manager's Schedule," "The Top Idea in Your Mind," "How Not to Die," "Ramen Profitable," "Default Alive or Default Dead?," "Startup = Growth," "How to Get Startup Ideas," "Schlep Blindness," and "Founder Mode." Each is cited inline where it is used; all are published at [paulgraham.com](https://paulgraham.com/articles.html).

The Harvard Innovation Labs canon is drawn from talks given at the i-lab — including Michael Skok's *Startup Secrets* workshops, Lily Lyman and Chris Gardner of Underscore VC, Helen Riley (CFO/COO of Alphabet X), Megan Smith (3rd U.S. CTO), Phil Green, and Rebekah Emanuel. Much of that material is published on the [Harvard Innovation Labs YouTube channel](https://www.youtube.com/@harvardilab), but not all of it is: where an axiom rests on a talk with no published recording, the reference file says so inline rather than letting the attribution read as a citation. The original talks remain the property of the speakers and Harvard Innovation Labs. This skill paraphrases and synthesizes — it does not reproduce them.

Axioms attributed to Brian Chesky, Jeanne DeWitt Grosser, and Elizabeth Stone are drawn from three episodes of Lenny's Podcast: Brian Chesky (Airbnb), "Brian Chesky's new playbook"; Jeanne DeWitt Grosser (Vercel; previously Stripe and Google), "What world-class GTM looks like in 2026"; and Elizabeth Stone (CPTO, Netflix), "Why Netflix is betting on systems thinkers - not specialists - in the AI era." The episodes remain the property of the speakers and the podcast. This skill paraphrases and synthesizes — it does not reproduce them.

The strategy and management sections draw on frameworks from published books: Hamilton Helmer's *7 Powers*, Richard Rumelt's *Good Strategy/Bad Strategy*, Peter Thiel's *Zero to One*, Bruce Greenwald's *Competition Demystified*, Clayton Christensen's *The Innovator's Dilemma*, and Michael Porter's work (via Joan Magretta) in `references/strategy-moats.md`; and Andy Grove's *High Output Management*, Ben Horowitz's *The Hard Thing About Hard Things*, Matt Mochary's *The Great CEO Within*, and Elad Gil's *High Growth Handbook* in `references/management-execution.md`. These books remain the property of their respective authors and publishers. This skill paraphrases and synthesizes their frameworks into a different format — it does not reproduce their text. Readers who want the full argument should consult the original books directly.

The co-founder, governance, and market sections draw on three more books: Noam Wasserman's *The Founder's Dilemmas* in `references/cofounders-equity.md` and `references/governance.md`; Geoffrey Moore's *Crossing the Chasm* in `references/customers-market.md`, `references/product.md`, and `references/sales-gtm.md`; and Brad Feld, Matt Blumberg, and Mahendra Ramsinghani's *Startup Boards* in `references/governance.md`. Three shorter sources sit alongside them — Thomas Hellmann and Noam Wasserman's paper "The First Deal," Fred Wilson's board posts on [AVC](https://avc.com), and the one-pager "Expectations for Outside Board Members," written by a portfolio CEO and reprinted on Brad Feld's blog, which the corpus keeps distinct from *Startup Boards*. These remain the property of their authors and publishers. The same rule applies: this skill paraphrases and synthesizes their frameworks — it does not reproduce their text.

Beyond the startup canon, a newer layer of the corpus reaches to older sources for its risk, incentive, and forecasting axioms — each cited inline where it is used, and introduced to the corpus for the first time here. Shakespeare's *King Lear*, who banishes the daughter who tells him the truth, stands behind the bad-news axiom in `references/culture.md`; Sophocles' *Oedipus the King*, who hunts the outsider whose corruption turns out to be himself, behind the you-are-the-constant pattern in `references/meta.md`; Charlie Munger's incentive-caused bias behind the advisor-incentive scan in `references/meta.md`, and his Persian-Messenger discussion — with *King Lear* — behind the bad-news axiom; Peter Thiel's power law from *Zero to One*, here in its founder-side sense, the fund's payoff distribution seen from the one path the founder travels, in `references/capital-valuation.md`, distinct from the *Zero to One* strategy material cited above; Ole Peters on ergodicity, the Kelly criterion, and Nassim Taleb on risk of ruin behind the survive-the-bet axiom in `references/finance-ops.md`; Jay Forrester and Donella Meadows on feedback delay and overshoot in system dynamics behind the signal-lag whipsaw in `references/finance-ops.md`; Daniel Kahneman and Amos Tversky's inside-versus-outside view with Bent Flyvbjerg's reference-class forecasting behind the reference-class downside in `references/finance-ops.md` and the outside-view move in `references/socratic-technique.md`; and Pierre-Simon Laplace's rule of succession with Philip Tetlock's forecasting research behind the calibration move in `references/socratic-technique.md`. These plays, papers, and books remain the property of their authors and publishers; as everywhere else in this corpus, the skill paraphrases and synthesizes — it does not reproduce their text.

The non-canon axioms in the corpus reflect widely-circulated startup wisdom that has no single attributable source. Where a specific person originated an axiom, attribution is given inline.

## Structure

```
founder-wisdom/
├── SKILL.md                          # The main routing logic for Claude
├── evals/                            # Behavioral scenarios that pin down SKILL.md
│   ├── scenarios.yaml
│   ├── check_scenarios.py
│   └── README.md
├── scripts/
│   └── build_bundle.py               # Generates dist/ from SKILL.md + references/
├── dist/                             # Generated artifacts for non-Claude LLMs (do not edit)
│   ├── founder-wisdom-full.md
│   └── system-prompt.md
└── references/
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

The reference files are designed to be readable on their own as well as consumed by Claude. If you want to browse the corpus directly, start with `references/meta.md` and `references/yc-canon.md`.

`references/yc-canon.md` and `references/yc-canon-product.md` are companion halves of the same canon: the first carries the essay-derived axioms and YC's pocket guide, the second the product and product-market-fit material.

`evals/` holds a small set of hand-checkable scenarios covering triggering, routing, mode selection, and output discipline. It is data plus instructions, not a test harness — see `evals/README.md`.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for what makes a good axiom, what kinds of additions are likely to be accepted, and what kinds are likely to be rejected.

A few general principles:

- **The corpus is opinionated by design.** "Add both sides" is usually the wrong instinct. If you have a counter-axiom that's genuinely true, propose it — but be willing to defend it as observed pattern, not just as balance.
- **Axioms must be quotable in one sentence.** If the axiom needs three sentences to state, it's not an axiom — it's an essay.
- **Attribution matters.** If you can trace an axiom to a specific person, name them.
- **Pattern, not just opinion.** The bar is "this has been observed across many companies," not "this seems right to me."

## License

This skill is released under the MIT License. See [LICENSE](LICENSE) for details.

The axioms themselves represent widely-circulated startup wisdom. The synthesis, organization, and skill machinery are MIT-licensed. The original YC essays remain the property of their authors; consult them directly via the sources named in `references/yc-canon.md`, `references/yc-canon-product.md`, and in the [YC Startup Library](https://www.ycombinator.com/library).

## Acknowledgments

This skill stands on the shoulders of the founders, operators, and investors who wrote down what they learned — particularly the Y Combinator partners whose essays form the YC canon section, and the speakers at Harvard Innovation Labs whose recorded talks form the i-lab canon section. It also reflects the broader community of operators who have made startup wisdom a generally accessible body of knowledge over the past two decades.
