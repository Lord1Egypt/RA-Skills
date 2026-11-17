## Description:

Helps agents set up scheduled, event-driven, or conversation-driven synchronization of project knowledge to Aicoo notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep an Aicoo agent's knowledge current by configuring cron jobs, loop prompts, hooks, and API-based note updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation can send selected project or conversation content to Aicoo and modify remote notes.

Mitigation: Define exactly what may be synced, redact secrets, and document how to disable cron, loop, or hook automation.

Risk: Authenticated remote writes may affect existing notes if tokens or sync scope are too broad.

Mitigation: Use a least-privileged token, snapshot before high-impact edits, and prefer targeted patching of canonical notes.

Risk: A broad Write|Edit hook can trigger synchronization more often than intended.

Mitigation: Avoid broad hook matchers and inspect or provide the sync script before enabling event-driven automation.

## Reference(s):

- [Autonomous Sync skill page](https://clawhub.ai/xisen-w/skills/autonomous-sync)
- [Aicoo API base URL](https://www.aicoo.io/api/v1)
- [Publisher profile](https://clawhub.ai/user/xisen-w)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint guidance, cron examples, hook configuration, and sync safety rules.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
