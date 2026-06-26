## Description: <br>
Researches, compiles, or assesses best practices for AWS services by using official AWS documentation, with optional live AWS resource assessment when credentials and resource details are provided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and reviewers use this skill to build AWS best-practice checklists across high availability, disaster recovery, failover planning, security, and operational categories. When given appropriate AWS access details, it can also guide live resource assessment and produce findings against the checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live assessment can involve AWS credentials and account configuration details. <br>
Mitigation: Use a scoped, temporary, read-only IAM role or AWS profile for the target account, region, and service, and review assessment steps before running them. <br>
Risk: Generated reports may include infrastructure and security configuration details. <br>
Mitigation: Store generated checklists and assessment reports in private locations and review them before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/panlm/aws-best-practice-research) <br>
- [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) <br>
- [Assessment Workflow](references/assessment-workflow.md) <br>
- [Output Template](references/output-template.md) <br>
- [Search Queries](references/search-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and checklists, with optional AWS CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checklist-only mode writes a best-practice checklist; live-assessment mode writes a self-contained assessment report.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
