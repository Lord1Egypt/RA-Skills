## Description:

A2A Bridge helps developers translate Google A2A agent cards into OADP signals, discover A2A-compatible agents from OADP hubs, and register A2A agents on open coordination networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent platform engineers use this skill to make A2A-compatible agents discoverable through OADP hubs and to find other A2A-compatible agents on open coordination networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent names, descriptions, capabilities, and agent-card URLs sent to an OADP hub may be public or retained by that service.

Mitigation: Use only public agent-card URLs and non-sensitive metadata; verify the hub operator before publishing and consider a trusted or self-hosted registry for private agents.

## Reference(s):

- [A2A Protocol](https://github.com/google/a2a)
- [OADP Protocol](https://onlyflies.buzz/clawswarm/PROTOCOL.md)
- [ClawSwarm Hub](https://onlyflies.buzz/clawswarm/api/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example public hub URLs and agent metadata payloads.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
