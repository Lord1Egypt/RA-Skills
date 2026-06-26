## Description: <br>
BilldDesk Remote Desktop guides agents on using the WebRTC-based BilldDesk remote desktop tool, including high-resolution remote control, custom device codes, privacy and virtual screen features, screen walls, batch control, and safer use with Tailscale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operators, and authorized device owners use this skill for BilldDesk setup, connection workflows, Tailscale pairing, private relay deployment, and remote-control best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote desktop guidance can enable sensitive remote-control actions if used on devices the user does not own or administer. <br>
Mitigation: Use BilldDesk only on authorized devices, set strong unique passwords, keep clients updated, and prefer private-network access such as Tailscale or a trusted self-hosted relay. <br>
Risk: Clipboard synchronization and file transfer can expose sensitive data during remote sessions. <br>
Mitigation: Review clipboard and file-transfer activity before enabling it and avoid moving secrets or confidential files unless the remote session is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/billd-desk) <br>
- [BilldDesk website](https://desk.hsslive.cn) <br>
- [BilldDesk download page](https://desk.hsslive.cn/#/download) <br>
- [BilldDesk GitHub project](https://github.com/galaxy-s10/billd-desk) <br>
- [Tailscale install documentation](https://tailscale.com/install.sh) <br>
- [Tailscale downloads](https://tailscale.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No generated files; guidance should be reviewed before use on remote-control systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
