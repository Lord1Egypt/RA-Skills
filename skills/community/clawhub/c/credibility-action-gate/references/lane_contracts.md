# Lane Contracts

The coordinator compares independent lane outputs. Lanes may be produced by code, models, retrieval, human notes, or domain tools, but each lane should be normalized before coordination.

## Lane Record

```json
{
  "lane_type": "evidence",
  "status": "completed",
  "confidence": "medium",
  "findings": [
    {
      "code": "IDENTITY_OR_LINKAGE_UNVERIFIED",
      "severity": "medium",
      "summary": "The record supports the general need but not claimant linkage."
    }
  ],
  "positives": [
    {
      "code": "DATED_PRIMARY_DOCUMENT_PRESENT",
      "summary": "A dated document is present and legible."
    }
  ],
  "decision": {
    "supports_core_claim": "partial",
    "supports_requested_action_size": "unknown",
    "claimant_linkage": "unknown",
    "source_independence": "not_applicable"
  },
  "limitations": [
    "Document authenticity was not independently checked."
  ]
}
```

## Required Fields

- `lane_type`: stable lane name, such as `evidence`, `external_context`, `graph_history`, `policy`, or `domain`. This must match the `NAME` in `--lane NAME=file.json`; mismatches are rejected.
- `status`: `completed`, `missing`, `not_applicable`, or `error`. Required lanes satisfy policy only when `completed`; `not_applicable` is preserved as a valid lane status but does not count as completed evidence for a required lane.
- `findings`: array of concern objects.
- `decision`: lane-specific normalized facts used by the coordinator.

## Finding Severity

- `info`: note only.
- `low`: weak concern or limitation.
- `medium`: material uncertainty that should reduce size or confidence.
- `high`: strong concern that should usually reject, monitor, or require a much smaller action.
- `critical`: hard blocker under ordinary policies.

## Recommended Generic Codes

- `UNSUPPORTED_ON_CURRENT_RECORD`
- `CONTRADICTION_IN_RECORD`
- `IDENTITY_OR_LINKAGE_UNVERIFIED`
- `USE_OF_FUNDS_UNVERIFIED`
- `REQUESTED_ACTION_SIZE_UNSUPPORTED`
- `SOURCE_INDEPENDENCE_WEAK`
- `COPIED_TEXT_OR_TITLE_RISK`
- `SYNTHETIC_CONSENSUS_RISK`
- `REPEATED_RECIPIENT_PATTERN`
- `RELATED_RECORD_NETWORK_CONCERN`
- `POST_ACTION_MOVEMENT_UNREVIEWED`
- `POLICY_AUTHORITY_EXCEEDED`
- `DOMAIN_HARD_BLOCKER`

## Decision Fields The Coordinator Understands

Completed lanes require an explicit `status: "completed"`, a `findings` array (which may be empty), and a `decision` object. Omitted status is treated as `missing`. Completed `evidence` lanes must include `supports_core_claim`, `supports_requested_action_size`, and `claimant_linkage`; completed `external_context` lanes must include `public_context_plausibility` and `source_independence`. Other lane types retain their domain-specific decision shape, including an empty object for a completed history review with no decision fields.

Known decision fields must use the values below. Malformed records, invalid decision values and invalid finding severities cause a nonzero CLI exit without a disposition. Callers must treat that failure as no eligibility and must not reuse an earlier output file as the current result. Existing complete bundled records remain compatible; integrations relying on implicit completion or missing required decision fields must update their lane producers before adoption.

The coordinator uses these decision fields:

- `supports_core_claim`: `yes`, `partial`, `unknown`, `no`, `contradiction`, or `unsupported`.
- `supports_requested_action_size`: `yes`, `partial`, `unknown`, `no`, or `unsupported`. `no` and `unsupported` reject the current requested action size; `partial` and `unknown` require explicit bounded-uncertainty permission for any action.
- `source_independence`: `strong`, `some`, `weak`, `none`, or `not_applicable`.
- `public_context_plausibility`: `all_found`, `some_found`, `weak`, `not_found`, or `not_applicable`.
- `claimant_linkage`: `verified`, `partial`, `unknown`, `unverified`, or `contradicted`.
- `repeat_or_top_up_support`: `fresh_reason_present`, `weak`, `none`, or `not_applicable`.

Unknown top-level fields are preserved in the coordinator's `lane_details` output but do not affect deterministic rules.

For repeat actions, only `fresh_reason_present` supplies affirmative support. Omitted support, `not_applicable`, `weak`, and `none` leave the recommended amount at zero. Support is read from a completed evidence lane, falling back to a completed external-context lane only if evidence omits that field. A first action does not require repeat support.

Completion records that a review occurred; it does not establish that every operator minimum was met. Domain-specific mandatory checks can use existing `required_lanes` entries: keep a required check `missing` or `error` while unavailable, and emit a configured hard blocker when a completed check establishes that an operator condition is unmet. Unknown linkage is uncertainty, not a universal identity-document requirement. The calling review must explicitly represent any non-waivable operator minimum; unrelated positive fields or uncertainty permission cannot substitute for it.

## Eligibility policy in contract 0.3.0

The coordinator applies these rules in order:

1. Authority limits and configured hard blockers keep the amount at zero.
2. A completed lane reporting core support `no`/`unsupported` or core/linkage contradiction rejects the current record, even with positive public context or disabled high-finding rejection. Unsupported requested size also rejects. These are adverse conclusions; unknown information is handled separately.
3. Required lanes and fresh repeat support must still be present. Uncertainty permission never waives them.
4. Partial, unknown or unverified material support, missing material decisions across completed lanes, weak source independence, missing/unknown/low reviewer confidence, and medium findings default to `monitor_until_new_evidence` with amount zero and explicit reasons.
5. Only `disposition_preferences.uncertainty_action: "small_test"` permits action with medium uncertainty. Its amount is capped by the minimum of `small_test_action_size`, requested size and maximum autonomous size. The opt-in requires an explicitly supplied positive finite numeric `authority.small_test_action_size`; it cannot use an implicit fallback. The default is `"monitor"`; other values are errors. High/critical signals cannot use this permission. The selected preference is included as `policy.uncertainty_action` in output.

The older `multiple_medium_concerns` preference no longer authorizes an action. `reject_on_any_high` and `reject_on_any_critical` may still select rejection for other findings; disabling rejection does not authorize spending on high/critical findings. Callers using old complete lane JSON remain structurally compatible, but uncertain cases now wait unless the operator explicitly permits a bounded test.

Completed reviewers may report `confidence` as `high`, `medium`, `low`, `unknown`, null or omit it. Invalid values are rejected. Missing/unknown/low confidence produces an uncertainty reason and `low_to_medium` aggregate confidence. With no material uncertainty, all completed reviewers must explicitly report high confidence for `medium_to_high`; any medium reviewer caps it at `medium`. No completed reviewers cannot imply high confidence. Confidence is a review summary, not a platform trust score or a substitute for support.

No rule requires formal identity documents, payment, additional evidence purchases or human escalation. Use proportionate available evidence and operator policy; an inaccessible optional source alone is not an adverse fact.

Only completed lanes supply decision assertions to the semantic rules. Incomplete optional lanes remain visible in `lane_details` as limitations; unavailable access no longer synthesizes a medium finding. Explicitly reported material findings are still considered even when a lane could not finish. An incomplete required lane still blocks through the required-lane check. Stale decision fields retained in an errored lane cannot support or reject the current action.
