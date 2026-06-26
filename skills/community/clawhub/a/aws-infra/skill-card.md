## Description: <br>
Chat-based AWS infrastructure assistance using AWS CLI and console context for querying, auditing, and monitoring AWS resources, with explicit confirmation required before any write or destructive action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bmdhodl](https://clawhub.ai/user/bmdhodl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect AWS accounts, troubleshoot infrastructure, review security posture, and prepare safe AWS CLI commands. It defaults to read-only queries and requires explicit confirmation for write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive AWS account context through the user's local AWS CLI configuration. <br>
Mitigation: Use a dedicated least-privileged or read-only AWS profile and confirm account identity and region with sts get-caller-identity before relying on results. <br>
Risk: Proposed write or destructive AWS commands could change infrastructure if approved without review. <br>
Mitigation: Review exact commands before approval, prefer dry-run modes where available, and require explicit confirmation before execution. <br>


## Reference(s): <br>
- [AWS CLI Query Patterns](references/aws-cli-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline AWS CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local AWS profile and region context; write or destructive command proposals require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
