## Description: <br>
Transforms business questions and supplied datasets into structured analytical reports through a seven-layer workflow with method routing, Python analysis, quality checks, and Feishu-style output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, product managers, operations teams, and developers use this agent to turn business agendas and supplied data into reproducible analytical reports with method selection, validation notes, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python or package-install steps could affect the local environment or process sensitive data. <br>
Mitigation: Review generated Python before execution, run it in a virtual environment or sandbox, and require approval before installing packages or analyzing sensitive datasets. <br>
Risk: Analytical conclusions may be misleading when data is incomplete, small, biased, or method selection is weak. <br>
Mitigation: Apply the skill's pre-execution checks, cross-validation guidance, confidence annotations, and data-quality caveats before relying on recommendations. <br>
Risk: Reports could expose raw sensitive business data. <br>
Mitigation: Use anonymized or aggregated outputs and avoid including raw sensitive records in the final report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/full-link-data-analysis) <br>
- [Analysis Methods Library](artifact/references/methods.md) <br>
- [Data-Aware Routing Rules](artifact/references/routing.md) <br>
- [Quality Assurance Mechanism](artifact/references/quality.md) <br>
- [Feishu Document Format Report Template](artifact/references/feishu-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Feishu-style Markdown analytical report with confidence annotations, method notes, and actionable recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute Python analysis using pandas, numpy, scipy, statsmodels, or sklearn; reports should avoid raw sensitive data and include data-quality caveats.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
