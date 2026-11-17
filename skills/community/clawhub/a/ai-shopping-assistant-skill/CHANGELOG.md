# Changelog

## 2.0.1

- Reworded public instructions to remove agent-control and identity-override phrasing.
- Replaced prompt-specific detection fields with neutral source-quality signals.
- Preserved deterministic ranking, pricing, review, merchant and content-quality analysis.
- Added static release checks for risky instruction phrases.

## 2.0.0

- Added a deterministic Python engine under `scripts/`.
- Added dynamic state updates and product-line refresh decisions.
- Added user-fit candidate ranking and realizable-price calculation.
- Added review evidence weighting, merchant evidence analysis and source-quality detection.
- Added JSON request/response contracts and built-in self-tests.
- Kept order submission, payment and credential handling outside the Skill boundary.
