## Description:

Architects, debugs, secures, and cost-optimizes Google Cloud environments across Cloud Run, GKE, Compute Engine, BigQuery, Cloud SQL, IAM, VPC, Vertex AI, Pub/Sub, Dataflow, backups, disaster recovery, and gcloud workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and operators use this skill to plan, troubleshoot, secure, and cost-optimize Google Cloud environments across compute, data, networking, IAM, and production operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use existing gcloud authentication to inspect Google Cloud resources.

Mitigation: Use a restricted read-only or project-scoped identity and avoid routine use as an organization admin.

Risk: The skill can save non-secret cloud inventory, billing, IAM, topology, project, and contact notes under ~/Clawic/data/.

Mitigation: Review or disable memory and shared-box behavior where operational metadata is sensitive.

## Reference(s):

- [ClawHub Google Cloud skill page](https://clawhub.ai/ivangdavila/skills/gcp)
- [Clawic Google Cloud skill page](https://clawic.com/skills/gcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Clawic notes and existing gcloud authentication when available; does not produce credentials.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
