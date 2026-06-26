## Description: <br>
Use when a data engineer needs a structured design review of a proposed data pipeline, ETL/ELT flow, or dbt/SQL model before it ships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers and reviewers use this skill to evaluate proposed pipeline, ETL/ELT, streaming, or dbt/SQL designs before release. It produces severity-rated findings, a remediation checklist, and a go/no-go recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pipeline designs can include internal architecture, business logic, or other sensitive operational details. <br>
Mitigation: Share only information appropriate for the agent session and omit secrets, credentials, and unnecessary sensitive data. <br>
Risk: A design review can produce incorrect or incomplete guidance when the submitted pipeline context is incomplete. <br>
Mitigation: Review findings before acting on them and validate recommendations against the actual pipeline, data contracts, and production constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/data-pipeline-design-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with severity-rated findings, dimension coverage, remediation checklist, and go/no-go recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviews user-provided designs in-session and treats missing context as explicit assumptions.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
