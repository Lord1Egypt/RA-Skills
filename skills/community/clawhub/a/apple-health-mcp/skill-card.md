## Description:

Read a local Apple Health export and expose activity, sleep, heart, HRV, workouts, and long-term trends to agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, configure, audit, and troubleshoot Apple Health MCP for MCP-compatible clients while keeping Apple Health exports local and consent explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an automatically downloaded, unpinned npm package against sensitive Apple Health data.

Mitigation: Review the npm package first, prefer a pinned and verified version, run it with the least access practical, and provide only the intended local Apple Health export.

Risk: Sensitive health data could be exposed through tool output or logs.

Mitigation: Avoid using the skill where private health data could be exposed to tools or logs outside the user's control, and do not print secrets or private user data.

## Reference(s):

- [Apple Health MCP ClawHub page](https://clawhub.ai/davidmosiah/skills/apple-health-mcp)
- [Apple Health MCP repository](https://github.com/davidmosiah/apple-health-mcp)
- [Apple Health connector documentation](https://wellness.delx.ai/connectors/apple-health)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup, privacy, safety-boundary, and troubleshooting guidance for local Apple Health exports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
