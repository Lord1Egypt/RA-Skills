## Description:

Perform web searches using Alibaba Cloud Unified Search API and return relevant results with snippets, scores, metadata, and optional raw JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neotize](https://clawhub.ai/user/neotize)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run Alibaba Cloud Unified Search queries, especially for Chinese web content or time-filtered search tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, selected options, and the configured API key are used with Alibaba Cloud's search service.

Mitigation: Use only an ALIYUN_IQS_API_KEY intended for this skill and avoid sensitive private queries unless they fit the account's data-handling expectations.

## Reference(s):

- [Alibaba Cloud Unified Search API documentation](https://help.aliyun.com/zh/document_detail/2883041.html?spm=a2c4g.11186623.help-menu-2837261.d_4_0_2_3_0.153cda16tmvRJQ)
- [Alibaba Cloud credential documentation](https://help.aliyun.com/zh/document_detail/2872258.html)
- [ClawHub skill page](https://clawhub.ai/neotize/skills/aliyun-unified-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown-formatted search results or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes result titles, links, snippets, hostnames, optional published times, relevance scores, search time, and request ID when returned by the API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
