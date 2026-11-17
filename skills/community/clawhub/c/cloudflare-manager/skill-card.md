## Description:

Manage Cloudflare DNS records, Tunnels (cloudflared), and Zero Trust policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Cloudflare DNS records, expose local services with cloudflared tunnels, and update tunnel ingress configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate Cloudflare DNS records and zone settings with the configured API token.

Mitigation: Use a narrowly scoped Cloudflare token for the intended zone, review proposed commands, and run dry-run previews before applying changes.

Risk: Tunnel ingress updates can write to /etc/cloudflared/config.yml and restart the cloudflared service with sudo.

Mitigation: Grant sudo only for the minimum required cloudflared operations, review configuration diffs, and keep a backup or rollback path for the tunnel config.

Risk: The release references restricted sudoers guidance that is not present in the artifact files.

Mitigation: Do not grant broad sudo access until the expected sudoers guidance is supplied and reviewed.

Risk: Cloudflare setting updates are broad and under-documented in the security evidence.

Mitigation: Limit setting changes to reviewed setting IDs and values until scoping and validation are clarified.

## Reference(s):

- [Cloudflare Manager ClawHub page](https://clawhub.ai/1999azzar/skills/cloudflare-manager)
- [Cloudflare Tunnel Configuration](references/tunnel-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON command output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Cloudflare APIs and may propose or run sudo-backed cloudflared configuration changes when explicitly used by an agent.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
