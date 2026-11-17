## Description:

Provides guidance for using a work assistant's Obsidian and Git sync, SQLite-backed memory database, natural language memory queries, and local monitoring status tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awublack](https://clawhub.ai/user/awublack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to ask what core assistant capabilities are available and to receive commands or guidance for Obsidian notes, Git sync, memory lookups, and monitoring checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad file, Git, sync, cron, and service operations in local workspaces.

Mitigation: Require explicit user confirmation before file edits, deletes, commits, pushes, manual sync, or service restarts.

Risk: The skill references external helper scripts that are not included in the reviewed package.

Mitigation: Review and verify memory_query_agent.py and monitor_server.py separately before relying on commands that execute them.

Risk: The skill may be used around sensitive notes, credentials, or private repositories.

Mitigation: Install only in workspaces where Obsidian, Git, memory sync, cron jobs, and localhost monitoring are intended and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awublack/skills/core-capabilities)
- [Publisher profile](https://clawhub.ai/user/awublack)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Release summary](artifact/SUMMARY.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and status descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local workspace files, cron jobs, localhost monitoring endpoints, and external helper scripts that must exist in the user's environment.]

## Skill Version(s):

1.0.0 (source: frontmatter, metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
