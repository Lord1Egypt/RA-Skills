## Description:

AI-optimized web search via Bailian(Alibaba ModelStdio) API. Returns multisourced, concise web search results for LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to run concise web searches through Alibaba Cloud Bailian WebSearch while keeping queries bounded and credential handling explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are transmitted to Alibaba Cloud and can disclose private or sensitive context if included in the query.

Mitigation: Use generic public-topic query terms, and do not include credentials, personal identifiers, financial details, project codenames, or other private context.

Risk: The DASHSCOPE_API_KEY can be exposed through debugging commands, logs, or copied shell snippets.

Mitigation: Do not echo, print, log, or include the key value in commands or responses; verify only whether the variable is set or check non-secret metadata such as length.

Risk: Search results may contain user-contextual information and could be exfiltrated if piped or redirected to another network service.

Mitigation: Review results locally before any onward transfer, and do not chain the search script output to network-transmitting commands without separate review.

Risk: Unbounded search volume can consume Alibaba Cloud API quota and create unexpected cost.

Mitigation: Keep per-query result counts within the documented maximum of 20 and confirm with the user before issuing more than 20 search requests in one conversation.

## Reference(s):

- [Bailian WebSearch MCP Marketplace](https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/bailian-web-search-hardened)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/bailian-web-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Terminal output with JSON-formatted web search responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and DASHSCOPE_API_KEY; default result count is 5 and documented maximum is 20.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
