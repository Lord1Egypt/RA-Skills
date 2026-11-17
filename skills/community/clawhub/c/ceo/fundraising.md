# Fundraising

Assume the reader can already build a deck and a data room. This file covers the deltas that decide the round: leverage mechanics, what each term actually costs, and the process errors that quietly kill deals.

Contents: [When to Raise](#when-to-raise) · [Dilution Base Rates](#dilution-base-rates) · [Timeline](#timeline) · [Leverage](#leverage-is-manufactured-not-found) · [Term Sheet](#term-sheet-what-each-term-actually-costs) · [Closing](#closing-where-deals-die) · [Bridge Rounds](#bridge-rounds) · [SAFEs and Notes](#safes-and-notes-the-conversion-surprise) · [Down Rounds and Recaps](#down-rounds-and-recaps) · [Venture Debt](#venture-debt-and-non-dilutive-capital) · [Secondaries](#secondaries) · [When the Round Does Not Come Together](#when-the-round-does-not-come-together)

## When to Raise

| Signal | Meaning |
|--------|---------|
| Runway at `runway_alarm_months` (default 12) | Start conversations — a round runs 3-6 months end to end, close included, so 9 months is the hard floor to start (SKILL.md rule 4; canonical zone table → SKILL.md Quick Reference: finance) |
| Clear milestone ahead | Raise into the metric inflection, not after it flattens |
| Market hot | Opportunistic, even if not needed — cheapest capital you'll ever get |
| Market cold | Raise fast if you can, or cut to reach default-alive |

The trap is treating "raise" as the goal. Raising is dilution against a future you haven't proven. Raise the smallest amount that clears the next fundable milestone with margin, not the largest you can defend.

**Never raise:** when desperate (the round smells it), without a use of funds that maps to a milestone, or before you can recite your metrics cold under hostile questioning.

## Dilution Base Rates

The numbers founders lose track of. These are conventional ranges, not laws — but a deal far outside them needs a reason.

| Round | Equity sold (typical) | Notes |
|-------|----------------------|-------|
| Seed | 10-20% | Below 10% is founder-favorable; above 20% you're overselling stage |
| Series A | 15-25% | The board-control round — see below |
| Series B+ | 10-20% | Ownership matters more here; lead expects a real slice |

Two mechanics that dilute you more than the headline number:
- **The option pool shuffle.** A new 10-15% pool created *pre-money* dilutes only founders and existing holders, not the incoming investor — it's effectively a valuation cut disguised as housekeeping. Negotiate the pool size down to what the next 18 months actually needs (bring a hiring plan), or push it post-money.
- **Stacking preferences.** Each round's liquidation preference sits on top of the last. In a modest exit, a few rounds of 1x can consume the whole outcome before common sees a dollar. Model the exit waterfall, not just the cap table percentages.

## Timeline

| Phase | Duration | The point |
|-------|----------|-----------|
| Prep | 4-8 weeks | Materials, list, warm intros lined up before anyone sees the deck |
| Process | 6-12 weeks | Meetings run in parallel — this is where leverage is made or lost |
| Close | 4-6 weeks | Legal, diligence, wire — deals still die here |

**Total: 3-6 months, close included** — the three phases above sum to 14-26 weeks; do not add the close again on top. The single most expensive mistake is starting late, because it converts every other decision into a desperation decision.

## Leverage Is Manufactured, Not Found

Terms follow leverage. Leverage comes from a real, parallel process — nothing else.

- **Run it in parallel, not serial.** Batch first meetings into the same 2-3 weeks so term sheets land in the same window. A serial process means you're always negotiating against one option, which is no negotiation.
- **Never soft-circle early.** Telling investor A you're "leaning toward" them before you have a competing sheet spends your only leverage for nothing.
- **A round needs a lead.** Ten "we'll follow" commitments and no lead is not a round. Prioritize finding the one fund that will set the price and the terms; followers are easy after.
- **Talk to partners, not associates.** Associates gather information and cannot say yes. If you're three meetings deep and haven't met the partner who'd sponsor the deal, you're in a data-collection funnel, not a process.
- **Don't name your number first when you can avoid it.** "What are you thinking on valuation?" is a test. A range tied to comparables and use-of-funds beats a single figure you'll have to defend or retreat from.
- **Create real urgency, not fake.** "We're taking meetings through the 20th" is credible when true and poison when bluffed — VCs compare notes and a caught bluff ends the process.

## Term Sheet: What Each Term Actually Costs

The headline valuation is one line. These decide control and outcomes, and most are where the real negotiation happens — not the price.

| Term | Standard (accept) | The real fight |
|------|-------------------|----------------|
| **Liquidation preference** | 1x non-participating | Resist *participating* preferred (investor takes their money back *and* their share) and any multiple above 1x — both surface in cold markets and cost you most in a modest exit |
| **Option pool** | Sized to 18-month hiring plan | Where it comes from (pre- vs post-money) and how big — this is a hidden valuation lever, negotiate it as hard as price |
| **Board composition** | Seed: founder-majority. Series A: often 2 founders / 2 investors / 1 independent | *Who picks the independent* is the whole game — a mutually-agreed independent is very different from an investor-chosen one |
| **Anti-dilution** | Broad-based weighted average | Refuse *full ratchet* — it re-prices the investor's whole stake to a down-round price and can wipe out founders |
| **Protective provisions** | Consent on major events (sale, new stock, debt) | Negotiate the *thresholds and scope* — a broad list lets a minority investor veto ordinary operating decisions |
| **Founder vesting** | 4-year, 1-year cliff on unvested | Watch for *re-vesting of already-vested* founder shares; negotiate acceleration — double-trigger (change of control *plus* termination) is founder-standard, single-trigger is rare |
| **Pro-rata rights** | Standard for the lead | Resist *super pro-rata* (right to buy more than their share) — it caps who else you can bring into the next round |

**Rule of thumb:** concede on economics you can earn back (a slightly lower valuation), fight on control terms you can't (board, protective provisions, full ratchet, participating preferred). A great partner on clean terms beats a higher number on dirty ones.

## Closing: Where Deals Die

Signing the term sheet starts exclusivity — it is not the finish line. Between sheet and wire:

- Keep other conversations *warm but honest* — you're exclusive, but the round isn't closed and diligence can reopen everything.
- Confirmatory diligence surprises the unprepared: reference calls to your customers, a cap-table error, an unassigned-IP contractor. Clean these before diligence, not during.
- Don't commit the spend or announce publicly until the money clears. A funded-but-not-wired round has fallen apart at legal more than once.

## Bridge Rounds

A bridge is a bet that a defined milestone within 6-12 months will unlock a priced round. Without that milestone it's just delaying the shutdown.

- **Instrument:** convertible note or SAFE, usually a 15-20% discount to the next round, sometimes a cap. Keep it simple and fast — bridge legal shouldn't cost more than the bridge.
- **Green light:** clear near-term milestone, existing investors leading or participating (their willingness is the market signal), and a specific fundable event on the other side.
- **Warning signs:** bridge-to-bridge-to-bridge, no defined milestone, existing investors declining to participate, or the pitch reduces to "we just need three more months." When insiders won't bridge, that *is* the answer.

## SAFEs and Notes: The Conversion Surprise

Stacked pre-priced instruments are the most common source of a founder discovering they own less than they thought at the Series A.

- Every SAFE and note converts at the priced round, usually at the better of its cap or the round price. Several caps from different years convert at different prices simultaneously.
- **Post-money SAFEs (the current standard) fix the investor's percentage, so all dilution from later SAFEs falls on you, not on them.** Two 3M post-money SAFEs are not "6M of dilution split" — each holder's percentage is locked, and the founders absorb the difference.
- Maintain a running pro-forma of the cap table as-converted, including the new option pool, before you agree a price. The number that matters is founder ownership after conversion and after the pool, not the headline valuation (`cfo` for the model; the ledger → SKILL.md Quick Reference: governance).

## Down Rounds and Recaps

- A clean down round is survivable and common in a repricing market. Structure — participating preferred, multiple liquidation preferences, full ratchet — is what does lasting damage, because it sits on the cap table through every future round and exit (→ SKILL.md Quick Reference: exit).
- Anti-dilution adjusts existing investors' conversion price automatically; broad-based weighted average is the standard, and full ratchet reprices their whole stake to the new low. Know which you signed before you price a down round.
- A recapitalization (converting preferred to common, restarting the stack) is the tool when the preference overhang exceeds any plausible exit value and the team has no reason to stay. It is a board and stockholder process with real conflicts — independent process matters (→ SKILL.md Quick Reference: governance).
- Refresh the team's equity as part of any down round or recap. Employees holding underwater options with a repriced cap table above them have no economic reason to stay, and they will do that arithmetic.

## Venture Debt and Non-Dilutive Capital

- Venture debt extends runway without dilution but adds covenants, warrants, and a claim ahead of equity (payment order → SKILL.md Quick Reference: shutdown). The usable window is when you are healthy: lenders size against your last round and pull availability precisely when you need it.
- Read the material-adverse-change clause and any minimum-cash covenant. Those are the terms that convert a bad quarter into a demand for repayment.
- Revenue-based financing and receivables factoring are expensive per dollar and fast; they fit a bounded, provable need (a hardware build, a collections gap), not general runway.
- Never take debt to avoid an equity conversation you will still have to have in six months, at a lower valuation, with a lender ahead of you.

## Secondaries

Founder secondaries — selling some of your own shares in a round — are normal at Series B and later, typically a modest slice of the round, and require the lead's and often the board's agreement. Two things to know: taking too much reads as reduced conviction and can kill the round, and any secondary establishes a share price with tax and 409A implications (→ SKILL.md Quick Reference: governance).

## When the Round Does Not Come Together

Diagnose honestly instead of adding meetings: consistent feedback across investors is the signal (metrics, market, or team), while inconsistent feedback usually means the story is unclear. Then act on the timeline you have — cut to reach default alive rather than raising desperately (→ SKILL.md Quick Reference: finance, layoffs), go back to the insiders with a specific milestone-based bridge, or accept a smaller round from the fund that actually believes. A round abandoned cleanly and reopened in six months with new evidence beats a round that limps for nine and closes on structure.
