## Description:

Queries Chinese financial market and macroeconomic data through AKShare, including A-shares, indices, futures, funds, bonds, forex, and cryptocurrency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grandpaniu-fandougarden](https://clawhub.ai/user/grandpaniu-fandougarden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to query Chinese equities, funds, futures, bonds, macroeconomic indicators, exchange rates, and cryptocurrency data without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install hint does not pin dependency versions.

Mitigation: Install in an isolated virtual environment and pin reviewed versions of akshare and pandas before use.

Risk: Queries contact AKShare-backed external data sources and may send requested symbols or keywords to those providers.

Mitigation: Avoid submitting sensitive query terms and disclose that lookups use external market-data sources.

Risk: Network-backed financial data can be delayed, unavailable, or dependent on upstream source stability.

Mitigation: Retry transient failures and verify important financial data against authoritative sources before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grandpaniu-fandougarden/skills/finance-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [JSON from the helper script, typically summarized by the agent as concise text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script returns interface name, arguments, query time, and structured result or error fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
