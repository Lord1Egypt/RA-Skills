## Description: <br>
Agent Runtime provides a JavaScript agent runtime for tool registration, permission labels, hook interception, context compression, and usage tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhmqq616](https://clawhub.ai/user/xhmqq616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a lightweight JavaScript runtime pattern for registering tools, running simple agent turns, tracking token usage, and experimenting with sub-agent modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime exposes local shell execution while advertised permission and hook controls do not actually enforce limits. <br>
Mitigation: Review before installing or using; remove or lock down the shell tool, add real permission enforcement, and require explicit approval for command execution. <br>
Risk: Built-in local file access can expose sensitive workspace data when used without path restrictions. <br>
Mitigation: Run only in a sandboxed workspace and restrict file tools to approved paths before use. <br>


## Reference(s): <br>
- [Agent Runtime on ClawHub](https://clawhub.ai/xhmqq616/agent-runtime) <br>
- [Publisher profile](https://clawhub.ai/user/xhmqq616) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, text, guidance, configuration] <br>
**Output Format:** [Markdown usage guidance plus a JavaScript module and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes built-in read_file, bash, search, and todo tool examples with token usage tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
