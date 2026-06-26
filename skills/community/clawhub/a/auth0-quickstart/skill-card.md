## Description: <br>
Use when adding authentication or login to any app - detects your stack (React, Next.js, Vue, Nuxt, Angular, Express, Fastify, FastAPI, ASP.NET Core, React Native, Expo, Android, Swift), sets up an Auth0 account if needed, and routes to the correct SDK setup workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify the application framework, configure an Auth0 tenant and application, and route to the appropriate Auth0 SDK setup workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auth0 CLI commands can create, update, or delete tenant resources. <br>
Mitigation: Use a non-production tenant while testing and require explicit confirmation before executing tenant-changing commands. <br>
Risk: Auth0 client secrets, tokens, and tenant credentials may be exposed through chat, logs, screenshots, or source control. <br>
Mitigation: Keep secrets out of chat and logs, store them in environment variables or secret managers, and avoid committing generated credential files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auth0/auth0-quickstart) <br>
- [Auth0 agent skills homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 Documentation](https://auth0.com/docs) <br>
- [Auth0 Quickstart Guides](https://auth0.com/docs/quickstart) <br>
- [Auth0 CLI Documentation](https://auth0.github.io/auth0-cli/) <br>
- [CLI Reference](references/cli.md) <br>
- [Auth0 Concepts and Troubleshooting](references/concepts.md) <br>
- [Environment Variables Reference](references/environments.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and framework-specific references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Auth0 CLI access and handling of tenant credentials or application secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
