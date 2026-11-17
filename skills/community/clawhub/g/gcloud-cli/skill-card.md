## Description:

Manage Google Cloud Platform resources using the official gcloud CLI, discovering command syntax dynamically with `gcloud <group> --help` before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipe0liveira](https://clawhub.ai/user/felipe0liveira)

### License/Terms of Use:


## Use Case:

Developers and cloud operators use this skill to plan and run Google Cloud CLI workflows with explicit account, project, command, and approval checks before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The active Google Cloud identity or project may target the wrong environment.

Mitigation: Show the active account and project before each task, prefer a dedicated least-privilege service account, and confirm the intended target before proposing commands.

Risk: Approved gcloud commands can change cloud resources, IAM policies, networking, or billing-related configuration.

Mitigation: Present the exact command and its expected impact, then execute only after explicit user approval.

## Reference(s):

- [Google Cloud CLI reference](https://cloud.google.com/sdk/gcloud)
- [Install Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are proposed for user review and require explicit approval before execution.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
