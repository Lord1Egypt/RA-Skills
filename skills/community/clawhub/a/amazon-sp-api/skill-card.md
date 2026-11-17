## Description:

Amazon Seller Central SP-API wrapper (Python) for orders, catalog, FBA inventory, reports including restock recommendations, and financial events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berkgungor](https://clawhub.ai/user/berkgungor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query Amazon Seller Central SP-API data for orders, catalog records, FBA inventory, reports, restock planning, and financial events through a bundled Python CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Amazon seller and AWS credentials and can access sensitive seller, inventory, order, and financial data.

Mitigation: Install only where exposing those credentials to the CLI is intended; use least-privilege SP-API and IAM credentials and avoid pasting secrets into chat.

Risk: Downloaded report TSV files can contain sensitive business data.

Mitigation: Save report files only to locations appropriate for sensitive seller, inventory, order, and financial data.

Risk: Runtime dependency changes can affect network request behavior.

Mitigation: Prefer a virtual environment with pinned dependencies for httpx and related Python packages.

## Reference(s):

- [Amazon Selling Partner API Documentation](https://developer-docs.amazon.com/sp-api/)
- [Amazon SP-API Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids)
- [Amazon SP-API Report Type Values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)
- [HTTPX Documentation](https://www.python-httpx.org/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON and optional TSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python3 and httpx; requires Amazon SP-API LWA and AWS SigV4 credentials from environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
