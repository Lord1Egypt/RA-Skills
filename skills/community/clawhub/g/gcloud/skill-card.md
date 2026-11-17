## Description:

Manage Google Cloud Platform resources via gcloud CLI. Use for Compute Engine VMs, Cloud Run services, Firebase Hosting, Cloud Storage, and project management. Covers deployment, monitoring, logs, and SSH access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jortega0033](https://clawhub.ai/user/jortega0033)

### License/Terms of Use:


## Use Case:

Developers and cloud operators use this skill to manage Google Cloud resources with gcloud, gsutil, and Firebase CLI command references for deployment, monitoring, storage, billing, secrets, and troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broad Google Cloud administration commands that can change live cloud resources.

Mitigation: Use least-privilege Google Cloud accounts and confirm the target project, region, zone, and resource names before running commands.

Risk: Some examples can expose services or storage publicly when public access flags or allUsers IAM bindings are used.

Mitigation: Avoid public access flags and public IAM bindings unless public exposure is explicitly intended and approved.

Risk: Secret and database examples can lead users to type sensitive values inline.

Mitigation: Avoid entering production secrets or database passwords inline; prefer managed secret storage, files, or approved credential handling workflows.

Risk: Installer examples download CLI tooling from live package sources.

Mitigation: Prefer pinned, verified, or organization-approved installer methods before enabling the skill in managed environments.

## Reference(s):

- [Cloud SQL Auth Proxy documentation](https://cloud.google.com/sql/docs/mysql/sql-proxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples require the user to supply project, region, zone, resource, credential, and account values before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
