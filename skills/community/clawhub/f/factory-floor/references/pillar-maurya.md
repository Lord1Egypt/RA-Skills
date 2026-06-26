# Pillar 2: The Customer Factory (Ash Maurya) — Reference

## Contents
- [Origin](#origin)
- [The Customer Factory Blueprint](#the-customer-factory-blueprint)
- [Key Definitions](#key-definitions)
- [Constraint Identification by Stage](#constraint-identification-by-stage)
- [The GOLEAN Framework](#the-golean-framework)
- [The Referral Loop and Viral Coefficient](#the-referral-loop)
- [The Local vs. Global Optimization Trap](#the-local-vs-global-optimization-trap)
- [The Premature Optimization Warning](#the-premature-optimization-warning)
- [Connecting to Goldratt](#connecting-to-goldratt)
- [Throughput Accounting on the Lean Canvas](#throughput-accounting-on-the-lean-canvas)

## Origin

Ash Maurya created the Customer Factory model in *Scaling Lean* (2016),
explicitly building on Goldratt's Theory of Constraints. As Maurya puts it:
"The Theory of Constraints was a key influence — I adapted his focusing steps
for systems thinking to the business modeling process."

The core idea: treat your business as a factory whose output is happy customers.
Apply the same constraint-thinking Goldratt used on manufacturing floors to the
steps of creating, delivering, and capturing value.

## The Customer Factory Blueprint

Every business — B2B, B2C, SaaS, services, hardware — has the same five
macro steps:

```
[Unaware Visitors]
       ↓ Acquisition
[Interested Prospects]
       ↓ Activation
[Active Users / Trialists]
       ↓ Revenue
[Paying Customers]
       ↓ Retention
[Retained Happy Customers]
       ↓ Referral
[New Unaware Visitors from word-of-mouth]
```

Each step has a conversion rate. Each step has capacity. The step with the
lowest throughput relative to your goal is your constraint.

## Key Definitions

**Throughput** = the rate at which you create happy customers. Not signups. Not
pageviews. Not MQLs. Happy customers who achieve their desired outcome and
pay you for it. This is traction.

**Happy customers ≠ customers made happy.** Making customers happy is easy —
give them stuff for free. Making happy customers means helping them achieve
results (desired outcomes). Happy customers get you paid.

**Traction** = the rate at which a business model captures monetizable value
from its customers. Not the same as current revenue. Revenue is a lagging
indicator. Traction is the leading indicator.

## Constraint Identification by Stage

Maurya maps the typical constraint to the startup's maturity stage:

### Pre-Problem/Solution Fit
**Typical constraint: The problem itself.**
Are you solving a real problem that's painful enough for people to switch from
their current solution? If not, no amount of engineering or marketing matters.

**Actions:** Customer interviews. Lean Canvas stress-testing. Demo the problem,
not the solution. Validate willingness to pay before building.

**The Innovator's Bias and the Innovator's Gift (from *Running Lean*)**

The **Innovator's Bias** is the #1 contributor to startup failure: falling in
love with your solution before validating the problem. Maurya: "When you've
decided you want to build a hammer, everything starts looking like a nail."
Founders unconsciously invent problems to justify the solution they already
want to build, then seek just enough evidence to convince themselves they're
on track. Intelligence makes the bias worse — smart founders rationalize
more effectively, not more honestly. The bias is "immune to lecture" — you
can't overcome it through awareness alone. You need systemic countermeasures.

The antidote is the **Innovator's Gift**: the realization that **new problems
worth solving are created as by-products of old solutions.** To build
something better, it must be better *relative to* what customers use today.
The starting point is always the existing alternative — not your idea.

Maurya's prescribed Lean Canvas fill order makes this concrete: start with
**Existing Alternatives** (what customers use now), then **Problems** (what's
broken about those alternatives), then everything else. Existing Alternatives
is the most important Lean Canvas building block — more important than the
Problem box itself, because without it, you're defining problems in a vacuum.

**Maurya's Lean Canvas questions** and the **Napkin Test** are the core
pre-building tools. See `stages/pre-revenue.md` for the full operational
versions (the questions to ask and the math to run). The Lean Canvas is a
set of hypotheses to test, ordered by risk — test the riskiest assumption
first.

**The Mafia Offer** — an offer so good customers can't refuse, tested
BEFORE building an MVP. Maurya's sequence: **Desirability → Feasibility →
Viability.** Test whether people want this (Mafia Offer) before testing
whether you can build it (MVP) before testing whether the business model
works at scale (traction metrics).

**The 3x rule:** The offer must promise at least a 3x improvement over the
existing alternative on the dimension the customer cares about most. Not 10%
better — dramatically, obviously better. Anything less won't overcome
switching costs and inertia.

See `stages/pre-revenue.md` for the operational template and commitment test.

### Problem/Solution Fit → Product/Market Fit
**Typical constraint: Activation.**
People sign up but don't get value. Time-to-value is too long. The aha moment
doesn't arrive. Churn is high because customers never actually activated.

**Actions:** Concierge onboarding. Measure time-to-first-value. Reduce steps
to activation. Talk to churned users — most churned before they ever really
used the product.

### Product/Market Fit → Scale
**Typical constraint: Acquisition.**
The product works. Users who activate tend to stay. But not enough people enter
the funnel. Growth is flat.

**Actions:** Channel experiments. Positioning refinement. Pricing changes.
Apply Sharp's mental/physical availability framework. This is where "nobody
knows you exist" becomes the bottleneck.

### Scale
**Typical constraint: Retention or Revenue.**
The machine runs but leaks. Customers churn, or they stay but don't expand.
Unit economics don't work at volume.

**Actions:** Churn analysis. Expansion revenue. Pricing optimization.
Investigate whether "happy" customers are actually achieving desired outcomes.

## The GOLEAN Framework

Maurya's tactical cycle for continuous improvement at the constraint:

- **G**o — Identify the constraint. Set a goal for improving it.
- **O**bserve — Measure current performance at the constraint.
- **L**earn — Run experiments to address the constraint.
- **E**valuate — Did throughput increase? Was the constraint broken?
- **A**nalyze — Reconcile learnings. Systemize what worked.
- **N**ext — If constraint broken, identify the next one. If not, run another
  experiment. Repeat.

Each cycle should be 2 weeks (a "LEAN sprint"). Fast enough to learn, slow
enough to execute meaningfully.

## The Referral Loop and Viral Coefficient

The referral step in the customer factory is the only step that creates a
reinforcing loop — retained happy customers generate new unaware visitors,
feeding the top of the funnel. When the loop is strong, each cohort of
customers generates part of the next cohort, reducing the cost of
acquisition over time.

### The viral coefficient (K)

K = (number of invitations per customer) × (conversion rate of invitations)

- **K > 1:** Viral growth. Each customer generates more than one new customer.
  The product grows without paid acquisition. Extremely rare — Dropbox,
  WhatsApp, and early Slack are canonical examples.
- **K = 0.5 to 1:** Amplified growth. Referrals supplement acquisition but
  don't sustain it alone. Each dollar of acquisition spend is amplified by
  word-of-mouth.
- **K < 0.5:** Referral is negligible. Growth depends entirely on direct
  acquisition.

Most startups pre-scale have K < 0.3. This is normal. Referral is rarely
the constraint early — you need enough happy customers to generate meaningful
referral volume, and you need the rest of the factory working first.

### When to invest in referral

Referral becomes high-leverage when three conditions are met:
1. **Retention is strong** — customers stay long enough to refer.
2. **The product delivers the job** — customers achieve their desired outcome
   and would naturally tell peers.
3. **The referral mechanism is frictionless** — sharing is built into the
   product flow, not bolted on as an afterthought.

If any of these is missing, investing in referral programs is premature.
Fix retention and activation first — a referral from a customer who churns
in 30 days is negative signal, not growth.

### Types of referral loops

**Word-of-mouth (passive):** Customers mention you in conversation. Not
engineered. Driven entirely by how well the product delivers the job. The
strongest form long-term, but slowest to build.

**Inherent virality:** The product requires or benefits from multiple users.
Collaboration tools, shared workspaces, team messaging. Each user invited is
a potential new customer. The product IS the referral mechanism.

**Incentivized referral:** Discounts, credits, or features unlocked for
referring. Effective for boosting K when the base product already generates
organic referrals. Dangerous when used as a substitute for authentic demand
— incentivized referrals from unhappy customers create churn, not growth.

**Content as referral:** The product's output is shareable — reports, designs,
dashboards, summaries. When the output carries your brand and demonstrates
value, every share is a referral. This is also a "feature that IS
distribution" (see Sharp's framework).

### The reinforcing loop

When referral works, it creates a compounding cycle:

```
More customers → More referrals → More acquisition → More customers
```

A small improvement at any point in this loop accelerates the whole cycle.
This is why, once retention is solid and the factory is flowing, even modest
referral improvements can produce outsized growth.

Maurya's caution: the loop is fragile. If retention breaks (customers churn
before referring), if activation breaks (referred users don't reach the aha
moment), or if the product stops delivering the job, the loop collapses. The
referral step depends on every upstream step working. Fix the factory first,
then amplify with referral.

---

## The Local vs. Global Optimization Trap

This is the most common mistake Maurya identifies in growing startups. Teams
optimize their local metrics while system throughput stagnates or declines:

- **Marketing** generates more leads → but leads are lower quality → conversion
  drops → net throughput unchanged.
- **Sales** closes more deals via aggressive tactics → customers churn faster →
  net throughput unchanged.
- **Engineering** ships more features faster → but features don't address the
  bottleneck → customers don't activate better → net throughput unchanged.

The antidote: every team's effort must be evaluated against system throughput
(happy paying customers created), not local metrics (leads generated, features
shipped, deals closed).

## The Premature Optimization Warning

Maurya: "Going fast on everything is a recipe for getting lost faster."

The counter-intuitive move is slowing down to build a repeatable customer
factory in stages. Each stage is a smaller version of the next stage. You
can't scale what isn't first repeatable.

**When is something repeatable?** When you know where your next 10 customers
will come from. Random isn't repeatable. Repeatable is what scales.

**Focus on repeatability right after your first sale.** If you don't establish
repeatable sales quickly, you get pulled in many directions, lose focus, and
hit a wall.

## Connecting to Goldratt

Maurya's explicit connection: "How do you know when a constraint is broken?
When your customer factory throughput goes up as a result of something you
just did."

The customer factory IS the system. The five macro steps ARE the machines on
the factory floor. The conversion rates ARE the machine capacities. The
constraint IS the machine with the lowest throughput relative to demand.

Goldratt's Five Focusing Steps map directly:

| Goldratt step | Customer factory equivalent |
|---|---|
| Identify | Which of the 5 steps has the lowest rate relative to goal? |
| Exploit | Improve that step's conversion with existing resources. |
| Subordinate | All other teams serve that step. Pause work that doesn't. |
| Elevate | Invest in that step — hire, buy tools, redesign. |
| Repeat | Constraint moves to next weakest step. Re-identify. |

## Throughput Accounting on the Lean Canvas

Maurya adapts Goldratt's throughput accounting to the business model:

- **Throughput** maps to the Revenue Streams box of the Lean Canvas. Focus on
  maximizing revenue potential (pricing, right customers) before optimizing
  costs.
- **Operating Expense** maps to the Cost Structure box. There's a floor — you
  can only cut so much. The upside potential is on the revenue side.
- **Inventory** maps to everything in progress but not yet generating revenue:
  features being built, leads being nurtured, customers being onboarded.

Maurya: "Yes, we want to worry about cost-cutting and efficiency, but the
bigger potential here is thinking about upside potential." This is Goldratt's
hierarchy (T > I > OE) restated for the startup context.
