## Description: <br>
Delegate coding tasks to a separate autonomous agent with AST validation, security scanning, automatic retry, multiple backend options, and structured JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabriel-hurtado](https://clawhub.ai/user/gabriel-hurtado) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding tasks such as creating code, modifying existing projects, fixing bugs, building components, and generating tests to a separate coding agent with validation and budget controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, edit, and run commands in the selected workspace through an autonomous coding agent. <br>
Mitigation: Run it in a git-controlled or disposable workspace, keep sandboxing enabled, and restrict allowed write paths when possible. <br>
Risk: Autonomous coding runs can consume provider tokens, time, and cost. <br>
Mitigation: Set maximum cost, token, time, and iteration limits before execution. <br>
Risk: Disabling sandboxing or using a backend without sandbox support increases workspace and command-execution exposure. <br>
Mitigation: Avoid no-sandbox mode except inside an isolated container or VM, and trust the chosen AI provider and Agenter package before installation. <br>


## Reference(s): <br>
- [Agenter Backend Comparison](references/backends.md) <br>
- [Agenter SDK](https://github.com/Moonsong-Labs/agenter) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON results plus file modifications in the selected workspace] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status, summary, files modified, generated file content, iterations, token usage, cost, and duration when available.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
