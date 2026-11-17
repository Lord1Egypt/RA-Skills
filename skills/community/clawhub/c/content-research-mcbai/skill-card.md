## Description:

Researches recent articles, news, blog posts, and other content sources for a topic using Brave Search and Tavily.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to gather recent source material for LinkedIn, social media, case study, and content curation workflows before drafting posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an unsafe shell-based Tavily workflow that reads a shared secret file and interpolates user input into PowerShell.

Mitigation: Prefer a structured API call that passes the research topic as data, validates or quotes user-controlled values, and avoids executable shell interpolation.

Risk: Research queries are sent to Brave and Tavily, which can expose sensitive topics to external search providers.

Mitigation: Use approved provider accounts and avoid sending confidential, regulated, or unreleased business topics unless that use is authorized.

Risk: The documented Tavily workflow depends on a shared local secret file for TAVILY_API_KEY.

Mitigation: Use a managed, least-privilege Tavily secret and avoid logging, displaying, or copying the API key into command history.

## Reference(s):

- [Source Filters Reference](references/source-filters.md)
- [Tavily Search API Endpoint](https://api.tavily.com/search)
- [Tavily](https://tavily.com)
- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/skills/content-research-mcbai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research result lists with source URLs, summaries, dates, tags, and search-engine labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns numbered, deduplicated research results and may include follow-on article selections for content writing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
