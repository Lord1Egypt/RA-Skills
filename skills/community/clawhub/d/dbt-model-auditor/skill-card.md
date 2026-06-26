## Description: <br>
Audits dbt projects for model quality, test coverage, documentation completeness, performance, and adherence to best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analytics engineers, and data teams use this skill to audit dbt projects for naming, lineage, tests, documentation, materialization choices, SQL quality, governance, and performance. It produces prioritized findings and remediation examples for improving dbt model health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect dbt profile configuration that can contain warehouse credentials. <br>
Mitigation: Keep the audit scoped to the intended project directory and provide redacted target or profile details instead of granting access to an unredacted profiles.yml. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/dbt-model-auditor) <br>
- [Publisher Profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit report with inline SQL, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes health scores, category breakdowns, prioritized issues, per-model findings, and remediation examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
