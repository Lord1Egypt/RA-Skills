## Description:

Launch Doubao desktop application and configure real-time translation window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banner90](https://clawhub.ai/user/banner90)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to launch the Doubao desktop application, configure a real-time translation window, and return launch status for a larger YouTube translation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package points to an unbundled Python file at an absolute host path, so installation alone does not prove which code will run.

Mitigation: Require the Doubao automation script to be bundled with the release and invoked through a package-relative entry point, or pin and verify the external script before execution.

Risk: Windows GUI automation requires a visible desktop session and may fail or act on the wrong desktop state when the session is disconnected.

Mitigation: Run the skill only in a dedicated visible Windows desktop session and verify the target Doubao window before using downstream translation or capture steps.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, json, guidance]

**Output Format:** [Markdown usage guidance with JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an optional mode parameter of dual or single and returns a success flag, window handle, window title, mode, and error fields when applicable.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
