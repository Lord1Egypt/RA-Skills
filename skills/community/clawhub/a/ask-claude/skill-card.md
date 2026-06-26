## Description: <br>
Delegates a task to Claude Code CLI and returns the result in chat, with support for persistent sessions and user-selected workdirs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xManel](https://clawhub.ai/user/0xManel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to delegate coding, analysis, and development tasks to Claude Code CLI within a selected project directory, then summarize the result back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected project files and prompts may be exposed to Claude Code, and Claude Code session history may be retained locally. <br>
Mitigation: Use the skill only with workdirs whose contents are acceptable to share with Claude Code, and avoid sensitive, regulated, credential-heavy, or account data unless that exposure is explicitly accepted. <br>
Risk: The skill delegates execution to Claude Code with bypassed permission prompts. <br>
Mitigation: Review the wrapper command before use and install only when that execution authority is acceptable for the selected workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xManel/ask-claude) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands and summarized CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the claude binary and may continue prior Claude Code sessions for the same workdir.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
