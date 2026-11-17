## Description:

Citation Intelligence helps users analyze which URLs AI engines cite for queries, whether their domain is cited, how citation rates change, and how coverage compares with competitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO teams, and site operators use this skill to query AI citation coverage across engines, inspect cited evidence, compare competitors, and track citation trends for domains or pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned external npm MCP server with local MCP host privileges.

Mitigation: Review and pin the npm package version before installation, verify the publisher and source, and expose only the provider API keys needed for planned engines.

Risk: Citation analysis across third-party AI engines may require sensitive provider API keys.

Mitigation: Configure only required engine credentials and avoid sharing unnecessary keys with the MCP server environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/automatelab/skills/automatelab-citation-intelligence)
- [Citation Intelligence Homepage](https://github.com/AutomateLab-tech/citation-intelligence)
- [Citation Intelligence Configuration README](https://github.com/AutomateLab-tech/citation-intelligence#configuration)
- [AutomateLab Publisher Profile](https://clawhub.ai/user/automatelab)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON configuration examples and citation-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-supplied provider API keys and Node 20+ when configuring the external MCP server.]

## Skill Version(s):

0.10.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
