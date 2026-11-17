## Description:

This skill helps an agent query Eastmoney financial market, company, relationship, and operating data through natural-language requests and returns structured JSON from the Eastmoney API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current financial market and company data from Eastmoney when answering questions about securities, sectors, funds, bonds, valuation, financial indicators, executives, shareholders, and business relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial query text is sent to Eastmoney's external API.

Mitigation: Use the skill only when sending the query content to Eastmoney is acceptable for the user and deployment context.

Risk: API keys can be exposed through terminal history, logs, or direct printing.

Mitigation: Store EASTMONEY_APIKEY only in trusted environment variables and check whether it is set without printing the secret value.

Risk: Large date ranges or broad financial queries can return too much data for an agent context.

Mitigation: Prefer scoped entities, metrics, and time ranges, then summarize or paginate results before using them in model context.

Risk: Production API calls without explicit timeouts or redirect controls can hang or follow unexpected network paths.

Mitigation: Add request timeouts and disable redirects before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/eastmoney-financial-data-1-0-2)
- [Eastmoney Skills API key page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1)
- [Eastmoney query API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY and sends the query text to Eastmoney's API.]

## Skill Version(s):

1.0.0 (source: server release metadata and generated changelog; artifact _meta.json lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
