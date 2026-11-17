# Run and report

Choose the account path, contact path, or both. Run each selected path only after its audit and
disabled build pass. A deployed disabled play can still mutate CRM records when manually run, so
disabled deployment approval and merge-capable pilot approval are separate gates for each path.
Approval for one path does not authorize the other.

## Shared deployment safety

Before deploying either path, run the checks from `SKILL.md`, inspect the compiled graphs, and
review `cargo-ai project plan`. Deploy only the approved resources, with every selected play set to
`isEnabled: false`, `runCreationRule: noConcurrency`, and `limit: 15`.

Resolve `workspaceUuid` from `cargo-ai whoami` (`workspace.uuid`) and each selected play UUID from
`cargo.state.json` or the matching list command. Send the direct play URL for each selected path:

`https://app.getcargo.io/workspaces/<workspaceUuid>/plays/<deduplicationPlayUuid>`

Immediately before either pilot, refresh the live audit and target population, re-read the selected
CRM integration schema and costs plus Slack for paths with active review, inspect the compiled graph,
and run from this skill's folder:

```sh
node --import tsx evals/contract.mjs
```

Run only the approved rows. Monitor every workflow until it reaches a terminal outcome. A Human
Review request is pending work, not a completed pilot. After a successful pilot, ask separately
before enabling that path's recurring schedule.

## Path 1: Run account deduplication

### Before the account pilot

1. Confirm the account audit and policy are approved, and confirm the operator separately authorized
   disabled deployment of the account path.
2. Confirm `deduplicate_accounts` runs directly on `crm_accounts` and matches the audited CRM account
   record ID.
3. Confirm the compiled graph searches the live CRM, retains the source once, prepares account
   evidence, runs native Scoring, selects the survivor, and merges only on the automatic or approved
   review paths.
4. Confirm the automatic path requires a score of at least 60, one exact shared LinkedIn company ID,
   and no identity, protected-ID, or parent-subsidiary conflict.
5. Confirm `PLACEHOLDER_REVIEW_CHANNEL_ID` and all protected-ID and parent-company property
   placeholders are resolved.
6. Confirm the account play is disabled, uses `noConcurrency`, and is limited to the exact approved
   population of no more than 15 account rows.
7. Recount the account candidates and refresh the current CRM search, merge, and Slack review costs.
8. Send the direct account play link, confirm that it resolves, and provide the complete pilot
   handoff.

### Approve the account pilot

The handoff names the approved account matching keys, protected fields, 60/25/15 evidence score,
automatic class, survivor precedence, review owner, Slack channel, timeout, exact population, and
current action costs. Ask the operator to approve this account population and merge-capable policy.
Do not treat contact approval or disabled deployment approval as account pilot approval.

### Run the account pilot

Run only the approved account rows. Monitor every `findRecords`, Scoring, Human Review, and
`mergeRecords` action until the workflow reaches `no_duplicates`, `source_missing_or_changed`,
`merged_automatically`, `merged_after_review`, or `review_declined_or_timed_out`.

Do not broaden the population, relax the conflict gates, or rerun a failure until the operator sees
the new target and any repeat action cost.

### Verify and report the account pilot

For every account merge, re-read the surviving CRM account and confirm that each absorbed account ID
no longer resolves as an independent company. Verify the retained protected identifiers,
parent-company relationship, and survivor fields against the approved precedence.

Report:

- the direct account play link and exact approved population
- every source account ID, score, survivor ID, absorbed ID, conflict flag, and terminal outcome
- automatic merges, approved merges, declines, timeouts, exclusions, stale sources, and failures
- reviewer identity when present, the CRM response, and current action costs
- confirmation that every merged survivor and absorbed account ID was verified in the CRM
- processed rows reconciled against terminal outcomes and named unresolved reviews
- one recommended `Next step`: improve weak identity coverage, remediate failed merges, review
  declined clusters, or approve recurring account deduplication

### Account stop conditions

Stop the account run and report the evidence if:

- the live CRM or Slack action schema differs from the compiled graph
- the play is enabled, allows concurrency, or exceeds the approved 15-row maximum
- a CRM account ID matches the wrong source record or the fresh search does not contain the source
- an account merges automatically without the exact shared LinkedIn company ID or while a conflict
  flag is present
- a decline or timeout reaches a CRM write
- an absorbed account still resolves independently after merge
- processed rows do not reconcile to terminal outcomes and unresolved reviews
- the current action cost or target population exceeds the approved account handoff

## Path 2: Run contact deduplication

### Before the contact pilot

1. Confirm the contact audit and policy are approved, and confirm the operator separately authorized
   disabled deployment of the contact path.
2. Confirm `deduplicate_contacts` runs directly on `crm_contacts` and matches the audited CRM contact
   record ID.
3. Confirm the compiled graph performs the direct live search, expands the transitive search, retains
   the source once, prepares contact evidence, runs native Scoring, selects the survivor, and merges
   only on the automatic or approved review paths.
4. Confirm automatic eligibility is limited to exact LinkedIn person ID, exact LinkedIn URL without
   person-ID conflict, exact non-generic email without LinkedIn conflict, or a conflict-free
   transitive chain of those classes.
5. Confirm LinkedIn identity conflict and generic or shared email disqualify every automatic class,
   and phone-only groups never merge automatically.
6. Confirm every contact identity property slug matches the live CRM. When low-confidence review is
   enabled, confirm `PLACEHOLDER_REVIEW_CHANNEL_ID` resolves to the approved channel. Otherwise,
   confirm the review branch and its Slack dependency were removed during adaptation.
7. Confirm the contact play is disabled, uses `noConcurrency`, and is limited to the exact approved
   population of no more than 15 contact rows.
8. Recount the contact candidates and refresh current CRM search and merge costs plus Slack review
   costs when review is enabled.
9. Send the direct contact play link, confirm that it resolves, and provide the complete pilot
   handoff.

### Approve the contact pilot

The handoff names the approved contact matching keys, global conflict guards, automatic classes,
survivor precedence, low-confidence disposition, exact population, and current action costs. When
review is enabled, it also names the review owner, Slack channel, and timeout. Ask the operator to
approve this contact population and merge-capable policy. Do not treat account approval or disabled
deployment approval as contact pilot approval.

### Run the contact pilot

Run only the approved contact rows. Monitor every direct and transitive `findRecords` search,
Scoring, Human Review, and `mergeRecords` action until the workflow reaches `no_duplicates`,
`source_missing_or_changed`, `merged_automatically`, `merged_after_review`, or
`review_declined_or_timed_out`. When low-confidence review is disabled,
`low_confidence_not_reviewed` is also a terminal outcome.

Treat the native contact merge as the final CRM write. Do not add or run a post-merge update.
Do not broaden the population, relax the global conflict guards, or rerun a failure until the
operator sees the new target and any repeat action cost.

### Verify and report the contact pilot

Do not assume the pre-merge primary contact ID survives. Use the `mergeRecords` response ID or search
by the approved identity keys, require exactly one canonical contact, inspect the properties retained
by the CRM's native merge, and confirm that every absorbed contact ID no longer resolves
independently.

Report:

- the direct contact play link and exact approved population
- every source contact ID, matched classes, score, survivor ID, absorbed ID, conflict flag, and
  terminal outcome
- automatic merges, approved merges, declines, timeouts, exclusions, stale sources, and failures
- reviewer identity when present, the CRM response, and current action costs
- confirmation that every canonical contact and absorbed contact ID was verified in the CRM
- confirmation that no post-merge update ran
- processed rows reconciled against terminal outcomes and named unresolved reviews
- one recommended `Next step`: improve weak identity coverage, remediate failed merges, review
  declined clusters, or approve recurring contact deduplication

### Contact stop conditions

Stop the contact run and report the evidence if:

- the live CRM or active Slack action schema differs from the compiled graph
- the play is enabled, allows concurrency, or exceeds the approved 15-row maximum
- a CRM contact ID matches the wrong source record or the fresh search does not contain the source
- a LinkedIn conflict, generic or shared email cluster, or phone-only group merges automatically
- a decline or timeout reaches a CRM write
- a post-merge update appears or the canonical contact cannot be resolved exactly once
- an absorbed contact still resolves independently after merge
- processed rows do not reconcile to terminal outcomes and unresolved reviews
- the current action cost or target population exceeds the approved contact handoff
