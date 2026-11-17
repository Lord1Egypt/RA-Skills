## Description:

一个用于在 LLM 响应中注入广告的 MCP 服务器演示项目，展示广告注入中间件的风险。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers can use this skill as a demonstration of ad-injection middleware risk and as a wrapper for XiaoBenYang-hosted completion, code-analysis, and developer-tip tools. It requires explicit care because prompts, code, and the configured API key may be sent to a third-party service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, code, and API keys may be sent to the XiaoBenYang service.

Mitigation: Avoid confidential code, secrets, regulated data, and sensitive prompts; require explicit user consent before network uploads.

Risk: The skill collects and stores an API key locally.

Mitigation: Use a dedicated low-privilege API key, keep .env out of source control, and rotate or revoke the key if exposure is suspected.

Risk: The security verdict is suspicious and the documented ad-injection framing does not fully match the API-routing behavior.

Mitigation: Review the artifact and security evidence before installation; prefer a version with accurate documentation, pinned dependencies, strict response validation, and clear data-handling disclosures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/advertising-analysis)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, code, guidance, configuration]

**Output Format:** [Markdown summaries of upstream JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XBY_APIKEY and may return raw third-party API response data for agent summarization.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
