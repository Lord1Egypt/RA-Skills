# Evidence and Finding Contract

Every successful action produces an evidence object conforming to `schemas/evidence.schema.json`. Its `raw_path` and SHA-256 hash preserve traceability to the captured response. Search results are discovery evidence; retrieved first-party pages and dedicated scraper results carry higher directness.

Every material conclusion uses a finding object conforming to `schemas/finding.schema.json` and references one or more existing evidence IDs. A structural verifier must reject dangling evidence IDs. Semantic review must still confirm that the cited source supports the claim.

Research plans and action states conform to `schemas/research-plan.schema.json` and `schemas/action.schema.json`. Preserve action IDs across resume and snapshot comparison.
