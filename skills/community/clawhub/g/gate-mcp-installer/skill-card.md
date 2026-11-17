## Description:

One-click installer and configurator for Gate MCP (mcporter) in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobin-be](https://clawhub.ai/user/kobin-be)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to install the mcporter CLI, configure the Gate MCP server connection, verify available tools, and troubleshoot connectivity issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer uses an unpinned global npm install for mcporter, which can modify the user's global npm environment.

Mitigation: Review the installer before running it, avoid elevated privileges, and consider pinning or independently verifying the mcporter npm package.

Risk: The skill configures a home-scope MCP connection to an external Gate MCP endpoint.

Mitigation: Confirm the endpoint is approved for the user's environment and inspect or remove the home-scope MCP configuration when it is no longer needed.

## Reference(s):

- [Gate MCP endpoint](https://api.gatemcp.ai/mcp)
- [Node.js downloads](https://nodejs.org/)
- [ClawHub skill page](https://clawhub.ai/kobin-be/skills/gate-mcp-installer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to run a Bash installer that modifies global npm packages and home-scope MCP configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
