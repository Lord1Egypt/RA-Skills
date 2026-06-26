## Description: <br>
Delegates repository coding tasks to the local OpenCode CLI for planning and implementation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciding](https://clawhub.ai/user/deciding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to route repository coding tasks through OpenCode, first asking its plan agent for a plan and then using its build agent to implement approved work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates broad repository planning and implementation work to a local OpenCode CLI. <br>
Mitigation: Install only when the local opencode CLI is trusted, review the plan before build steps, and inspect file changes before accepting them. <br>
Risk: The documented command pattern places user instructions inside a shell command. <br>
Mitigation: Avoid pasting untrusted text directly into the command; use safer argument passing or prompt files where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciding/easy-opencode) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local opencode binary and a selected repository working directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
