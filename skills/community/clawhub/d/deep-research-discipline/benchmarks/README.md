# Benchmark: evidence discipline

A small protocol to check whether a research run is **auditable**, not whether it is *correct*. It measures labelling and traceability, which can be checked mechanically; factual accuracy still needs a domain reviewer.

## Metrics

| Metric | Definition | How to compute |
|---|---|---|
| Citation coverage | share of material claims with a URL and retrieval date | count claims in the report; count those with a source |
| Unsupported claims | claims with no source, or a source that does not contain the claim | manual spot-check of 5 claims |
| Label completeness | share of material claims carrying verified / single-source / unresolved | count labelled claims |
| Conflict disclosure | conflicts shown rather than averaged | read the conflicting-evidence section |
| Review performed | independent review exists, or `not performed` is explicit | read the review section |

## Protocol

1. Give the agent one case from `cases.json` with no hints.
2. Collect the report.
3. Score the five metrics; spot-check 5 claims against their cited URLs.
4. Record the capability line the agent declared at start; a missing capability must appear in limitations.

## What this does not measure

- Whether the answer is true. That requires a domain expert.
- Search quality or speed.
- Performance across models. No cross-model comparison has been run.

## Current status

`results-partial.md` contains 3 of 10 cases, run once on a single environment. **No aggregate accuracy or improvement claim is made.** Publish your own numbers if you run the full set.
