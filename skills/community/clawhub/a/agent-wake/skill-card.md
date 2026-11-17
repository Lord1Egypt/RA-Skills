## Description:

Wake an OpenClaw agent session from an external script or process so the agent receives a notification and responds in the correct Discord channel when asynchronous work completes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisco65](https://clawhub.ai/user/krisco65)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to wake an OpenClaw agent when background work, scheduled jobs, command-line tasks, webhooks, or alerts finish and require agent follow-up in a target Discord channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a high-trust external control path that can wake an agent and inject event text into the agent session.

Mitigation: Allow only trusted local processes to call the script, avoid connecting it directly to untrusted webhooks or user-controlled text, and review the agent tools available during automatic wake events.

Risk: The script handles a gateway token and can read it from environment variables, a local .env file, or the OpenClaw gateway command file.

Mitigation: Protect the gateway token and local .env file, restrict file access on systems that run the script, and rotate the token if it may have been exposed.

Risk: A misconfigured GATEWAY_URL could send wake requests and authorization headers to an unintended endpoint.

Mitigation: Keep GATEWAY_URL pinned to a trusted local gateway and review endpoint configuration before use in automation.

## Reference(s):

- [Setup Guide](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/krisco65/skills/agent-wake)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a gateway token and a trusted local OpenClaw gateway endpoint.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
