## Description:

Design Norm Quantity helps estimate construction quantities and costs from design parameters using norm-based ratios, QDV quantity decomposition, uncertainty analysis, and estimation-report workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, construction estimators, and project teams use this skill to produce early-stage building quantity and cost estimates from design parameters, regional factors, material assumptions, and norm-based ratios. Results should be treated as advisory and reviewed before professional costing, procurement, budgeting, or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains overstated accuracy claims and should not be treated as a guaranteed +/-3% professional costing system.

Mitigation: Use it as an advisory estimating aid and validate results with drawings, source cost data, and qualified construction-cost review before decisions.

Risk: An optional international PDF downloader may retrieve external documents from source URLs that have not been independently validated.

Mitigation: Avoid running the downloader unless the URLs are verified first, and scan downloaded documents before opening or using them.

## Reference(s):

- [README](README.md)
- [Estimation Protocol](PROTOCOL.md)
- [Precision Target 3 Percent](docs/PRECISION_TARGET_3PCT.md)
- [Building Norms](references/building-norms.json)
- [Design Quantity Ratios](references/design-quantity-ratios.json)
- [Innovative Ratios](references/innovative-ratios-v2.json)
- [Material Factors](references/material-factors-v3.json)
- [MEP Quantity Ratios](references/mep-quantity-ratios.json)
- [Region Adjustments](references/region-adjustments.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and guidance with Python and shell command snippets; some workflows can export structured estimate data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory construction estimates whose reliability depends on input design detail, regional factors, material-price assumptions, and source data quality.]

## Skill Version(s):

3.3.5 (source: server release metadata; artifact frontmatter lists 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
