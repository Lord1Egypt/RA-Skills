## Description:

Context Guard is a context-management protocol for OpenClaw agents that monitors context budget, partitions working memory, checkpoints state before compaction, and restores context after compaction or session restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unicornnoway](https://clawhub.ai/user/unicornnoway)

### License/Terms of Use:


## Use Case:

OpenClaw users and agent developers use Context Guard to help agents and sub-agents manage limited context, persist task state, and recover working context after compaction or a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to read conversation and memory data and persist sensitive task details in local checkpoint and memory files.

Mitigation: Use it in a dedicated workspace, review generated files before committing or sharing them, and avoid storing secrets, wallet details, personal profile data, or unrelated conversation history.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local checkpoint, memory, status, and heartbeat files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
