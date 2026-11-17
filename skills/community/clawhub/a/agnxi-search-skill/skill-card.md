## Description:

The official search utility for Agnxi.com - The premier directory of AI Agent Tools, MCP Servers, and Skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doanbactam](https://clawhub.ai/user/doanbactam)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to search Agnxi for agent skills, MCP servers, and tool resources, then review returned links for relevance before using them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill performs a live request to Agnxi, which can affect availability assumptions in tightly controlled or shared environments.

Mitigation: Add timeout and response-size limits before deployment in controlled environments, and have agents verify returned links before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/doanbactam/skills/agnxi-search-skill)
- [Agnxi Directory](https://agnxi.com)
- [Agnxi Sitemap](https://agnxi.com/sitemap.xml)
- [OpenClaw Standard](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text search results with URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 10 matching links and reports when additional matches exist.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
