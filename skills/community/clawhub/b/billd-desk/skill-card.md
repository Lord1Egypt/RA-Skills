## Description:

BilldDesk Remote Desktop guides agents on installing, configuring, and operating the BilldDesk WebRTC remote desktop tool, including Tailscale-assisted connectivity and private relay deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT operators, and device administrators use this skill to get agent guidance for BilldDesk remote access setup, device management, Tailscale-based connectivity, and private relay deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance may execute changing remote code.

Mitigation: Prefer official platform installers or package-manager instructions, and inspect any install script before execution.

Risk: An unverified container service could expose relay ports or run unexpected code.

Mitigation: Verify the container image registry and digest, and bind deployment ports only to trusted interfaces.

Risk: Unattended access, clipboard sync, file transfer, and bulk control can increase remote-control and data-transfer impact.

Mitigation: Enable these features only for devices you own or administer, and require strong authentication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smseow001/skills/billd-desk)
- [Publisher Profile](https://clawhub.ai/user/smseow001)
- [BilldDesk Official Site](https://desk.hsslive.cn)
- [BilldDesk Download Page](https://desk.hsslive.cn/#/download)
- [BilldDesk GitHub Repository](https://github.com/galaxy-s10/billd-desk)
- [Tailscale Download Page](https://tailscale.com/download)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes remote-desktop installation, Tailscale setup, and Docker deployment guidance; no API keys or credential environment variables were detected.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
