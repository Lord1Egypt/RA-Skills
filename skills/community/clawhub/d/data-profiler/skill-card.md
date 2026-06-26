## Description: <br>
Profile construction data to understand characteristics, distributions, quality metrics, and patterns for data quality assessment and ETL planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data engineers, and construction analytics teams use this skill to inspect user-provided construction datasets before ETL, quality monitoring, schema validation, and anomaly review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports or exports may expose sensitive construction dataset contents such as column names, repeated values, contacts, costs, or project identifiers. <br>
Mitigation: Install and run the skill only for datasets the agent is allowed to read, and store or share generated reports with the same care as the source data. <br>
Risk: Profiling recommendations and quality flags may be incomplete or misleading if input data is stale, malformed, sampled, or lacks expected construction context. <br>
Mitigation: Review the reported findings before changing ETL logic, quality rules, or project decisions. <br>


## Reference(s): <br>
- [DataDrivenConstruction Homepage](https://datadrivenconstruction.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/data-profiler) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Guidance] <br>
**Output Format:** [Markdown summaries and tables, with optional JSON export data and Python code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from user-provided datasets and may include source column names, repeated values, contacts, costs, project identifiers, or other sensitive data.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
