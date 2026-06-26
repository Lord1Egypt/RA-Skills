## Description: <br>
Invoke Claude Code CLI as a subprocess for coding tasks that require file access, editing, and shell execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EZPeasyDave](https://clawhub.ai/user/EZPeasyDave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate repository work, code review, debugging, build/test execution, and file edits to Claude Code CLI when local filesystem and shell access are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates coding work to a non-interactive external agent with local repository access. <br>
Mitigation: Use the narrowest working directory that can complete the task and review changes before deployment. <br>
Risk: Allowed shell tools can enable broad filesystem or command execution. <br>
Mitigation: Keep the allowed tool list minimal and avoid Bash unless the task explicitly requires builds, tests, or git operations. <br>
Risk: Claude Code inherits environment variables that may include unrelated secrets. <br>
Mitigation: Run with a clean environment and exclude credentials that are not needed for the delegated task. <br>


## Reference(s): <br>
- [Claude Code Dispatch on ClawHub](https://clawhub.ai/EZPeasyDave/claude-code-dispatch) <br>
- [EZPeasyDave publisher profile](https://clawhub.ai/user/EZPeasyDave) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text with status, model, cost, duration, and result fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results longer than 2000 characters are truncated at a line boundary.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
