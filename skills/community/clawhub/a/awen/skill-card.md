## Description: <br>
Create and bootstrap Google Cloud projects for new workloads, including project naming, billing and region setup, API enablement, service accounts, and readiness checks for Cloud Run, Vertex AI, BigQuery, Cloud Storage, or Firebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xswazx](https://clawhub.ai/user/xswazx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan or bootstrap Google Cloud projects with deliberate choices for billing, regions, APIs, IAM, and service accounts. It is also useful for auditing whether a planned GCP project setup is complete before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Google Cloud setup steps can create persistent, billable cloud resources or change IAM access. <br>
Mitigation: Before running suggested gcloud commands, verify the active account, project ID, organization or folder, billing account, region, API list, and IAM roles; use least privilege. <br>


## Reference(s): <br>
- [Project Creation Checklist](gcp-project-bootstrap/references/project-creation-checklist.md) <br>
- [Billing and APIs](gcp-project-bootstrap/references/billing-and-apis.md) <br>
- [Common gcloud Commands](gcp-project-bootstrap/references/common-gcloud-commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xswazx/awen) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries, missing-input lists, safe creation sequences, workload-specific API lists, and IAM or service-account recommendations when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
