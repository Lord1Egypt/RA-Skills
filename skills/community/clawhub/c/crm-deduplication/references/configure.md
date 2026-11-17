# Configure CRM deduplication

Choose account deduplication, contact deduplication, or both. Apply only the matching and survivor
policy approved for each selected path. Approval for one path does not authorize resources or
merges for the other.

## Shared CRM and review setup

The checked example uses one default HubSpot connector and one default Slack connector. Reuse
compatible project resources rather than deploying duplicate slugs. For Salesforce or Attio,
replace the connector, selected extracts, object names, record IDs, search action, merge action, and
property slugs together. Keep one CRM shape across selected paths.

Both paths must keep these properties:

- the play runs directly on its CRM-backed object model
- the filter requires the CRM record ID and at least one approved identity key
- every decision refreshes candidate records through the live CRM search
- connectors have no cache
- the play is disabled, uses `noConcurrency`, and is limited to 15 rows

A cached CRM read is the one kind of staleness the fresh-source guard cannot see.

## Path 1: Configure account deduplication

### Account resources

The account path consists of:

- `infra/models/crm-accounts.ts`
- `infra/plays/deduplicate-accounts.ts`
- `infra/scripts/accounts/account.ts`
- `infra/scripts/accounts/cluster.ts`
- `infra/scripts/accounts/policy.ts`
- `infra/scripts/accounts/survivor.ts`
- `infra/scripts/accounts/evidence.ts`

It also reads `infra/scripts/common/`, which both paths share. Adapt matching and survivor policy in
`infra/scripts/accounts/policy.ts`; the rest of `accounts/` is machinery that reads it.

`crm_accounts` must remain a direct CRM company extract. `deduplicate_accounts` owns the live
company search, evidence score, Human Review, and every company merge.

### Account search and score

The live company search passes only LinkedIn company ID, LinkedIn company page, and domain. Empty
criteria are skipped. The evidence script retains the source row exactly once, normalizes the
cluster, rejects generic-domain-only identity, exposes conflicts, and selects the survivor.

The compiled graph contains one native Scoring node:

| Evidence                                                | Score |
| ------------------------------------------------------- | ----: |
| Exact LinkedIn company ID across the cluster            |    60 |
| Exact LinkedIn company URL or handle across the cluster |    25 |
| Exact non-generic domain across the cluster             |    15 |

The score explains confidence. It does not replace the conflict gate. LinkedIn URL plus domain
remains manual even when both agree.

### Account survivor and guards

The default survivor precedence is:

1. record with a protected business ID
2. customer record
3. most open opportunities
4. most contacts
5. most activities
6. most populated properties
7. latest activity
8. oldest creation time
9. lexicographically smallest CRM record ID

Map the approved protected-ID and parent-company properties into the workflow input. When the
operator changes precedence, update the account ranker and its contract fixture together.

Automatic company merge requires all of these:

- at least one other CRM record remains after the fresh search
- score is at least 60
- every record has the same non-empty normalized LinkedIn company ID
- there is no non-null LinkedIn ID, LinkedIn URL, or domain conflict
- there is no protected business ID conflict
- there is no parent-subsidiary relationship inside the cluster

The automatic path calls `mergeRecords` with the deterministic survivor and every other company ID.
The manual path shows score, survivor, absorbed IDs, conflict flags, and normalized evidence in
Human Review. Approval calls the same merge action. Decline or timeout writes nothing.
`PLACEHOLDER_REVIEW_CHANNEL_ID` must resolve to the approved account review channel before planning.
If it cannot be resolved, keep the account play disabled and stop before a pilot.

If the queued source company has already been absorbed or changed, end as
`source_missing_or_changed` before scoring or emitting merge IDs.

### Account graph review

Confirm the compiled graph has:

- one live company search followed by deterministic evidence preparation
- one native Scoring node with the 60/25/15 criteria
- an automatic branch requiring both score and `autoEligible`
- one native Human Review node on the non-automatic path
- exactly two company merge nodes, one automatic and one approved
- no merge on decline, timeout, missing source, or no-duplicate paths

## Path 2: Configure contact deduplication

### Contact resources

The contact path consists of:

- `infra/models/crm-contacts.ts`
- `infra/plays/deduplicate-contacts.ts`
- `infra/scripts/contacts/contact.ts`
- `infra/scripts/contacts/identity.ts`
- `infra/scripts/contacts/cluster.ts`
- `infra/scripts/contacts/policy.ts`
- `infra/scripts/contacts/survivor.ts`
- `infra/scripts/contacts/search.ts`
- `infra/scripts/contacts/transitive-search.ts`
- `infra/scripts/contacts/evidence.ts`

It also reads `infra/scripts/common/`, which both paths share. Adapt generic-email and survivor
policy in `infra/scripts/contacts/policy.ts`; the rest of `contacts/` is machinery that reads it.

`crm_contacts` must remain a direct CRM contact extract. `deduplicate_contacts` owns both live
contact searches, evidence score, optional Human Review, and every contact merge.

### Contact search and score

The first live search uses LinkedIn person ID, four normalized LinkedIn URL variants, normalized
email, and the phone value exactly as stored. The second search expands normalized identity values
from the direct results, including one normalized phone per record, so pairwise high-confidence
matches form one transitive cluster. In-cluster comparison also uses phone match keys.

The native Scoring node assigns 60 to each approved high-confidence class:

- exact LinkedIn person ID
- exact LinkedIn URL without a person-ID conflict
- exact non-generic email without a LinkedIn conflict
- conflict-free transitive chain of those classes

The score shows which approved classes matched. Several criteria can be true, so the score is
additive and not a percentage. Automatic merge still requires `autoEligible`.

### Contact survivor and guards

The default survivor precedence is:

1. most associated deals
2. most activity
3. oldest creation time
4. most populated properties
5. lexicographically smallest CRM record ID

When the operator changes precedence, update the contact ranker and its contract fixture together.

Automatic contact merge requires all of these:

- at least one other CRM record remains after both fresh searches
- score is at least 60
- one approved high-confidence class is true
- there is no LinkedIn person-ID or LinkedIn URL conflict
- there is no generic or shared-email risk
- the group is not phone-only

When `lowConfidenceContactReviewEnabled` is true, every non-automatic group reaches Human Review.
Its message shows the score, proposed survivor, absorbed IDs, LinkedIn conflicts, generic-email
risk, and one evidence line per record. Approval merges. Decline or timeout writes nothing. When
review is disabled, the same group ends as `low_confidence_not_reviewed` without a CRM write.
Resolve `PLACEHOLDER_REVIEW_CHANNEL_ID` before planning when contact review is enabled. When it is
disabled, remove the contact review branch and its Slack dependency during adaptation, then update
the exact resource inventory, shared connector loop, contact graph assertions, and fixtures in
`evals/contract.mjs`.

If the queued source contact has already been absorbed or changed, end as
`source_missing_or_changed` before scoring or emitting merge IDs. Treat `mergeRecords` as the final
CRM write. Normalization, enrichment, and association changes require a separate approved workflow.

### Contact graph review

Confirm the compiled graph has:

- one direct and one transitive live contact search
- deterministic search preparation and evidence preparation
- one native Scoring node with the four approved 60-point classes
- an automatic branch requiring both score and `autoEligible`
- one optional native Human Review node on the non-automatic path
- exactly two contact merge nodes when review is enabled, one automatic and one approved
- no `updateRecords` node after either merge
- no merge on decline, timeout, disabled review, missing source, or no-duplicate paths

## Validate selected paths

```sh
npm run typecheck
node scripts/check-pipelines.mjs
node --import tsx crm-deduplication/evals/contract.mjs
cargo-ai project plan
```

Confirm the plan contains the shared CRM connector, the Slack connector when at least one selected
path uses Human Review, shared ownership folders, and only the approved object models and plays. If
one path is out of scope, remove its model and play files plus its object-specific contract
assertions, exact resource inventory entries, and connector-loop entries before running the checks.
Deploy selected plays disabled. Send direct Cargo links for each deployed play before requesting its
separate merge-capable pilot approval.
