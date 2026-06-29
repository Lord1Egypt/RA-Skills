# Precision Review Pipeline

Precision review is optional and advisory.

## Use

Use a review pipeline when the repository benefits from periodic deeper checks beyond per-slice proof.

## Review Dimensions

A runtime MAY schedule checks such as:

- static analysis
- changed-file regression scan
- touched-interface review
- architecture boundary review
- security review
- contract adherence review

## Rules

- Review findings MUST be classified by severity.
- Review findings MUST NOT silently rewrite core loop status.
- Review findings are advisory unless a repo-local runtime policy explicitly defines a control action.
- Review cadence MUST be configurable.

## Output Shape

A review report SHOULD include:

- scope reviewed
- checks run
- findings by severity
- exact commands where applicable
- one recommendation
