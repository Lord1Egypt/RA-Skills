## Description: <br>
Manage Bring! shopping lists via CLI to add, remove, complete, and view items or lists using the Bring! API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joekravelli](https://clawhub.ai/user/joekravelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate their Bring! shopping lists through a local CLI, including listing lists and items, adding groceries, removing entries, and marking items complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Bring! account credentials and can change shopping-list contents. <br>
Mitigation: Keep credentials out of repositories and backups, prefer environment variables or the documented local credentials file, and confirm add, remove, or complete actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/joekravelli/bring-app) <br>
- [bring-api Python package](https://github.com/miaucl/bring-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bring! credentials through BRING_EMAIL and BRING_PASSWORD or a local credentials file; commands can change shopping-list state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
