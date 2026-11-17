## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-owo](https://clawhub.ai/user/lulu-owo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve live Baidu web search results for current information, documentation lookups, and research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu's AI Search service using BAIDU_API_KEY.

Mitigation: Use only for queries appropriate to send to Baidu and manage the API key through the environment rather than hard-coding it.

Risk: Some usage documentation is in Chinese, which may lead to incorrect invocation by non-Chinese readers.

Mitigation: Translate and review the usage examples before running the skill in a workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lulu-owo/skills/baidu-search-1-1-0-skip)
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results printed to standard output, with error text for missing input, credentials, or API failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts a JSON string, a JSON file path, or JSON from stdin.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
