## Description:

博查 AI 搜索工具。调用 https://api.bocha.cn 进行网页搜索，返回带摘要的中文结果。不依赖 OpenClaw 内置 web_search。

This skill is ready for commercial/non-commercial use.

## Publisher:

[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to run Bocha web searches from an agent workflow and receive Chinese search results with titles, links, and AI-generated summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries to the external Bocha web search API.

Mitigation: Avoid submitting secrets, private terms, or sensitive business data in search queries.

Risk: The setup script stores the Bocha API key in ~/.openclaw/skills-config/bocha-search.json.

Mitigation: Prefer BOCHA_API_KEY or another protected secret input; if the config file is used, restrict its filesystem permissions.

Risk: The skill requires a Bocha API key to authorize outbound API calls.

Mitigation: Use a low-privilege API key and rotate it if the local configuration may have been exposed.

## Reference(s):

- [Bocha Web Search API documentation](https://bocha.com/documents/web-search-api)
- [Bocha Open Platform](https://open.bocha.cn)
- [Bocha website](https://www.bocha.cn)
- [ClawHub skill page](https://clawhub.ai/justaboyhai-wq/skills/bocha-search-momo)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Markdown, Configuration]

**Output Format:** [Terminal text with search result titles, URLs, and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, a Bocha API key, and outbound access to the Bocha web search API.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
