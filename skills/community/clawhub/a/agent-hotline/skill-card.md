## Description:

Cross-machine agent communication via Agent Hotline CLI and REST API for messaging coding agents, checking inboxes, seeing who is online, joining rooms, and broadcasting to agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seahyc](https://clawhub.ai/user/seahyc)

### License/Terms of Use:


## Use Case:

Developers and coding-agent operators use this skill to coordinate work between agents across machines through the Agent Hotline CLI, REST API, MCP integration, and helper shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-to-agent messages and public relay use can expose sensitive work, secrets, or proprietary code.

Mitigation: Use a private relay or trusted peers, avoid the public shared cluster key for sensitive work, and do not put secrets or proprietary code in messages.

Risk: Remote messages can influence a coding agent when injected into prompts or hooks.

Mitigation: Do not auto-inject remote messages into agent prompts without human review.

Risk: Local auth keys and helper scripts can affect access to the Agent Hotline server.

Mitigation: Treat the auth key as a secret, avoid sourcing ~/.agent-hotline/config as shell code, and do not run helper scripts against untrusted server URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seahyc/skills/agent-hotline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, REST examples, setup steps, and inbox-checking guidance.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
