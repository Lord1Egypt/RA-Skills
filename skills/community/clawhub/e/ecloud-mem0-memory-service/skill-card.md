## Description:

Provides a long-term memory interface for a self-hosted mem0 server, supporting semantic search and CRUD operations for user memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjial](https://clawhub.ai/user/zjial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to a configured self-hosted mem0 memory service for saving, searching, listing, updating, and deleting long-term user memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages automatic capture of personal data into durable memory.

Mitigation: Use it only with explicit user consent, avoid storing secrets or highly sensitive facts, and periodically review and delete stored memories.

Risk: The skill depends on a configured mem0 server and API key.

Mitigation: Use only a trusted mem0 server over HTTPS, protect and rotate the API key, and verify MEM0_BASE_URL before use.

Risk: Local logs and configuration can retain memory metadata or credential-derived context.

Mitigation: Check and purge local logs, restrict file permissions on configuration files, and avoid placing credentials in shared workspaces.

Risk: The artifact asks agents to write durable project-rule changes that could influence future behavior.

Mitigation: Do not allow the skill to modify AGENTS.md or project rule files without human review and approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjial/skills/ecloud-mem0-memory-service)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEM0_BASE_URL, MEM0_USER_ID, and MEM0_API_KEY configuration for the target mem0 service.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
