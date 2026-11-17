## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeayoo](https://clawhub.ai/user/jeayoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live Baidu web searches for current information, documentation, and research topics. It supports optional result-count and freshness filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu's search API using the configured BAIDU_API_KEY.

Mitigation: Do not submit secrets, regulated personal data, or confidential internal material unless sharing it with Baidu is approved.

Risk: The skill requires an API key in the runtime environment.

Mitigation: Store BAIDU_API_KEY in approved secret management or environment configuration and avoid hard-coding it in prompts, files, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeayoo/skills/baidu-search-1-1-2)
- [Baidu Qianfan AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON search references with plain-text status or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, optional count from 1 to 50, and optional freshness filters.]

## Skill Version(s):

1.1.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
