## Description:

Analyzes OpenClaw agent skill configurations, estimates token and efficiency metrics, recommends skill changes, tracks trends, and can generate or send optimization reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect local OpenClaw agent configurations, identify redundant or costly skills, discover candidate skill changes, and produce JSON or Markdown optimization reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect local OpenClaw agent skill configuration.

Mitigation: Use it only in workspaces where the agent configuration may be reviewed, and keep generated reports local unless sharing is intentional.

Risk: Optimization recommendations may remove useful skills or add inappropriate ones.

Mitigation: Review each generated recommendation before applying any configuration change.

Risk: Webhook or scheduled notification features can send derived recommendations outside the local environment.

Mitigation: Enable notifications only with an approved webhook destination and known report contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/agent-efficiency-manager)
- [metrics_definitions.md](references/metrics_definitions.md)
- [optimization_patterns.md](references/optimization_patterns.md)
- [recommendation_logic.md](references/recommendation_logic.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON and Markdown reports with inline shell commands and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local agent configuration and optionally send report content to a user-supplied webhook.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
