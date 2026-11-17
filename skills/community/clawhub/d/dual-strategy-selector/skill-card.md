## Description:

Screens A-share stocks from user-provided CSV data using the Xianren Zhilu B and Laoyatou B technical-analysis strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, analysts, and agents use this skill to identify A-share stocks that match two configured technical-analysis patterns for a selected trading date. It is intended to produce informational screening results from data the user supplies, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package metadata declares dependencies for a Python tool in npm-style metadata, which may create avoidable supply-chain exposure during installation.

Mitigation: Review package metadata before installing and replace unnecessary npm dependency declarations with pinned Python requirements.

Risk: Generated stock picks may be interpreted as investment recommendations.

Mitigation: Treat outputs as informational screening results, verify the input data, and apply independent financial review before acting on any result.

Risk: The script may write a dated CSV results file in the current directory.

Mitigation: Run it in a controlled working directory and review generated CSV files before sharing or reusing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chen6896qqwee/skills/dual-strategy-selector)
- [Publisher Profile](https://clawhub.ai/user/chen6896qqwee)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, command examples, console text, and optional CSV file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided CSV with stock prices, turnover, moving averages, volume ratio, percent change, and limit-up fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
