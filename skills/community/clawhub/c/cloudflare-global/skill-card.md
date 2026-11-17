## Description:

Cloudflare DNS and zone operations using a Global API Key. Use when the user needs to list, create, update, delete, export, or import DNS records, inspect zone settings or SSL mode, purge cache, inspect page rules or firewall rules, or work with Cloudflare tunnels using a Global API Key instead of a modern API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform Cloudflare zone, DNS, SSL, cache, firewall, page-rule, analytics, and tunnel operations through the legacy Global API Key flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad live Cloudflare control through a legacy Global API Key.

Mitigation: Use it only when legacy Global API Key automation is intentionally required; prefer scoped API-token workflows when possible and run it only on trusted systems.

Risk: Delete, import, SSL, cache purge, and tunnel operations can make disruptive live changes.

Mitigation: Verify zone and record IDs before mutations and require an explicit confirmation process before high-impact operations.

Risk: Cloudflare credentials and identifiers could be exposed through examples, logs, or local environment handling.

Mitigation: Keep credentials in local environment variables and keep examples, logs, and future edits free of real zone IDs, account IDs, emails, and record contents.

## Reference(s):

- [Cloudflare API v4 endpoint](https://api.cloudflare.com/client/v4)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local environment variables for Cloudflare credentials; script output is filtered through jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
