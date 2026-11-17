## Description:

Comprehensive Gandi domain registrar integration for domain and DNS management, including domain checks, DNS record changes, email forwarding, SSL status checks, snapshots, renewals, and certificate workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisagiddings](https://clawhub.ai/user/chrisagiddings)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and manage Gandi domains, DNS records, email forwarding, SSL certificates, snapshots, renewals, and related account configuration from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A token with write access can modify DNS, email forwarding, domain registration, renewal, certificate, and related Gandi resources.

Mitigation: Use separate least-privilege Gandi tokens, prefer read-only tokens for routine checks, and test changes against non-production domains or sandbox accounts before production use.

Risk: Credential handling and local profile storage have safety gaps according to the security evidence.

Mitigation: Do not place real tokens on command lines, store file-based tokens with owner-only permissions, and avoid profile names or configs from untrusted input until path validation is fixed.

Risk: Bulk DNS or snapshot restore operations can replace current records and disrupt websites or email delivery.

Mitigation: Create DNS snapshots before bulk changes, review generated commands before execution, and keep api_url pinned to the intended Gandi production or sandbox endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrisagiddings/skills/gandi-skill)
- [Gandi API Overview](references/api-overview.md)
- [Authentication](references/authentication.md)
- [Domain Management](references/domains.md)
- [LiveDNS](references/livedns.md)
- [Setup](references/setup.md)
- [Official Gandi API Documentation](https://api.gandi.net/docs/)
- [Gandi Personal Access Tokens](https://admin.gandi.net/organizations/account/pat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide or run Node.js scripts that call the Gandi API when the required token and tools are available.]

## Skill Version(s):

0.2.7 (source: release evidence, artifact metadata, and CHANGELOG, released 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
