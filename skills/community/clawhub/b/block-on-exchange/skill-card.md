## Description: <br>
Sync any ICS/iCal calendar to Microsoft Exchange as blocked time slots, with recurring event support, change detection, and privacy-preserving sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Blucaru](https://clawhub.ai/user/Blucaru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and individual users use this skill to mirror busy time from a personal or external ICS calendar into Microsoft Exchange without copying event titles, descriptions, attendees, or locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Microsoft calendar read/write access and stores an ICS secret URL plus OAuth tokens locally. <br>
Mitigation: Install only if that access is acceptable, keep the generated local files restricted, and protect the configured ICS URL and OAuth token files. <br>
Risk: Syncing to the wrong Exchange calendar or enabling background sync too early could create or remove blocked events unexpectedly. <br>
Mitigation: Run a manual sync first, verify the target calendar and created blocked events, set CALINT_MS_CALENDAR_ID when needed, and load the launchd job only when continuous background syncing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Blucaru/block-on-exchange) <br>
- [Project homepage](https://github.com/Blucaru/CalIn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, or delete Microsoft Exchange calendar events named Blocked through Microsoft Graph when the user runs sync commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
