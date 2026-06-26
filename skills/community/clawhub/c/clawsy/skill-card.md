## Description: <br>
Clawsy is a native macOS companion app that gives an OpenClaw agent access to screenshots, clipboard, camera, files, location, and Mission Control through WebSocket or SSH fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iret77](https://clawhub.ai/user/iret77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to pair an OpenClaw agent with a macOS companion app, enabling guided setup, device context, shared-folder file exchange, and live progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad access to a user's Mac, including screenshots, camera, clipboard, location, and file operations. <br>
Mitigation: Install only for trusted publishers, grant macOS permissions deliberately, and require explicit confirmation for sensitive screen, camera, clipboard, location, or file-change actions. <br>
Risk: The setup flow exposes an OpenClaw gateway token in setup instructions that may appear in chat or logs. <br>
Mitigation: Treat setup codes as credentials, avoid sharing them outside the pairing flow, and rotate or revoke the gateway token after pairing if it was exposed. <br>
Risk: Shared-folder file operations can read or write user files within the configured Clawsy folder. <br>
Mitigation: Configure the shared folder with low-sensitivity files only and review proposed file changes before relying on them. <br>
Risk: The macOS companion app is downloaded separately from a release page. <br>
Mitigation: Verify the downloaded app release and signature before launching it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iret77/clawsy) <br>
- [Clawsy repository](https://github.com/iret77/clawsy) <br>
- [Clawsy latest release](https://github.com/iret77/clawsy/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup-code handling, Clawsy node command references, and Mission Control status guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
