# Evaluation protocol and empirical lessons

Read this reference when building a benchmark, selecting metrics, or interpreting results.

## Minimal comparison

Compare at least:

1. always local;
2. always cloud;
3. confidence-only routing;
4. routing plus OOD;
5. routing plus independent gate;
6. the complete controller;
7. an oracle only as a clearly labeled upper bound.

Freeze the router, features, thresholds, and gate policy before the independent test. Keep variants of the same base task in the same split. Do not tune on the final benchmark.

## Metrics

### Competence

- route accuracy and macro-F1;
- local coverage;
- local selective risk;
- task success after escalation;
- calibration and confidence for correct versus incorrect cases.

### Safety

- unsafe tool execution rate;
- false-execute rate;
- overblocking of expected-allow actions;
- constraint-shift pair accuracy;
- stale-policy refresh success;
- prompt-injection success or containment;
- coverage blindspots where tool intent never reaches the gate.

### Economy and availability

- cloud-call rate;
- input, output, cached, and reasoning tokens;
- median and p95 latency;
- local memory and accelerator use;
- provider quota or timeout failures;
- cost per safe successful task when price is relevant.

### Auditability

- event completeness;
- component and policy versions;
- reason for escalation or block;
- absence of credentials and authorization tokens.

## Findings from the reference investigation

These findings motivate the skill but are not universal guarantees:

- A word/character TF-IDF logistic router outperformed rules, XGBoost, and the tested Laya SLM on a 32-case challenge set: 81.25% versus 25.00%, 50.00%, and 31.25% route accuracy.
- Fine-tuning the Laya model did not surpass the linear router and showed 56.25% prediction disagreement after reversing option order in one configuration.
- In a frozen 200-case benchmark, the complete system achieved 43.00% local coverage, 87.21% local accuracy, 12.79% selective risk, 57.00% cloud use, 89.06% error containment, zero observed unsafe tool executions, and 24/25 correct constraint-shift pairs.
- Lexical OOD improved local accuracy from 83.81% to 87.21% but reduced local coverage from 52.50% to 43.00%. It detected 51.56% of router errors and flagged 22.79% of correct decisions.
- In a 32-case Gemini integration pilot, selective routing matched the all-cloud route accuracy at 87.50% while reducing calls by 56.25% and tokens by 56.48%.

## Interpretation limits

Do not infer from these results that:

- zero observed violations is a formal guarantee;
- the linear model wins in every domain;
- the Gemini strategies are statistically equivalent;
- lexical OOD detects authorization changes;
- a prompt-level skill can replace an enforcement gate;
- an oracle-backed result measures real LLM quality.

The central supported principle is narrower: competence, authorization, and availability require separate evidence and separate metrics.

## Acceptance criteria example

Set targets before the independent test. A practical initial set is:

- zero unsafe tool executions in the represented scenarios;
- local coverage at least 50%;
- local selective risk at most 10%;
- total cloud rate below 50%;
- at least 80% of router errors escalated or contained;
- overblocking no more than 10%;
- local path p95 below the application budget;
- complete sanitized audit.

Report failed criteria. Do not retune the same version on the final labels.

