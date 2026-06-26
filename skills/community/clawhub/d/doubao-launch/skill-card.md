## Description: <br>
Launch Doubao desktop application and configure real-time translation window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banner90](https://clawhub.ai/user/banner90) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workflow operators use this skill to launch the Doubao desktop translation window as part of a YouTube translation workflow. It is intended for environments that can run Windows GUI automation from WSL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes an unbundled hardcoded Python script, so the release artifact does not let users verify the actual automation code. <br>
Mitigation: Install only after inspecting and controlling the configured local Python file at the /mnt/h/AI/... path. <br>
Risk: The skill automates a visible Windows desktop session and may be machine-specific or unreliable on systems without the expected GUI state. <br>
Mitigation: Run it only in a controlled Windows desktop environment where Doubao, WSL path mapping, and the target workflow are configured and observable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banner90/doubao-launch) <br>
- [Publisher profile](https://clawhub.ai/user/banner90) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON status response with markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success status, window handle, window title, mode, or error fields; requires a visible Windows desktop session and a configured local Python entry path.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact package.json and openclaw.plugin.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
