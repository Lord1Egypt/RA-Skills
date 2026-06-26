## Description: <br>
Organizes desktop files on macOS, Linux, and Windows by backing up the desktop and moving files or folders into configured destinations based on type, name, and folder rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hujxhed](https://clawhub.ai/user/hujxhed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to safely clean up a cluttered desktop by previewing files, creating a timestamped backup, moving items according to configured rules, and reporting the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move many desktop files and top-level folders without a clear approval gate. <br>
Mitigation: Require a dry run or explicit confirmation that lists every file and folder to be moved before executing commands, and verify the timestamped backup completed successfully. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hujxhed/desktop-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a file movement plan, backup location, categorized move commands, and a post-operation report.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
