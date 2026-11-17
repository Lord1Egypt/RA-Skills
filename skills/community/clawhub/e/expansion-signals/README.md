# Expansion signals: find customers ready to expand before renewal

To know which customers to approach before renewal, judge each one as its renewal nears, from its
won deals and dated public events, and send the customer team one list. Every Monday this cookbook
picks up customers whose won deal is ten to twelve months old, has an agent mark each account
`renewal`, `expansion`, `repeat_purchase`, `at_risk` or `none` with a reason, writes that onto the
account, and posts one Slack digest.

```sh
cargo-ai project add cookbook/expansion-signals
```

## What it does

- A weekly play picks up each won deal whose close date entered the ten-to-twelve-month window. A
  deal enters once, so each renewal is judged once.
- An agent judges the account from its won deals in SQL (a newer win, the cadence, the last price),
  your expansion plays in the workspace context, and dated public events: `renewal`, `expansion`,
  `repeat_purchase`, `at_risk` or `none`, with a reason, a play and its sources.
- The play writes `expansion_signal`, `expansion_reason` and
  `expansion_signal_at` onto the account record by id, and nothing else.
- A digest agent posts one Slack message that afternoon, at-risk first, and records the week in a
  ledger so a re-run posts nothing.

## What's inside

Adds 11 resources.

| File                                | Resource                        | Role                                                    |
| ----------------------------------- | ------------------------------- | ------------------------------------------------------- |
| `infra/models/gtm-accounts.ts`          | `defineModel` (native account)  | the customer book, plus the three expansion columns     |
| `infra/models/gtm-opportunities.ts`             | `defineModel` (native deal)     | every deal; the play's model and the purchase history   |
| `infra/models/expansion-digests.ts` | `defineModel` (native custom)   | the digest ledger: one row per week posted              |
| `infra/plays/flag-expansion.ts`     | `definePlay` + `defineWorkflow` | who is judged, the judgment, the one account write      |
| `infra/agents/analyst.ts`           | `defineAgent`                   | the judgment, as JSON, read-only                        |
| `infra/agents/digest.ts`            | `defineAgent`                   | the weekly Slack post, channel locked                   |
| `infra/connectors/slack.ts`         | `defineConnector` (`slack`)     | the digest's post path                                  |
| `infra/connectors/anthropic.ts`     | `defineConnector` (`anthropic`) | the model both agents run on                            |
| `infra/folders/index.ts`            | `defineFolder` ×3               | where the models, agents and play are filed             |
| `references/expansion-plays.md`     | (not a resource)                | the example to copy into `context/expansion-plays.md`   |

## Why native models in the example

Fewest dependencies: the example deploys with a Slack and an Anthropic connector and nothing else.
The judgment does not care where the deals come from. A team whose deals live in a CRM swaps the two
models for connector-backed ones and the write for the CRM's `updateRecords` on the record id; the
play, the analyst and the digest stay as they are.

## Why a play writes and the agent does not

The agent hands back a judgment; the play persists it on the account by id. That keeps the write in
one reviewable place, limited to three columns, and makes a missing signal mean one thing: the run
failed.

## Placeholders (edit before deploy)

1. **The renewal window** in `infra/plays/flag-expansion.ts`, if contracts are not annual.
2. **`channelId`** in `infra/agents/digest.ts`.
3. **`languageModel`** on both agents.
4. **`context/expansion-plays.md`** in your project, from `references/expansion-plays.md`.

## What it does not do

It does not change a deal, a contact or an owner, contact a customer, or post anywhere but the
locked channel.
