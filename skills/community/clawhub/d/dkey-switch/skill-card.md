## Description: <br>
Dkey Switch helps an agent find, list, and activate Windows application windows or tabs using keyword, process, and handle based commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddmy](https://clawhub.ai/user/ddmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route desktop window-switching requests into Windows commands that find candidate windows, request confirmation when needed, and activate the selected window or tab. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports missing main Windows automation files. <br>
Mitigation: Verify that the complete release includes the expected Windows scripts before installing or running the skill. <br>
Risk: The included launcher bypasses PowerShell execution policy. <br>
Mitigation: Install only from a trusted publisher and review the scripts before execution. <br>
Risk: The skill can enumerate window titles and switch desktop focus or tabs. <br>
Mitigation: Avoid running it while sensitive windows or active text fields are open, and require confirmation before ambiguous matches. <br>


## Reference(s): <br>
- [Dkey Switch ClawHub Page](https://clawhub.ai/ddmy/dkey-switch) <br>
- [Publisher Profile](https://clawhub.ai/user/ddmy) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [AI E2E Cases](references/ai-e2e-cases.md) <br>
- [Onboarding Flow](references/onboarding-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PowerShell on Windows; command behavior may enumerate window titles and switch desktop focus.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
