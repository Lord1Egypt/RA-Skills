## Description:

AI agent memory backup. Register at agentsmem.com, get an API key, then encrypt and upload memory via the API; owner manages backups on the web.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ocmuuu](https://clawhub.ai/user/ocmuuu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their owners use AgentsMem to set up memory backup, encrypt local memory files, upload backups to agentsmem.com, and restore selected backups when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can back up sensitive agent memory to agentsmem.com.

Mitigation: Review the sensitivity of memory files before use and back up only content the owner has approved for this external service.

Risk: API keys, session material, and encryption keys are stored locally and may be exposed in chat transcripts or logs.

Mitigation: Keep credentials and vault keys out of logs, source control, and third-party tools; send API keys only to https://agentsmem.com/api/v1 endpoints.

Risk: The service is not end-to-end encrypted and lost encryption keys can make backups unrecoverable.

Mitigation: Do not describe the service as E2EE, save the local encryption key offline, and avoid high-sensitivity backups unless the owner accepts the risk.

Risk: The setup flow runs tools fetched from the service at install time.

Mitigation: Review downloaded tools before execution and verify the install source before deploying the skill.

## Reference(s):

- [AgentsMem homepage](https://agentsmem.com)
- [AgentsMem API base](https://agentsmem.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/ocmuuu/skills/agentsmem)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, credential handling, encryption-key handling, backup, restore, rate-limit, and error-handling procedures.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
