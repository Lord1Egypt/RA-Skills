## Description: <br>
Sync, inspect, and modify CalDAV calendars with vdirsyncer and khal using deterministic windows, verified writes, and recurrence-aware workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and calendar power users use this skill to operate existing CalDAV calendars through a local vdirsyncer and khal setup. It supports bounded calendar reads, verified event creation or edits, stale-sync troubleshooting, and cautious handling of ambiguous or recurring events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can operate on already-configured CalDAV calendars, including real calendar data. <br>
Mitigation: Use explicit calendar names and bounded date ranges, and require confirmation before deletes, bulk changes, recurring-event edits, or conflict-resolution changes. <br>
Risk: Stale sync state or ambiguous event matches can lead to incorrect scheduling decisions or changes to the wrong event. <br>
Mitigation: Run vdirsyncer sync before freshness-sensitive reads, verify writes with a read-back pass, and stop when matching remains ambiguous. <br>
Risk: Recurring events, timezone-sensitive edits, and one-sided conflict policies can cause calendar data loss or series drift. <br>
Mitigation: Inspect before editing, prefer recreate-only-with-approval for fragile series, and review configured conflict policy before resolving sync conflicts. <br>


## Reference(s): <br>
- [CalDAV Skill Page](https://clawhub.ai/ivangdavila/caldav) <br>
- [CalDAV Skill Homepage](https://clawic.com/skills/caldav) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires existing vdirsyncer and khal configuration; prompts confirmation for destructive or ambiguous calendar changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
