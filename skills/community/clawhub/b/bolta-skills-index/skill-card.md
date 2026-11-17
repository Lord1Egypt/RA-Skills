## Description:

Bolta Skills Registry - canonical index and orchestration layer for all Bolta skills, organized by plane

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxfritzhand](https://clawhub.ai/user/maxfritzhand)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this registry to discover Bolta social media automation skills, select install sets, and route workflows according to workspace policy, quotas, autonomy mode, and agent permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registry can recommend mutable remote skill content and high-impact automation workflows.

Mitigation: Install from a pinned, reviewed release or commit, verify checksums where possible, and review downloaded skills before enabling sensitive workflows.

Risk: Bolta API credentials can grant access to workspace operations and social media automation.

Mitigation: Use least-privilege keys, store them in environment variables or a secret manager, rotate them regularly, and start in a test workspace.

Risk: Admin, cron, autopilot, key-rotation, workspace-configuration, and agent-memory workflows can materially change workspace behavior.

Mitigation: Enable those workflows only after a separate review and confirm that Safe Mode, autonomy mode, quotas, and role permissions match the intended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxfritzhand/skills/bolta-skills-index)
- [Bolta API documentation](https://bolta.ai/docs/api)
- [Bolta MCP endpoint](https://mcp.bolta.ai/mcp)
- [Bolta Skills Pack](https://github.com/boltaai/bolta-skills)
- [BoltaClaw self-hosted runtime](https://github.com/boltaai/boltaclaw-self-hosted)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with structured examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registry output includes skill recommendations, compatibility notes, setup guidance, and routing advice rather than direct content operations.]

## Skill Version(s):

2.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
