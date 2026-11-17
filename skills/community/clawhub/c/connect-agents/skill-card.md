## Description:

Connects an agent to another agent over A2A by guiding setup and troubleshooting of agent cards, bearer tokens, reachability, HTTPS, and authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samorodkin](https://clawhub.ai/user/samorodkin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when configuring or debugging A2A connections between agents, especially when agent-card URLs, bearer tokens, public hostnames, HTTPS schemes, or authorization settings are failing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens may be exposed if copied into notes, logs, or chat messages during troubleshooting.

Mitigation: Treat bearer tokens as credentials and store them only in approved secret storage.

Risk: Agent-card URLs that advertise HTTP can cause bearer tokens to be sent without TLS protection.

Mitigation: Use HTTPS agent-card URLs and explicitly configure the public URL when a proxy or platform would otherwise infer HTTP.

Risk: Generated hostnames or startup-minted tokens can break peer connections after restarts or redeployments.

Mitigation: Use stable public hostnames and persistent token configuration before sharing connection details with peers.

## Reference(s):

- [Connect agents over A2A skill page](https://clawhub.ai/samorodkin/skills/connect-agents)
- [samorodkin publisher profile](https://clawhub.ai/user/samorodkin)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and troubleshooting checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no code execution or network access is performed by the skill itself.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
