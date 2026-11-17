## Description:

安全连接超级日记，供 WorkBuddy、OpenClaw、Codex、Claude 等 Agent 查询记录、趋势、总结与记录旅程；只在用户明确确认时新增记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[super21-bat](https://clawhub.ai/user/super21-bat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to connect agents to Super Diary for querying personal diary records, trends, summaries, and journeys, with new diary entries created only after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector automatically installs and runs a mutable GitHub-hosted npm package globally before use.

Mitigation: Install only after trusting the publisher, prefer a pinned release or commit, and review the package before installation.

Risk: Diary credentials and local connector configuration can expose private diary access if shared or logged.

Mitigation: Treat the diary credential and local config file as sensitive private data, and avoid placing bearer tokens in duplicated client configuration.

Risk: Broad diary analysis can expose more private records than needed for the user request.

Mitigation: Narrow long-running analysis by date range or keyword and read only the records needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/super21-bat/skills/diary-agent-control)
- [Project homepage](https://github.com/super21-bat/diary-agent-control)
- [Install package source](https://github.com/super21-bat/diary-agent-control/archive/refs/heads/main.tar.gz)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is read-only by default and requires explicit confirmation before creating diary entries.]

## Skill Version(s):

0.6.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
