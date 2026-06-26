## Description: <br>
Build the Clawdbot macOS menu bar app from source for menu bar status, permissions, and Mac hardware access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manish-basargekar](https://clawhub.ai/user/manish-basargekar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build, sign, install, and launch the Clawdbot macOS companion app from source on macOS systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The build instructions clone and run commands from unpinned remote source code. <br>
Mitigation: Review or pin the repository version before running dependency install, build scripts, or packaging scripts. <br>
Risk: The app install path, launch, signing, and Xcode license steps may require elevated macOS trust decisions. <br>
Mitigation: Confirm each sudo, code-signing, /Applications install, and first-launch action before proceeding. <br>
Risk: The resulting app can request camera, microphone, screen recording, Accessibility, persistent service, remote gateway, and deep-link permissions. <br>
Mitigation: Grant only the permissions needed for the intended use and confirm how to disable remote access and uninstall the app first. <br>


## Reference(s): <br>
- [Clawdbot macOS documentation](https://docs.clawd.bot/platforms/macos) <br>
- [Clawdbot macOS release documentation](https://docs.clawd.bot/platforms/mac/release) <br>
- [ClawHub skill page](https://clawhub.ai/manish-basargekar/clawdbot-macos-build) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with bash command blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes prerequisite, build, signing, install, launch, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
