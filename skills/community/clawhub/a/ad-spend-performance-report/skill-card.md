## Description:

Turns a monthly platform export into a spend, ROAS and cost-per-conversion report with the attribution caveats stated next to every number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US in-house marketing managers and agency leads use the skill to prepare monthly paid-media reports, compare platform and analytics attribution, and explain campaign performance to finance.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled report generator does not perform the advertised calculations, so its performance output may be incomplete or misleading.

Mitigation: Independently validate CSV parsing, calculations, and attribution details before using reports for finance or budget decisions.

Risk: Writing a report into an existing output directory can overwrite its calculation.md file.

Mitigation: Choose a fresh output directory or preserve the existing report before running the script.

## Reference(s):

- [ClawHub release](https://clawhub.ai/rapidworker1/skills/ad-spend-performance-report)
- [Declared homepage](https://github.com/rapidworker1)
- [Spend report rules](references/spend-report-rules.md)
- [Ad spend export template](templates/ad-spend-export.csv)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown performance report with campaign metrics, attribution notes, reconciliation, and a monthly summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented report covers spend, revenue, conversions, ROAS, cost per conversion, clicks, impressions, CTR, CPC, and attribution context; validate generated calculations independently.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
