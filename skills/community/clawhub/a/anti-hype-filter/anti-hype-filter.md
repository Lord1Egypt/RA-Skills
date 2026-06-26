# SKILL: anti-hype-filter

## Purpose
Detect hype triggers and neutralize them by rewriting into verifiable claims with explicit uncertainty and risk.

## Inputs
- `text`, `policy.max_response_words`

## Steps
1. Extract claims and detect hype triggers.
2. Classify (signal|noise|manipulation_risk).
3. Produce a verifiable rewrite and minimal response draft.

## Output
- `anti_hype_result` with `classification`, `rewrite`, `response_draft`.

## Safety Rules
- Label risk, not intent. No financial promises.

