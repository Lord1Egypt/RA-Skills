# Marketplaces — Channel or Cage

Scope: deciding whether a freelance marketplace is a rational channel, what it really costs, and how to leave without losing the clients. Per-platform tactics — profile, proposals, gig SEO, level systems — are `upwork` and `fiverr`.

**Before advising on a platform**, read `## Platforms` and `## Win/Loss` in `~/Clawic/data/freelance/memory.md`, and `channels` in `config.yaml`. Fee schedules and level rules change often: treat any number here as a ratio to verify on the platform's current fee page before it moves money.

**Contents:** [All-In Commission](#all-in-commission) · [The Platform Map](#the-platform-map) · [When a Marketplace Is Rational](#when-a-marketplace-is-rational) · [The Rate Ceiling](#the-rate-ceiling) · [Escrow and Payment Protection](#escrow-and-payment-protection) · [Ratings as Collateral](#ratings-as-collateral) · [Going Off-Platform](#going-off-platform) · [Automation and Account Rules](#automation-and-account-rules) · [Exiting](#exiting)

## All-In Commission

The advertised take rate is never the cost. Compute the real one over a full period:

```
all_in_commission = (service fees + lead costs + membership + withdrawal and FX fees + unbilled proposal time × your rate)
                    ÷ revenue earned on the platform, same period
```

- **Lead costs are the hidden half.** Bid credits or connects spent on proposals that went nowhere are a customer-acquisition cost. Fifteen credits spent to win one job is the number that matters, not the credit price.
- **Unbilled proposal time is real.** Twenty minutes per proposal at your rate, times the proposals it takes to win one, often exceeds the service fee.
- **Withdrawal and FX**: the platform's conversion spread plus the transfer fee, often several percent for a non-domestic freelancer (`international.md`).
- A well-run marketplace practice lands in the 15-30% all-in range. Above 40%, it is a lead-generation subscription with a bad price, not a channel.

Record the observed number and the date in `## Platforms` — advertised rates change, and your own history is the only reliable input to the next decision.

## The Platform Map

Positioning of the main categories. Verify current fees and thresholds before quoting them to a user.

| Platform type | Examples | Economics | Fits |
|---|---|---|---|
| Hourly/project marketplace with escrow | Upwork, Freelancer.com | Percentage service fee on earnings, plus paid bids/connects and optional memberships; escrow and hour-tracking protection | Ongoing contracts, hourly work, clients who want protection too (`upwork`) |
| Productized gig marketplace | Fiverr | High flat commission on each order, discovery driven by search and conversion, seller levels gate visibility | Repeatable, packaged deliverables with a fixed scope (`fiverr`) |
| Vetted talent network | Toptal and similar | No bidding; the network sets or negotiates the rate and matches clients; heavy screening to join | Senior specialists who dislike selling and accept a managed rate |
| Contract/staffing marketplaces and recruiters | Local and sector-specific | Margin taken from the bill rate, often invisible | Long full-time-shaped contracts — check `classification.md` first |
| Niche and community boards | Trade- or stack-specific | Usually free or a listing fee, no escrow, no protection | Specialists; treat as an inbound source, not a platform |

## When a Marketplace Is Rational

Use one deliberately, with an exit date, when at least one holds:

- **No proof yet.** Ratings and completed contracts substitute for a portfolio in the first months, and they compound faster than an unread personal site.
- **Cross-border credibility gap.** A buyer who would not wire money to a stranger abroad will pay through escrow.
- **Bounded capacity to fill.** A predictable channel for the two days a week nobody else booked.
- **The buyer only buys there.** Some companies' procurement is genuinely wired into one marketplace.

It is not rational as a permanent primary channel for a specialist: the all-in commission plus the rate ceiling means the same hours sold directly pay 30-60% more, and every platform hour is one not spent building an owned channel (`pipeline.md`).

## The Rate Ceiling

Marketplace prices are set by global supply meeting a search ranking, not by the value you deliver. Consequences to state plainly:

- The visible "market rate" on a platform is a floor-seeking number. Reading it as your market is the most common cause of a rate under the derived floor (`rates.md`).
- Rate movement inside a platform is slow and capped: reputation raises what you can charge, but the buyer population is anchored by the cheapest visible alternative.
- **The escape is packaging, not bidding.** A defined outcome with a fixed price competes on scope clarity; an hourly rate competes with everyone on earth.
- Test the ceiling honestly: quote the direct-client rate on the platform for a quarter and read the win rate. If it holds, the platform is a channel; if it collapses, it is a segment you are pricing wrong for.

## Escrow and Payment Protection

The real product a marketplace sells, and the reason its commission is not simply theft.

| Protection | What it actually covers | Where it fails |
|---|---|---|
| Milestone escrow (fixed price) | Funds deposited before work; released on approval | Unfunded milestones protect nothing — verify funding *before* starting each one |
| Hourly protection with tracked time | Hours logged by the platform's tracker are covered against non-payment | Manual time entries typically are not; untracked hours are unprotected |
| Dispute mediation | Platform arbitration on evidence in the platform's messages | Anything agreed off-platform is invisible to it — and often a ToS breach besides |
| Payment verification | Marks whether the client's payment method is real | Verified is not solvent; a first-time client with no hire history is still a risk |

Keep the whole trail inside the platform for the life of the contract: scope, changes, approvals, deliveries. In a dispute, the messages are the case (`disputes.md`).

## Ratings as Collateral

A rating is an asset with strange mechanics, and treating it as one changes decisions.

- **Averages are sticky both ways.** Early ratings dominate for a long time; a single bad score in the first ten orders takes many good ones to dilute, which is why the first jobs should be small and comfortably inside your competence.
- **Cancellations and late deliveries usually cost more than a mediocre review**, because completion and response metrics feed the ranking directly. Read your platform's actual metric list before optimizing anything.
- **A rating does not travel.** Everything invested in it is a switching cost the platform is deliberately building. It is a reason to leave earlier, not later.
- **Never buy, trade or solicit fake reviews.** It is instant permanent removal on every major platform, and on some it is fraud.

## Going Off-Platform

Platforms prohibit circumventing fees, and the rule is enforced by message scanning and by the client's own incentives. What is generally allowed and what is not:

- **Not allowed**: sharing contact details before a contract exists, asking to pay outside the platform, or taking a platform-sourced client direct while a contract or the platform's exclusivity window is running. Consequence ladder is warning → restriction → suspension → permanent ban, plus loss of escrow protection and any pending funds.
- **Usually allowed**: continuing with a client outside the platform after the contracted period ends, or after paying the platform's contract-buyout fee where one exists.
- **The correct move** is to read the specific platform's terms, wait out or buy out the window, and move the relationship with a proper contract, deposit and terms on your own paper (`contracts.md`).
- A client who pushes to go direct *before* a contract exists is a red flag, not an opportunity: they are demonstrating how they treat agreements, and the escrow you would lose is protecting you from exactly them.

## Automation and Account Rules

Every major platform's terms converge on the same list. Breaking it risks the account and the earnings in it.

- **Prohibited everywhere**: auto-submitting proposals at scale, mass or automated messaging, account sharing, one person operating under another's identity, scraping, and evading rate limits or captchas.
- **Generally allowed**: AI-assisted drafting that a human reviews and sends manually; using AI in the delivered work where the category permits it.
- **Identity is the bright line.** Every major platform requires the account to be operated by the real person it names. Assistance is a tool; a persona, a fabricated portfolio, a synthetic profile photo presented as you, or a review you wrote is fraud (SKILL.md Rule 9).
- **The consequence ladder is the same everywhere** — warning → restriction → suspension → permanent ban — with pending earnings and escrowed funds at risk from the second step, and identity or payment fraud referred onward rather than merely banned.
- Disclosure requirements differ by platform and by client contract — follow `ai_disclosure` and the contract, and disclose when asked, always. A platform's terms are themselves a contract: breaching them with automation is a breach of contract, not only a policy matter.

## Exiting

Leave on a plan, not on a bad month.

1. Set the exit trigger in advance: a revenue level from owned channels, a date, or an all-in commission ceiling. Write it into `## Platforms`.
2. Stop bidding, keep delivering. Ratings decay slowly; unfinished contracts do not.
3. Move eligible clients only after the contract or exclusivity window closes, onto your own contract, deposit and terms.
4. Leave the account dormant rather than deleted where the platform allows it — reactivating a rated account is cheaper than earning a rating twice.
5. Reallocate the freed hours to the two channels with the best source numbers in `## Pipeline`, not to "marketing" in general.

**After any platform session**, update `## Platforms` in `~/Clawic/data/freelance/memory.md`: status, the all-in commission observed with the date it was measured, level or rating changes, and any exit trigger agreed. Clients met on a platform go to the shared `~/Clawic/data/contacts/contacts.md` with the platform named as their source; the engagement's commercial terms go to `## Engagements`.
