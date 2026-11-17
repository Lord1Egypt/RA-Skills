# Complex Form Review Template

Use for onboarding, configuration, applications, checkout, multi-step editors, and high-consequence submission flows.

## Scope Inputs

- Completion goal, required roles, expected duration, and abandonment cost.
- Field dependencies, validation source, save model, and destructive exits.
- Privacy, compliance, payment, or irreversible submission constraints.

## Evidence Checklist

- Field sequence follows user knowledge and reveals dependencies at the right time.
- Labels, help, defaults, formats, optionality, and examples are explicit.
- Validation occurs at a useful time, points to the cause, preserves input, and supports recovery.
- Progress describes meaningful stages; back navigation and resume behavior are predictable.
- Draft, autosave, concurrent edit, expiration, offline, retry, duplicate submit, and success states are covered.
- Review/confirmation exposes the exact consequences before high-risk submission.

## High-Risk Findings

- `P0`: data loss, double submission, hidden charge, inaccessible required field, or irreversible action without informed confirmation.
- `P1`: validation loops, unclear dependencies, or forced re-entry materially reduce completion.
- `P2`: grouping, microcopy, input sizing, or progressive disclosure needs polish.

## Acceptance Examples

- First invalid field receives focus and every error is associated with its control.
- Reload or recoverable failure does not discard completed work.
- Back navigation preserves valid input and explains any invalidated dependent fields.
- Submission status prevents duplicates and announces the final result.
