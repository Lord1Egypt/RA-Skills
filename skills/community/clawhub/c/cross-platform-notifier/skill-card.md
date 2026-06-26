## Description: <br>
Triggers native system notifications across Windows, macOS, and Linux (including WSL) to alert the user when tasks are complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1tsnakers](https://clawhub.ai/user/1tsnakers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send desktop alerts when long-running tasks finish, urgent blockers need attention, or high-impact actions complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification title or message text that includes untrusted strings may be interpreted by PowerShell or AppleScript command wrappers. <br>
Mitigation: Use simple trusted notification text, and avoid passing raw logs, untrusted filenames, or user-supplied strings unless the script is hardened to escape those arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1tsnakers/cross-platform-notifier) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces native desktop notifications through OS-specific command-line tools; no API keys or credential parameters are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
