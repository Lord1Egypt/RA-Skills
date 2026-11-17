## Description:

Manage Neon Serverless Postgres via CLI - projects, branches, databases, roles, endpoints, connection strings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Neon Serverless Postgres resources from an agent-assisted CLI workflow, including projects, branches, databases, roles, endpoints, and connection strings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Neon API keys and connection strings can expose database access if printed, logged, or shared.

Mitigation: Treat credentials and connection strings as secrets, avoid exposing them in shared terminals or logs, and use JSON output only in trusted programmatic paths.

Risk: Delete and reset commands can remove or alter Neon projects, branches, databases, and roles.

Mitigation: Double-check project, branch, database, and role identifiers before executing destructive Neon commands.

Risk: A globally installed neonctl package may change behavior over time.

Mitigation: Pin a reviewed neonctl version or use a controlled project-local install when repeatable supply-chain behavior matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/melvynx/skills/cli-neon)
- [Publisher Profile](https://clawhub.ai/user/melvynx)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends JSON output for programmatic command use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
