## Description:

博查搜索 lets agents query Bocha's web search API and return structured web results with optional summaries and time filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunjingji](https://clawhub.ai/user/sunjingji)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add Bocha web search to agents that need current web results, optional page summaries, and date-range filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Bocha's external search API.

Mitigation: Review Bocha's handling of submitted queries and avoid sending secrets, credentials, private customer data, or confidential internal names unless disclosure is acceptable.

Risk: The skill requires a user-provided Bocha API key.

Mitigation: Use a dedicated Bocha API key and keep it in an environment variable or untracked local configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunjingji/skills/bocha-search)
- [Bocha Open Platform](https://open.bochaai.com)
- [Bocha API documentation](https://bocha-ai.feishu.cn/wiki/RXEOw02rFiwzGSkd9mUcqoeAnNK)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [JSON search or error response printed by a Node.js command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result objects may include title, URL, description, optional summary, site name, and publication or crawl date.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
