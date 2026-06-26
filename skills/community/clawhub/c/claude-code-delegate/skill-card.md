## Description: <br>
Delegate programming tasks to Claude Code CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhab03](https://clawhub.ai/user/chenhab03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to delegate coding, debugging, testing, and file-editing tasks to a local Claude Code CLI while the main agent remains responsive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The delegated Claude Code process may receive broad filesystem read and write capability when permission bypass mode is used. <br>
Mitigation: Use an enforceable write-guard or path allowlist before running the skill, and restrict execution to an isolated project directory. <br>
Risk: Running delegated coding tasks in repositories that contain secrets can expose or modify sensitive material. <br>
Mitigation: Avoid repositories containing secrets and review delegate output before accepting changes. <br>
Risk: Continuing a prior Claude Code session across unrelated projects can carry task context into the wrong workspace. <br>
Mitigation: Treat session resume as project-specific and start fresh sessions for unrelated work or independent verification. <br>


## Reference(s): <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch asynchronous local Claude Code CLI sessions and relay concise execution summaries.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
