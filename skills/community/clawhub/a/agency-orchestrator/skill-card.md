## Description:

Agency Orchestrator analyzes tasks, selects suitable agents, and coordinates multi-agent collaboration for complex work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonghaiquan](https://clawhub.ai/user/gonghaiquan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawX users use this skill to route complex tasks to relevant design, engineering, marketing, product, testing, and support agents and inspect the selected agents through Python or command-line entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration script makes persistent OpenClaw configuration and shell profile changes.

Mitigation: Review integrate_with_clawx.sh before running it, and remove or skip PATH and alias additions that are not needed.

Risk: Task text can be written to local orchestration and collaboration logs.

Mitigation: Avoid sending secrets or sensitive data in tasks, and review or delete logs under ~/.openclaw/agency-agents-zh/logs when appropriate.

Risk: collaborative_mode.py imports external local code that is not included in the artifact.

Mitigation: Treat collaborative_mode.py as unsafe unless the external collaborative_agents module and local paths are trusted and audited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gonghaiquan/skills/agency-orchestrator)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON/text command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local orchestration and integration logs when used.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
