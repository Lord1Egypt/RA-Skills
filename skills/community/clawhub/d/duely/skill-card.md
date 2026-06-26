## Description: <br>
Track recurring maintenance tasks from the command line, including scheduling, due checks, run and skip logging, and task removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halbotley](https://clawhub.ai/user/halbotley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to maintain recurring local tasks such as backups, reviews, and periodic checks without calendar overhead. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI is installed from a third-party Homebrew tap. <br>
Mitigation: Install only after trusting the halbotley/tap source and confirming it matches the expected duely release. <br>
Risk: Recurring task names, notes, and logs may expose sensitive operational details. <br>
Mitigation: Avoid putting secrets or sensitive details in task names, notes, or logs, especially when used from cron or an agent heartbeat. <br>
Risk: Agent-triggered maintenance actions can affect high-impact local workflows. <br>
Mitigation: Keep sensitive or high-impact tasks under explicit approval before marking them complete or acting on due items. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halbotley/duely) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/halbotley) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through the local duely CLI and store task data locally in ~/.duely/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
