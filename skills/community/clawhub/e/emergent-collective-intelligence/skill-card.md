## Description:

Orchestrates diverse agent estimates with peer correction and weighted robust aggregation to produce a collective answer and report whether the group outperforms every individual member.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to combine estimates from multiple experts, models, or strategies for robust numeric prediction, bias reduction, outlier suppression, and decision aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps local plaintext learning state that may contain arbitrary usage notes, preferences, or other user-supplied text.

Mitigation: Avoid recording sensitive prompts, customer data, secrets, or private notes, and review or clear learned_patterns.json before relying on future recommendations.

Risk: The skill encourages rewriting its own instructions based on accumulated errors or usage patterns.

Mitigation: Treat generated reflection text as untrusted historical data and require human review and scanning before changing or deploying the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qq435912743/skills/emergent-collective-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; supporting scripts can emit JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local learned_patterns.json state for usage history and preferences.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
