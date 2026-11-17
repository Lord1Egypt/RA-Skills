## Description:

Use when adding authentication or login to any app - detects your stack (React, Next.js, Vue, Nuxt, Angular, Express, Fastify, FastAPI, ASP.NET Core, React Native, Expo, Android, Swift), sets up an Auth0 account if needed, and routes to the correct SDK setup workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 authentication to web, mobile, and API projects by identifying the app framework, setting up Auth0 CLI and application configuration, and routing to the relevant framework-specific Auth0 skill or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes high-impact Auth0 tenant administration commands, including application and user management operations.

Mitigation: Review the target tenant, command arguments, and resource IDs before running commands, especially delete or tenant-admin operations.

Risk: Using the skill against a real Auth0 tenant can affect authentication configuration and credentials.

Mitigation: Review before installing or using with a real tenant, prefer the Homebrew Auth0 CLI install path, and validate changes in a non-production tenant first when possible.

Risk: Some Auth0 CLI examples involve credentials or secrets for application setup.

Mitigation: Avoid entering real passwords directly in command lines, keep secrets in environment variables or a secret manager, and do not commit credential files.

## Reference(s):

- [Auth0 Quickstart on ClawHub](https://clawhub.ai/auth0/skills/auth0-quickstart)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Auth0 CLI Reference](references/cli.md)
- [Auth0 Concepts and Troubleshooting](references/concepts.md)
- [Environment Variables Reference](references/environments.md)
- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 Quickstart Guides](https://auth0.com/docs/quickstart)
- [Auth0 CLI Documentation](https://auth0.github.io/auth0-cli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes framework routing, Auth0 CLI commands, and configuration guidance; does not directly execute tenant changes.]

## Skill Version(s):

1.0.1 (source: evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
