## Description: <br>
This skill guides analytics engineering work across dbt transformation, warehouse design, business intelligence, pipeline orchestration, and data quality testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, analytics engineers, and BI teams use this skill to draft data models, dbt project structures, quality tests, governance procedures, monitoring plans, and operational runbooks for modern analytics stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated analytics examples may be production-sensitive templates rather than deployment-ready code. <br>
Mitigation: Review and adapt generated code before use, test changes in development or staging, and require approval before production deployment. <br>
Risk: Generated warehouse, BI, or alerting examples may involve credentials, sensitive data, or privileged services. <br>
Mitigation: Move credentials into a secrets manager, use least-privilege service accounts, and avoid exposing sensitive warehouse data in generated outputs. <br>
Risk: Automation examples can refresh BI assets, deploy dbt changes, query sensitive data, or send email alerts. <br>
Mitigation: Require explicit human approval before running those actions and verify the target environment, recipients, and data scope. <br>


## Reference(s): <br>
- [Analytics Engineer Code Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dbt project structures, SQL and Python examples, BI integration patterns, monitoring configurations, and runbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
