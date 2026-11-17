## Description:

Provides a FastAPI backend development guide covering async SQLAlchemy 2.0, Alembic migrations, Pydantic v2 schemas, CRUD, authentication, testing, and deployment patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold or review FastAPI backend services with database models, REST endpoints, authentication, migrations, tests, and deployment commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated authentication and user API examples may expose account data or omit required authorization checks if used directly.

Mitigation: Review and harden authentication, authorization, JWT claim validation, and user read endpoints before adapting the examples for production.

Risk: Example database and secret settings could be copied into committed configuration files.

Mitigation: Keep real DATABASE_URL and SECRET_KEY values in protected local secrets and avoid committing environment-specific credentials.

Risk: Unbounded or weakly bounded pagination can increase service load or expose more data than intended.

Mitigation: Apply explicit pagination bounds and access controls on list endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/fastapi-backend)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python, bash, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes framework version guidance and example project structure; generated examples should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
