## Description:

Enforce cloud resource tagging policies for cost allocation, compliance, and governance across AWS/GCP/Azure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and cloud governance teams use this skill to audit AWS, GCP, and Azure resources for missing or non-compliant tags, define tagging policies, generate compliance reports, and prepare remediation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated remediation scripts can make broad changes to live cloud resources.

Mitigation: Review scripts before use, narrow the account, project, and resource scope, and avoid running generated remediation directly against production.

Risk: Placeholder tag values can create inaccurate ownership, cost allocation, or compliance records.

Mitigation: Replace placeholder values with approved real values before applying tags.

Risk: Repository scans over untrusted infrastructure code can expose the agent to unsafe local content.

Mitigation: Run repository scans in a sandbox and use least-privileged read-only cloud credentials where possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, policy, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cloud inventory summaries, tagging policy definitions, preventive policy examples, and remediation scripts for human review before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
