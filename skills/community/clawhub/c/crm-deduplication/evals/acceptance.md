# CRM deduplication acceptance

## Shared skill boundary

- `crm-deduplication` remains one root pipeline skill with `SKILL.md`, `README.md`, `infra/`,
  `references/`, and `evals/`.
- The operator selects the account path, contact path, or both. Approval and completion for one path
  do not authorize or complete the other.
- It installs and operates without `crm-enrichment`.
- Supporting instructions contain no nested `SKILL.md`.
- No relative import leaves the skill folder.

## Shared audit and approval

- Every selected-path audit reads its source CRM model without paid calls, review requests, or CRM
  writes.
- Each selected path produces its own JSON, Markdown, and chat summary. Identifier coverage,
  candidate counts, classifications, conflicts, exclusions, survivor evidence, and exact proposed
  merge IDs agree across all three representations.
- The operator approves each selected path's matching keys, survivor precedence, automatic classes,
  global conflict guards, and manual-review destination before that path's project adaptation.
- Policy approval, disabled deployment authorization, and exact merge-capable pilot authorization
  are separate gates for each selected path.

## Shared resources and graph

- The isolated plan contains `connector:crm`, `connector:slack` when at least one selected path uses
  Human Review, and the two ownership folders, plus only the model and play resources for the
  selected paths. When both paths are selected, it contains `model:crm_accounts`,
  `model:crm_contacts`, `play:deduplicate_accounts`, and `play:deduplicate_contacts`.
- No account or contact candidate staging model exists.
- Each selected play runs directly on its CRM-backed model. Its filter requires the CRM record ID and
  at least one supported identity key.
- Each selected graph calls the CRM's live record-search action, retains the fresh source exactly
  once, normalizes evidence, runs native Scoring, selects one deterministic survivor, and applies
  the path's approved automatic gate.
- A source row missing from the fresh search stops before scoring as
  `source_missing_or_changed`.
- Every selected play has only automatic and human-approved CRM merge paths.
- Neither connector configures a cache, so every duplicate decision reads the CRM live.
- Every selected play is disabled, uses `noConcurrency`, and is limited to 15 CRM rows.

## Path 1: Account deduplication

### Account audit and policy

- The account audit uses `crm_accounts`, the selected account record ID, and a dedicated account
  JSON, Markdown, and chat summary.
- Company name alone never creates or scores a candidate.
- The checked score assigns LinkedIn company ID 60, LinkedIn URL 25, and non-generic domain 15.
- The automatic branch requires score at least 60, exact shared LinkedIn company ID, and no identity,
  protected-ID, or parent-subsidiary conflict.
- LinkedIn URL-only, domain-only, junk/shared-domain, parent/subsidiary, and conflicting-identity
  candidates remain outside the automatic path.
- The account survivor follows the approved precedence across protected ID, customer status, open
  opportunities, contacts, activities, populated properties, latest activity, oldest creation time,
  and CRM record ID.
- The operator approves account protected fields and parent-company fields before adaptation.
- Every non-automatic account candidate reaches native Human Review. Approval reaches the reviewed
  company merge; decline or timeout reaches a no-write end.

### Account resources and completion

- The account path contains `model:crm_accounts` and `play:deduplicate_accounts` and runs directly on
  the account CRM extract.
- Its live search uses non-empty LinkedIn company ID, LinkedIn company URL, and domain criteria.
- Account evidence preparation and survivor selection remain deterministic, and the automatic gate
  includes every approved account conflict guard.
- The Slack channel, protected-ID fields, and parent-company fields resolve before account planning.
- Generated consumer types confirm the account search, merge, and Human Review payloads.
- The operator approves the account policy, disabled account deployment, and exact account pilot as
  three distinct gates.
- The final account report verifies every surviving company and absorbed account ID and accounts for
  every terminal outcome.

## Path 2: Contact deduplication

### Contact audit and policy

- The contact audit uses `crm_contacts`, the selected contact record ID, and a dedicated contact JSON,
  Markdown, and chat summary.
- Person name, job title, company association, and fuzzy similarity never create or score a contact
  candidate.
- Contact scoring assigns 60 to exact LinkedIn person ID, exact LinkedIn person URL without person-ID
  conflict, exact non-generic email without LinkedIn conflict, and a conflict-free transitive chain
  of those classes.
- LinkedIn identity conflict and generic/shared email guards apply to every automatic class,
  including clusters that also share a person ID.
- Phone-only clusters never merge automatically.
- The contact survivor follows the approved precedence across associated deals, activity, oldest
  creation time, populated properties, and CRM record ID.
- When low-confidence review is enabled, non-automatic contact candidates reach native Human Review;
  approval merges and decline or timeout writes nothing. When review is disabled, they end as
  `low_confidence_not_reviewed` without a write.

### Contact resources and completion

- The contact path contains `model:crm_contacts` and `play:deduplicate_contacts` and runs directly on
  the contact CRM extract.
- Direct contact search prepares normalized LinkedIn URL variants and email while querying phone
  exactly as stored. A second live search expands normalized values from the direct results,
  including one normalized phone per record; in-cluster comparison also uses phone match keys.
- The contact automatic gate applies the approved score, `autoEligible`, LinkedIn identity guard,
  and generic/shared-email guard to the complete cluster.
- Contact merge paths end after the native merge and never create post-merge update nodes.
- Contact normalization, enrichment, and association changes remain outside this deduplication
  workflow and require separate approval.
- Contact identity fields resolve before contact planning. The Slack channel resolves when
  low-confidence review is enabled; otherwise the review branch and Slack dependency are removed.
- Generated consumer types confirm the contact searches and merge payloads plus Human Review when
  enabled.
- The operator approves the contact policy, disabled contact deployment, and exact contact pilot as
  three distinct gates.
- The final contact report resolves the survivor from the merge response or an approved identity
  lookup, verifies every absorbed contact no longer resolves independently, and accounts for every
  terminal outcome.

## Shared adaptation and validation

- `infra/` keeps connectors, ownership folders, models, plays, and typed scripts in separate files.
- The checked resources contain one HubSpot shape. Salesforce or Attio replaces that shape in place.
- Compatible CRM resources already in the consumer project are reused and duplicate declarations
  removed.
- `node --import tsx evals/contract.mjs`, `cargo-ai project types`, `cargo-ai project check`, and
  `cargo-ai project plan` pass in the consumer project.
- Every enrolled row in each approved pilot has a terminal outcome or a named unresolved review.
- Each selected-path report accounts for every search, score, review, merge, decline, timeout,
  exclusion, stale source, and error.
