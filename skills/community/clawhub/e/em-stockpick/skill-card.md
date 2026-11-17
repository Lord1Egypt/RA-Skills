## Description:

Uses Eastmoney's official stock-selection site to run natural-language screening queries across A-shares, Hong Kong stocks, ETFs, convertible bonds, and sectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverfoxchina-gif](https://clawhub.ai/user/silverfoxchina-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agent operators use this skill to translate natural-language stock-screening criteria into Eastmoney queries and collect matching market instruments. It is suited for exploratory screening, not for financial advice or automated trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening queries are sent to Eastmoney.

Mitigation: Use the skill only when sending those screening criteria to Eastmoney is acceptable; avoid submitting confidential strategies or sensitive account information.

Risk: The script can leave result CSVs and an Eastmoney fingerprint cache in the workspace.

Mitigation: Review and remove generated workspace files when they are no longer needed, and open generated CSVs in protected view or a plain text viewer unless formula sanitization is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silverfoxchina-gif/skills/em-stockpick)
- [Eastmoney stock selection site](https://xuangu.eastmoney.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, CSV files, Guidance]

**Output Format:** [Markdown guidance with command-line examples and generated CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes result CSVs and an Eastmoney fingerprint cache under the workspace when the Python script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
