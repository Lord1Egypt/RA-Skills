## Description:

Claw Multi Agent enables parallel multi-agent orchestration for OpenClaw research, model comparison, writing, and code pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcyynl](https://clawhub.ai/user/zcyynl)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to coordinate multiple OpenClaw agents for parallel research, multi-model comparison, code review, writing workflows, and staged task pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may spawn multiple OpenClaw agents with broad tool access.

Mitigation: Review the proposed agent plan before execution and limit use to tasks where parallel agents are expected and appropriate.

Risk: Child agent processes may inherit environment variables, including unnecessary secrets.

Mitigation: Run with a minimal environment and remove credentials that are not required for the task.

Risk: Workflows may persist reports to disk or send results through chat or Feishu integrations.

Mitigation: Require explicit confirmation before file writes or external delivery, especially for sensitive content.

Risk: Multi-provider model comparisons may disclose prompt content to additional model providers.

Mitigation: Confirm the intended providers before comparison and avoid including confidential information unless approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zcyynl/skills/claw-multi-agent)
- [README](README.md)
- [Skill Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, summaries, comparisons, code snippets, shell command examples, and JSON pipeline configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May aggregate multiple sub-agent outputs and may save reports to disk depending on the selected workflow.]

## Skill Version(s):

1.0.5 (source: server release metadata; package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
