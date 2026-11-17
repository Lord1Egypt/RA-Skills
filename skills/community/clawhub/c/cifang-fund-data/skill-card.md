## Description:

Retrieves China A-share exchange-traded fund data, including ETF and LOF lists, historical quotes, real-time quotes, and return rankings from the Cifang Quant API using a required API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyuwu](https://clawhub.ai/user/tianyuwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial data analysts use this skill to retrieve and summarize China A-share ETF and LOF market data for research, comparison, and reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Cifang API key and sends it to the Cifang Quant service.

Mitigation: Install only when you intend to use that service and provide the key through a scoped secret manager or short-lived environment variable.

Risk: Passing the API key directly on the command line can expose it through shell history, process listings, or logs.

Mitigation: Avoid inline command-line secrets on shared, monitored, or logged systems.

Risk: Fund market data may be mistaken for financial advice.

Mitigation: Treat outputs as market data for analysis and validate results before making financial decisions.

## Reference(s):

- [Cifang Quant Data API](https://www.cifangquant.com/tool/data-api)
- [Cifang Quant](https://www.cifangquant.com)
- [API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and JSON-formatted fund data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include fund lists, historical price objects, real-time quote snapshots, return rankings, summary statistics, and data quality notes.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
