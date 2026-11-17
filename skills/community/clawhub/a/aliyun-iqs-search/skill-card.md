## Description:

阿里云信息查询服务（IQS）UnifiedSearch API联网搜索

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilisidu1210-ui](https://clawhub.ai/user/lilisidu1210-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web searches through Alibaba Cloud IQS UnifiedSearch and return structured results with titles, URLs, descriptions, relevance scores, and positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Alibaba Cloud IQS using the configured API key.

Mitigation: Install only when Alibaba Cloud IQS is an intended search provider, and avoid submitting secrets, confidential internal information, or sensitive queries.

Risk: The skill can read ALI_IQS_API_KEY from a local .env file if the environment variable is not set.

Mitigation: Prefer setting ALI_IQS_API_KEY as an environment variable and protect any local .env file from disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilisidu1210-ui/skills/aliyun-iqs-search)
- [Aliyun IQS product documentation](https://help.aliyun.com/product/42958.html)
- [Aliyun IQS UnifiedSearch endpoint](https://cloud-iqs.aliyuncs.com/search/unified)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration guidance]

**Output Format:** [JSON search results emitted by a Node.js CLI, with Markdown setup and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and ALI_IQS_API_KEY. Search results with rerank scores at or below 0.5 are filtered out.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
