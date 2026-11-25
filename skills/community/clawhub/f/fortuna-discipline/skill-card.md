## Description:

Randomness with exactly one office — tiebreaker among genuinely equivalent options, proposer of seeds and directions, never ruler — with every draw and counter state logged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchkeeper-simon](https://clawhub.ai/user/torchkeeper-simon)

### License/Terms of Use:

MIT-0

## Use Case:

An agent can use this skill to break ties among genuinely equivalent acceptable choices, or to let a draw propose a seed or direction while leaving the decision-maker accountable for the outcome. It provides a pre-draw checklist and an auditable draw-log format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A draw could be used to decide a question involving truth, safety, or the principal's interests, or to avoid making a decision.

Mitigation: Use a lot only among genuinely equivalent acceptable options; retain the decision-maker's judgment over truth, safety, principal interests, and any proposal produced by a draw.

Risk: An unlogged draw, unauditable entropy source, or unexplained mapping can make the outcome hard to verify or reproduce.

Mitigation: Use true entropy, record each draw and its source counter where available, show the mapping arithmetic, and accept the result without re-rolling.

## Reference(s):

- [ClawHub release](https://clawhub.ai/torchkeeper-simon/skills/fortuna-discipline)
- [Server-resolved GitHub provenance](https://github.com/torchkeeper-simon/threshold-kit/tree/main/fortuna-discipline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance with a pre-draw checklist and structured text draw-log template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recommendations for recording draw values, dates, source counters, mappings, and outcomes.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
