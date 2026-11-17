## Description:

Biver Builder lets an agent manage Biver landing pages, sections, products, forms, gallery assets, subdomains, custom domains, workspace settings, analytics, checkout data, and AI generation through the authenticated Biver API or MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramaaditya49](https://clawhub.ai/user/ramaaditya49)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to read or change Biver workspace resources through authenticated REST or MCP calls. It is suited for agent-assisted site, commerce, domain, media, analytics, and workspace administration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can affect the Biver workspace attached to the key, including high-impact writes.

Mitigation: Start with read-only, least-privilege scopes and add write scopes only when the task requires them.

Risk: Deletes, publishes, domain changes, gallery deletion, and workspace setting mutations can materially change a live workspace.

Mitigation: Require fresh explicit confirmation naming the target and impact before each high-impact call.

Risk: Credentials could be exposed through logs, URLs, files, prompts, or responses.

Mitigation: Store BIVER_API_KEY in the client secret store and never print, log, or embed it in generated content.

Risk: Ambiguous mutation retries after timeouts could duplicate or conflict with previous changes.

Mitigation: Re-read the resource after an ambiguous timeout before retrying create, deploy, or delete operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ramaaditya49/skills/biver-builder)
- [Project Homepage](https://github.com/RamaAditya49/biver-builder)
- [Live Biver REST Contract](https://api.biver.id/SKILL.md)
- [Biver MCP Endpoint](https://mcp.biver.id/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and structured API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include REST or MCP request instructions and should avoid exposing API keys.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
