## Description:

Automates Windows desktop workflows by opening CMD in a selected folder, sending commands or batch scripts, downloading latest GitHub source ZIPs, and showing a full-screen interruptible progress overlay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced Windows users use this skill to drive local Windows automation tasks, including running commands in a chosen directory, launching batch scripts, and downloading a repository's latest source package. It is intended for supervised local automation where the user can review inputs and stop execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run arbitrary commands and manipulate desktop applications.

Mitigation: Review the requested path, command, script, and URL before execution, and run only in an isolated Windows environment when accepting this control level.

Risk: The skill can install or reinstall Python packages and modify the local Python environment.

Mitigation: Use a disposable virtual environment and review package installation behavior before normal use.

Risk: The release includes an unrelated WeChat UI automation task that is not clearly disclosed in the main skill description.

Mitigation: Remove, disable, or explicitly disclose and gate that task before normal use.

Risk: Command logs may capture operational details or sensitive command text.

Mitigation: Avoid passing secrets in commands and review log output handling before using the skill with sensitive projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/claw-windows-automator)
- [Publisher profile](https://clawhub.ai/user/wangminrui2022)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on Windows, manipulates desktop applications, and may open browsers or write logs.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
