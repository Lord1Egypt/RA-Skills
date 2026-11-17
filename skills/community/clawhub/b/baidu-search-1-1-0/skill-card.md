## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leileitian](https://clawhub.ai/user/leileitian)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Baidu web searches for live information, documentation, and research topics with optional filtering by site, date, resource type, recency, blocked websites, and safe search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, filters, URLs, and related request parameters are sent to Baidu using BAIDU_API_KEY.

Mitigation: Do not include secrets, private internal URLs, regulated data, or confidential material in searches unless organizational policy permits that use.

Risk: The command-line script prints parsed request data and returned search results to stdout, which may be captured in logs.

Mitigation: Avoid submitting sensitive request content and route command output only to approved destinations.

Risk: The skill requires a Baidu API key for network access to the search service.

Mitigation: Provide BAIDU_API_KEY through approved environment or secret-management mechanisms and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leileitian/skills/baidu-search-1-1-0)
- [Baidu AI Search web_search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON search results printed to stdout, with status and error text when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; sends search queries, filters, and related request parameters to Baidu.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
