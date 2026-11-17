## Description:

Connect an MCP-compatible agent to local Fitbit activity, sleep, heart-rate, HRV, SpO2, breathing, weight, food, and water data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install, configure, troubleshoot, and safely operate Fitbit MCP with MCP-compatible clients while preserving explicit consent and local privacy boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow runs a mutable unpinned npm package with local user permissions.

Mitigation: Prefer a pinned, reviewed package version or a locally installed binary before setup, authentication, or MCP startup.

Risk: The MCP server can access Fitbit OAuth tokens and sensitive health data.

Mitigation: Keep user consent explicit, avoid exposing token files or private health data in agent output, and use status, manifest, doctor, privacy audit, or dry-run surfaces before writes or live provider calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidmosiah/skills/fitbit-mcp)
- [Fitbit MCP repository](https://github.com/davidmosiah/fitbitmcp)
- [Fitbit connector docs](https://wellness.delx.ai/connectors/fitbit)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup, authentication, MCP client configuration, troubleshooting, privacy-boundary, and safety guidance.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
