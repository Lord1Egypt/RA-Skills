## Description:

Aiwencai helps an agent query iWencai financial and economic data for instruments such as stocks, indices, funds, futures, options, convertible bonds, bonds, wealth-management products, and insurance, including macroeconomic data, shareholder information, financial ratings, and global market information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliangjie91](https://clawhub.ai/user/liliangjie91)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn natural-language finance questions into standardized iWencai queries, call the financial data API, and summarize returned records. It is suited for market and instrument lookup workflows that need structured data such as result rows, total counts, and query chunk information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User query text is sent to an external iWencai API with API-key authentication.

Mitigation: Set IWENCAI_API_KEY as an environment variable, avoid sending personal account details or confidential trading strategies, and review the API provider's handling of submitted queries before use.

Risk: The skill forces a promotional source phrase into responses.

Mitigation: Review generated responses before sharing them in formal or customer-facing contexts and remove unsupported promotional language when it is not appropriate.

Risk: The security summary notes that the cache-control option is ignored.

Mitigation: Do not rely on the --is-cache option to control freshness; verify data recency through the API response or an independent source when freshness matters.

## Reference(s):

- [Aiwencai ClawHub Skill Page](https://clawhub.ai/liliangjie91/skills/aiwencai)
- [API Reference](artifact/references/api.md)
- [Requirements Reference](artifact/references/requirement.md)
- [iWencai Query API Endpoint](https://openapi.iwencai.com/v1/query2data)
- [iWencai Web Query Fallback](https://www.iwencai.com/unifiedwap/chat)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IWENCAI_API_KEY for API access and returns datas, code_count, and chunks_info from the iWencai API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
