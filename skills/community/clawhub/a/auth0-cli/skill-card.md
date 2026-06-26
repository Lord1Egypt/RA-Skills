## Description: <br>
Reference for Auth0 CLI commands covering applications, APIs, users, roles, organizations, actions, logs, custom domains, Universal Login, Terraform export, raw Management API calls, and machine-readable JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to produce Auth0 CLI workflows for administering Auth0 tenants, including tenant authentication, application and API setup, user and role management, organization setup, actions, logs, custom domains, Universal Login, Terraform export, and direct Management API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide powerful Auth0 tenant-management operations, including update, delete, raw API, action deploy, user import, unblock, and log-stream commands. <br>
Mitigation: Confirm the active tenant and exact resource before executing any tenant-changing command. <br>
Risk: Auth0 CLI workflows may involve OAuth tokens, client secrets, passwords, private keys, or revealed application secrets. <br>
Mitigation: Do not paste real secrets or passwords into chat or shell history, and redact any --reveal-secrets output before sharing. <br>
Risk: Commands run against the wrong tenant or resource can alter production authentication behavior. <br>
Mitigation: Check the active tenant with the CLI before making changes and prefer machine-readable JSON output for reviewable command results. <br>


## Reference(s): <br>
- [Auth0 CLI command reference](references/cli.md) <br>
- [Auth0 agent skills repository](https://github.com/auth0/agent-skills) <br>
- [Auth0 CLI documentation](https://auth0.github.io/auth0-cli/) <br>
- [Auth0 Management API v2](https://auth0.com/docs/api/management/v2) <br>
- [Auth0 documentation](https://auth0.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples typically prefer --json or --json-compact output for machine-readable CLI results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
