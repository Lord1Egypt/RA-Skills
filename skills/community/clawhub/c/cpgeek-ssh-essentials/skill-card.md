## Description: <br>
Essential SSH commands for secure remote access, key management, tunneling, and file transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpgeek](https://clawhub.ai/user/cpgeek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and operators use this skill as an SSH command reference for secure remote access, key management, tunneling, and file transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH command examples can affect host verification, credentials, tunnels, file transfers, or server configuration if copied without review. <br>
Mitigation: Review commands before running them, especially StrictHostKeyChecking=no, agent forwarding, background tunnels, and SSH server configuration changes. <br>
Risk: File transfer examples such as rsync --delete can remove destination files when paths or options are wrong. <br>
Mitigation: Run dry-run checks first, confirm source and destination paths, and use destructive options only after reviewing the expected changes. <br>


## Reference(s): <br>
- [OpenSSH](https://www.openssh.com/) <br>
- [OpenSSH Manual Pages](https://www.openssh.com/manual.html) <br>
- [SSH Essentials on ClawHub](https://clawhub.ai/cpgeek/cpgeek-ssh-essentials) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and SSH configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance with visible, user-run examples and no hidden execution or installation behavior.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; changelog lists 2.0 security remediation dated 2026-05-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
