## Description:

Akshare Fund helps agents query and analyze public fund net values, holdings, estimates, and aggregated holdings with AkShare-backed fund and stock market data.

This skill is for research and development only.

## Publisher:

[bingobinf](https://clawhub.ai/user/bingobinf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill for Chinese-language fund research workflows, including fund lookup, NAV checks, holdings review, valuation estimates, and multi-fund holdings summaries. The release evidence and artifact text frame the output as research reference data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial outputs may be stale, incomplete, or unsuitable for decision-making because fund holdings are periodically disclosed and the artifact states the data is for research reference only.

Mitigation: Treat results as research data, verify material findings against authoritative fund disclosures or market data sources, and do not present the output as investment advice.

Risk: AkShare or pandas dependency behavior may change, and upstream data interfaces may fail when source websites change.

Mitigation: Install dependencies in an isolated Python environment, pin reviewed versions where possible, and re-test commands before relying on the skill in a workflow.

Risk: The skill interface and messages are Chinese-language only.

Mitigation: Use it in workflows where Chinese-language CLI output is acceptable or add a separate translation/review step for non-Chinese readers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingobinf/skills/akshare-fund)
- [ClawHub publisher profile](https://clawhub.ai/user/bingobinf)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Chinese-language terminal text and tabular CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on AkShare and pandas; market-time behavior changes whether real-time estimates or historical values are shown.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
