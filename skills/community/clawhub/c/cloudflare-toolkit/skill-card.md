## Description:

Manage Cloudflare domains, DNS records, SSL settings, zone configuration, firewall rules, tunnels, and analytics through the Cloudflare API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[insipidpoint](https://clawhub.ai/user/insipidpoint)

### License/Terms of Use:


## Use Case:

Developers, operators, and site administrators use this skill to inspect and manage Cloudflare zones, DNS records, SSL settings, tunnels, cache, firewall rules, and analytics from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Cloudflare configuration, including DNS records, SSL settings, tunnels, cache state, and other zone settings.

Mitigation: Use a narrowly scoped Cloudflare API token for the specific account or zones needed, and require explicit confirmation before delete, import, SSL/settings, tunnel, or full cache-purge commands.

## Reference(s):

- [Cloudflare API Quick Reference](references/api-guide.md)
- [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
- [Cloudflare API v4 Endpoint](https://api.cloudflare.com/client/v4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit Cloudflare API JSON summaries when commands are run.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
