## Description:

CodeBuddy Coding lets agents invoke CodeBuddy CLI for code generation, refactoring, debugging, file operations, command execution, progress monitoring, and structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13770626440](https://clawhub.ai/user/13770626440)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to delegate coding tasks to CodeBuddy CLI in a project workspace. It supports generating or refactoring code, fixing bugs, running commands, monitoring progress, and returning structured execution results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to bypassing permission checks for CodeBuddy CLI execution.

Mitigation: Prefer permission-gated execution, require explicit approval for file changes and commands, and use a disposable or version-controlled workspace.

Risk: The skill runs user-supplied tasks through shell-backed CLI execution in the selected working directory.

Mitigation: Constrain cwd to the intended project, sandbox execution where possible, and avoid passing unreviewed tasks or paths.

Risk: Detached background runs can continue outside normal task tracking.

Mitigation: Avoid background execution unless process IDs are tracked and runs are cancellable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13770626440/skills/codebuddy-coding)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON or text result objects with progress updates and file and tool-call summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify files and run commands in the configured workspace through CodeBuddy CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
