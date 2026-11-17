## Description:

Archon is a personal AI assistant for technical managers that manages local Markdown records for daily logs, decision support, team signals, coaching, meeting preparation, periodic reviews, and user-designated priority project reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Technical managers use Archon as a local-first chief-of-staff for work journals, decisions, coaching, stakeholder preparation, team signal tracking, and priority project cadence. It is intended for workspace-based use where records remain in local Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation triggers may cause the agent to load sensitive personal or workplace context during ordinary conversations.

Mitigation: Use Archon in a dedicated workspace and avoid installing it where unrelated sensitive records are available.

Risk: The skill can create or update personal management records, including daily logs and growth-area files.

Mitigation: Review proposed file writes and inspect local changes before accepting updates to profile, coaching, daily log, or project records.

Risk: The assistant depends on local records for personalized advice, so stale or incorrect records can lead to misleading guidance.

Mitigation: Periodically review the local profile, organization, decision, signal, and project files for accuracy.

## Reference(s):

- [Archon ClawHub listing](https://clawhub.ai/sopaco/skills/archon)
- [Prompts Reference](references/prompts.md)
- [File Schemas Reference](references/schemas.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown records with YAML frontmatter plus conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workspace records for logs, decisions, signals, coaching notes, workflow state, and project reviews.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
