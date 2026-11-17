## Description:

Finnhub Pro is a Python CLI skill for retrieving Finnhub U.S. equities data such as quotes, company profiles, news, analyst trends, insider transactions, earnings calendars, fundamentals, market status, peers, and symbol search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsj210001](https://clawhub.ai/user/lsj210001)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent operators use this skill to fetch current U.S. stock market data through Finnhub-backed CLI commands and optional JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses FINNHUB_API_KEY to call Finnhub, so plaintext credential storage could expose market-data API access.

Mitigation: Store FINNHUB_API_KEY in a protected environment or credential manager instead of a plaintext file.

Risk: The skill sends ticker symbols, search queries, and date ranges to Finnhub using the configured API key.

Mitigation: Use the skill only for queries that are appropriate to transmit to Finnhub and review data-handling expectations before deployment.

Risk: The skill depends on finnhub-python, and dependency drift can change runtime behavior.

Mitigation: Pin finnhub-python to a reviewed version before installation.

Risk: Finnhub free-tier limits and paid-tier boundaries can produce 403 or 429 failures.

Mitigation: Plan for rate-limit handling and confirm that requested endpoints are available for the configured Finnhub plan.

## Reference(s):

- [Finnhub](https://finnhub.io)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text or JSON, often accompanied by Markdown command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINNHUB_API_KEY and the finnhub-python dependency.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
