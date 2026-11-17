## Description:

Context Vault Manage helps agents manage layered memory with semantic and hybrid retrieval, automatic summarization, vector database integration, multi-project isolation, smart cleanup, and memory relationship tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agent builders use this skill to add persistent, searchable memory management to RAG applications, multi-project agents, support knowledge bases, and long-running project workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain sensitive memory on disk or in vector indexes.

Mitigation: Use it only in workspaces where persistent memory storage is acceptable, and avoid secrets or regulated data unless additional retention, access, and deletion controls are in place.

Risk: Callback URL and command execution behavior is under-scoped in the security evidence.

Mitigation: Require explicit review before using callback URLs or command execution, restrict outbound destinations, and apply command allowlists where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/context-vault-manager-pro)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown guidance with TypeScript and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe persistent memory storage, vector indexing, callback configuration, and command execution safeguards.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
