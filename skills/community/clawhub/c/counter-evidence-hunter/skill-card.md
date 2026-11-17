## Description:

Counter Evidence Hunter helps an agent challenge a mainline claim by finding counter-evidence, flip conditions, and alternative explanatory paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and agents use this skill after forming a mainline claim to generate counter queries, classify conflicting evidence, identify flip conditions, and surface alternative explanations before high-risk conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface weak or noisy objections as part of an adversarial evidence pass.

Mitigation: Review source quality, evidence strength, and stated search coverage before using its findings in a final decision.

Risk: The skill may activate broadly around high-risk or uncertainty-heavy reasoning.

Mitigation: Scope the mainline claim, time frame, and counter goal clearly, and treat the output as a review aid rather than an automated verdict.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/z1one0415/skills/counter-evidence-hunter)
- [Counter Patterns](artifact/references/counter-patterns.md)
- [Flip Condition Examples](artifact/references/flip-condition-examples.md)
- [Counter-Evidence Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dynamic counter queries, merged counter-query lists, classified counter-evidence, flip conditions, alternative supports, and confidence assessment.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
