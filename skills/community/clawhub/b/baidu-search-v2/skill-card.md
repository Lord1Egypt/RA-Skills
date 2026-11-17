## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15914355527](https://clawhub.ai/user/15914355527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live Baidu web searches for current information, documentation, and research topics. It accepts a query, optional result count, and optional freshness filter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu's API and may include sensitive, personal, or confidential content.

Mitigation: Do not submit secrets, personal data, or confidential business queries unless the environment's privacy and logging controls are appropriate.

Risk: The script prints the parsed request body to stdout, which may expose query content in logs.

Mitigation: Remove or redact request logging before using the skill in environments where stdout is retained or monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15914355527/skills/baidu-search-v2)
- [Baidu Qianfan web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results printed to stdout, with command-line usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; count is limited to 1-50 results and freshness supports date ranges or pd, pw, pm, and py.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
