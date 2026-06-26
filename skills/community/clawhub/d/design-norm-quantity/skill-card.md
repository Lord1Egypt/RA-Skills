## Description: <br>
Design Norm Quantity helps agents produce heuristic construction quantity and cost estimates, uncertainty ranges, and report artifacts from building design parameters and bundled quantity-ratio reference data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and construction cost analysts use this skill to generate early-stage building quantity and cost estimates, uncertainty ranges, and spreadsheet or text reports from project parameters. Outputs should be treated as heuristic estimating aids and independently validated for budgeting, procurement, or investment decisions. <br>

### Deployment Geography for Use: <br>
Global, with bundled reference defaults focused on China construction standards and regional cost factors. <br>

## Known Risks and Mitigations: <br>
Risk: The release materially overstates its AI, BIM, and advertised accuracy claims. <br>
Mitigation: Treat estimates as prototype or heuristic outputs and require independent professional validation before using them for bids, budgets, procurement, or investment decisions. <br>
Risk: Crawler and download scripts can request third-party sources and write data to local storage. <br>
Mitigation: Run those scripts only when third-party data collection is intended, and review the target sources, permissions, and output paths before execution. <br>
Risk: Generated construction estimates may be mistaken for authoritative cost advice. <br>
Mitigation: Use the outputs for early-stage analysis only unless a qualified cost professional validates assumptions, reference data, and project-specific inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruiyongwang/design-norm-quantity) <br>
- [README](artifact/README.md) <br>
- [Precision target documentation](artifact/docs/PRECISION_TARGET_3PCT.md) <br>
- [Building norms reference data](artifact/references/building-norms.json) <br>
- [Design quantity ratios reference data](artifact/references/design-quantity-ratios.json) <br>
- [Innovative ratios reference data](artifact/references/innovative-ratios-v2.json) <br>
- [Material factors reference data](artifact/references/material-factors-v3.json) <br>
- [MEP quantity ratios reference data](artifact/references/mep-quantity-ratios.json) <br>
- [Region adjustments reference data](artifact/references/region-adjustments.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated artifacts may be JSON, TXT, or XLSX.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may write estimate JSON, crawled-data JSON, SQLite or CSV exports, and XLSX or TXT reports when run.] <br>

## Skill Version(s): <br>
3.3.5 (source: server release metadata; artifact frontmatter reports 5.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
