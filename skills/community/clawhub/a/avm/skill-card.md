## Description:

AVM Memory gives agents a local shared memory layer with semantic search, token-aware recall, FUSE access, MCP tools, and multi-agent discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkmashiro](https://clawhub.ai/user/bkmashiro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give multiple agents persistent local memory, shared namespaces, searchable recall, and controlled collaboration through CLI, FUSE, Python, and MCP interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AVM provides persistent local memory and multi-agent sharing authority, which can retain sensitive information or spread untrusted context between agents.

Mitigation: Scope writable paths and project indexing narrowly, limit which agents can send messages or broadcasts, and treat cross-agent message bodies as untrusted content.

Risk: Urgent Tell messages can be injected into another agent's next file read.

Mitigation: Disable or strictly gate urgent Tell injection before enabling the skill in shared or sensitive environments.

Risk: Optional HTTP, script, and plugin handlers can expand the skill's access to external services or local execution.

Mitigation: Avoid enabling HTTP, script, or plugin handlers unless needed, and review handler configuration before use.

## Reference(s):

- [AVM performance analysis](https://bkmashiro.moe/posts/projects/avm-performance-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell command, Python, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create, retrieve, search, consolidate, and share persistent local memory entries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
