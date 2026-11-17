## Description:

Manages the full deploy cycle: build validation, GitHub push, Vercel deployment, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Deploy Pilot to plan, execute, and verify GitHub-to-Vercel deployments for Next.js applications, including preview, production, rollback, environment-variable, and health-check workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through production deployment actions using GitHub and Vercel credentials.

Mitigation: Use least-privilege GitHub and Vercel credentials, and require explicit approval before pushes, PR merges, production promotions, domain changes, environment-variable changes, or rollbacks.

Risk: The skill uses mutable CLI execution patterns such as npx for deployment and verification commands.

Mitigation: Prefer pinned or locally installed CLI versions and review command output before continuing with deployment-sensitive steps.

Risk: Incorrect environment-variable, migration, or health-check handling can cause a failed or unsafe deployment.

Mitigation: Complete the planning checklist before deployment, verify required environment variables and migrations, and run post-deploy health checks before reporting success.

## Reference(s):

- [Deploy Pilot on ClawHub](https://clawhub.ai/guifav/skills/deploy-pilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment plans, pre-deploy checklists, command sequences, health-check summaries, rollback steps, and environment-variable guidance.]

## Skill Version(s):

0.1.2 (source: server release metadata, generated 2026-09-10T20:42:47Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
