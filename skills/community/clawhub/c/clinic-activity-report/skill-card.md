## Description:

Generate a plain-English weekly clinic activity report for a veterinary clinic owner from NxVET data, including total recordings, per-device and per-day/hour breakdowns, week-over-week trend, and health flags for silent devices, outdated firmware, and failing webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[talnirnx](https://clawhub.ai/user/talnirnx)

### License/Terms of Use:

MIT-0

## Use Case:

External veterinary clinic owners or managers use this skill to build and run a local, read-only weekly activity report from NxVET data. The report summarizes recording volume, usage patterns, and operational health signals without sending or changing clinic data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles NxVET API credentials and local clinic activity data.

Mitigation: Use a dedicated project folder, set NXVET_API_KEY via the process environment when possible, and keep .env, state, and output paths out of git and cloud sync.

Risk: Generated reports and cached responses may contain clinic business information.

Mitigation: Store reports locally, disable or delete the cache for sensitive clinics, and get clinic approval before syncing or sharing the project folder.

Risk: Webhook URLs may appear in generated artifacts.

Mitigation: Redact webhook URLs before sharing reports, logs, or support bundles.

## Reference(s):

- [NxVET clinic activity skill homepage](https://api.nx.vet/skills.html#clinic-activity)
- [NxVET API documentation](https://api.nx.vet/)
- [NxVET API guide for agents](https://api.nx.vet/llms-full.txt)
- [NxVET OpenAPI specification](https://api.nx.vet/openapi/nxvet-api.yaml)
- [NxVET MCP setup](https://api.nx.vet/mcp.html)
- [NxHUB product information](https://nx.vet/products/nxhub)
- [NxVET API reference notes](reference/nxvet-api.md)
- [Security and privacy notes](reference/security.md)
- [Caching and state notes](reference/caching-and-state.md)
- [Good practices](reference/good-practices.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report, optional self-contained HTML dashboard, JSON stats, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and NXVET_API_KEY; generated reports and cache files remain local.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
