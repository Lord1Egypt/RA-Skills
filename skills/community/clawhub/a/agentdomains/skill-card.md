## Description:

Helps agents claim and manage public hostnames for sites, APIs, and webhooks using the AgentDomains CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tashfeenahmed](https://clawhub.ai/user/tashfeenahmed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to claim a public hostname, configure DNS, redirects or reverse proxying, and manage an AgentDomains account for a site, API or webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing a hostname or changing its DNS, redirects, proxy, or nameservers can expose a service or disrupt an existing address.

Mitigation: Confirm the intended destination and obtain user approval before exposing services or changing DNS, redirects, proxying, or nameserver delegation.

Risk: The setup script may install external code and store an API key locally; the optional local MCP package is unpinned.

Mitigation: Review the setup script and dependencies before running them; protect API keys from logs and transcripts and avoid the unpinned local MCP package unless reviewed.

Risk: Deleting a name or account can remove a public address and may be irreversible.

Mitigation: Confirm deletions with the user and inspect held names before account closure.

## Reference(s):

- [AgentDomains skill listing](https://clawhub.ai/tashfeenahmed/skills/agentdomains)
- [AgentDomains documentation](https://docs.agentdomains.co)
- [AgentDomains MCP documentation](https://docs.agentdomains.co/#mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Text]

**Output Format:** [Markdown with CLI examples and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check the serving status before reporting that a hostname is live.]

## Skill Version(s):

0.6.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
