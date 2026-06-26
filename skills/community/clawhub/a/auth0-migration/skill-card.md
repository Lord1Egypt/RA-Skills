## Description: <br>
Use when migrating or switching from an existing auth provider to Auth0, including bulk user import, gradual migration strategies, code migration patterns, and JWT validation updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute migrations from Firebase, Cognito, Supabase, Clerk, custom authentication, or other providers to Auth0. It helps with user export/import planning, gradual migration strategy, application code updates, and JWT validation changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User exports, password hashes, salts, and profile data can expose sensitive account information during migration. <br>
Mitigation: Restrict access to migration files, encrypt them in storage and transit, avoid pasting them into logs or chats, and securely delete temporary artifacts after verification. <br>
Risk: Auth0 Management API tokens, client secrets, database URLs, and other migration credentials can grant privileged access. <br>
Mitigation: Use least-privilege temporary credentials where possible, rotate or revoke them after migration, and keep them out of source control and shared transcripts. <br>
Risk: Authentication migration changes can break login, session, or JWT validation behavior for production users. <br>
Mitigation: Test the migration in staging, validate issuer and JWKS configuration, review generated code changes, and keep a rollback plan before production rollout. <br>


## Reference(s): <br>
- [Auth0 Agent Skills](https://github.com/auth0/agent-skills) <br>
- [User Export and Import Guide](references/user-import.md) <br>
- [Code Migration Patterns](references/code-patterns.md) <br>
- [Auth0 User Migration Documentation](https://auth0.com/docs/manage-users/user-migration) <br>
- [Bulk User Import](https://auth0.com/docs/manage-users/user-migration/bulk-user-imports) <br>
- [Password Hash Algorithms](https://auth0.com/docs/manage-users/user-migration/bulk-user-imports#password-hashing-algorithms) <br>
- [Management API - User Import](https://auth0.com/docs/api/management/v2/jobs/post-users-imports) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include migration steps, before/after code patterns, Auth0 CLI commands, and authentication configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
