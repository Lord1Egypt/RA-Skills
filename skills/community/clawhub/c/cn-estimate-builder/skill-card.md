## Description: <br>
Estimate Builder helps create construction project estimates with line-item cost categories, markups, totals, validation warnings, and export-oriented reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Construction estimators, cost engineers, and project teams use this skill to assemble and review project estimates, categorize labor, material, equipment, subcontractor, and other costs, apply markups or rates, and produce summary tables with validation warnings. <br>

### Deployment Geography for Use: <br>
Global, with source behavior focused on Chinese construction cost standards such as GB/T 50500-2024. <br>

## Known Risks and Mitigations: <br>
Risk: Generated estimates may contain incorrect quantities, unit costs, standards, markups, taxes, or currency assumptions. <br>
Mitigation: Independently verify all estimate inputs, formulas, standards, rates, taxes, and currency before using outputs for real project decisions. <br>
Risk: The skill requests filesystem access and can help import or export estimate documents. <br>
Mitigation: Restrict file access to the intended project documents and review exported files before sharing or relying on them. <br>
Risk: Release metadata is inconsistent across evidence sources. <br>
Mitigation: Confirm the publisher, version, and license before installation or production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruiyongwang/cn-estimate-builder) <br>
- [Publisher profile](https://clawhub.ai/user/ruiyongwang) <br>
- [Project homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown tables, explanatory text, and optional Python-oriented estimate structures or export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rounds monetary values to two decimal places and includes cost category summaries, markup breakdowns, grand totals, and validation warnings when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
