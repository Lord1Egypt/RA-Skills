## Description:

Analyze energy, metals, and agricultural commodity markets alongside macro indicators to generate cross-asset macro signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and financial research teams use this skill to fetch Finskills commodity data and produce macro signal reports about inflation, growth, sector rotation, and asset-class implications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commodity macro interpretations may be mistaken for personalized trading advice.

Mitigation: Frame results as informational market analysis and avoid automated trading or individualized portfolio recommendations.

Risk: The skill requires a Finskills API key for commodity data requests.

Mitigation: Keep FINSKILLS_API_KEY in environment configuration and avoid exposing it in prompts, logs, or generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/commodity-macro-signal)
- [Project homepage](https://github.com/finskills/commodity-macro-signal)
- [Finskills API registration](https://finskills.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown market analysis report with commodity snapshots, signal ratios, cycle classification, and sector implications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY; outputs should be treated as informational market analysis, not automated trading or personalized financial advice.]

## Skill Version(s):

1.0.1 (source: server release metadata; target metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
