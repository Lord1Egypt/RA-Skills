## Description:

A model-agnostic game theory and negotiation skill that computes Nash bargaining, Rubinstein alternating-offer, Shapley value, and zero-sum minimax solutions for multi-party negotiation and allocation scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn negotiation, allocation, cooperative game, or adversarial payoff inputs into computable strategy or allocation guidance. It is suited for structured bargaining analysis where transparent formulas and self-tests are preferred over informal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Negotiation inputs may include private business strategy, pricing, or personal preferences.

Mitigation: Review inputs before use and avoid recording sensitive free-form details in local learning notes.

Risk: The learner component can persist user preferences, notes, usage history, and errors locally without clear consent or deletion controls.

Mitigation: Use the learner only when local persistence is acceptable, and inspect or delete learned_patterns.json according to the deployment's data-handling policy.

Risk: Approximate minimax and high-complexity Shapley calculations can produce incomplete or misleading results for unsupported problem sizes.

Mitigation: Check documented limits, run the provided self-test, and independently review results before using them for consequential negotiations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/game-negotiation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON command examples and computed strategy values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected mode and supplied payoff, bargaining, discount, or cooperative-game inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
