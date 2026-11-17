## Description:

Auth0 helps agents add, secure, debug, audit, migrate, and configure Auth0 authentication across web, mobile, backend, API, and tenant tooling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Auth0 sign-in, protect applications and APIs, configure tenant features such as MFA, Organizations, custom domains, branding, and Vercel integration, and troubleshoot or migrate authentication flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make real Auth0 tenant, DNS, and local configuration changes when instructed.

Mitigation: Review the active tenant and each proposed change before approval, especially changes to DNS, branding resets, custom domains, and audit remediation.

Risk: CheckMate environment configuration may expose or persist sensitive tenant access details if added broadly to shell startup files.

Mitigation: Keep CheckMate environment settings scoped to the session or project where they are needed, and avoid adding them to global shell startup files.

## Reference(s):

- [ClawHub Auth0 Skill Page](https://clawhub.ai/auth0/skills/auth0)
- [ClawHub Auth0 Publisher Profile](https://clawhub.ai/user/auth0)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Auth0 CLI Tooling Reference](artifact/references/tooling-cli/index.md)
- [Auth0 Security Guidance Reference](artifact/references/pattern-security/index.md)
- [Auth0 MFA Reference](artifact/references/feature-mfa/index.md)
- [Auth0 Tenant Audit Reference](artifact/references/feature-audit/index.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, shell commands, configuration steps, and generated or edited project files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform Auth0 tenant, DNS, branding, custom-domain, audit, and local configuration changes when the user asks.]

## Skill Version(s):

2.2.0 (source: evidence.release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
