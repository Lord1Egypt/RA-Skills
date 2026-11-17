## Description:

Connect to the Anycast agent network. List agents, query cross-environment connectors, send messages to remote agents, and check fleet status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markspeed](https://clawhub.ai/user/markspeed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Anycast agent fleets, query configured connectors, send remote-agent messages, and manage scoped tenant memory through the Anycast portal API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Anycast token can be used to query external systems through configured connectors.

Mitigation: Use a least-privilege, revocable ANYCAST_API_TOKEN and require explicit user approval before connector queries.

Risk: Remote-agent messages may trigger actions or disclose information outside the local session.

Mitigation: Require explicit user approval before sending messages to remote agents and confirm the target agent identity.

Risk: Tenant-scoped memory can persist sensitive data or untrusted instructions.

Mitigation: Avoid storing secrets or untrusted instructions in shared memory and review tenant-memory writes before execution.

Risk: A malicious or incorrect portal URL could redirect API calls and tokens.

Mitigation: Pin ANYCAST_PORTAL_URL to a trusted HTTPS origin before use.

## Reference(s):

- [Anycast Agent Network](https://agents.anycast.com)
- [ClawHub Skill Page](https://clawhub.ai/markspeed/skills/anycast-network)
- [Publisher Profile](https://clawhub.ai/user/markspeed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector query results are expected as markdown tables; agent lists should include name, status, and last seen time.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
