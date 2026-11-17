# Product-Led Growth — Self-Serve, Trials, Activation, Loops

Applies when `motion` is `plg-self-serve` or when a sales-led company adds a self-serve entry point. The defining constraint: the product does the selling, so marketing's job moves from generating meetings to generating *qualified signups* and removing friction between signup and value.

## Free Trial vs. Freemium vs. Demo

| Model | Fits when | Cost | Main failure |
|-------|-----------|------|--------------|
| Free trial (time-boxed) | Value is demonstrable in days; the product is complete without setup | Support load at scale | Trial expires before the user's first real use case arrives |
| Free trial (usage-boxed) | Value scales with volume; setup takes time | Metering complexity | Limit set where nobody reaches it, so nobody experiences value |
| Freemium | Huge top-of-funnel, near-zero marginal cost per free user, a natural upgrade trigger | Permanent infrastructure and support cost for non-payers | The free tier is good enough forever — no upgrade reason exists |
| Reverse trial (full features, then downgrade to free) | You want both the aha moment and a durable free base | Slightly more complex packaging | Downgrade feels like punishment if the free tier is unusable |
| Demo-first | High ACV, configuration required, buying committee | Sales capacity | Self-serve buyers bounce off a form they did not need |

Default: time-boxed trial with no credit card for mid-market B2B; freemium only when the free user has standalone value *and* creates a growth loop (invites, shared artifacts, public output). Freemium without a loop is a hosting bill.

## Activation Is the Metric That Matters

Define one activation event: the smallest observable action that reliably predicts retention. Find it empirically — compare the behaviour of accounts still active at 90 days against those that churned, and look for the action with the largest separation in the first days.

- State it as a compound event, not a single click: "invited a teammate *and* connected a data source in week one" is a real activation definition; "logged in" is not.
- Every marketing surface upstream should be judged on activated users, not signups. A channel with 3× the signups and half the activation rate is buying you support tickets.
- Report time-to-value as a distribution, not an average — the median user's experience is what the funnel actually looks like.

## Signup Friction

Remove: credit card for a free trial, phone number, company size, "how did you hear about us" as a *required* field (keep it optional — it is the cheapest attribution instrument you have, `measurement.md`), email verification before first value, SSO-only entry.

Keep: work-email requirement if your ICP is companies and abuse is a real cost; a single qualifying question if it changes onboarding materially.

Rule: every field you add multiplies against every field before it. Add a field only when someone can name the decision it changes.

## PQLs — Product-Qualified Leads

A PQL is an *account* showing both fit and product behaviour that predicts willingness to pay. Build it in this order:

1. Instrument the events that correlate with paid conversion (seats added, volume approaching a limit, integration connected, repeated returns by more than one person).
2. Combine with fit (company size, domain, role) exactly as the fit × intent grid in `demand.md` — behaviour is intent, firmographics are fit.
3. Route only the high-fit, high-behaviour accounts to a human, and route them with the *usage context* attached; an AE calling a PQL blind performs worse than the product would have.
4. Leave a self-serve path open at every point. Forcing a call on a buyer who wants to swipe a card is the classic PLG own goal.

## Loops, Not Funnels

A loop is any mechanism where output re-enters as input: invites, shared documents with your branding, public profiles, integrations that expose you to a partner's users, content the product generates.

- **Virality math**: k = invites sent per user × invite acceptance rate. Sustained k > 1 is rare outside consumer messaging; treat loops as a durable CAC discount, not as a growth engine, and model growth without them.
- Time matters as much as k: a loop with a two-week cycle at k = 0.4 beats a loop with a six-month cycle at k = 0.7.
- The strongest B2B loop is usually collaborative, not referral-based: a workflow that requires inviting a colleague brings a qualified user in with the work already contextualized.
- Instrument loops separately from paid; a loop's users often get attributed to direct traffic and disappear from the report (`measurement.md`).

## Pricing and Packaging Interlock

Self-serve exposes packaging decisions to everyone. The value metric (seats, usage, records, workspaces) must be something the customer can see growing and would accept paying more for. Depth and the price-change playbook live in `pricing.md`; the PLG-specific rules:

- The upgrade trigger should arrive during success, not during failure — a hard wall in the middle of the user's first real workflow converts frustration, not value.
- Show the price. A self-serve motion behind "contact us" is a sales motion in a trench coat.
- Never gate the collaboration features behind the paid tier if collaboration is your loop; you are charging admission to your own growth engine.

## In-Product Marketing

The highest-response channel you own, and the easiest to over-use. Rules: one message per surface per session; every message dismissible and frequency-capped globally alongside email (`lifecycle.md`); target by behaviour, not by segment membership; never interrupt a task the user started. Announcements about features irrelevant to the account are the fastest way to train users to close your banners without reading.

## Where PLG Breaks

- **Enterprise arrives anyway.** The moment procurement, SSO, and security review appear, you need a sales motion (`b2b.md`) — the mistake is bolting on sales without keeping the self-serve path clean.
- **Support becomes the cost centre.** Free users generate real load; budget it as a marketing cost, because that is what it is.
- **Bottom-up stalls at the department boundary.** Growth inside accounts plateaus where a budget owner must be convinced; that is a positioning and expansion-sales problem, not an onboarding one.
