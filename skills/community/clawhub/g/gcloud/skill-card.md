## Description: <br>
Manage Google Cloud Platform resources through gcloud, gsutil, and Firebase CLI commands for cloud administration, deployment, monitoring, logs, and SSH access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jortega0033](https://clawhub.ai/user/jortega0033) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud operators use this skill to ask an agent for Google Cloud CLI command guidance across Compute Engine, Cloud Run, Firebase Hosting, Cloud Storage, Secret Manager, Artifact Registry, Cloud SQL, billing, logs, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide powerful Google Cloud operations, including deployments, VM resets, billing changes, deletes, rollbacks, and production changes. <br>
Mitigation: Require explicit approval for high-impact commands and verify the active account, project, region, and resource names before execution. <br>
Risk: Commands may expose services or storage publicly, including Cloud Run unauthenticated access and Cloud Storage public IAM changes. <br>
Mitigation: Review public access flags and IAM changes before running commands, and use least-privileged accounts for routine work. <br>
Risk: Secret Manager examples include reading, adding, disabling, and destroying secret versions. <br>
Mitigation: Require explicit approval before secret reads or destructive secret operations, and avoid displaying secret values unless necessary. <br>


## Reference(s): <br>
- [Google Cloud CLI Linux x86_64 archive](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz) <br>
- [Cloud SQL Auth Proxy documentation](https://cloud.google.com/sql/docs/mysql/sql-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud commands that change resources, costs, IAM, secrets, networking, or deployments; users should confirm the active account, project, and target resource before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
