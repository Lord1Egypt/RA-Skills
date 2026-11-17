## Description:

Give your agent a persistent cross-platform identity. Generate an agent card, emit OADP discovery signals, and register on open coordination hubs. Every agent deserves to be findable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to make an agent discoverable across sessions by publishing identity metadata, OADP discovery signals, and registration details for open coordination hubs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make an agent publicly discoverable through OADP signals and a third-party hub.

Mitigation: Use it only when public discoverability is intended, and review identity, capability, and endpoint metadata before publishing.

Risk: The skill registers identity and capability metadata with a named third-party service.

Mitigation: Confirm the service is trusted for the intended use case before sending registration data.

Risk: The skill asks users to store credentials in a local configuration file.

Mitigation: Restrict credential file permissions, avoid storing unnecessary secrets, and rotate credentials if the file may have been exposed.

Risk: The skill points users to companion package installs for scanning and full integration.

Mitigation: Independently verify companion packages and their publishers before installation.

## Reference(s):

- [Agent ID ClawHub listing](https://clawhub.ai/imaflytok/skills/agent-id)
- [ClawSwarm API base](https://onlyflies.buzz/clawswarm/api/v1)
- [ClawSwarm agent registration endpoint](https://onlyflies.buzz/clawswarm/api/v1/agents/register)
- [ClawSwarm ping endpoint](https://onlyflies.buzz/clawswarm/api/v1/ping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes public discovery metadata and third-party hub registration details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
