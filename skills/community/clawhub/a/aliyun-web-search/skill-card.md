## Description:

Provides real-time web search through Aliyun Open Search Platform with the Quark engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyunbowen](https://clawhub.ai/user/xiaoyunbowen)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to configure and call Aliyun real-time web search for Chinese-focused, current web results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and search queries can be sent over unsafe or unvalidated endpoints.

Mitigation: Use HTTPS Aliyun endpoints, restrict who can set ALIYUN_SEARCH_HOST, and review configuration before installation.

Risk: Search prompts or conversation history may be sent to Aliyun's search service.

Mitigation: Avoid sending sensitive prompts, private conversation history, or regulated data through the skill.

Risk: Sample credentials or copied configuration can be exposed if committed or shared.

Mitigation: Replace sample values with user-owned credentials and store API keys in environment variables or encrypted configuration.

## Reference(s):

- [Aliyun AI Gateway Console](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)
- [Aliyun API Key Management](https://ipaas.console.aliyun.com/api-key)
- [Aliyun Web Search Official Docs](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/networked-search)
- [Aliyun Formal Activation](https://help.aliyun.com/document_detail/2869993.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON search responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALIYUN_SEARCH_API_KEY and ALIYUN_SEARCH_HOST; search results depend on Aliyun endpoint configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
