## Description:

Use when migrating or switching from an existing auth provider to Auth0, covering bulk user import, gradual migration strategies, code migration patterns, and JWT validation updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to plan and carry out migrations from existing authentication providers such as Firebase, Cognito, Supabase, Clerk, or custom auth systems to Auth0. It helps with user export/import, phased rollout planning, SDK migration patterns, and API JWT validation updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full identity exports, password hashes, salts, metadata, error reports, and API tokens during migration.

Mitigation: Use least-privilege credentials, keep migration files in a private encrypted working location with restrictive permissions, avoid committing or uploading secrets, and define cleanup or encrypted retention before production use.

## Reference(s):

- [Code Migration Patterns](references/code-patterns.md)
- [User Export and Import Guide](references/user-import.md)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [Auth0 User Migration Documentation](https://auth0.com/docs/manage-users/user-migration)
- [Bulk User Import](https://auth0.com/docs/manage-users/user-migration/bulk-user-imports)
- [Password Hash Algorithms](https://auth0.com/docs/manage-users/user-migration/bulk-user-imports#password-hashing-algorithms)
- [Management API - User Import](https://auth0.com/docs/api/management/v2/jobs/post-users-imports)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code examples, shell commands, JSON examples, SQL snippets, and migration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Auth0 CLI for CLI-based import workflows; applicable to macOS and Linux according to release metadata.]

## Skill Version(s):

1.0.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
