## Description:

Family Partner helps OpenClaw agents manage family calendars, tasks, local memories, household labor, anniversaries, milestones, voting, challenges, and morning briefings through a local SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-plusplus](https://clawhub.ai/user/ai-plusplus)

### License/Terms of Use:

MIT

## Use Case:

Families and OpenClaw users use this skill to organize household schedules, shared tasks, shopping items, preferences, allergies, family activities, anniversaries, milestones, votes, and challenges from conversational requests. It is intended for local-first family organization where the agent can read and update a SQLite database on the user's machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive household schedules, preferences, allergies, tasks, and family history in a local SQLite database.

Mitigation: Store only family details the user is comfortable retaining locally, restrict access to the Family Partner data directory, and protect any backups of the database.

Risk: Broad chat triggers and shell-run SQLite commands can update local family data when untrusted or ambiguous messages reach the agent.

Mitigation: Prefer explicit user confirmation for sensitive create, update, or delete actions, avoid untrusted free-form input, and run OpenClaw under a limited account scoped to the Family Partner data directory.

Risk: The skill depends on SQLite and a correctly initialized local schema.

Mitigation: Verify that sqlite3 is installed and initialize the database with the included schema before relying on calendar, task, memory, or reporting workflows.

## Reference(s):

- [Family Partner ClawHub listing](https://clawhub.ai/ai-plusplus/skills/family-partner)
- [AI-PlusPlus publisher profile](https://clawhub.ai/user/ai-plusplus)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [ClawHub skill format specification](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [SQLite documentation](https://www.sqlite.org/docs.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline SQLite shell commands and local configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confirmations, reminders, briefings, statistics, SQL-backed query results, and setup or troubleshooting commands.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter, artifact/package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
