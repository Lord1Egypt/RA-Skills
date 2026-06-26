# Changelog

## 0.4.4 - 2026-05-19

- sync the published feed manager runtime with the latest repo implementation
- add scripted `deploy-communal-proxy` support and communal-proxy-aware post-funding execution
- preserve the guarded execution boundary while improving downstream EVK/Morpho readiness guidance

## 0.4.0 - 2026-04-28

- clarified that `browser-assisted` funding should hand off to `browser-plan` plus browser execution when the Api3 Market flow is reachable
- documented that feed readiness must be re-checked after any direct, wrapper, or browser-assisted funding execution before downstream EVK steps continue
- tightened downstream handoff guidance so agents preserve `fundingExecutionClassification.state` and do not blur deployment success into borrowability proof

## 0.3.0 - 2026-04-22

- synced the packaged skill runtime with the latest repo `api3-feed-manager` implementation
- added guarded `execute-buy-subscription` support for the first exact executable funding path
- added execution-mode selection:
  - `auto`
  - `direct`
  - `wrapper` when exact wrapper calldata is safely derivable
- added machine-usable funding state classification:
  - `not-needed`
  - `executable`
  - `browser-assisted`
  - `unsupported`
- updated the skill docs to reflect the current automation boundary and browser-assisted fallback path
