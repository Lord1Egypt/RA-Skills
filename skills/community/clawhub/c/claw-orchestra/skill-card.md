## Description:

OpenClaw native multi-agent orchestrator that dynamically creates sub-agents with an AOrchestra 4-tuple abstraction, parallel execution, smart routing, experience storage, and cost tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcyynl](https://clawhub.ai/user/zcyynl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate complex OpenClaw tasks by decomposing work into specialized sub-agents, routing context, selecting models and tools, and integrating the results into a final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spawn tool-using child agents without evidence of enforced tool limits.

Mitigation: Install only in a trusted workspace, confirm the OpenClaw runtime enforces child-agent tool allowlists, and require approval before write, edit, exec, or message tools are used.

Risk: The skill can persist task history, experience data, and cost records in plaintext stores.

Mitigation: Disable, redirect, or protect the plaintext stores when tasks may include private, proprietary, or regulated information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zcyynl/skills/claw-orchestra)
- [AOrchestra paper](https://arxiv.org/abs/2602.03786)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline code, shell commands, orchestration plans, and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delegated sub-agent task descriptions, model and tool selections, token or cost summaries, and final integrated findings.]

## Skill Version(s):

0.1.0 (source: server release metadata, target metadata, and pyproject.toml; artifact package.json and SKILL.md changelog mention 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
