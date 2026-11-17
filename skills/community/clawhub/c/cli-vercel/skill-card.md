## Description:

Deploy and manage Vercel projects via the Vercel CLI, including deployments, environment variables, domains, projects, logs, teams, and local development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent propose Vercel CLI commands for deployment, project configuration, environment variables, domains, logs, teams, and local development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide production deploys, promotions, rollbacks, project, domain, or environment variable removal, team switching, environment file pulls, and `--yes` operations that affect live Vercel projects or account state.

Mitigation: Require explicit confirmation before production or destructive actions, and prefer preview deployments unless production is explicitly requested.

Risk: A global or unpinned Vercel CLI install can change behavior over time.

Mitigation: Prefer a pinned or project-local Vercel CLI install when the project supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melvynx/skills/cli-vercel)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Programmatic command guidance should prefer JSON output when supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
