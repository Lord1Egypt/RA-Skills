## Description: <br>
Launches Claude Code in a new macOS Terminal window, navigates to a project, enables Remote Control, and captures the session state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QusaiiSaleem](https://clawhub.ai/user/QusaiiSaleem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start Claude Code in a selected project and enable Remote Control for access from another trusted device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Desktop automation can send commands to the wrong foreground window or operate on an unexpected project path. <br>
Mitigation: Review before installing or running, use only trusted project paths with ordinary characters, and keep the intended Terminal session focused during execution. <br>
Risk: Remote Control can expose sensitive repository context through session URLs or QR codes. <br>
Mitigation: Avoid enabling Remote Control for sensitive repositories unless the exposure is understood, and share session access only in trusted environments. <br>
Risk: Saved logs and screenshots can contain sensitive project or session information. <br>
Mitigation: Protect or periodically delete screenshots and logs saved under ~/.openclaw/workspace/logs/claude-code-launcher. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/QusaiiSaleem/claude-code-launcher) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style status text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local logs and screenshots under ~/.openclaw/workspace/logs/claude-code-launcher.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
