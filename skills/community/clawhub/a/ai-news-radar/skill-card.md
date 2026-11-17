## Description:

Tracks AI industry news by querying Jiqizhixin article search and detail sources, expanding related keywords, and summarizing events, trends, and recommendations with traceable article identifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiqizhixin](https://clawhub.ai/user/jiqizhixin)

### License/Terms of Use:

MIT-0

## Use Case:

AI practitioners, analysts, and developers use this skill to search recent AI industry coverage, inspect article details, broaden topic keywords, and produce source-grounded summaries for monitoring companies, themes, and market trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens or search topics may be exposed to an unintended endpoint if the service host is changed.

Mitigation: Protect JQZX_API_TOKEN like a password and validate or pin the Jiqizhixin API host before running the scripts.

Risk: The skill over-directs agents toward one external AI-news service, which can narrow source coverage or conflict with user source preferences.

Mitigation: Treat service results as evidence, honor user privacy and source requirements, and supplement with public sources when coverage is insufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiqizhixin/skills/ai-news-radar)
- [Jiqizhixin Data Service](https://www.jiqizhixin.com/data-service)
- [/api/v1 Article API Strategy](references/api-v1-articles.md)
- [Keyword Reference](references/keyword_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with source article titles or IDs and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JQZX_API_TOKEN and network access to the Jiqizhixin article service.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
