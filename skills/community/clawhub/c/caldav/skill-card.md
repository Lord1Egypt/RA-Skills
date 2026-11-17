## Description:

Sync, inspect, and modify CalDAV calendars with vdirsyncer and khal using deterministic windows, verified writes, and recurrence-aware workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and calendar power users use this skill to operate existing CalDAV calendars through local vdirsyncer and khal tooling. It supports local-first querying, event creation, safer edits, sync troubleshooting, and conflict-aware handling of ambiguous or recurring events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to modify real calendar events, including recurring events and deletes.

Mitigation: Review proposed writes carefully, prefer bounded windows and explicit calendar scope, and require read-back verification after create, update, or delete operations.

Risk: Ambiguous event matches or stale local sync state can lead to wrong scheduling decisions or edits to the wrong event.

Mitigation: Sync before freshness-sensitive reads, resolve exact dates and time zones before writing, and stop when verification is ambiguous.

Risk: Existing vdirsyncer conflict policy can overwrite local or remote calendar data.

Mitigation: Inspect conflict behavior before risky operations and avoid manual filesystem edits, cache resets, or storage path changes unless they are deliberate and reversible.

Risk: Calendar connection details, collection URLs, certificates, and sync configuration may expose private account information.

Mitigation: Avoid including private connection details in summaries unless requested, and treat certificate or TLS failures as blockers until the trust issue is fixed.

## Reference(s):

- [CalDAV Skill Page](https://clawhub.ai/ivangdavila/skills/caldav)
- [CalDAV Homepage](https://clawic.com/skills/caldav)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and concise operational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar scope, time window, action taken or proposed, verification status, and whether another sync is needed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
