# Confidence scoring guide

## Example weighted score

- hard identifier exact: +0.55
- brand exact: +0.10
- model family exact: +0.15
- storage/RAM exact: +0.10
- color exact: +0.05
- condition exact: +0.05

Penalty examples:

- variant conflict: -0.40
- condition conflict: -0.30
- bundle ambiguity: -0.25

## Decision thresholds (example)

- score >= 0.85: auto-match
- 0.65 to 0.84: manual review
- < 0.65: reject

Tune thresholds by category and measured false-positive rate.

