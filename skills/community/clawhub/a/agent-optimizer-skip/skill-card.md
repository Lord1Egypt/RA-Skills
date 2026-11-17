## Description:

A lightweight agent performance optimization skill for recording trajectories, collecting reward feedback, analyzing performance trends, and generating prompt or ROI improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang-shao](https://clawhub.ai/user/huang-shao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor agent trajectories, reward signals, A/B prompt versions, success rates, and ROI-oriented metrics. It helps produce trend summaries and optimization reports for agents whose workspace data they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unchecked agent IDs are used in workspace paths and could expose or overwrite another agent's optimizer data in shared workspaces.

Mitigation: Only run the scripts for agent IDs you control, and add agent-id validation plus path containment checks before shared or automated use.

Risk: Trajectory records may contain sensitive prompts, outputs, tool use, or metrics.

Mitigation: Avoid storing secrets in trajectory data and review or redact optimizer records before sharing reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huang-shao/skills/agent-optimizer-skip)
- [OpenClaw repository homepage from artifact metadata](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Python and shell examples; bundled scripts print text summaries and can write JSON optimization reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses agent-specific optimizer data under /workspace/subagents/{agent_id}/optimizer when the provided scripts are run.]

## Skill Version(s):

1.0.0 (source: server release, artifact README.md, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
