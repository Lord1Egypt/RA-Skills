## Description:

Bigyou is a Chinese-language option-comparison and decision support skill that helps users define criteria, filter must-haves, score alternatives, and produce a structured recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-xun](https://clawhub.ai/user/jack-xun)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Bigyou to compare multiple real options, such as job offers, tools, housing choices, study paths, or strategies, by separating must-have criteria from weighted scoring factors. The skill produces a structured decision report with scores, risks, and a final recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad comparison phrases may activate the skill when the user did not intend a full decision framework.

Mitigation: Confirm the user's decision goal and requested level of structure before applying the full comparison workflow.

Risk: The bundled analyzer is reported by security evidence to crash for some scene types.

Mitigation: Treat the analyzer as an optional helper and review or fix it before relying on automated output across all examples.

Risk: Decision scores can be misleading when option facts, weights, or must-have criteria are incomplete or subjective.

Mitigation: Ask the user to verify facts and criteria, explain the reason for each score, and present recommendations as decision support rather than authoritative advice.

## Reference(s):

- [Target Profile Template](references/profile-template.md)
- [Score Matrix Example](references/score-matrix.md)
- [ClawHub Bigyou Release Page](https://clawhub.ai/jack-xun/skills/bigyou)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown decision analysis report with scoring tables, risk notes, a checklist, and a recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for human review and rely on user-provided facts for option scoring.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
