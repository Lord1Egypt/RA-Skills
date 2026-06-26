## Description: <br>
Aliyun Web Search lets an agent run real-time web searches through Aliyun Open Search Platform with the Quark search engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyunbowen](https://clawhub.ai/user/xiaoyunbowen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve recent Chinese web results from Aliyun and return source snippets for tasks that need current information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and any context the agent includes are sent to Aliyun. <br>
Mitigation: Use this skill only when that data flow is acceptable, and avoid sending sensitive prompts, private documents, or regulated data unless approved. <br>
Risk: API keys can be exposed if configured broadly or copied from examples. <br>
Mitigation: Scope the key to this skill when supported, keep it in environment or secret configuration, avoid realistic example secrets, and rotate the key if exposure is suspected. <br>
Risk: A plaintext or incorrect ALIYUN_SEARCH_HOST can send requests to an unsuitable endpoint. <br>
Mitigation: Prefer an HTTPS Aliyun endpoint and verify the configured host before use. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/xiaoyunbowen/aliyun-web-search) <br>
- [Aliyun AI Gateway Web Search Documentation](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/networked-search) <br>
- [Aliyun AI Gateway Console](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway) <br>
- [Aliyun API Key Management](https://ipaas.console.aliyun.com/api-key) <br>
- [Aliyun Formal Activation Flow](https://help.aliyun.com/document_detail/2869993.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown setup guidance with shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIYUN_SEARCH_API_KEY and ALIYUN_SEARCH_HOST; queries are sent to the configured Aliyun endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
