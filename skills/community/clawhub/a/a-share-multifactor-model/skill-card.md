## Description:

Provides Chinese-language A-share multifactor and Barra-style factor analysis, using market and financial data to build factor exposures, factor returns, and covariance outputs with brief or formal reporting styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzswk](https://clawhub.ai/user/yzswk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to prepare A-share multifactor analysis, run local CSV-based factor regressions, and summarize exposures, factor returns, and risk-model statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis may be misleading if local CSV inputs, upstream market data, or model assumptions are stale or incorrect.

Mitigation: Review data sources, input files, and generated outputs before using results for financial decisions.

Risk: The skill may depend on a separate cn-stock-data skill for market and financial data collection.

Mitigation: Confirm the data dependency is installed and produces the expected A-share quote, kline, and finance inputs before running analysis.

## Reference(s):

- [Multifactor Guide](references/multifactor-guide.md)
- [ClawHub skill page](https://clawhub.ai/yzswk/skills/a-share-multifactor-model)
- [Publisher profile](https://clawhub.ai/user/yzswk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON analysis output from the local builder script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports brief and formal reporting styles; the builder script reads local CSV returns and exposures and emits factor statistics, covariance values, and recent factor returns.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
