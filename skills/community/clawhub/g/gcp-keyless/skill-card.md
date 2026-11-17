## Description:

Operate Google Cloud without recurring browser OAuth or service-account key files. Use when an agent needs GCP access, local gcloud credentials expire, a project needs GitHub OIDC Workload Identity Federation, or cloud workloads should use attached managed service accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to choose a keyless GCP access route, validate a read-only GitHub Actions Workload Identity Federation workflow, and avoid recurring browser OAuth or service-account key files during routine cloud inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential diagnostics inspect local GitHub and gcloud state and, when gcloud is installed, may briefly generate an access token to validate credentials.

Mitigation: Run the helper only in trusted environments, review its output, and avoid printing, storing, or archiving tokens or credential files.

Risk: The workflow validator is a convenience check and does not prove live IAM policy, WIF bindings, or full deployment security.

Mitigation: Verify an authorized read-only run, confirm the Google Cloud audit-log principal, and have an administrator review WIF conditions and least-privilege service accounts.

Risk: Adapting the workflow for paid or mutating cloud work can change cloud authority or cost exposure.

Mitigation: Use narrow typed operation allowlists, protected environment approvals, budget authority, and separate least-privilege service accounts before paid or mutating operations.

## Reference(s):

- [One-time Workload Identity Federation bootstrap](references/bootstrap.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and YAML workflow configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic route guidance and read-only workflow validation guidance; installing the skill does not grant cloud access.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
