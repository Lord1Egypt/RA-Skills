## Description:

Use when initializing or migrating an AI agent harness in a repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or migrate repository agent instructions, configuration, hooks, and memory into a Claude Code-centered harness, with optional support for other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent memory can retain summaries of confidential prompts and be committed to the repository.

Mitigation: Review the memory policy before installation; disable prompt summaries for confidential work and exclude sensitive memory from commits.

Risk: Harness migration can remove existing agent configuration and install broad, persistent instructions, hooks, and permissions.

Mitigation: Review the discovery plan and deletion list, then inspect generated settings, hooks, and sub-agents before approval.

Risk: The workflow may proceed to repository changes and pull-request creation with limited final confirmation.

Mitigation: Require explicit confirmation before deleting tracked files, pushing changes, or opening a pull request.

## Reference(s):

- [ClawHub release](https://clawhub.ai/afonsoft/skills/create-agent-harness)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Author-listed project link (not verified release provenance)](https://github.com/afonsoft/skills)
- [Memory protocol](artifact/references/memory-protocol.md)
- [Migration map](artifact/references/migration-map.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Code, Shell commands]

**Output Format:** [Repository files and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates or migrates agent-harness files after a discovery review.]

## Skill Version(s):

1.0.11 (source: ClawHub release; skill metadata lists 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
