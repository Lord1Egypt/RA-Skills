## Description: <br>
Build comprehensive GEO performance reports with executive summaries, platform breakdowns, competitive analysis, and strategic action plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, SEO, and GEO practitioners use this skill to turn raw AI search and GEO metrics into structured performance reports with executive summaries, platform breakdowns, competitive position, insights, and action plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user-specified metrics file path could lead an agent to read unintended local files if the path is chosen from untrusted prompt content. <br>
Mitigation: Use explicit report datasets, keep --data paths scoped to intended files, and avoid broad directories or sensitive locations. <br>
Risk: Incomplete or inaccurate GEO metrics can produce misleading performance conclusions or action priorities. <br>
Mitigation: Review the input data and generated recommendations before using the report for business decisions. <br>


## Reference(s): <br>
- [Report Structure Guide](references/structure-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables and action-plan sections; optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided GEO metrics JSON; report quality depends on the completeness and accuracy of the input data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
