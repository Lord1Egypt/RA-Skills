## Description: <br>
Displays Claude Code session status information, including Git branch, current model, context usage, output tokens, cost, duration, and changed line counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mark-heartflow](https://clawhub.ai/user/mark-heartflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code use this skill to configure a local status line that summarizes session and Git working-tree state while they work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures Claude Code to run a persistent local Bash statusLine command. <br>
Mitigation: Review the Bash script before enabling it, store it in a trusted local path, and remove the statusLine setting from ~/.claude/settings.json when it is no longer needed. <br>
Risk: The status-line script reads local Claude settings and Git working-tree state. <br>
Mitigation: Use it only in repositories and local environments where displaying branch, model, and change-summary information is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mark-heartflow/claude-statusline-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and Bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local Claude Code settings guidance and a Bash status-line command script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
