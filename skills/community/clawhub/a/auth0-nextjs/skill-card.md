## Description: <br>
Use when adding authentication to Next.js applications (login, logout, protected pages, middleware, server components) - supports App Router and Pages Router with @auth0/nextjs-auth0 SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Auth0 authentication to Next.js applications, including login, logout, protected pages, middleware, server components, and Pages Router or App Router integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated setup can write Auth0 credentials or placeholders to an environment file. <br>
Mitigation: Require explicit user approval before writing to .env or .env.local, and have the user review the target file and values before proceeding. <br>
Risk: Installation instructions can involve downloading and running an Auth0 CLI install script. <br>
Mitigation: Review the downloaded installer before execution, and prefer official Auth0 installation instructions or a pinned installer when possible. <br>
Risk: The skill handles OAuth client identifiers, secrets, and Auth0 session configuration. <br>
Mitigation: Do not read existing env files without permission, keep secrets out of version control, generate a strong AUTH0_SECRET, and verify production HTTPS callback settings. <br>


## Reference(s): <br>
- [Auth0 Next.js SDK Documentation](https://auth0.com/docs/libraries/nextjs) <br>
- [Auth0 Next.js Quickstart](https://auth0.com/docs/quickstart/webapp/nextjs) <br>
- [Auth0 Next.js SDK GitHub](https://github.com/auth0/nextjs-auth0) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript, environment variable, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Auth0 CLI steps and environment-file changes that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
