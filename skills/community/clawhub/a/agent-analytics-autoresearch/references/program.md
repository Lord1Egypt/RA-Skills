# Autoresearch Growth Loop

You are running an instruction-driven growth loop. Produce two high-quality variants that can be tested against the current control for the project described in `brief.md`.

Do not change product code while running the loop. Produce reviewable copy artifacts first.

Default mode is review-only. Only move into implementation, experiment creation, or measurement after the user explicitly approves that next phase.

## Setup

1. Read `brief.md` fully.
2. Treat `brief.md` as the source of truth for the project, audience, surface, control, metrics, analytics data, and drift constraints.
3. If `results.tsv` does not exist, create it with:

```tsv
round	candidate_a	candidate_b	candidate_ab	winner	borda_a	borda_b	borda_ab	status	rationale
```

4. If `final_variants.md` exists, overwrite it only at the end of a completed loop.

## Data Brief

Before generating copy, collect or read the data described in `brief.md`.

The data source can be Agent Analytics, another analytics CLI, an API, SQL, CSV, exported reports, product logs, or manually supplied data.

Rules:

- Never invent numbers.
- If a command fails, record the failure.
- Treat missing data as missing data, not zero data.
- Separate primary outcome data from proxy and guardrail data.
- If data is sparse, say so and treat it as weak signal.

## Scope

During the loop, edit only:

- `results.tsv`
- `final_variants.md`
- optional scratch notes

Do not edit the live site, app, product code, or experiment setup until the variants have been reviewed.

## Product Truth

Every candidate must preserve the product truth from `brief.md`.

Penalize:

- generic category language
- copy a competitor could say word for word
- unsupported claims
- drift away from the real product value
- clickbait that weakens primary conversion intent
- changes that ignore the current control's strengths

Reward:

- specificity
- clear audience fit
- concrete user outcome
- stronger primary-event intent
- honest use of the available data
- language only this product could credibly say

## Loop

Run at least 5 rounds unless `brief.md` specifies a different count.

Each round has four phases.

### 1. Candidate A

For round 1, candidate A is your first new hypothesis based on the brief, control, and data.

For later rounds, candidate A is the previous round winner.

Include the editable parts named in the brief, usually headline, subheadline, CTA, supporting copy, and hypothesis.

### 2. Critique

Critique candidate A harshly:

- what is generic
- what a competitor could say
- where value is unclear
- where copy drifts from product truth
- whether primary-event intent is strong enough
- whether the control is clearer

### 3. Candidate B And Synthesis AB

Write candidate B from the critique as if starting fresh. It may use the brief and critique, but it should not be a mild rewrite of A.

Then write candidate AB by combining the strongest parts of A and B. Do not average them into bland middle copy.

### 4. Blind Borda Ranking

Blind-rank A, B, and AB. To simulate blind judging, anonymize them as `option_1`, `option_2`, and `option_3` in a different order each round before scoring.

Score:

- first place: 2 points
- second place: 1 point
- third place: 0 points

Use the rubric in `brief.md`. If none exists, rank by specificity, clarity, primary-event intent, product truth, low competitor-sayable language, and fit with analytics data.

Append one row to `results.tsv` after each round. Keep rationale short and TSV-safe.

Winner becomes candidate A for the next round.

## Final Selection

After the final round, choose the two strongest distinct candidates. They should not be tiny wording variations of each other.

Write `final_variants.md` with:

- candidate_1
- candidate_2
- exact changed copy
- rationale
- risks
- recommended experiment name
- experiment shape
- data limitations

End with a clear note that the experiment has not been wired yet.

## Approved Outer Experiment Loop

Run this section only if the user explicitly asks you to implement or wire the approved experiment.

1. Implement the approved variant or variants in the product surface named in `brief.md`.
2. Create the experiment with the recommended control and candidate variants.
3. Verify tracking for the primary metric, proxy metric, and guardrails.
4. Let the experiment collect behavior for the requested window.
5. Pull the experiment results into a new dated data snapshot, including:
   - winning and losing variants
   - primary metric movement
   - proxy metric movement
   - guardrail movement
   - screenshots or changed-copy notes
   - data limitations
6. Start the next autoresearch loop from that measured evidence.

The LLM loop generates pressure. The outer experiment loop decides what survived contact with users.
