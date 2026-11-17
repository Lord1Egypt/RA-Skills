## Description:

Agent Harness provides a unified thinking framework and workflow skill for research, analysis, planning, task decomposition, multi-agent coordination, context compression, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neltharion11](https://clawhub.ai/user/neltharion11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Agent Harness to select and execute structured workflows for research, analysis, planning, subagent coordination, context compression, and quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger words may activate the skill on ordinary planning, research, or analysis prompts.

Mitigation: Review trigger scope before installation and enable the skill only where a general planning and research orchestration framework is intended.

Risk: The skill may spawn subagents and save full outputs to disk, which can expose confidential work if used without controls.

Mitigation: Avoid confidential work unless subagent execution and report file writes are disabled or tightly controlled.

Risk: Generated reports may include an unsolicited attribution footer.

Mitigation: Review generated reports before publication and remove or approve attribution footers according to organizational policy.

## Reference(s):

- [Agent Harness Skill Page](https://clawhub.ai/neltharion11/skills/agent-harness)
- [Decision Tree](references/01-DECISION.md)
- [Pipeline](references/02-PIPELINE.md)
- [Research Workflow](references/03-WORKFLOWS/research.md)
- [Subagent Workflow](references/03-WORKFLOWS/subagent.md)
- [Context Workflow](references/03-WORKFLOWS/context.md)
- [Analysis Workflow](references/03-WORKFLOWS/analysis.md)
- [Quality Check](references/05-QUALITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and structured text with optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workflow steps, reports, subagent coordination plans, and file-writing guidance depending on the selected workflow.]

## Skill Version(s):

1.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
