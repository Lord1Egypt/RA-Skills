## Description:

Manage Cloudflare via API \u2014 DNS zones and records, page rules, SSL/TLS settings, caching, firewall rules, Workers, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexlunae](https://clawhub.ai/user/rexlunae)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Cloudflare zones, DNS records, SSL/TLS settings, cache purges, firewall access rules, and analytics through a local command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local helper requires access to a Cloudflare API token that can modify Cloudflare resources if over-scoped.

Mitigation: Use the narrowest Cloudflare token permissions and account scopes possible, and store the token with restrictive filesystem permissions.

Risk: Zone deletion, DNS changes, firewall rules, SSL/TLS changes, and cache purges can disrupt production traffic.

Mitigation: Review commands before execution and confirm the target domain, record ID, and action before running destructive operations.

Risk: The security evidence states that documented Workers and page-rules commands do not work in this version.

Mitigation: Do not rely on the Workers or page-rules workflows until the skill documentation and helper implementation are updated and revalidated.

## Reference(s):

- [Cloudflare API documentation](https://developers.cloudflare.com/api/)
- [Cloudflare API v4 base URL](https://api.cloudflare.com/client/v4/)
- [Cloudflare API token dashboard](https://dash.cloudflare.com/profile/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper prints Cloudflare API responses as JSON for many commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
