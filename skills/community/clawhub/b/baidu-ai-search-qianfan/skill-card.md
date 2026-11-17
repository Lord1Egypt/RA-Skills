## Description:

基于百度千帆平台，这个技能让代理通过联网智能搜索生成答案，并返回来源引用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[k176060444-lgtm](https://clawhub.ai/user/k176060444-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ask web-connected questions through Baidu Qianfan and receive AI-generated summaries with citation metadata. It is suited for current-information lookup, source-backed question answering, and configurable search depth or recency filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu Qianfan and may expose sensitive user intent or data.

Mitigation: Do not submit secrets, private documents, or sensitive personal data as search queries; set clear data-handling expectations before deployment.

Risk: The skill depends on an external API key and Baidu Qianfan service availability.

Mitigation: Store BAIDU_API_KEY in the environment, restrict access to it, and handle API errors or quota limits in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k176060444-lgtm/skills/baidu-ai-search-qianfan)
- [Baidu Qianfan AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON containing an AI-generated answer, references, request_id, safety flag, and usage metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends the user query to Baidu Qianfan; supports model selection, result count, recency filtering, and deep search behavior described in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
