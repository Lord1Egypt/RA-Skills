## Description: <br>
Lint your Claude Code config for token waste. Checks CLAUDE.md, hooks, skills, and commands. Gives health score and actionable fixes. Use when user asks about config optimization or token waste. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[singggggyee](https://clawhub.ai/user/singggggyee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to lint local Claude configuration for token waste and receive health scores and actionable fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes an external cclint CLI against local Claude Code configuration, so results depend on the installed CLI and its source. <br>
Mitigation: Install cclint only from a trusted source and review its behavior before running it on sensitive workstations. <br>
Risk: Claude configuration files may contain private prompts, hooks, commands, or secrets. <br>
Mitigation: Run the linter locally, avoid sharing raw output that includes sensitive configuration content, and review findings before applying changes. <br>


## Reference(s): <br>
- [cclint GitHub repository](https://github.com/SingggggYee/cclint) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external cclint CLI and reads local Claude Code configuration files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
