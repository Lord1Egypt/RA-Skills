## Description:

Quickly creates and deploys web applications to Cloudflare Pages, with safeguards for file overwrites, Git pushes, and system-level changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samueli](https://clawhub.ai/user/samueli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create simple web projects or deploy existing web app directories to GitHub and Cloudflare Pages. It is intended for agent-assisted deployment workflows that need explicit confirmation before file changes, repository pushes, or cloud publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad project contents may be committed, pushed, or deployed.

Mitigation: Review the selected source directory and build output before execution; use --skip-github and --skip-deploy until publication is explicitly authorized.

Risk: Existing files may be overwritten when a target directory exists or when source and in-place modes are used.

Mitigation: Require explicit user approval for overwrite-prone modes and prefer a dedicated project directory or reviewed source path.

Risk: Cloudflare and GitHub credentials can enable external publication of code or assets.

Mitigation: Use scoped credentials, keep secrets out of project contents, and confirm the exact command before any GitHub or Cloudflare action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samueli/skills/dev-deploy)
- [Cloudflare API token documentation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [Cloudflare API token management](https://dash.cloudflare.com/profile/api-tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local project files, Git commits, GitHub repository changes, and Cloudflare Pages deployments when authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
