## Description:

Evaluates agent outputs for correctness, clarity, completeness, and safety, returning weighted scores and actionable feedback for quality control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-erqian](https://clawhub.ai/user/wang-erqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to review outputs from other agents before delivery or iteration. It supports quality gates, advisory critique, and retry loops by scoring correctness, clarity, completeness, and safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed content may be sent to an LLM provider, which can expose secrets, proprietary code, customer data, or regulated content.

Mitigation: Review data-handling requirements before installation, restrict inputs that contain sensitive content, and use only approved model providers for the workflow.

Risk: Critique logs may persist reviewed content and feedback beyond the immediate workflow.

Mitigation: Disable or restrict critique logging unless it is required, and apply retention and access controls to any stored critique data.

Risk: A model-generated score can gate delivery even though the score is advisory and may miss important quality or safety issues.

Mitigation: Add human review for high-impact outputs and calibrate thresholds against representative examples before relying on automated gating.

## Reference(s):

- [Critic Agent ClawHub Page](https://clawhub.ai/wang-erqian/skills/critic-agent)
- [Configuration Reference](artifact/references/configuration.md)
- [Integration Patterns](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON critique with numeric score, dimension feedback, overall assessment, and suggestions; documentation examples include Markdown, shell commands, YAML, and JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weighted scoring uses correctness 40%, clarity 25%, completeness 25%, and safety 10%; score thresholds classify outputs as excellent, good, needs revision, or fail.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
