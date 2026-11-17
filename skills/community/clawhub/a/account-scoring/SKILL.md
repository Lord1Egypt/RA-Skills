---
name: account-scoring
description: 'Score every account against your ICP on a schedule: a deployed agent tiers each company in a Cargo model (tam-building''s, or your CRM companies) A / B / C / disqualified against the ICP and rubric in workspace context, and the tier, a two-sentence reason and evidence are written onto the row and, optionally, the matching HubSpot or Salesforce company. New companies are tiered hourly; the book is re-scored weekly or on any window set. Triggers: "score our TAM", "tier the market we just sourced", "which accounts should the team work first", "why is this account tier A", "keep our accounts tiered as they arrive", "our lead scoring is a spreadsheet nobody trusts". Cargo project, defineAgent, webSearch, context, tam_companies, tier segments. Skip when: someone hands you a list and wants it scored once, which is score-leads; or there is no account universe yet, which is tam-building.'
version: "0.5.4"
compatibility: "Requires the cargo-project skill, a Cargo project (cargo.json at its root), @cargo-ai/cdk 1.0.58 or later, an authenticated LLM connector (Anthropic in the example), and a model of companies to tier: tam-building's tam_companies, which this example carries a copy of. No CRM needed; a HubSpot or Salesforce connection only when the tier is written back to it. The repository example does not deploy or tier anything until an agent adapts it in the consumer project."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/account-scoring
metadata:
  author: getcargo
  source: cookbook
  personas:
    - revops
    - sales-leadership
    - gtm-engineering
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

# Account scoring

## The outcome

Every company in your TAM tiered A, B, C or disqualified, with a two-sentence reason and the page
that decided it written on the row, so a rep can read why an account is tier A and argue with it.
New companies are tiered as they land. The tiers are four segments: tier A is what contact
sourcing and engagement run on, and disqualified is what everything else suppresses.

It runs on `tam_companies`, the model tam-building lands, and needs nothing else: no CRM, no
scoring code, no point weights. When reps work in a CRM, one setting writes the tier, its reason and
the scored-at date onto the matching HubSpot or Salesforce company as well, in the same run.

**The judgment lives in the context repo, not in code.** The agent reads the ICP and
`tiering-rubric.md` from the workspace context on every call. Changing what tier A means is a
reviewed commit to that file, with no deploy, and the rep reading the tier can read the same file
the agent read.

**Firmographics are tam-building's job; the tier is about what no column holds.** Headcount band,
industry and country are already in the filter that sourced the row. What separates an A from a C
is whether the company runs the motion you sell into: an open role, a public stack, an
engineering post. So the agent judges on the sourced row first, and searches only to settle one
doubt that would change the tier.

**Two failure modes worth knowing before you start.** Writing a custom column with its
`custom__` read-side name drops the value while the node reports success, so the play runs
perfectly over a book with no tiers in it. And a play enabled without a backfill never tiers the
rows that were already there: `changeKinds: ["added"]` only enrols rows that arrive after it is on.

## Example

> Tier every company in our TAM against the ICP and the rubric in our context repo, and keep new ones tiered as they land.

Illustrative output, fictional records:

| Company (domain)              | tier         | tier_reason                                                                                                                                   | tier_evidence_url                         |
| ----------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Northwind (northwind.example) | A            | Fits the firmographics: 240-person B2B software company in the US. Has a GTM engineer on staff, which the rubric ranks as the strongest sign. | https://northwind.example/careers/gtm-eng |
| Fabrikam (fabrikam.example)   | C            | Fits industry, size and country. No technical revenue role and no public automation practice was found, so nothing lifts it above C.          |                                           |
| Tailspin (tailspin.example)   | disqualified | Services-only consultancy with no software product, which the ICP lists as a disqualifier. The sourced industry label was misleading.         | https://tailspin.example/about            |

Every row also gets `tiered_at` and lands in `tier_a_accounts`, `tier_b_accounts`,
`tier_c_accounts` or `disqualified_accounts`. With `crmWriteback` set to HubSpot, `northwind.example`'s
company record gets `cargo_tier = A`, the same rationale in `cargo_tier_reason`, and today's date in
`cargo_tiered_at`. The report closes on the tier distribution and one
recommended next step.

## Guide the operator through every phase

```mermaid
flowchart LR
  rubric["1. Rubric"] -->|"Approve the rubric"| build["2. Build"]
  build -->|"Approve deploy, play disabled"| pilot["3. Pilot"]
  pilot -->|"Approve the backfill and the play"| run["4. Backfill, enable, report"]
```

Every substantive message starts with the current phase and ends with a `Next step` section giving
the operator one concrete decision, what it unlocks, and what stays blocked. During an in-progress
operation, say `No action needed` and name the next checkpoint. Never end with a generic offer to
help.

1. **Rubric.** Read the ICP and any tiering rubric from the workspace context. If there is no ICP,
   stop and send the operator to tam-building's first phase: tiering against an unwritten ICP is
   guessing. If there is no rubric, propose A, B, C and disqualified from the ICP's own language,
   using this skill's `context/tiering-rubric.md` as the shape, and have the operator correct it.
   End by asking the operator to approve the rubric. Nothing bills in this phase.
2. **Build.** Reconcile with tam-building, adapt, run the contract, types, check and plan, and show
   the plan: the tier columns added to `tam_companies`, the agent, the play **disabled**, and the
   four segments. End by asking to deploy with the play disabled. A deploy tiers nothing.
3. **Pilot.** Run ten rows through the workflow as a batch, with the play still disabled
   ([`references/run.md`](references/run.md#pilot)). Spot-check one A, one C and one disqualified
   against the rubric, quote the evaluator results, and give the observed cost per company and
   what the whole book would cost. With `crmWriteback` set, read one piloted company back from the
   CRM and show its three fields. End by asking to approve the backfill at that cost and to
   enable the play.
4. **Backfill, enable, report.** Backfill every untiered row, enable the play, and report the
   tier distribution, the disqualified share, the evaluator pass rate and actual credits, with a
   direct Cargo link to each segment. Recommend one next step.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job
is to end up with the code your company would have written, in your project, and an agent does the
adapting.

**Install the required authoring skill first.** If `cargo-project` is absent, run:

```sh
npx skills add getcargohq/cargo-skills --skill cargo-project
```

Then read `.agents/skills/cargo-project/SKILL.md` directly; no session reload is needed. Complete its
bootstrap and use its authoring, state, plan, and deployment rules throughout. Stop before any
template work if the skill cannot be installed or read.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/account-scoring` writes this example to `infra/account-scoring/` and
   this procedure to `.claude/skills/account-scoring/`. No project yet?
   `cargo-ai project init <dir> --cookbook account-scoring && cd <dir> && npm install` does both.
   **If you are reading this from the project's `.claude/skills/`, the install already happened:
   start at step 2.**
2. **Reconcile it with tam-building.** This example carries a copy of `tam_companies` and its AI
   Ark connector so it deploys on its own. When `infra/tam-building/` exists, move the four
   `additionalColumns` from the copy onto tam-building's model, point the play and the segments
   at that export, and delete the copy and its connector: one slug declared twice collides at
   deploy. Reuse an existing Anthropic connector the same way. A deploy drops any custom column
   the model declaration no longer lists, values included, so first compare the declaration with
   `cargo-ai storage column list` on the live model and carry over every `custom__` column you
   want to keep. This skill declares no `defineContext`: that resource is a per-workspace
   singleton the project owns.
3. **Write or confirm the rubric.** Phase 1 above. It goes in the project's context repo beside
   the ICP, never into the agent's prompt.
4. **Adapt and deploy disabled.** Work the sections below in order: _What should not change_ is
   what you argue back about (say what breaks, then do it if they still want it); _What you can
   change_ is what you offer unprompted; _What you will be asked_ is the floor, and you derive
   before you ask. Record what you changed and why under a `## Decisions` section in your copy of
   this file. Then run `node --import tsx evals/contract.mjs` from this skill's folder, followed by
   `cargo-ai project types && cargo-ai project check && cargo-ai project plan` from the project root. Show the
   diff, and deploy only on a yes. Never run `cargo-ai project init --force` in a non-empty directory.
5. **Pilot, backfill, verify.** Follow [`references/run.md`](references/run.md), then walk _Done
   when_ line by line with evidence. Deployed cleanly and tiered nothing is the normal failure.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked.

| Input           | Kind    | How it is answered                                                                                                                                            | Why it matters                                                                                                          |
| --------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `icp`           | derived | Read from the workspace context (`cargo-ai context …`, or the project's context directory). None? Stop and run tam-building's first phase                     | The rubric decides against it. A tier that cannot name the ICP line it came from is a guess, and the evaluator fails it |
| `tier_rubric`   | asked   | An existing rubric in the context is shown and confirmed. Otherwise propose A / B / C / disqualified from the ICP's language and have the operator correct it | It is the one input that is genuinely a decision about the business: what "work it now" means here                      |
| `model`         | derived | `tam_companies` from tam-building. Another companies model works if it has an id, a name and a domain; map its columns in the workflow input                  | The workflow interpolates these columns into the prompt. A renamed one hands the agent an undefined                     |
| `languageModel` | derived | Whichever LLM connector the workspace already holds (`cargo-ai connection connector list`)                                                                    | Judgment quality and the cost per company both live here                                                                |
| `rescoreAfter`  | derived | `"6 months"` in `infra/settings.ts`. Ask only to change it; `"7 days"` is weekly                                                                              | How often a tiered company is judged again. Shorter re-bills the whole book more often                                  |
| `crmWriteback`  | asked   | `none` unless the tier should reach a CRM. Then the connected CRM (`cargo-ai connection connector list`) and the three property names the operator created    | Reps read the CRM, not the Cargo row. A property that does not exist is a write that ends green and lands nothing       |

Checked before moving on, not after the deploy:

- `icp`: it names at least one disqualifier, not only fit signals
- `tier_rubric`: every tier is decidable from the sourced row plus at most one search, and each
  tier names what evidence counts for it
- `model`: the column names in the workflow input match `cargo-ai storage column list` on the live
  model
- `crmWriteback`: the three properties exist on the CRM company object (HubSpot company properties,
  Salesforce Account fields), and the match property holds the same value as the row: a bare domain,
  or the record id when the play runs on a CRM model

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something; that is what makes it a variation and not the
default.

| Variation               | When it is right                                                                                               | How                                                                                                                                                                          | What it costs                                                                                                                                                                           |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crm-writeback`         | Reps work in HubSpot or Salesforce and the tier should be visible there                                        | Set `crmWriteback` in `infra/settings.ts`: the CRM, `matchOn` (`domain`, or `id` when the play runs on a CRM companies model), the match property, and the three field names | A CRM connection and three CRM properties to maintain. A miss ends the run green, so the pilot reads one CRM record back. A domain shared by duplicate CRM companies tiers none of them |
| `crm-accounts`          | The accounts already live in a CRM rather than in tam_companies                                                | Point the play, its write and the segments at a CRM companies model carrying the four tier columns, map its columns in the workflow input, and set `matchOn: "id"`           | The CRM's own fields decide what the agent sees. A thin CRM record is a thin judgment                                                                                                   |
| `weekly-rescore`        | The market moves fast enough that a month-old tier is wrong                                                    | `rescoreAfter: "7 days"` in `infra/settings.ts`                                                                                                                              | Every account is judged, and billed, once a week instead of twice a year                                                                                                                |
| `numeric-score`         | A downstream router or report needs a 0 to 100 number, not four buckets                                        | Add `score` to the agent's output schema, a `score` custom column, and the mapping in the write; define what the number means in the rubric                                  | A number reads more precise than the judgment behind it. Keep the tier as the field people act on                                                                                       |
| `deterministic-tiering` | The rubric turns out to be thresholds on sourced columns (headcount, industry, country) with no judgment in it | Delete the agent and write the tier in the play from the columns, or push the thresholds into tam-building's filter                                                          | You lose the rationale and the evidence, and anything the sourced row does not hold can no longer move a tier                                                                           |
| `tier-once`             | The market is stable and nobody reads a tier older than a quarter anyway                                       | Remove the `lowerThan` condition from the play's filter                                                                                                                      | A company that changed (hired the persona, got acquired) keeps its old tier until someone re-tiers it by hand                                                                           |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The rubric lives in the context repo.** (`context/tiering-rubric.md` in the project's knowledge
  layer.) Put it in the prompt and changing what tier A means becomes a deploy, the reason for the
  change stops being reviewable, and the rep reading the tier can no longer read the same file the
  agent read.
- **The agent judges and the play writes.** (`infra/agents/tier-analyst.ts`) The agent carries no
  model in `uses`. Give it one and it decides its own routing, at which point an untiered row could
  be a failed run, a skip, or a choice.
- **Custom columns are written with their bare slugs.** (`infra/plays/tier-accounts.ts`)
  `custom__tier` on the write becomes `custom.custom__tier`, the node reports "Record upserted",
  and the value is dropped.
- **Eligibility is the stamp, not the tier.** (`infra/plays/tier-accounts.ts`) Filter on `tiered_at`
  being null or stale. Filter on the tier and a failed run looks the same as a legitimate
  `disqualified`, so it is either retried forever or never.
- **A tier ships with its rationale, its evidence, and its stamp, on the same write.**
  (`infra/plays/tier-accounts.ts`) A tier nobody can audit is a number a rep will not trust, and a
  tier with no stamp is judged again on every tick.
- **`changeKinds: ["added"]` stays.** (`infra/plays/tier-accounts.ts`) Runs are created for rows
  entering the filter. Without it, the LLM bill scales with how often the cron fires.
- **The CRM write-back updates, never creates, and writes only the fields named in
  `settings.ts`.** (`infra/plays/tier-accounts.ts`) `upsertRecords` would create a CRM company for
  every TAM row the CRM does not hold, and a field nobody named is a CRM value overwritten without a
  decision. It runs after the row write, so the row is the record of the judgment whatever the CRM
  does.
- **The CRM write-back fails on multiple matches.** (`infra/plays/tier-accounts.ts`) The update sets
  `isFailingOnMultipleMatches: true`, so a domain that matches two CRM companies writes to neither
  and the CRM step fails with the match count. Remove it and every duplicate gets the tier, and
  nothing shows that the CRM holds the company twice.
- **Every tier the agent can emit has a segment.** (`infra/segments/tiers.ts`) A tier with no
  segment is a row that lands nowhere and quietly disappears from the book.

## Done when

- the ICP and the tiering rubric are in the workspace context, and the rubric was approved
- the pilot tiered ten rows, and one A, one C and one disqualified were checked against the rubric
  by hand
- every row in the model carries a tier the rubric defines, a rationale naming the deciding lines,
  and a `tiered_at` stamp, and no row carries one without the others
- the four segments resolve, and their counts sum to the tiered row count
- the agent's evaluator pass rate is at or above its threshold
- with `crmWriteback` set, one piloted company read back from the CRM carries the same tier, reason
  and scored-at date as its row
- editing the rubric in the context repo changes the next tier with no deploy
- the report gave the tier distribution, actual credits against the pilot's estimate, and one
  recommended next step
- `node --import tsx evals/contract.mjs` passes against the adapted resources

## What it costs

**Tiering is one agent run per company**, billed as LLM tokens through the bound connector, plus
the web searches the agent makes. The prompt holds it to one search per company and `maxSteps: 4`
is the ceiling: on the 2026-10-18 pilot, holding the agent to one search more than halved the
cost per company against an agent left at eight steps, with the same tiers coming back. The pilot is how you learn
the real number: read actual credits for the ten rows, then multiply by the untiered row count
before approving the backfill.

After the backfill, the play only tiers what arrives (`changeKinds: ["added"]`) and what goes stale
after `rescoreAfter`, so the steady-state cost follows how many companies tam-building lands and how
short that window is, not how often the cron fires. A weekly window bills every account every week.
The CRM write-back is one connector action per tiered company; the pilot's actual credits include it.

## Composes into

`contact-sourcing` (the buyers at every tier A account), `agentic-engagement` (talk to the accounts
this ranked), `new-hire-detection` (watch tier A for the hires that move a C up). Works best after
`tam-building`, whose `tam_companies` it tiers.
