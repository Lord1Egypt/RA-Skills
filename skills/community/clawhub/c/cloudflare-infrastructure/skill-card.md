## Description:

Manage Cloudflare zones, DNS records, workers, rules, firewall settings, and account resources via the Cloudflare API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill from OpenClaw to inspect and manage Cloudflare infrastructure, including zones, DNS records, account resources, workers, rules, firewall settings, WAF lists, tunnels, and related Cloudflare API resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages high-impact Cloudflare infrastructure through a third-party ClawLink plugin that stores and uses Cloudflare credentials.

Mitigation: Install only if the publisher and ClawLink are trusted, use the narrowest Cloudflare permissions possible, and revoke the Cloudflare connection when it is no longer needed.

Risk: Write operations can create, update, or delete zones, DNS records, WAF lists, tunnel configuration, and other account resources.

Mitigation: Confirm the target resource and intended effect before every write, preview tool calls where supported, and prefer read/list/describe operations before changes.

Risk: Tunnel configuration updates replace the full configuration and can unintentionally remove existing ingress rules.

Mitigation: Fetch and review the current tunnel configuration before applying an update, then confirm that the preview preserves required rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/cloudflare-infrastructure)
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [Cloudflare DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone)
- [Cloudflare Zones API](https://developers.cloudflare.com/api/operations/zones)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=cloudflare-infrastructure)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cloudflare tool names, preview guidance, confirmation prompts, and troubleshooting steps.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
