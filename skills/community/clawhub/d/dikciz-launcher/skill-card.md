## Description:

Install and operate Dikciz Launcher on an owner-selected Android device. Use when controlling its home, HTML widgets, Lua, Android data, sensors, camera, audio, speech, Bluetooth, NFC, USB, Wi-Fi, files, APKs, shell sessions or command jobs through MCP, HTTP or WebSocket. Source builds use the Android Lab skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device owners use this skill to install and operate Dikciz Launcher on an owner-selected Android phone through its discovered MCP, HTTP, or WebSocket controls. It guides scoped access to launcher features, apps, files, Android data, and device hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence rates the release suspicious because setup directs downloads from GitHub beyond its declared network scope; the scan was partial and also noted a credential-access reference it judged unexpected for the skill's purpose.

Mitigation: Review the download source and verification steps before installation, limit network access to what the selected setup requires, and keep bearer credentials in the secret environment.

## Reference(s):

- [Setup and connection guide](references/setup.md)
- [Capabilities reference](references/capabilities.md)
- [Hardware and speech operations](references/hardware-and-speech.md)
- [Managed operations](references/operations.md)
- [Dikciz user guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/user-guide.md)
- [Automation control guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/automation-control.md)
- [Files, APKs, and shell guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/files-and-apks.md)
- [Remote access token permissions](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/token-permissions.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline command, JSON, Lua, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-specific procedures and examples; available actions depend on the connected Android device, installed build, and granted permissions.]

## Skill Version(s):

0.32.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
