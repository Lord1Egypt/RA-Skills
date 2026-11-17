## Description:

抓取网站数据的本地 Firecrawl 服务。使用本地 API (http://192.168.1.2:3002/) 进行网页抓取、数据提取和站内搜索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobowg163](https://clawhub.ai/user/bobowg163)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to call a local Firecrawl service for webpage scraping, site mapping, and site search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends arbitrary scrape targets and results to an unauthenticated HTTP service on a private-network address.

Mitigation: Install only when you control and trust the Firecrawl service at 192.168.1.2:3002, and add authentication, target allowlists, and network egress controls before sensitive use.

Risk: Sensitive URLs, credentials in query strings, or prompt-provided targets could be exposed to the local Firecrawl service.

Mitigation: Avoid using the skill with sensitive URLs or untrusted prompts unless inputs are reviewed and constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobowg163/skills/firecrawl-local-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python helper usage, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library urllib.request and a 30-second HTTP timeout.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
