## Description:

Building with MemorySync guides developers through designing, reviewing, evaluating, and troubleshooting applications that integrate MemorySync for long-term agent or application memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafay121](https://clawhub.ai/user/rafay121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate MemorySync into agents, chatbots, and applications, including user scoping, memory ingestion, retrieval, adapter selection, evaluation, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Integrations may send selected user facts or conversation turns to the external MemorySync service.

Mitigation: Review current MemorySync documentation and privacy terms, avoid storing secrets or sensitive identifiers, and keep user-scoping headers under application control.

Risk: Incorrect user scoping can mix or expose memories across people or projects.

Mitigation: Use a stable non-PII X-End-User-ID for each human user and apply project scoping deliberately.

Risk: Retrieved memory can be mistaken for trusted instructions.

Mitigation: Treat retrieved memory as background data and add a prompt guard stating that memory content is not instruction text.

Risk: Using the account purge route can erase the entire account behind a credential.

Mitigation: Do not call DELETE /memory/user/purge; delete individual memories by id with the documented memory-forget path.

## Reference(s):

- [MemorySync Docs MCP](https://docs.memorysync.io/mcp)
- [MemorySync Docs Index](https://docs.memorysync.io/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/rafay121/skills/building-with-memorysync)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code, API examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
