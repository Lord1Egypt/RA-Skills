# Product & Strategy

## Core axioms

**If you're not embarrassed by your first version, you launched too late.** Reid Hoffman's line, still true. The cost of delay is the cost of unbuilt learning. The first version exists to test the riskiest assumption, not to be good.

**Do things that don't scale.** (Paul Graham.) Startups don't take off on their own — founders push them off, often through embarrassingly manual work: recruiting users one at a time, hand-delivering the product, doing as a human what you'll later automate. The 100-person founder who refuses to do this loses to the founder who'll fly across the country to onboard a single customer. See `yc-canon.md` for the full treatment of this axiom — it's foundational enough to warrant its own section there.

**The 90/10 solution.** (Paul Buchheit.) When sketching a 100% solution to a customer problem, pause and ask: what's the version that gets 90% of the value for 10% of the work? Almost always, one exists. The 100% version usually delays shipping by months for marginal additional value. Build the 90/10 version, ship it, and let the customer's reaction tell you whether the remaining 10% is worth building.

**Talk to customers. Then talk to more customers.** Founders who lose touch with customers lose product instinct within a year. Once you can't articulate, unprompted, what your 10 most engaged customers said last week, you're flying blind. Schedule customer calls on your calendar permanently — not as a project, as a recurring obligation.

**Beware the feature factory.** Shipping ≠ progress. The discipline is killing features, not adding them. Most product roadmaps are 60% noise — features that won customers in a single sales call, executive pet projects, "we said we would" features. The high-performing PM is the one who kills features, not the one who ships them.

**The riskiest assumption first.** Don't build the whole product before testing whether anyone wants it. Most failed startups built things beautifully that nobody needed. List your assumptions in descending order of "if this is wrong, we're dead" and test them in that order.

**Product-market fit feels like the building is on fire and you can't keep up.** If you're wondering whether you have it, you don't. Marc Andreessen's framing. The texture of real PMF is unmistakable: servers crashing, sales calls you can't return, customers using the product in ways you didn't anticipate, organic growth you didn't engineer.

**Pivot from a position of learning, not desperation.** Pivots driven by panic almost never work because they're not based on a new insight — they're based on the need to do something different. The good pivots come from founders who notice that customers are using the product for something other than the original purpose, and lean into that signal.

**Strategy is what you say no to.** A startup trying to serve three customer segments serves none well. The discipline is in the no's: no to the customer who would pay $5M but needs a feature you'd never build for anyone else, no to the adjacent market that "would be easy," no to the enterprise deal that requires deploying on-prem.

**Roadmaps are wishes; commitments are roadmaps.** What's on the public roadmap is aspirational. What's committed to a specific customer or quarter is the real roadmap. Founders who confuse the two over-promise externally and under-deliver internally.

**Your most engaged users tell you what to build next; your least engaged users tell you what's broken.** Power users are biased toward complexity and edge cases. Lapsed and churned users tell you where the friction is. Talk to both, weight accordingly.

**Build for the customer you have, not the customer you want.** A startup that builds for an aspirational enterprise buyer while serving SMBs ends up with a product that's too complex for SMBs and too immature for enterprise. Pick a customer and serve them ruthlessly well.

**The product is the entire experience, not the software.** Onboarding, support, billing, account management, contract terms — every touchpoint is the product. SaaS companies that obsess over the UI but have a 6-week onboarding ticket queue have a product problem, not a support problem.

**Vitamins lose to painkillers.** "Nice to have" products struggle even when they're well-built. "Has to have" products grow even when they're broken. If your customers can put off buying for a quarter without consequence, you have a vitamin problem — and the fix is usually finding a more acute customer segment, not improving the product.

**Differentiation has a half-life.** Whatever makes you special today gets copied within 18–24 months. The question isn't "what makes us unique now?" — it's "what will make us unique in two years?"

**The metric you optimize is the metric you'll hit, sometimes at the expense of everything else.** "Active users" optimized hard enough produces dark patterns. "Revenue" optimized hard enough produces churn six months later. Choose metrics with the awareness that the org will Goodhart them.

**Simple things at scale; complex things in the niche.** Mass-market products win by being radically simple. Niche products can be complex because the user is sophisticated enough to learn them. Trying to be both — complex *and* mass-market — is the most common positioning mistake.

**Build a Minimum Evolvable Product, not just a Minimum Viable Product.** (Gustaf Alströmer.) MVP asks "does this solve the problem at all?" MEP asks "can this adapt to what we learn from early users?" The earliest version only needs to survive contact with the first users and evolve from there. The product you have in five years will be a direct descendant of the product you build for your first users today — choose them carefully. See `yc-canon.md` for the full MEP treatment.

**Founder-market fit is its own variable, separate from product-market fit.** Some teams are uniquely suited to a particular problem; others aren't. The founder who spent five years building self-driving cars in research has 10/10 founder-market fit for a self-driving car startup. The founder with no domain experience has 0/10. Founders pivoting toward an idea where they have weak founder-market fit are usually about to make the next mistake. See `yc-canon.md` for Caldwell's idea-quality framework.

**For technical founders, building is the lowest-leverage way to reduce risk.** (Peter Reinhardt.) A technical team has ~90% odds of being able to build it and ~10% odds of solving a real problem. Time spent on validation interviews — finding out whether anyone actually has the problem — reduces risk far more than another week of coding does. Most failed technical-founder startups failed at conception, not execution.

**Iterate on a one-to-two-week cycle.** (Michael Seibel.) Anything longer breaks the feedback loop that makes startups work. Triage features as Easy (under a day), Medium (1–2 days), or Hard (a developer's full cycle). For hard ideas, ask which parts are useless versus genuinely hard — most "hard" features are also useless and should be cut entirely. Ship the rest fast.

**Measure PMF with the Sean Ellis / Superhuman 40% test.** Survey active users: "How would you feel if you could no longer use this product?" If more than 40% answer "very disappointed," you have PMF. Below that, you don't, regardless of growth rate. Pair with the qualitative tests (building on fire, can't keep up with demand) for triangulation.

**Use Rahul Vohra's PMF Engine to systematically move the score past 40%.** Vohra (Superhuman) turned the Ellis survey into a five-stage operational loop instead of a one-time diagnostic:
1. **Survey** users who have experienced the core product at least twice (ideally three weeks post-onboarding). Four questions: (a) How would you feel if you could no longer use the product? (b) What type of person would benefit most? (c) What is the main benefit you get? (d) How can we improve the product?
2. **Segment.** Filter to only the "very disappointed" cohort. Use their answers to question (b) to build a sharp persona — the **High Expectation Customer (HEC)**. Then re-run the PMF score using only users who match that persona. The HEC-filtered score is the one that matters.
3. **Analyze.** Why do the "very disappointed" users love it? What barriers stop the "somewhat disappointed" from reaching the same value?
4. **Decide.** Allocate roughly **50% of the roadmap to strengthening the core** loved by the very-disappointed, and **50% to removing friction** for the somewhat-disappointed. Not just feature requests — barriers to value.
5. **Track.** Re-run weekly, monthly, and quarterly to catch drift as you scale into new segments.

The HEC concept is the key insight. Without segmentation, the 40% test gives you an average that lies. With it, you find out whether you have PMF *for the right people* — and that's the only PMF that compounds into a real business.

**Bezos's Type 1 vs. Type 2 decisions.** Type 1 decisions are one-way doors: irreversible, high-consequence (changing your core architecture, signing a multi-year enterprise SLA, picking a primary pricing model, accepting a strategic investor). Treat them slowly, deliberately, with multiple options surfaced before committing. Type 2 decisions are two-way doors: reversible, low-consequence (a landing-page test, an outbound email variant, a feature MVP). Treat them fast, experimentally, and don't burn meetings on them. Most founders flip the polarity — debating two-way doors for weeks and walking through one-way doors on a Tuesday afternoon because everyone wanted to feel decisive.

**Jobs to be Done is the customer-centric reframe of "what is your product."** (Clayton Christensen.) Customers don't buy products; they "hire" products to do a job. The classic milkshake example: people weren't buying the milkshake for taste; they were hiring it to be a one-handed breakfast for a long commute. The reframe is useful when you're stuck explaining a product through its features — switch to articulating the job the customer is hiring you to do, and your positioning, pricing, and roadmap often re-sort themselves. The five Migicovsky questions in `yc-canon.md` are essentially a JTBD interview by another name.

**Two years of iteration is the realistic baseline for finding PMF.** (Seibel.) Founders who expect to find PMF in six months are usually wrong. The companies that do find it quickly are exceptional. Plan, fundraise, and pace yourselves for a multi-year journey.

**The Four U's: unworkable, unavoidable, urgent, underserved.** (Michael Skok.) A four-test triage for whether a problem deserves a company — sharper than the binary vitamins/painkillers split. *Unworkable* means consequences so bad someone gets fired (Skok's canonical example is the original iPhone activation failures). *Unavoidable* means death, taxes, aging, menopause — biology and regulation, not preference. *Urgent* means it beats the customer's other top-three priorities, not just yours. *Underserved* means no adequate alternative exists. A problem that scores on three of four is interesting; one that scores on all four is the right one to start.

**Set the kill criterion before you start, not after you're attached.** (Helen Riley, Alphabet X.) X's Matera plastics moonshot launched with a pre-declared economic threshold — "must be cheaper than virgin plastic" — and the team would have shut it down had they not hit it. Most founders define kill conditions only retrospectively, by which point ego, sunk cost, and team loyalty have made the call impossible. Write the failure condition down on day one and tape it to the wall. The pre-emptive version of the existing "killing too late" mistake.

**The Five Whys yields a stack of viable companies, not one root cause.** (Rebekah Emanuel.) The textbook use peels through layers of cause to reach the "real" problem. The founder's reframe: each layer is a complete startup. Better cleaning chemicals, spider-deterrent coatings, insect-population shifts, lighting-cycle redesigns — Emanuel's Lincoln Memorial example surfaces four companies in one exercise. Pick the layer that matches your founder-market fit and go deep; don't keep peeling.

## Common founder mistakes

- Treating customer requests as a backlog instead of a signal. Every request is a data point about what's missing — but the right response is usually a smaller insight than the literal feature request.
- Building for the demo. Demo-driven development creates products that look great in 5-minute walkthroughs and fall apart on day 30.
- Confusing usage with value. Users opening the app daily isn't proof of value — it could be a habit, addiction, or required workflow. Value is willingness to pay, willingness to recommend, and willingness to stay when a competitor shows up.
- Killing too late. A failing product line drains attention from the working one. The decision to sunset a product is usually made 6–12 months after it should have been.
- Asking "what features would you like?" Users are better at identifying problems than identifying solutions. The famous (probably apocryphal) "faster horses" line captures the failure mode. See `yc-canon.md` for Eric Migicovsky's five-question user-interview framework.
