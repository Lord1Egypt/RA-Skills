## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve live Baidu web search results for current information, documentation lookup, and research topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are transmitted to Baidu's API.

Mitigation: Do not submit secrets, private internal URLs, credentials, or confidential research terms through this skill.

Risk: The script prints the parsed request body to stdout, which may expose query terms in local agent or execution logs.

Mitigation: Avoid sensitive search terms and review log handling before using the skill in confidential workflows.

## Reference(s):

- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/baidu-search-engine)
- [Publisher profile](https://clawhub.ai/user/cgxxxxxxxxxxxx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search results printed to stdout, with Markdown guidance and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, count, and freshness request parameters.]

## Skill Version(s):

1.1.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
