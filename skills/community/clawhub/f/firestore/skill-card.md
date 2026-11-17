## Description:

Manage Google Cloud Firestore databases using the Firestore REST API via curl commands. Authenticate using gcloud CLI tokens to perform CRUD operations on documents and collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipe0liveira](https://clawhub.ai/user/felipe0liveira)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to construct and review curl-based Firestore REST API operations for creating, reading, updating, deleting, listing, and querying documents. It is intended for use with a dedicated, least-privilege Google Cloud service account and explicit user approval before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated curl commands can perform high-impact Firestore reads, writes, updates, deletes, and batch operations with the authenticated account's permissions.

Mitigation: Use a dedicated least-privilege service account, verify the active account and project before each operation, prefer non-production or tightly scoped projects, and require explicit user approval before execution.

Risk: Unescaped user-provided values in shell commands may create shell-injection risk.

Mitigation: Carefully inspect generated commands before running them, especially values containing quotes, dollar signs, backticks, newlines, semicolons, ampersands, or unusual path and query characters.

Risk: OAuth access tokens inherit the permissions of the authenticated Google Cloud identity and may expose sensitive Firestore data.

Mitigation: Generate fresh short-lived tokens only when needed, avoid personal or admin credentials, revoke credentials if misuse is suspected, and monitor Cloud Audit Logs.

## Reference(s):

- [Firebase Firestore REST API Reference](https://firebase.google.com/docs/firestore/reference/rest)
- [Google Cloud CLI Installation](https://docs.cloud.google.com/sdk/docs/install-sdk)
- [Firestore ClawHub Skill Page](https://clawhub.ai/felipe0liveira/skills/firestore)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Firestore REST API curl commands and response interpretation guidance; commands require user approval before execution.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
