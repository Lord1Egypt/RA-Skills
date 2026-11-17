## Description:

Computes factual and counterfactual outcomes for explicit weighted linear decision models with thresholds, including flip detection and marginal variable contributions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to run local what-if comparisons against explicit scoring models, identify whether an intervention changes the decision, and attribute the score movement to individual variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep a local memory file containing usage, error notes, and preferences, which may capture sensitive decision context.

Mitigation: Use it only with non-confidential decision data unless persistence is removed or made opt-in, and review learned_patterns.json as untrusted data before reuse.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON counterfactual results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zero dependency local execution; may update a local learned_patterns.json memory file when the learning helper is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
