## Description:

Manage persistent VMs on exe.dev. Create VMs, configure HTTP proxies, share access, and set up custom domains. Use when working with exe.dev VMs for hosting, development, or running persistent services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjesuiter](https://clawhub.ai/user/bjesuiter)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage exe.dev persistent VMs for hosting, development, HTTP proxy setup, sharing access, custom domains, and Shelley agent access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing commands can expose VM services, reachable application data, or public links.

Mitigation: Verify the VM, exposed port, application data, and intended recipients before sharing; revoke public access or links when they are no longer needed.

Risk: Authentication headers contain user identity data that may be logged or used in authorization decisions.

Mitigation: Treat X-ExeDev-UserID and X-ExeDev-Email as sensitive data, minimize logging, and validate authorization logic before relying on those headers.

Risk: The skill was auto-built from exe.dev documentation and is marked as not yet tested.

Mitigation: Review the generated guidance against the exe.dev documentation and test commands in a controlled VM before operational use.

## Reference(s):

- [exe.dev VM service reference](artifact/references/exe-dev-vm-service.md)
- [exe.dev documentation](https://exe.dev/docs/all.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may affect live exe.dev VMs, HTTP exposure, sharing links, and identity headers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
