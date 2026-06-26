## Description: <br>
Use local CLI to manage Apple, Google, iCloud, Outlook, CalDAV, and other calendars synced in macOS Calendar, without API keys or OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users on macOS use this skill to look up, create, update, delete, and verify events across calendars already synced into Calendar.app. It is intended for local calendar operations that require deterministic command fallback, explicit write confirmation, and read-back verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal-based local tools can access and modify calendars visible in macOS Calendar. <br>
Mitigation: Review confirmations carefully before deletes, recurring edits, calendar moves, and bulk changes. <br>
Risk: Calendar preferences and safety notes are stored locally under ~/apple-calendar-macos/. <br>
Mitigation: Periodically review the local skill directory and remove stale preferences or safety notes that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/apple-calendar-macos) <br>
- [Skill Homepage](https://clawic.com/skills/apple-calendar-macos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise calendar operation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file updates under ~/apple-calendar-macos/ after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
