## Description:

Backstage Companion helps agents load project context, run health checks, enforce project governance checks, and keep README, ROADMAP, and CHANGELOG files aligned with current work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonlinear](https://clawhub.ai/user/nonlinear)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to start, wrap up, and update Backstage-managed project sessions by reading project status, running deterministic checks, and aligning documentation with implementation before commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run project-provided scripts and checks.

Mitigation: Use it only in repositories you trust, and review local and global check scripts before execution.

Risk: The update workflow can fetch unpinned remote code and synchronize checks/global, including overwrite or delete behavior.

Mitigation: Review the upstream source and change summary before approving updates, and keep changes in version control so they can be reverted.

Risk: The skill can modify README, ROADMAP, CHANGELOG, and related Markdown status files.

Mitigation: Run it on a clean branch or working tree and inspect generated documentation changes before committing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nonlinear/skills/backstage)
- [Backstage upstream repository](https://github.com/nonlinear/backstage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style status reports with inline shell commands and file update summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run shell workflows that read project checks, update Markdown status files, and synchronize checks/global after user confirmation.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
