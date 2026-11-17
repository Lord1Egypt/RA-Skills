# Analysis Frameworks

## Evidence Classification

- Fact: directly supported by a cited source.
- Inference: a reasoned interpretation of one or more facts.
- Recommendation: an action proposed for the user's decision.
- Unknown: material evidence not found, inaccessible, or not comparable.

Assign confidence to each major finding: high for consistent primary evidence, medium for partial or mixed evidence, and low for indirect or sparse evidence.

## Product Comparison

Compare only decision-relevant dimensions: target user, core job, coverage, inputs and outputs, integration, task lifecycle, observability, reliability signals, compliance claims, developer experience, and support model.

Use `present`, `partial`, `not found publicly`, or `not applicable`. Never turn `not found publicly` into `absent`.

## Pricing Intelligence

Normalize currency, billing period, included units, overage units, minimum commitment, discounts, and relevant limits. Compare the cost of the same defined workload, then list assumptions and sensitivity drivers. Do not compare plan sticker prices when the included workload differs.

## Review Intelligence

Report source, date range, sample size, and sampling bias. Cluster repeated themes and include frequency or evidence count. Separate isolated anecdotes from recurring signals.

## Hiring Signals

Group roles by function, location, seniority, and posting date. Hiring indicates possible investment direction, not confirmed strategy. Label this output as inference.

## Market Landscape

Separate direct competitors, adjacent competitors, substitutes, and build-it-yourself alternatives. Segment by customer, job-to-be-done, delivery model, or price model before identifying whitespace.

## Prioritization

Score recommendations using:

`priority = decision impact × evidence confidence × feasibility ÷ effort`

Use P0 only for a blocker that prevents adoption, creates material trust risk, or breaks the core promised workflow. Keep lower-confidence opportunities out of P0.
