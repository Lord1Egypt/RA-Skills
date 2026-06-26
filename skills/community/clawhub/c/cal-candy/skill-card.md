## Description: <br>
Manage a local Markdown-based calendar by adding, listing, viewing, reminding, and deleting events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage local calendar events through Markdown files and a Python CLI, including event creation, month views, reminders, upcoming-event checks, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deleting an event modifies local calendar files and can remove the wrong entry if the event ID is mistaken. <br>
Mitigation: List events first and confirm the exact event ID before running delete or remind-del commands. <br>
Risk: Setting MDCAL_DIR to a broad or unrelated directory can cause the tool to read or edit Markdown files outside the intended calendar store. <br>
Mitigation: Use a dedicated calendar directory for MDCAL_DIR or keep the default ~/.openclaw/workspace/calendar location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/cal-candy) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown calendar files, reminders JSON, CLI text output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local calendar files under MDCAL_DIR or ~/.openclaw/workspace/calendar by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
