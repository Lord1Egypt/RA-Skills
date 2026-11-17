## Description:

Cloud memory for AI agents. Store, search, and recall context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aerialcombat](https://clawhub.ai/user/aerialcombat)

### License/Terms of Use:


## Use Case:

Developers and agent operators use MyMemory.bot to register an agent with ctxly.app, store selected context, search or bootstrap memory across sessions, and delete stored memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected agent and user context is sent to ctxly.app for persistent third-party storage.

Mitigation: Use the skill only when that storage is acceptable, and save only context the user has approved for persistence.

Risk: Secrets, sensitive personal data, medical data, financial data, authentication data, or confidential business data could be stored if the agent saves broad context indiscriminately.

Mitigation: Do not store sensitive categories or secrets; keep API keys in configuration or environment storage rather than memory records.

Risk: Retrieved memories may be stale, incomplete, or unsuitable as instructions.

Mitigation: Treat recalled memories as reference data and confirm important actions with the user before acting on them.

Risk: Deleting memories changes persistent user context.

Mitigation: Require explicit user approval before deleting existing memories.

## Reference(s):

- [Ctxly homepage](https://ctxly.app)
- [ClawHub skill page](https://clawhub.ai/aerialcombat/skills/cloud-memory)
- [Publisher profile](https://clawhub.ai/user/aerialcombat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API key setup, memory storage and retrieval commands, deletion guidance, and rate-limit notes.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
