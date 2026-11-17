## Description:

Analyzes e-commerce product reviews with AI-generated tag dimensions, user personas, Voice of Customer insights, opportunity analysis, labeled CSV output, Markdown reports, and HTML dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:

MIT

## Use Case:

Product, market research, and e-commerce teams use this skill to analyze Amazon, eBay, AliExpress, or similar product reviews, extract customer pain points and personas, and produce actionable review intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local code paths and process user-provided review files.

Mitigation: Review before installing, run in an isolated environment, and avoid attacker-controlled or unusual filenames until the reported path-interpolation issue is fixed.

Risk: Excel processing may auto-install a dependency during execution.

Mitigation: Avoid Excel mode unless dependencies are preinstalled and approved for the execution environment.

Risk: Generated prompts, CSV files, Markdown reports, and HTML dashboards may persist raw review content.

Mitigation: Use only non-sensitive or anonymized review datasets and inspect generated output directories before sharing or retaining results.

## Reference(s):

- [Review Analyzer README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/liangdabiao/skills/amazon-research-reviews-skill)

## Skill Output:

**Output Type(s):** [files, text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CSV files, Markdown reports, HTML dashboards, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates output directories per product and date; batch review tagging is limited to 30 reviews per batch.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
