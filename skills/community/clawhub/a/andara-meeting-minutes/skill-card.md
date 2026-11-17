## Description:

Capture meeting summaries and action items from voice or text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atiati82](https://clawhub.ai/user/atiati82)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn voice or text meeting notes into structured meeting records, decisions, and action items. The skill stores the extracted records in PostgreSQL and replies with a German summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes potentially sensitive meeting content to PostgreSQL.

Mitigation: Use only with clear storage, retention, and review controls; avoid confidential meetings until those controls are established.

Risk: The skill uses unsafe SQL templates and provides limited user control before saving content.

Mitigation: Use a dedicated least-privilege PostgreSQL account, parameterized or safely escaped inserts, and an explicit confirmation step before saving meeting content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atiati82/skills/andara-meeting-minutes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [German structured Markdown summary with PostgreSQL psql command steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes meeting and action item records to PostgreSQL when DATABASE_URL is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
