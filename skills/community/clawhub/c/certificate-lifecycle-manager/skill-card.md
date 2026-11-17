## Description:

Manage TLS/SSL certificate lifecycle - discovery, monitoring, renewal planning, and rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and SRE teams use this skill to inventory TLS/SSL certificates, monitor expiry, plan renewals, automate ACME or manual renewal steps, and verify certificate rotation across services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Kubernetes certificate discovery can expose sensitive TLS secret metadata across namespaces.

Mitigation: Run discovery only against approved namespaces and labels with least-privilege read access.

Risk: Host-wide certificate file searches can touch sensitive or high-volume production paths.

Mitigation: Restrict searches to approved paths and permissions before running them on production systems.

Risk: Generated renewal or verification commands may be too broad for the target environment.

Mitigation: Review and narrow commands before execution, especially for certificate rotation and service restart steps.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command blocks, configuration snippets, and inventory tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be reviewed and scoped before execution in Kubernetes or production host environments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
