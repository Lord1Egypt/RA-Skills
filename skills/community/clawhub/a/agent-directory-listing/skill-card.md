## Description:

Check whether a product can be listed in AI agent directories (official MCP Registry, Claude Connectors Directory, ChatGPT apps, skills.sh, Manus) and give the next steps for each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitchkj25](https://clawhub.ai/user/mitchkj25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product owners use the skill to check whether a product can be listed across five AI agent directories and get next steps for the closest listing opportunity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided product URLs to whywontai.com; the security scan was partial and its evidence is incomplete.

Mitigation: Use public URLs without credentials or private details unless you are comfortable sharing them with that service, and review the skill before use.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/mitchkj25/why-wont-ai/tree/main/skills/agent-directory-listing)
- [Guide to listing a product in AI agent directories](https://whywontai.com/list-your-product-in-ai-agent-directories)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Code, Configuration]

**Output Format:** [Markdown status table and directory-specific next steps; optional listing files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include drafted server.json, SKILL.md, tool annotations, or llms.txt when requested.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
