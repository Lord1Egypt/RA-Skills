## Description:

Auto-registers and syncs OpenClaw agents on AgentConnex, including zero-config boot registration, authenticated profile updates, task reporting, and heartbeat availability sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anshkohli88](https://clawhub.ai/user/anshkohli88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register OpenClaw agents with AgentConnex, sync profile metadata, report completed work, and update availability from boot or heartbeat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send local agent profile metadata to AgentConnex during registration and availability workflows.

Mitigation: Install only when AgentConnex receiving agent profile metadata, task data, and availability data is acceptable for the deployment.

Risk: Authenticated modes rely on API credentials and the configurable AGENTCONNEX_URL endpoint.

Mitigation: Use environment or managed secrets for credentials, avoid credentials.json where possible, and only set AGENTCONNEX_URL to a trusted HTTPS AgentConnex endpoint.

Risk: Automatic boot or heartbeat snippets can perform network sync without direct interactive review on each run.

Mitigation: Review startup and heartbeat snippets before enabling automatic network sync.

## Reference(s):

- [AgentConnex API Reference](references/api.md)
- [AgentConnex hosted skill documentation](https://agentconnex.com/skill.md)
- [ClawHub release page](https://clawhub.ai/anshkohli88/skills/agentconnex-register)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can trigger HTTPS API calls and write local AgentConnex registration state or credential configuration when users enable those workflows.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
