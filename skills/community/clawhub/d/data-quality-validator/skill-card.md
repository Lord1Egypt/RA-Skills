## Description: <br>
Validates data quality in pipelines by checking completeness, consistency, freshness, accuracy, and distribution anomalies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to audit pipeline data, profile datasets, define validation expectations, identify anomalies or schema drift, and generate quality reports for operational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Data quality reports can expose sensitive values, internal schemas, or business metrics from inspected datasets. <br>
Mitigation: Point the skill only at approved projects or datasets, prefer masked or sampled data, and review reports before sharing. <br>
Risk: Generated checks, expectations, or monitoring rules may not match the organization's business rules or freshness SLAs. <br>
Mitigation: Review generated expectations with data owners and validate thresholds against approved baselines before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/data-quality-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline SQL, Python, shell commands, and monitoring configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include data quality scores, dimension scores, data profiles, schema drift reports, freshness dashboards, expectation definitions, monitoring rules, and trend analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
