## Description:

Essential SSH commands for secure remote access, key management, tunneling, and file transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpgeek](https://clawhub.ai/user/cpgeek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and operations teams use this skill as a practical SSH reference for remote login, key management, tunneling, file transfers, and security-sensitive troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable SSH examples can weaken host verification when users apply StrictHostKeyChecking=no or append ssh-keyscan output without trusted comparison.

Mitigation: Prefer StrictHostKeyChecking=accept-new or verified known_hosts entries, and compare ssh-keyscan output against a trusted out-of-band source before appending it.

Risk: Forwarding, background tunnels, and multiplexed SSH sessions can expose local services, credentials, or persistent access paths beyond the intended session.

Mitigation: Use agent forwarding, remote forwarding, and background tunnels only with trusted hosts; set reasonable lifetimes and clean up sessions with ssh -O exit, ssh-add -d, or ssh-add -D when finished.

Risk: File transfer examples such as rsync --delete, scp, and temporary SFTP files can cause data loss or leave sensitive data behind.

Mitigation: Run rsync --dry-run before destructive syncs, prefer sftp or rsync over deprecated scp workflows, and remove sensitive temporary files from remote systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cpgeek/skills/cpgeek-ssh-essentials)
- [OpenSSH homepage](https://www.openssh.com/)
- [OpenSSH manual pages](https://www.openssh.com/manual.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and security callouts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copyable examples for ssh, scp, sftp, rsync, ssh-keygen, and ssh-copy-id; users should vet commands before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata; changelog reports 2.0 security remediation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
