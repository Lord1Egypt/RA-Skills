## Description: <br>
Helps agents analyze, visualize, and explain data from SQL, spreadsheets, notebooks, dashboards, exports, or ad hoc tables, with emphasis on decision-ready metrics and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business stakeholders use this skill to structure KPI reviews, experiment readouts, cohort and funnel analysis, anomaly investigations, charts, and decision briefs. It helps turn raw data and metric questions into concise evidence, caveats, confidence levels, and recommended next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated analysis can be misleading when metric definitions, denominators, time windows, or comparison groups are ambiguous. <br>
Mitigation: Confirm the metric contract, baseline, exclusions, and uncertainty before using results for decisions. <br>
Risk: Generated SQL, formulas, charts, or report text could encode incorrect assumptions or unsupported causal claims. <br>
Mitigation: Review query logic, transformations, caveats, and recommendations before execution or publication. <br>
Risk: Data analysis workflows may involve sensitive business data even though the skill itself declares no external endpoints or persistent storage. <br>
Mitigation: Keep datasets in approved local or enterprise systems and avoid sharing credentials, raw exports, or regulated data unnecessarily. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tigertamvip/data-analysis-1) <br>
- [Skill homepage](https://clawic.com/skills/data-analysis) <br>
- [Metric Contracts](metric-contracts.md) <br>
- [Chart Selection](chart-selection.md) <br>
- [Decision Briefs](decision-briefs.md) <br>
- [Analytical Pitfalls](pitfalls.md) <br>
- [Analysis Techniques](techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose, tables, analytical summaries, code or query snippets, and recommended next actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external network requests or persistent local storage by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
