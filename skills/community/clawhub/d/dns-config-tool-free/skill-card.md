## Description:

DNS配置工具免费版 helps users plan basic DNS record changes, TTL updates, email authentication records, www/apex handling, and DNS propagation checks for personal and small-site deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, site owners, and small teams use this skill to plan DNS TTL changes, configure SPF/DKIM/DMARC records, handle www and apex domain variants, and run basic DNS checks before site or mail-service changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares write capability and broad routing text that could cause use outside DNS guidance.

Mitigation: Use it only for DNS record lookup, TTL planning, email authentication records, and propagation checks; require explicit confirmation before any DNS or file-changing action.

Risk: Incorrect DNS or email authentication advice can disrupt service availability or mail delivery.

Mitigation: Review proposed record changes before applying them, validate against the DNS or mail provider's authoritative documentation, and check multiple resolvers after changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-config-tool-free)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline DNS record examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DNS record values, TTL planning steps, verification commands, and cautionary notes for manual DNS-provider changes.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
