## Description:

Production-grade backend development for implementing APIs, database schemas, authentication, and server-side logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement backend APIs, database schemas, validation, authentication, error handling, and production-oriented server patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples could lead agents to generate backend code that mishandles password persistence or responses.

Mitigation: Review generated authentication and user-response code to ensure passwords are hashed, secrets are never returned, and sensitive fields are excluded from API responses.

Risk: Rate limiting examples that rely on raw X-Forwarded-For values can be spoofed or misapplied in production.

Mitigation: Use trusted proxy configuration and deployment-aware client identity handling before applying rate limits.

Risk: Unpinned npx migration commands can execute unexpected tooling versions.

Mitigation: Use lockfile-pinned local tooling and reviewed migration workflows for production database changes.

## Reference(s):

- [Backend Patterns Reference](references/backend-patterns.md)
- [Database Patterns Reference](references/database-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/emersonbraun/skills/eb-senior-backend)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
