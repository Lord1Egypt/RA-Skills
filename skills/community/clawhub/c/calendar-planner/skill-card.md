## Description:

Plan work and life across Google Calendar, Outlook, Apple Calendar, and CalDAV with CLI adapters, conflict repair, and weekly reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use Calendar Planner to reconcile commitments across approved calendars, repair overloaded weeks, choose defensible slots, and prepare dry-run calendar commands before any write.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar metadata may be sent to Google Calendar, Microsoft Graph, or a user-configured CalDAV server through the adapter the user selects.

Mitigation: Use one provider path at a time, prefer read-only scopes for audits and planning, and keep the queried calendar and time window as narrow as possible.

Risk: Calendar write permissions can create, update, delete, or invite from the wrong calendar if applied without review.

Mitigation: Present dry-run commands first and require explicit approval of the calendar, event details, and side effects before any write.

Risk: Optional local planning memory could retain sensitive event details if used too broadly.

Mitigation: Store only high-level user-stated planning rules, protected hours, and recurring constraints; avoid credentials, attendee rosters, and private event descriptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/calendar-planner)
- [Skill Homepage](https://clawic.com/skills/calendar-planner)
- [Setup](artifact/setup.md)
- [CLI Adapter Recipes](artifact/commands.md)
- [Life Grid Protocol](artifact/planning-protocol.md)
- [Life Domains](artifact/life-domains.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown prose with optional shell commands, PowerShell snippets, AppleScript blocks, JSON examples, and local Python script outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run action sequences, normalized calendar JSON, conflict reports, and weekly planning summaries; writes require explicit user approval.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
