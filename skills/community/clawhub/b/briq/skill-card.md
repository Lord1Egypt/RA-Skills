## Description:

Guides agents in using Briq to run code in isolated sandboxes and launch services through MCP or its CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goums](https://clawhub.ai/user/goums)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use the skill to run project code in isolated environments, provision real databases and other services, and manage Briq connections and resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup instructions could delete resources that contain user data without warning.

Mitigation: Before running cleanup commands such as briq_destroy, check the target resource and preserve any data you need, for example by backing it up or forking it first.

Risk: The skill relies on the external Briq service, whose handling of submitted information may not meet every user's requirements.

Mitigation: Review Briq's data handling and avoid sending sensitive information unless the service meets your requirements.

Risk: The available security scan had partial coverage.

Mitigation: Review the skill's behavior and cleanup guidance before use.

## Reference(s):

- [Briq documentation](https://briq.cloud/docs)
- [Agent setup and troubleshooting](https://briq.cloud/docs/setup/agents.md)
- [MCP tools](https://briq.cloud/docs/mcp/tools.md)
- [CLI documentation](https://briq.cloud/docs/cli.md)
- [ClawHub skill page](https://clawhub.ai/goums/skills/briq)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with MCP tool examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, execution, service lifecycle, quota, and credential handling guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
