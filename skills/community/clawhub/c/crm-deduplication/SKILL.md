---
name: crm-deduplication
description: 'Deduplicate CRM accounts and contacts and keep them duplicate-free: audit company and person identity, run recurring deduplication plays directly on CRM models, merge safe exact matches, and route uncertain clusters to manual review. Triggers: "deduplicate our CRM accounts", "deduplicate CRM contacts", "our CRM has duplicate people", "merge duplicate contacts in HubSpot", "we keep creating duplicate account records", "merge duplicate companies in HubSpot", "set up recurring CRM deduplication", "review ambiguous duplicates". HubSpot, Salesforce, Attio, Slack, LinkedIn profiles, phone numbers, Cargo project, findRecords, Scoring, Human Review, mergeRecords. Skip when: the request is to add or refresh CRM data rather than merge duplicate records; use crm-enrichment.'
version: "0.1.3"
compatibility: "Requires the cargo-project skill, a Cargo project (cargo.json at its root), @cargo-ai/cdk 1.0.82 or later, an authenticated CRM connector, and a Slack connector for each selected path that uses Human Review. The repository example does not deploy or access a CRM until an agent adapts it in the consumer project."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/crm-deduplication
metadata:
  author: getcargo
  source: cookbook
  personas:
    - revops
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

# CRM deduplication

**State: to-be-approved.** Deploy-verified against a live workspace: not yet. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

Choose the account path, contact path, or both. Each selected path has its own CRM model, identity
audit, matching policy, survivor policy, disabled play, cost preview, pilot approval, and acceptance
criteria. Approval for one path does not authorize the other.

### Path 1: Account deduplication

`deduplicate_accounts` searches live CRM companies by LinkedIn company ID, LinkedIn company page,
and non-generic domain. It scores the evidence, selects a deterministic survivor, and merges only
an exact shared LinkedIn company ID when there is no identity, protected-ID, or parent-subsidiary
conflict. Every other candidate reaches Cargo's native Human Review node. Company name never
creates or scores a candidate.

The default survivor policy prefers protected business IDs, customers, commercial activity,
populated records, recent activity, older creation time, then the smallest CRM record ID.

### Path 2: Contact deduplication

`deduplicate_contacts` searches live CRM contacts by LinkedIn person ID, normalized LinkedIn URL,
exact email, and exact stored phone. A second search expands the direct results into transitive
clusters using normalized identity values from retrieved records. Phone normalization also compares
records inside the cluster. The play merges automatically only on an exact LinkedIn person ID,
exact LinkedIn URL without a person-ID conflict, exact non-generic email without a LinkedIn conflict,
or a conflict-free transitive chain of those classes.

LinkedIn identity conflicts, generic or shared email, and phone-only matches never merge
automatically. Low-confidence clusters reach Human Review when that path is enabled and otherwise
remain untouched. The native merge is the final CRM write. Normalization, enrichment, and
association changes belong in a separately approved workflow.

### Shared merge contract

Both plays run directly on authoritative CRM-backed models, refresh candidates from the CRM before
scoring, and stop when the queued source record is missing or no duplicate remains. Automatic and
approved Human Review paths are the only merge paths. Decline or timeout leaves records separate.
No candidate or staging model is created.

The checked example in `infra/` is HubSpot. Salesforce and Attio adapt the connector, extractor,
record-ID field, search action, merge action, and property slugs together. Keep one CRM shape across
the selected paths.

When matching-key coverage is weak, recommend `crm-enrichment` before building the affected path.
That is a recommendation, not a dependency: `crm-deduplication` installs and operates independently.

## Example

> Merge duplicate HubSpot companies automatically only when the LinkedIn company ID matches, and send everything else to #crm-hygiene for a human to approve.

Illustrative output, fictional records:

```text
#crm-hygiene · Review CRM account merge into 18234
Duplicate score: 72/100
Survivor: 18234
Records to merge: 20911
Identity conflict: false
Protected ID conflict: false
Parent/subsidiary warning: false
Evidence:
18234, linkedin id none, linkedin northwind-traders, domain northwind.example, protected no, parent none
20911, linkedin id none, linkedin northwind-traders, domain northwind.example, protected no, parent none
[Approve]  [Decline]
```

Two records sharing a LinkedIn page and a domain, but no LinkedIn company ID, wait for a reviewer;
approve merges 20911 into 18234, while decline or 24 hours of silence leaves both untouched.

## Put it in your project

This folder is a **worked example**: real project resources written for another company. The job is to
end with the code this company would have written in its project.

**Install the required authoring skill first.** If `cargo-project` is absent, run:

```sh
npx skills add getcargohq/cargo-skills --skill cargo-project
```

Read `.agents/skills/cargo-project/SKILL.md` directly after installation. Complete its bootstrap and use
its authoring, state, plan, and deployment rules throughout this pipeline.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/crm-deduplication` writes this example to
   `infra/crm-deduplication/` and this procedure to `.claude/skills/crm-deduplication/`. No project
   yet? `cargo-ai project init <dir> --cookbook crm-deduplication && cd <dir> && npm install` does both;
   this folder never ships a shell. **If you are reading this from the project's `.claude/skills/`,
   the install already happened. Start at step 2.** On a CLI too old to have `add`, copy this folder
   in as a sibling of what is there by hand; everything below is unchanged.
2. **Choose paths and reconcile resources.** Select account deduplication, contact deduplication, or
   both. Remove unselected model and play files, then update the contract's exact resource inventory,
   connector assertions, and object-specific assertions. Rewire each selected path to compatible CRM
   resources already in the project and remove duplicate declarations. Keep each play on its
   object-specific CRM model. Append environment requirements to `.env.example`; preserve existing
   content.
3. **Audit and approve each selected path.** Follow the matching path in
   [`references/audit.md`](references/audit.md). Present its identity coverage, candidate classes,
   conflicts, survivor policy, automatic class, and review destination. Stop for approval of that
   path's policy and disabled deployment. Approval does not carry across paths.
4. **Adapt and deploy disabled.** Follow the matching path in
   [`references/configure.md`](references/configure.md). Record adaptations under `## Decisions` in
   the copied skill. Run the executable contract, generated types, check, and plan. Inspect the
   selected graph and deploy only its approved resources with `isEnabled: false`. Never run
   `cargo-ai project init --force` in a non-empty directory.
5. **Hand off each path for pilot approval.** Send its direct play link, exact population, current
   action costs, and approved policy. Stop for explicit approval of that merge-capable pilot.
6. **Run and report each approved path.** Follow the matching path in
   [`references/run.md`](references/run.md), then walk its section in
   [`evals/acceptance.md`](evals/acceptance.md) line by line.

### Account path setup

Verify the live company schema, record ID, LinkedIn company properties, domain property, protected
business identifiers, parent-company property, and survivor inputs. The account audit and policy
must be approved before adapting `crm_accounts` or `deduplicate_accounts`.

### Contact path setup

Verify the live contact schema, record ID, LinkedIn person properties, email, phone, association
evidence, and survivor inputs. Decide whether low-confidence clusters enter Human Review or remain
untouched. The contact audit and policy must be approved before adapting `crm_contacts` or
`deduplicate_contacts`.

### Shared review setup

Resolve the default CRM connector for every selected path. Account deduplication requires Slack
Human Review. Contact deduplication requires Slack only when low-confidence review is enabled.
Replace each active `PLACEHOLDER_REVIEW_CHANNEL_ID` with its approved destination. If both paths use
one channel, each still needs its own approved review policy and pilot. No paid call, review request,
or CRM write occurs during either audit.

## What you will be asked

Derive what can be discovered before asking the operator. Ask only for decisions that change the
selected path's candidate population, merge policy, review ownership, or spend.

### Shared inputs

| Input            | Kind    | How it is answered                                                                  | Why it matters                                                     |
| ---------------- | ------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `crm_shape`      | derived | Inspect authenticated connectors, selected extracts, and generated action types     | Sets objects, IDs, search, merge, and property behavior            |
| `selected_paths` | derived | Read whether the request names account deduplication, contact deduplication, or both | Sets which audits, resources, approvals, and pilots are in scope   |
| `action_costs`   | derived | Read current CRM metadata plus Slack metadata for paths with active review          | Each path's handoff must disclose its current maximum cost          |

### Path 1: Account inputs

| Input                    | Kind    | How it is answered                                                                   | Why it matters                                         |
| ------------------------ | ------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| `account_evidence`       | derived | Audit company identifiers, conflicts, candidate classes, and survivor inputs         | Grounds the account policy in current CRM records      |
| `account_policy`         | asked   | Review keys, protected fields, survivor precedence, score, and automatic class       | Controls every company candidate and unattended merge  |
| `account_review`         | asked   | Select Slack channel, owner, and timeout for uncertain company clusters              | Gives manual company decisions an accountable owner    |
| `account_authorizations` | asked   | Approve the disabled build, then the exact merge-capable pilot as separate decisions | Separates deployment from company-record mutation      |

### Path 2: Contact inputs

| Input                    | Kind    | How it is answered                                                                   | Why it matters                                         |
| ------------------------ | ------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| `contact_evidence`       | derived | Audit person identifiers, conflicts, candidate classes, and survivor inputs          | Grounds the contact policy in current CRM records      |
| `contact_policy`         | asked   | Review keys, global guards, survivor precedence, and automatic classes               | Controls every person candidate and unattended merge   |
| `contact_review`         | asked   | Decide whether low-confidence groups enter review; if yes, approve channel and timeout | Defines the non-automatic contact path               |
| `contact_authorizations` | asked   | Approve the disabled build, then the exact merge-capable pilot as separate decisions | Separates deployment from contact-record mutation      |

## What you can change

Offer only variations relevant to the selected path. Record each approved variation with its
effect on candidates, safeguards, and validation.

### Shared variations

| Variation              | When it is right                              | How                                                                                                   | What it costs                                                  |
| ---------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `crm`                  | The consumer uses Salesforce or Attio         | Replace connector, extract, record ID, search, merge, and properties across selected paths            | Generated types and native merge semantics must be revalidated |
| `structured_ai_review` | Ambiguous evidence needs a concise review aid | Add priced structured evidence before Human Review only; never use it to bypass deterministic guards | Adds model cost and a non-deterministic review surface         |

### Path 1: Account variations

| Variation                     | When it is right                                                | How                                                                                  | What it costs                                                     |
| ----------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| `account_matching_keys`       | The CRM has another approved durable company identity           | Add it to search, normalization, evidence, conflict gates, review, and contract tests | Wider matching can create new false-positive company classes      |
| `account_survivor_precedence` | Protected lifecycle, billing, tier, or customer policy must win | Change the account ranker and its contract fixtures together                         | A policy change can select a different survivor for every cluster |

### Path 2: Contact variations

| Variation                     | When it is right                                           | How                                                                                 | What it costs                                                   |
| ----------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `contact_matching_keys`       | The CRM has another approved durable person identity       | Add it to both searches, normalization, evidence, conflict gates, review, and tests | Wider matching can create new false-positive person classes     |
| `contact_survivor_precedence` | Commercial history or activity policy differs              | Change the contact ranker and its contract fixtures together                        | A policy change can select a different survivor for every group |
| `low_confidence_review`       | The operator wants phone-only or ambiguous groups surfaced | Keep Human Review enabled, or remove that branch and update the contact contract so those groups end untouched | Review volume changes; disabled review leaves more duplicates |

## What should not change

### Shared invariants

- **Run on authoritative CRM models.** (`infra/plays/`) Each selected play uses its object-specific
  CRM extract and record ID. A candidate model introduces another identity system and can target
  the wrong record.
- **Search live CRM rows before scoring.** (`infra/plays/`) The CRM search refreshes candidate
  membership for every run. Audit snapshots can become stale before a merge.
- **Search, prepare, score, then decide.** (`infra/scripts/`) Deterministic preparation retains the
  fresh source once, normalizes evidence, and selects one survivor before the automatic gate.
- **Merge only on automatic or approved paths.** (`infra/plays/`) Human approval reaches the
  reviewed merge. Decline and timeout end without a CRM write.
- **Stop stale queued rows.** (`infra/plays/`) A source missing from the fresh search ends before
  scoring or emitting merge IDs.
- **Keep one CRM shape.** Adapt HubSpot in place. Parallel CRM branches drift from the generated
  types connected to the selected paths.
- **Keep pilots disabled, serial, and limited.** (`infra/plays/`) Each selected play remains
  disabled, `noConcurrency`, and limited to 15 rows until its verified pilot is approved for
  expansion.

### Path 1: Account invariants

- **Keep the automatic company class narrow.** (`infra/plays/deduplicate-accounts.ts`) Exact shared
  LinkedIn company ID, score at least 60, and no identity, protected-ID, or parent-subsidiary
  conflict are all required. Every other candidate reaches Human Review.
- **Keep names out of identity.** (`infra/scripts/accounts/`) Company name is excluded from candidate
  generation and scoring. The checked review payload does not rely on it.
- **Protect business identities and corporate structure.** Conflicting protected IDs and
  parent-subsidiary clusters never merge automatically.

### Path 2: Contact invariants

- **Apply person guards globally.** (`infra/scripts/contacts/evidence.ts`) Every automatic contact
  class is disqualified by a LinkedIn identity conflict or generic or shared email.
- **Keep phone-only groups out of automatic merge.** Phone is a candidate key and review aid, not
  sufficient unattended identity evidence.
- **Expand transitive groups before deciding.** (`infra/plays/deduplicate-contacts.ts`) The second
  live search gathers every high-confidence identity key discovered by the direct search.
- **End after native merge.** (`infra/plays/deduplicate-contacts.ts`) Deduplication creates no
  post-merge update node. A separate approved workflow owns normalization, enrichment, and
  association changes.

## Done when

### Shared completion

- the operator selected account deduplication, contact deduplication, or both
- each selected path has its own reconciled audit, policy approval, disabled-build approval, priced
  pilot approval, and final report
- the selected resources use one CRM connector, a Slack connector for every path with active review,
  object-specific CRM models, and no candidate or staging model
- generated types confirm selected search and merge payloads plus Human Review for paths that use it
- `node --import tsx evals/contract.mjs`, `cargo-ai project types`, `cargo-ai project check`, and
  `cargo-ai project plan` pass after adaptation
- every selected play is disabled, `noConcurrency`, and limited to 15 CRM rows before its pilot

### Path 1: Account completion

- the account audit reconciles company identifier coverage, mutually exclusive classes, conflicts,
  survivor evidence, and proposed merge IDs to the source total
- `deduplicate_accounts` runs directly on `crm_accounts` and searches companies live
- its graph contains preparation, native Scoring, the guarded Branch, native Human Review, and CRM
  merges only on automatic or approved paths
- automatic merge requires exact shared LinkedIn company ID and every account conflict guard
- every account survivor and absorbed company ID is verified in the CRM

### Path 2: Contact completion

- the contact audit reconciles source totals, person identifier coverage, unique candidate clusters,
  conflicts, survivor evidence, and proposed merge IDs, and reports overlapping matched classes
  separately
- `deduplicate_contacts` runs directly on `crm_contacts` and performs both direct and transitive live
  searches
- its graph contains preparation, native Scoring, the guarded Branch, optional native Human Review,
  and CRM merges only on automatic or approved paths
- automatic merge requires one approved high-confidence class plus every global contact guard
- the merge is the final CRM write, and every contact survivor and absorbed ID is verified in the CRM

## What it costs

Immediately before each selected path's preview, run
`cargo-ai connection integration get <crm>` and, when review is enabled,
`cargo-ai connection integration get slack`. Record the CLI version, lookup time, action slugs, and
current cost metadata. The repository does not hard-code pipeline action prices.

### Path 1: Account cost

Price the account search, automatic or approved company merge, and Human Review actions against the
exact account population. Approval authorizes only the company clusters shown for that pilot.

### Path 2: Contact cost

Price both contact searches, automatic or approved contact merge, and enabled Human Review actions
against the exact contact population. Approval authorizes only the person clusters shown for that
pilot.

Enabling either recurring schedule is a separate final approval after that path's pilot passes.

## Composes into

Nothing in particular comes after it: the survivors are the records anything reading the CRM sees.
