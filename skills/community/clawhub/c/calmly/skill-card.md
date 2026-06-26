## Description: <br>
calmly helps agents manage macOS Calendar events from the command line using EventKit, including listing calendars and events and creating all-day, multi-day, or timed events for iCloud, local, and CalDAV calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halbotley](https://clawhub.ai/user/halbotley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to inspect calendars and create calendar events from automated command-line workflows without relying on Calendar UI dialogs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar access can create events that persist and sync to iCloud or other connected calendars. <br>
Mitigation: Install only if the external Homebrew tap is trusted, grant Calendar access deliberately, and review event details before creating or batch-creating events. <br>
Risk: Batch event creation can add incorrect events when dates, times, or calendar names are wrong. <br>
Mitigation: Use date verification before batch creation and review the target calendar after running commands. <br>


## Reference(s): <br>
- [calmly on ClawHub](https://clawhub.ai/halbotley/calmly) <br>
- [halbotley publisher profile](https://clawhub.ai/user/halbotley) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces macOS Calendar CLI commands and usage guidance; event deletion is outside the documented skill behavior.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
