## Description:

Dynamic DNS updater for self-hosted, homelab, and edge devices that detects public IPv4 and IPv6 addresses, compares them with last-known addresses, and updates the configured DDNS provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kintansky](https://clawhub.ai/user/kintansky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and homelab operators use this skill to let an agent check current public IP addresses and update dynv6 dynamic DNS records when addresses change. It can also guide setup of the required local configuration and token environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says ordinary public-IP requests may lead to DNS-changing updates when a provider token is configured.

Mitigation: Use explicit DDNS update prompts, and treat public-IP-only requests as read-only unless a DNS update is intended.

Risk: A dynv6 token can authorize DNS record changes.

Mitigation: Keep the token scoped appropriately and store it outside the skill directory in a chmod-600 config file or protected environment variable.

Risk: The security guidance says referenced scripts should be verified before relying on the skill.

Mitigation: Confirm the expected scripts are present and inspect them before enabling automated or scheduled updates.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/kintansky/ddns-updator)
- [ClawHub skill page](https://clawhub.ai/kintansky/skills/ddns-updator)
- [ipify IPv4 API](https://api.ipify.org)
- [ipify IPv6 API](https://api64.ipify.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute network requests that read public IP addresses and update DDNS records when explicitly run.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
