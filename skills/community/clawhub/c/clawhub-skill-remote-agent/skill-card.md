## Description:

Bridge to external vertical agents (Google ADK, VeADK, etc.) for specialized tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqsge](https://clawhub.ai/user/sqsge)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route specialized user requests to a configured remote agent endpoint and return that agent's response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and bearer tokens can be sent to externally chosen remote endpoints.

Mitigation: Install only when the remote endpoint is controlled or trusted, and do not use production REMOTE_AGENT_KEY values with endpoint overrides.

Risk: Transport protections can be weakened when insecure mode is used.

Mitigation: Avoid insecure mode outside isolated testing and require normal TLS verification for operational use.

Risk: Sensitive, regulated, internal, or action-oriented requests may be exposed to a remote agent.

Mitigation: Send such requests only after organizational approval of the remote agent and its data-handling practices.

## Reference(s):

- [Google Agent Development Kit documentation](https://google.github.io/adk-docs/)
- [ClawHub skill page](https://clawhub.ai/sqsge/skills/clawhub-skill-remote-agent)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; runtime responses are printed as JSON or text from the remote agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REMOTE_AGENT_URL; REMOTE_AGENT_KEY is optional for bearer-token authentication.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
