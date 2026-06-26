## Description: <br>
Use the local Codex CLI through mcporter and codex-mcp-server for real coding work in the current project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hollywood3](https://clawhub.ai/user/Hollywood3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate non-trivial coding tasks, debugging, refactoring, test work, and implementation review to a machine-local Codex setup while keeping the target workspace explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate work that changes project files through a local Codex setup. <br>
Mitigation: Use a narrow --cwd, prefer read-only mode for analysis, review diffs and test results, and avoid --yolo or danger-full-access unless explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hollywood3/codex-mcp-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file changes, test results, command output summaries, and implementation notes depending on the delegated Codex task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
