---
name: expansion-signals
description: 'Find which customers are ready to expand before renewal: weekly, customers nearing renewal are judged for an expansion moment (won-deal cadence and last price, events such as funding, hiring, a new leader), with the signal and reason written onto the account and posted as one Slack digest. Triggers: "flag customers ready to expand", "which customers should we upsell this quarter", "renewal and expansion signals every week", "tell account managers which accounts to reach out to before renewal", "find expansion opportunities in our customer base", "at-risk renewals digest in slack". Cargo project, native accounts and deals models, definePlay, defineAgent, webSearch, Slack; adapts to HubSpot, Salesforce or Attio. Skip when: you want who raised money across prospects, which is track-funding-rounds; or buying signals on accounts that are not customers yet, which is monitor-buying-signals.'
version: "0.1.2"
compatibility: "Requires @cargo-ai/cli with @cargo-ai/cdk 1.0.92 or later, a Cargo workspace, and authorized Slack and Anthropic connectors. The worked example runs on native accounts and deals models, so no CRM connector is needed; the crm-backed variation swaps in HubSpot, Salesforce or Attio. Reads the workspace context when the project declares one."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/expansion-signals
metadata:
  author: getcargo
  source: cookbook
  personas:
    - revops
    - account-executive
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Expansion signals

## The outcome

The renewal stops being the first time anyone looks at a customer. Every Monday:

1. **A play picks up each won deal entering its renewal window** from a native `gtm_opportunities` model: the
   deal is won, has an account, and closed ten to twelve months ago. A deal enters that window once,
   so each renewal is judged once.
2. **An agent judges the account.** In SQL over `gtm_opportunities` it reads the account's purchase history:
   whether a newer win already renewed it, the cadence across its wins, the last price paid. It
   reads your expansion plays from the workspace context and runs up to three web searches for
   dated public events. It answers `renewal`, `expansion`, `repeat_purchase`, `at_risk` or `none`,
   with a reason of at most three sentences, the play to run, and every URL it relied on.
3. **The play writes the judgment onto the account record by its id**: `expansion_signal`,
   `expansion_reason` and a `expansion_signal_at` stamp. It writes nothing else: no
   deal, no contact, no owner.
4. **One digest lands in Slack** that afternoon: at-risk accounts first, then expansion, repeat
   purchase and plain renewal, each with the reason as written on the account and its owner. A
   ledger keeps it to one post a week.

The worked example runs on Cargo's native accounts and deals models, so it deploys with no CRM
connector. Customers who live in HubSpot, Salesforce or Attio take the `crm-backed` variation: the
same play, with connector-backed models and the write going back to the CRM record.

## Example

> Every Monday, flag which customers near renewal are ready to expand and post the digest to #cs-weekly.

Illustrative output, fictional records:

```text
:seedling: *Expansion signals, week of 2026-10-05*
_6 accounts in their renewal window: 1 at risk, 2 ready to expand._

*Tailspin Logistics* (tailspin.example) · at_risk · New CDO joined Sep 22 from a
  competitor's customer; renewed every 12 months, last at 24,000. Play: executive
  check-in. Sources: tailspin.example/news/new-cdo · owner 4411
*Fabrikam* (fabrikam.example) · expansion · Raised a Series B on Sep 9 and posted
  four data-engineer roles; renewed every 12 months, last at 38,000. Play: annual
  prepay offer. Sources: fabrikam.example/press/series-b · owner 4402
*Northwind Traders* (northwind.example) · expansion · Hired a Head of Compliance on
  Sep 30. Play: governance add-on demo. Sources: northwind.example/team · owner 4402
*Contoso* (contoso.example) · repeat_purchase · Ordered every 6 months, last at
  9,500 on Apr 2. Play: renewal call at the last price. · owner 4419
*Litware* (litware.example) · renewal · No outside event. · owner 4411
```

Six won deals entered their renewal window this week, so six accounts carry a signal and a reason; a
seventh account had already renewed early and was written `none`.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/expansion-signals` writes this example to `infra/expansion-signals/`
   and this procedure to `.claude/skills/expansion-signals/`. No project yet?
   `cargo-ai project init <dir> --cookbook expansion-signals && cd <dir> && npm install` does both.
   **If you are reading this from the project's `.claude/skills/`, the install already happened —
   start at step 2.**
2. **Reconcile it with what is already declared.** If the project already has a Slack or Anthropic
   connector, or a `gtm_accounts` or `gtm_opportunities` model, rewire the imports to the existing one and drop the
   copy; two resources with one slug is a collision at deploy. If the customer book lives in a CRM,
   take the `crm-backed` variation now, before the first deploy.
3. **Fill the models.** A native model starts empty. Load accounts, then won deals with their
   `account_id`, with `cargo-ai storage record create-bulk --model-uuid <uuid> --records '[{"data":{…}}]'`,
   or point a sync at them. A won deal with no account is never judged.
4. **Write your expansion plays** into the workspace context. `references/expansion-plays.md` is the
   example; copy it to `context/expansion-plays.md` and rewrite it for what you sell.
5. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about; _What you can change_ is what you offer unprompted; _What you will be asked_ is the floor,
   and you derive before you ask. Record what you changed and why under `## Decisions` in your copy
   of this file.
6. **Check, then plan.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root. Show the diff, and deploy only on an
   explicit yes. The play ships disabled.
7. **Pilot.** Run the play by hand on five deals from the window, read each written reason against
   its sources, then enable the play, execute it once (an `added` play does not backfill), and let
   the digest post the next Monday.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked.

| Input                         | Kind    | How it is answered                                                                                                                                      | Why it matters                                                                                                         |
| ----------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| where the customer book lives | derived | `cargo-ai storage model list` and `cargo-ai connection connector list`. Native models with rows: the default. A CRM with the deals: `crm-backed`.         | Judging an empty native model while the deals sit in HubSpot is a pipeline that runs green and flags nothing.           |
| the renewal window            | asked   | the contract length most customers sign. Annual is the default: a won deal ten to twelve months old.                                                     | A monthly book judged on an annual window is judged once a year; a two-year book is judged a year early.                |
| the expansion plays           | asked   | what you sell into an existing customer and which play answers which signal. Written once into the context.                                             | Without it, `suggested_play` is generic advice. With it, the digest tells the account manager what to do.              |
| `channelId` on the digest     | asked   | the Slack channel id (`C…`) from the connector's channel autocomplete. Invite the bot.                                                                   | The digest names customers and their renewal risk. Locked so it never lands in a customer shared channel.              |
| LLM connector and model       | value   | **derived**: `cargo-ai connection connector list`. `languageModel` is a placeholder on both agents.                                                      | It is what every judgment is billed against.                                                                           |

## What you can change

| Variation      | When it is right                                                   | How                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | What it costs                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crm-backed`   | The customers and deals live in HubSpot, Salesforce or Attio        | Add a `defineConnector` for the CRM (`default: true`). Replace both native models with connector-backed ones: `extractSlug: "fetchRecords"`, `config: { objectType: "companies" }` and `"deals"`, `columnSelectionMode: "all"`, an hourly `schedule`, and never a filter. Run the play on the gtm_opportunities model with the CRM's won flag and close date (HubSpot: `hs_is_closed_won`, `closedate`; or put it on companies and filter the `recent_deal_close_date` roll-up). Create three custom company properties (`expansion_signal` text, `expansion_reason` multi-line text, `expansion_signal_at` date) and replace `model.customColumn` with the CRM's `updateRecords` on `companies`, matched on the record id (`hs_object_id` of the deal's associated company), with those three mappings. | A write to a property that does not exist fails every row, so create them first. Never sit a unify step between the play and the write: it reports success and nothing lands. |
| `window`       | Contracts are not annual                                           | Change the two `close_date` values in `infra/plays/flag-expansion.ts`                                                                                                                                                                                                                                                                                                                                                                                                                                               | A window that overlaps the next renewal judges the same account twice.                                                                                                 |
| `whole-book`   | You want every customer judged on a cadence, not only near renewal  | Move the play to `gtm_accounts`, filter on `custom__expansion_signal_at` being empty or older than ninety days, and let the analyst decide in SQL whether the account has a win at all                                                                                                                                                                                                                                                                                                                              | Every account in the book is judged each cycle, customers or not, at one agent run and up to three searches each.                                                      |
| `no-web`       | Compliance does not allow web research on customers                 | Drop `webSearch` from the analyst and its search sentence                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Only `renewal`, `repeat_purchase` and `none` remain reachable from the deal history alone.                                                                             |
| `per-owner-dm` | Account managers want their own list                               | Replace the locked `channelId` with one `postMessage` use per owner channel, and split the post by owner                                                                                                                                                                                                                                                                                                                                                                                                            | More locked uses to keep in sync with the team. An owner with no use gets nothing.                                                                                     |

## What should not change

- **Customer status is computed from won deals, not kept as a flag.** (`infra/agents/analyst.ts`) A
  hand-kept "customer" column is a second answer to the question the deals already answer, and it
  drifts: an account that renewed early would be judged as if it had not.
- **The play writes the account by its id, and only the three expansion columns.**
  (`infra/plays/flag-expansion.ts`) A write to a deal or owner turns a judgment into a forecast
  change nobody approved. In the `crm-backed` shape, a unify step between the play and the write
  reports success while nothing lands. The contract fails on either.
- **Bare column slugs on the write.** The read side calls them `custom__expansion_signal`;
  the write takes `expansion_signal`. A prefixed slug is silently dropped while the node still
  reports success.
- **The analyst reads, never writes.** (`infra/agents/analyst.ts`) An agent that can write decides
  its own routing, and a missing signal could then be a failed run, a skip or a choice.
- **`changeKinds: ["added"]` stays.** It is what judges each renewal once. Without it every won deal
  in the window is re-judged every Monday for two months, and each run overwrites the last reason.
- **The digest re-judges nothing.** (`infra/agents/digest.ts`) It reads the reason the account
  carries. A second judgment in Slack is how the record and the channel disagree about one account.
- **The ledger, not Slack history, is the digest's dedupe.** A deleted post or another bot's
  message would otherwise read as "already sent" and drop a week in silence.

## Done when

- `node --import tsx evals/contract.mjs` passes
- `cargo-ai project plan` reports the `gtm_accounts`, `gtm_opportunities` and `expansion_digests` models, the two
  agents, the play, two connectors and three folders, with the play disabled and no CRM connector
- seeded accounts and won deals, with two deals inside the window, produced two analyst runs and
  two accounts carrying a signal, a reason and a stamp; every event named in a reason has a dated
  source in it
- an account whose newer win already renewed it (closed more than two months after the trigger)
  was written `none` with that reason, and an account with a second win within two months of the
  trigger was judged on its whole purchase history instead
- a second play execution the same week judged neither deal again
- the digest posted once in the locked channel, listed exactly the accounts stamped that week with
  a signal other than `none`, and a re-run that week posted nothing
- no deal or contact record changed

## What it costs

The model writes are native and the research is web search inside the analyst, at most three per
account. Immediately before the plan, read the live price of the one connector action:

- `cargo-ai orchestration action list postMessage --kind connector --integration-slug slack`

Say it out loud. The recurring cost is one analyst run per won deal entering its window each week,
plus one digest run, billed as LLM tokens through the Anthropic connector. It scales with how many
customers are near renewal, not with the size of the book. Count the window before enabling: a
`SELECT count(*)` over `gtm_opportunities` with `is_won` true and `close_date` ten to twelve months back.

## Composes into

`crm-enrichment` (firmographics on the same company records), `win-loss-review` (what closed-won
says about who expands), and `track-job-changes` (a champion who left is the first at-risk signal).
