## Description:

AgentKeys helps AI agents make API calls through a secure credential proxy so real secrets never leave the vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexandr-belogubov](https://clawhub.ai/user/alexandr-belogubov)

### License/Terms of Use:


## Use Case:

Developers and agent operators use AgentKeys to configure agents to call external APIs through the AgentKeys proxy with either a workspace API key and credential name or a single-credential proxy token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A workspace API key can allow an agent to proxy requests using multiple named credentials permitted in the workspace.

Mitigation: Prefer a single-credential proxy token when the agent only needs one credential, and review the workspace key's allowed credentials and target APIs before use.

Risk: The skill guides agents to forward requests to external target APIs through the AgentKeys proxy.

Mitigation: Limit use to agents that are intended to make those API calls and monitor the AgentKeys audit trail for proxied requests.

## Reference(s):

- [AgentKeys ClawHub listing](https://clawhub.ai/alexandr-belogubov/skills/agentkeys)
- [AgentKeys documentation](https://agentkeys.io/docs)
- [AgentKeys dashboard](https://app.agentkeys.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and environment variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTKEYS_PROXY_URL and either AGENTKEYS_API_KEY or AGENTKEYS_PROXY_TOKEN.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
