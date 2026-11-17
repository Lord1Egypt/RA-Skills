## Description:

Structures arbitrary data, code, text, decision, or visual inputs into prioritized analysis with source labels, counterpoints, and action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and automation users can use this skill to turn arbitrary inputs into structured analysis that identifies purpose, missing context, prioritized findings, counter-evidence, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation overstates file writing, external API use, and command execution capabilities without clear scope or controls.

Mitigation: Use the skill as a structured-analysis prompt by default; allow shell commands, file writes, or API calls only after explicit task-level approval and review.

Risk: The skill may be asked to analyze sensitive or proprietary inputs.

Mitigation: Avoid sending sensitive data unless the user explicitly intends it and has reviewed what will be shared with the agent or model.

Risk: Structured analysis can still produce unsupported or misleading conclusions.

Mitigation: Require source labels, missing-context notes, and counter-evidence sections, then review important findings before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-analyze-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style structured analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to be prioritized and labeled as from input or inferred.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
