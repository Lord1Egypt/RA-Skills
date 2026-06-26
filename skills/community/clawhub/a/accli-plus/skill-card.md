## Description: <br>
Manage Apple Calendar events from the command line on macOS, including creating, updating, deleting, searching, exporting, and checking availability with JSON output for agent use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopaljigaur](https://clawhub.ai/user/gopaljigaur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to operate Apple Calendar from automation workflows with structured JSON output, stable calendar identifiers, dry-run previews, and command guidance for common calendar tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The underlying third-party npm tool requires Full Access to Apple Calendar. <br>
Mitigation: Install only if the publisher and npm package are trusted, and grant Calendar access intentionally through macOS privacy settings. <br>
Risk: Update, delete, recurring-series, and broad export operations can affect or expose calendar data. <br>
Mitigation: Use narrow date ranges and calendar IDs, prefer --dry-run before updates or deletes, and require confirmation before destructive or broad-data operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gopaljigaur/accli-plus) <br>
- [npm package @gopaljigaur/accli](https://www.npmjs.com/package/@gopaljigaur/accli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends --json output, stable calendar IDs, --dry-run previews, and narrow date ranges for calendar operations.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
