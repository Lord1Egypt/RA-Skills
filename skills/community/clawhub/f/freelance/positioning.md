# Positioning — What You Sell, and to Whom

Scope: the offer, the niche, and the proof that makes a stranger believe it. Winning a specific deal is `pipeline.md` and `clients`; pricing the offer is `rates.md`.

**Before advising**, read `## Practice`, `## Win/Loss` and any positioning decision in `artifacts/` named by `## Boxes` in `~/Clawic/data/freelance/memory.md`. Repositioning a practice that already decided this last quarter is churn.

**Contents:** [The Offer Sentence](#the-offer-sentence) · [Choosing a Niche](#choosing-a-niche) · [Is the Niche Big Enough](#is-the-niche-big-enough) · [Proof Beats Copy](#proof-beats-copy) · [The Case Study Format](#the-case-study-format) · [Portfolio Rights](#portfolio-rights) · [Minimum Viable Presence](#minimum-viable-presence) · [Repositioning](#repositioning)

## The Offer Sentence

One sentence, in the buyer's words, containing three things: **who it is for · the problem · the outcome**. "I do backend development" fails all three; "I make payments reconciliation close in a day for fintechs that currently spend a morning on it" passes.

- The test: could a referrer forward it and would the recipient recognize their own problem in it? If it needs explaining, it is a job title, not an offer.
- Say the **problem in the buyer's vocabulary**, not the trade's. Buyers search for their symptom, never for your technique.
- **Name the deliverable and the outcome separately.** "A rebuilt onboarding flow" is what they get; "activation up, support tickets down" is why they pay.
- Avoid seniority words ("expert", "passionate", "10x"). They are unfalsifiable and read as noise; a number in a case study does the work they claim to do.

## Choosing a Niche

Three axes, and it only takes one to be specialized — combining all three usually makes the market too small.

| Axis | Example | Strength | Risk |
|---|---|---|---|
| Industry | Fintech, clinics, e-commerce | Domain language, referrals travel inside the sector, premium for compliance familiarity | Sector downturn takes the whole book |
| Problem | Migrations, reconciliation, accessibility audits, launch copy | Highest premium; urgent problems have budget | Runs out if the problem is one-off per client |
| Buyer type | Seed startups, agencies, public sector | Consistent sales cycle and procurement path | Buyer's funding climate is your climate |

- **Specializing shortens the sales cycle more than it raises the rate.** Both improve, but the cycle effect is what changes the year: fewer, better-qualified conversations.
- **Repeatability decides.** A niche whose engagements repeat (retainers, recurring audits, seasonal work) is worth more than a higher-paying one that ends permanently at delivery.
- **Keep a second competence quiet.** Publicly specialized, privately capable of the adjacent work — that is how a niche survives its sector's bad year without diluting the message.

## Is the Niche Big Enough

Arithmetic, not intuition:

```
buyers_needed_per_year = target_income ÷ average_engagement_value
reachable_buyers       = companies in the niche you can actually contact
```

Take a 5-15% conversion from reachable-and-contacted to client over a year, and a client base that turns over ~30% annually. Needing 8 clients a year from 60 reachable buyers is tight but workable; needing 8 from 15 is a hobby with a website. Under ~200 reachable buyers, widen an axis — and say that plainly rather than optimizing the copy.

## Proof Beats Copy

Ranked by what actually converts a stranger, best first:

1. **A referral from someone they trust** — arrives pre-sold; positioning's real job is to make you referable in one sentence.
2. **A case study with a measured outcome** in their situation.
3. **A named client list**, where the names are recognizable to that buyer.
4. **Public work** that demonstrates the skill directly: a teardown, an audit, an open repository, a published piece.
5. **Testimonials with specifics.** "Great to work with" converts nobody; "cut our close from four hours to thirty-five minutes" does.
6. **Certifications**, which matter in regulated and enterprise procurement and almost nowhere else.
7. **A polished site with no proof on it**, which is where most first-year effort goes and which converts near zero.

## The Case Study Format

Six lines, one page maximum. Longer does not get read.

```
Client (or "a fintech with ~80 staff" if anonymized)
Problem: the situation in their words, with the cost of it
What I did: three bullets, decisions not tasks
Outcome: a measured number, with the before and the after
Timeframe and basis: 6 weeks, fixed price
What they said: one quoted sentence
```

- **Get the number at delivery.** Nobody will measure it for you three months later, and an unmeasured outcome downgrades to a testimonial.
- **Anonymize rather than omit** when the client will not be named: sector, size and the number keep almost all of the persuasive force.
- One case study per niche axis is enough; a third one in the same niche adds nothing a second did not.
- Store each at `artifacts/case-study-<client>.md` with the rights recorded in its header.

## Portfolio Rights

The right to show the work is negotiated once, in the contract, and is worthless afterwards.

- **Ask at signature**, when goodwill and leverage are highest. The clause is short: the right to display the work and describe the outcome, with named exclusions.
- **Three tiers to offer** when the client resists: full case study with their name → anonymized sector plus metrics → logo only, no detail. Most refusals accept the second.
- **NDAs usually block naming, not describing.** Confidentiality covers their information; an anonymized outcome you produced is generally still tellable — check the specific wording before assuming either way.
- Record the agreed tier in the engagement's `Portfolio rights` field the day it is signed. A year later nobody remembers, and the default is silence (`contracts.md`).

## Minimum Viable Presence

Enough to be believed, no more. Anything beyond this is procrastination dressed as marketing.

| Asset | Minimum | Why it is enough |
|---|---|---|
| One page that states the offer sentence, three proofs and a way to contact | Yes | It is the link a referrer sends; it does not have to attract anyone by itself |
| A profile on the one network your buyers use | Yes | Buyers verify you exist before replying |
| Two or three case studies | Yes | The actual conversion asset |
| Email at your own domain | Yes | Costs almost nothing and is checked more than people admit |
| Blog, newsletter, video, logo, brand system | Only after the pipeline works | These are amplifiers of an offer that already converts, never a substitute for one |

## Repositioning

- **Trigger it on data, not on boredom**: a win rate under ~20% on qualified leads, inbound arriving for work you do not want, or the offer sentence needing a paragraph to explain.
- **Change one axis at a time.** Changing industry, problem and buyer together makes the result unattributable and burns the referral network built on the old message.
- **Give it two quarters** before judging. A repositioning judged after six weeks is always judged as a failure, because the pipeline lag alone is longer than that.
- **Tell the existing network explicitly.** People refer the version of you they last heard about; an unannounced repositioning keeps producing the old leads for a year.

**After any positioning decision** — niche, offer sentence, or a repositioning — write `~/Clawic/data/freelance/artifacts/decision-<topic>.md` with the decision in one sentence, what was rejected and why, the cost of the choice, and the condition that would revisit it; add its `## Boxes` line in the same turn and update `## Practice` in `memory.md`. **Every case study** becomes its own artifact with its portfolio-rights tier in the header, and the tier is copied into the engagement row in `## Engagements`.
