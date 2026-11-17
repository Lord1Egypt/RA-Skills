## Description:

Build, edit, and deploy Instant-backed apps using npx instant-cli, create-instant-app (Next.js + Codex), GitHub (gh), and Vercel (vercel). Use when asked to create a new app, modify an existing app, fix bugs, add features, or deploy/update an app. Projects live under ~/apps; always work inside the relevant app folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stopachka](https://clawhub.ai/user/stopachka)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, modify, version, and deploy Instant-backed Next.js applications with GitHub and Vercel workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create GitHub repositories, push directly to main, and deploy to Vercel production.

Mitigation: Require explicit user approval for repository creation, branch targets, pushes, and production deployments before executing those actions.

Risk: The skill may run unpinned npm packages through npx.

Mitigation: Pin package versions or review the resolved package and command before execution.

Risk: The skill may copy local environment variables into Vercel.

Mitigation: Approve individual secret names and target environments before syncing variables; avoid exposing unnecessary local secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stopachka/skills/app-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code changes, configuration steps, and progress updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify app files, GitHub repositories, Vercel deployments, and environment variable configuration when the required CLIs are available and authenticated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
