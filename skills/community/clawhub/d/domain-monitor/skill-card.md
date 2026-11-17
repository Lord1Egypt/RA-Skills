## Description:

Monitors domain expiration dates, WHOIS information changes, and SSL certificate status for webmasters and domain investors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, webmasters, and domain investors use this skill to add domains, review current WHOIS and SSL status, list tracked domains, and run checks across the monitored set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores monitored domain names in the user's home directory and performs live WHOIS/TLS lookups.

Mitigation: Only monitor domains you are comfortable storing locally and querying through external WHOIS and TLS services.

Risk: SSL status results may be inaccurate according to the security guidance.

Mitigation: Treat SSL output as informational and verify certificate status with a dedicated certificate validation tool before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/domain-monitor)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status output and markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, whois, and openssl; stores the monitored domain list in the user's home directory and performs live WHOIS/TLS lookups.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter, artifact metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
