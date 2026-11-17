## Description:

Control real Android and iOS devices, run apps, take screenshots, and execute on-device inference via Ghost in the Droid MCP server (62 tools).

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-k-loan](https://clawhub.ai/user/c-k-loan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate Ghost in the Droid for Android and iOS device automation, mobile app workflows, screenshots, UI tree inspection, and on-device inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over real Android and iOS devices, including screen interaction and app operations.

Mitigation: Use dedicated test devices, connect only owned or authorized devices, and require explicit approval before actions that affect apps, data, or device state.

Risk: Screenshots, OCR, UI trees, and clipboard access can expose sensitive visible text or copied data.

Mitigation: Avoid using the skill on devices with personal or production data, and require approval before screenshots, OCR, UI-tree inspection, or clipboard reads.

Risk: Credential entry, APK installation, app-data clearing, batch execution, and replayed flows can cause account or application side effects.

Mitigation: Review planned flows before execution, avoid entering real credentials unless necessary, and require explicit approval for APK installation, app-data clearing, credential entry, batch actions, and replay actions.

Risk: The server security verdict is suspicious because the skill lacks clear safety boundaries or user-confirmation guidance for sensitive mobile automation operations.

Mitigation: Install only when the package is trusted and needed, use a dedicated virtual environment, avoid running as root, and apply human approval gates around sensitive operations.

## Reference(s):

- [Ghost in the Droid repository](https://github.com/ghost-in-the-droid/android-agent)
- [iOS setup guide](https://github.com/ghost-in-the-droid/android-agent/blob/main/docs/ios/SETUP.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps and tool-use guidance for Android, iOS, emulator, batching, screen-reading, app-management, clipboard, and on-device inference workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
