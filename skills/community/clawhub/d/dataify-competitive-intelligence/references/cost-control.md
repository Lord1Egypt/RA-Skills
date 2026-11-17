# Scope and Cost Control

Use action count as the enforceable budget until Dataify exposes a reliable preflight credit quote. `quick`, `standard`, and `deep` default to 5, 12, and 20 total actions. The limit includes discovery and follow-up collection, so the planner reserves capacity for both stages.

Confirm before deep, high-volume, multi-page, media, or materially credit-sensitive collection. Do not invent a credit estimate. If a response exposes actual usage, record it in action metadata and report the observed total.

Retry discovery and page fetching at most once after an ordinary failure. After correcting an external problem, `--resume <run> --retry-failed-safe` resets only failed discovery and page actions. Do not automatically retry a failed structured scraper action because submission may already have incurred cost; recover through its task ID when available.
