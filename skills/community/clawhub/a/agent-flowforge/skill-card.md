## Description:

Run structured multi-step workflows via the FlowForge engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run and resume structured multi-step workflows, coordinate inline decisions with sub-agent delegation, and create YAML workflow definitions for repeatable agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a persistent workflow runner and may delegate workflow steps to sub-agents.

Mitigation: Review before installing and use it only when persistent FlowForge workflow execution and sub-agent delegation are intended.

Risk: Setup can require a global third-party CLI installation.

Mitigation: Prefer a pinned or local CLI install and avoid running npm with sudo.

Risk: Workflow result text or workflow actions may lead to consequential shell commands or external operations.

Mitigation: Do not paste untrusted result text into shell commands, and add explicit approval gates before workflows deploy, post, notify, create pull requests, or modify important data.

## Reference(s):

- [FlowForge Setup Guide](setup.md)
- [FlowForge YAML Format](references/yaml-format.md)
- [Code Contribution Workflow Example](references/examples/code-contribution.yaml)
- [Research Workflow Example](references/examples/research.yaml)
- [Code Review Workflow Example](references/examples/review.yaml)
- [ClawHub Skill Page](https://clawhub.ai/kagura-agent/skills/agent-flowforge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands, YAML examples, and JSON action descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FlowForge CLI state and workflow YAML files; no model output schema beyond the CLI action JSON is defined.]

## Skill Version(s):

1.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
