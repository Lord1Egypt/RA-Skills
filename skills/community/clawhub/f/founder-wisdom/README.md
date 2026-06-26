# Founder Wisdom

A [Claude Skill](https://www.anthropic.com/news/skills) that surfaces hard-won axioms from experienced startup founders and operators — the pattern-matched wisdom that first-timers usually learn by running into walls.

## What it does

Founders face decisions where the right answer isn't obvious from first principles — it's obvious from pattern. This skill gives Claude access to a curated corpus of those patterns, organized by domain, with the context that makes each one useful.

When you ask Claude a founder-stage question — hiring, fundraising, product, sales, finance, co-founders, governance, crisis, or any of the surrounding territory — Claude consults this corpus and responds with the relevant axioms rather than working from generic priors.

The skill operates in two modes:

- **Direct mode** (default): Surfaces relevant axioms with reasoning and qualifiers. Useful when you want a quick read on a decision.
- **Socratic mode**: Asks the question the axiom answers, rather than handing you the answer. Useful for working through ambivalence, for coaching/mentoring conversations, and for processing live decisions.

## Domains covered

- Hiring, firing, comp, and equity grants
- Fundraising, terms, runway, investor relations
- Product, product-market fit, pivots
- Sales, pricing, GTM, the founder-as-seller
- Finance, cash, burn, CFO timing
- Co-founder dynamics, splits, vesting
- Boards and governance
- Founder time, energy, sustainability
- Customers and market dynamics
- Crisis, layoffs, resilience
- Culture, vision, and the cultural DNA of the first 20 employees
- Startup mechanics: incorporation, founder stock, IP assignment, vesting
- The YC canon (Paul Graham, Sam Altman, Jessica Livingston, Michael Seibel, Geoff Ralston, Paul Buchheit, Aaron Harris, Gustaf Alströmer, Dalton Caldwell, Eric Migicovsky, Peter Reinhardt, Tim Brady)
- The Harvard Innovation Labs canon — talks hosted at the i-lab from Michael Skok's *Startup Secrets* series, Underscore VC partners (Lily Lyman, Chris Gardner), Alphabet X (Helen Riley), Megan Smith (3rd U.S. CTO), Phil Green, and Rebekah Emanuel
- Meta-wisdom: how to take advice, contextuality, founder peer groups

## Installation

Download `founder-wisdom.skill` from the latest release and install it through your Claude client's skill settings. Skills work in Claude.ai, Claude Code, and the Claude API.

For more on Claude Skills, see [Anthropic's skills documentation](https://docs.claude.com).

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

The skill is **not a substitute for qualified legal, financial, or specialized professional advice**. It's a thinking partner that knows the canonical wisdom, not an oracle.

## Attribution

The YC canon section attributes axioms to their sources: Paul Graham, Sam Altman, Jessica Livingston, Michael Seibel, Geoff Ralston, Paul Buchheit, and Aaron Harris, drawn from essays linked in [YC's Essential Startup Advice](https://www.ycombinator.com/blog/ycs-essential-startup-advice). The original essays remain the property of their authors. This skill paraphrases and synthesizes — it does not reproduce them.

The Harvard Innovation Labs canon is drawn from talks recorded at the i-lab and published on the [Harvard Innovation Labs YouTube channel](https://www.youtube.com/@harvardilab) — including Michael Skok's *Startup Secrets* workshops, Lily Lyman and Chris Gardner of Underscore VC, Helen Riley (CFO/COO of Alphabet X), Megan Smith (3rd U.S. CTO), Phil Green, and Rebekah Emanuel. The original talks remain the property of the speakers and Harvard Innovation Labs. This skill paraphrases and synthesizes — it does not reproduce them.

The non-canon axioms in the corpus reflect widely-circulated startup wisdom that has no single attributable source. Where a specific person originated an axiom, attribution is given inline.

## Structure

```
founder-wisdom/
├── SKILL.md                          # The main routing logic for Claude
└── references/
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

The reference files are designed to be readable on their own as well as consumed by Claude. If you want to browse the corpus directly, start with `references/meta.md` and `references/yc-canon.md`.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for what makes a good axiom, what kinds of additions are likely to be accepted, and what kinds are likely to be rejected.

A few general principles:

- **The corpus is opinionated by design.** "Add both sides" is usually the wrong instinct. If you have a counter-axiom that's genuinely true, propose it — but be willing to defend it as observed pattern, not just as balance.
- **Axioms must be quotable in one sentence.** If the axiom needs three sentences to state, it's not an axiom — it's an essay.
- **Attribution matters.** If you can trace an axiom to a specific person, name them.
- **Pattern, not just opinion.** The bar is "this has been observed across many companies," not "this seems right to me."

## License

This skill is released under the MIT License. See [LICENSE](LICENSE) for details.

The axioms themselves represent widely-circulated startup wisdom. The synthesis, organization, and skill machinery are MIT-licensed. The original YC essays remain the property of their authors; consult them directly via the links in `references/yc-canon.md` and in the [YC Startup Library](https://www.ycombinator.com/library).

## Acknowledgments

This skill stands on the shoulders of the founders, operators, and investors who wrote down what they learned — particularly the Y Combinator partners whose essays form the YC canon section, and the speakers at Harvard Innovation Labs whose recorded talks form the i-lab canon section. It also reflects the broader community of operators who have made startup wisdom a generally accessible body of knowledge over the past two decades.
