## Description:

Helps agents create and audit Google Cloud project bootstrap plans, including project IDs, billing, regions, APIs, service accounts, and workload setup for Cloud Run, Vertex AI, BigQuery, Cloud Storage, or Firebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xswazx](https://clawhub.ai/user/xswazx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan new Google Cloud projects, collect missing setup inputs, and produce safe bootstrap guidance for billing, APIs, regions, and IAM/service accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project, billing, API, and IAM commands can incur cloud charges or grant access if run against the wrong Google Cloud account or project.

Mitigation: Verify the target project ID, billing account, organization or folder placement, selected APIs, and IAM roles before executing commands.

Risk: Bootstrap guidance may be incomplete if billing authority, region requirements, or organization policies are unknown.

Mitigation: Confirm missing setup inputs and involve an authorized Google Cloud account administrator before proceeding with billable or privileged actions.

## Reference(s):

- [Billing and APIs](gcp-project-bootstrap/references/billing-and-apis.md)
- [Common gcloud Commands](gcp-project-bootstrap/references/common-gcloud-commands.md)
- [Project Creation Checklist](gcp-project-bootstrap/references/project-creation-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with checklists and inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples use placeholders that must be replaced and verified before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
