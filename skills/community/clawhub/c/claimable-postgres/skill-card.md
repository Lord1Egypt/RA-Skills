## Description:

Provision instant temporary Postgres databases via Claimable Postgres by Neon (neon.new) with no login, signup, or credit card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to provision a temporary Postgres database quickly for local development, demos, prototypes, tests, or agent workflows that need an immediate DATABASE_URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a database and write credentials into a local .env file.

Mitigation: Confirm intent before provisioning, check for existing environment variables before writing, and avoid overwriting credentials without explicit approval.

Risk: The skill recommends mutable remote package execution such as neon-new@latest and broad runtime permissions such as deno run -A.

Mitigation: Prefer the documented curl REST API path, or run package-based commands only after trusting the current package and accepting the local code-execution risk.

Risk: Temporary unclaimed databases expire and may not be suitable for production or durable workloads.

Mitigation: Report the claim URL and expiration behavior, and recommend standard Neon provisioning or claiming the database for long-term persistence.

## Reference(s):

- [Claimable Postgres documentation](https://neon.com/docs/reference/claimable-postgres#vite-plugin)
- [Neon parent skill](https://neon.com/docs/ai/skills/neon/SKILL.md)
- [Claimable Postgres API](https://neon.new/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, code snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database connection details, claim URLs, expiry details, and .env update guidance.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
