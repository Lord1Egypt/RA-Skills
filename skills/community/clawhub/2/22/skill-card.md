## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yannan](https://clawhub.ai/user/yannan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve live web search results, documentation, and research material through Baidu AI Search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu's AI Search service and may expose sensitive prompts or URLs.

Mitigation: Avoid searching for secrets, internal URLs, customer data, or regulated personal data.

Risk: The BAIDU_API_KEY credential can be exposed if local configuration files are shared or stored with weak permissions.

Mitigation: Protect the key in OpenClaw configuration, restrict local file permissions, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yannan/skills/22)
- [Baidu API Key Setup Guide](references/apikey-fetch.md)
- [Baidu AI Search API key console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON search results or plain-text error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and python3; result count is capped at 50.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
