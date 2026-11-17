## Description:

A paid Zixiang AI dual-engine web search connector that sends POST requests to China or global search engines and returns structured JSON search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tdxian](https://clawhub.ai/user/tdxian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run paid web searches through the Zixiang AI API, selecting a China or global engine, result count, time filter, and optional domain filters. It is useful when an agent needs current web search results returned as structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and domain filters are sent to a third-party paid search endpoint.

Mitigation: Avoid submitting secrets, private internal terms, regulated data, or sensitive customer information in search requests.

Risk: The ZIXIANGAI_API_KEY authorizes billable API calls.

Mitigation: Store the key as a managed environment secret, limit who can access it, monitor usage and balance, and rotate it if exposure is suspected.

Risk: Domain filters may affect policy-sensitive retrieval behavior.

Mitigation: Use reviewed or fixed versions when domain filters are relied on for policy enforcement, and verify filter behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tdxian/skills/ai-hybrid-search)
- [Zixiang AI open platform](https://open.zixiangai.com/)
- [Zixiang AI web search API](https://open.zixiangai.com/api/web-search/)
- [Zixiang AI dashboard](https://open.zixiangai.com/dashboard/index.html)
- [Search API endpoint](https://search.aiserver.cloud/v1/api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Structured JSON search responses with optional Markdown usage guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZIXIANGAI_API_KEY; supports engine, max_results, time_filter, include_domains, and exclude_domains inputs.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
