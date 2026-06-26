## Description: <br>
Install, update, run, and remove OpenClaw Gateway Monitor + Gateway Watchdog on macOS via LaunchAgent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yes999zc](https://clawhub.ai/user/yes999zc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, check, update, and remove a macOS LaunchAgent-based OpenClaw gateway monitor and watchdog. It is intended for local OpenClaw gateway health monitoring and recovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent macOS background services that monitor and attempt to recover OpenClaw gateway state. <br>
Mitigation: Review the scripts before execution, run only in a trusted macOS user environment, and confirm the LaunchAgent files and labels before bootstrapping services. <br>
Risk: The monitor server exposes unauthenticated HTTP APIs on all network interfaces while reading local OpenClaw logs, session status, and possible MiniMax credential material. <br>
Mitigation: Prefer a revised release that binds to 127.0.0.1, adds authentication, restricts network access, documents credential use, and removes or protects restore-config behavior. <br>
Risk: The installer expects LaunchAgent template files that are not present in the artifact, so installation may fail or leave a partial local setup. <br>
Mitigation: Verify the required LaunchAgent templates are present before running install.sh; if an install fails, use uninstall.sh and launchctl inspection to clean up any partial services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yes999zc/gateway-monitor-installer) <br>
- [Publisher profile](https://clawhub.ai/user/yes999zc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides installation, status, and uninstall guidance for bundled macOS scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
