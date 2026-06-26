## Description: <br>
Run arbitrary commands when files change. Useful for watching files and triggering builds or tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run build, test, or server commands automatically when watched files change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps an agent run user-chosen commands when files change, including shell-evaluated commands with entr -s. <br>
Mitigation: Review commands before execution, avoid shell-evaluated -s commands unless needed, and stop background watchers when they are no longer required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides command examples and notes that entr blocks the terminal while watching files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
