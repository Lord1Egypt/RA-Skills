## Description: <br>
Calendar Sync extracts deadlines, event dates, and date ranges from structured document data and turns them into Apple Calendar entries or importable ICS files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-automation users use this skill to convert structured document dates into calendar events, reminders, and importable calendar files. It supports workflows where parsed documents need follow-up deadlines, events, or periods reflected in Apple Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct Apple Calendar mode builds executable AppleScript from document fields. <br>
Mitigation: Prefer the ICS workflow, inspect generated events before import, and use direct AppleScript mode only when the structured JSON comes from a trusted source. <br>
Risk: Calendar entries can persist sensitive document details such as amounts, file paths, names, Notion links, and document IDs. <br>
Mitigation: Redact sensitive notes before syncing to calendars that may be shared, backed up, or visible to other users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkbeomjun-gkgkgk/calendar-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [ICS calendar files, AppleScript or osascript commands, Python code, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates calendar_events.ics by default and can attempt direct Apple Calendar registration on macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
