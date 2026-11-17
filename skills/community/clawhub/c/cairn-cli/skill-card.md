## Description:

Cairn helps AI agents use the cairn CLI to create projects, manage tasks, track status, and coordinate human-AI collaboration through shared markdown workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregoryehill](https://clawhub.ai/user/gregoryehill)

### License/Terms of Use:


## Use Case:

Developers and AI agent operators use this skill to install and operate the Cairn CLI for markdown-backed project and task tracking, work logs, status updates, and project artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run an external npm CLI package.

Mitigation: Install only if the cairn-work package is trusted, verify the package version and release source before use, and avoid automatic upgrades without review.

Risk: The CLI creates persistent markdown files that agents may later read as workspace context.

Mitigation: Use a project-specific workspace path and review generated AGENTS.md and .cairn/planning.md before relying on them for agent behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gregoryehill/skills/cairn-cli)
- [Cairn README](artifact/README.md)
- [Cairn CLI Command Reference](artifact/COMMANDS.md)
- [cairn-work npm package](https://www.npmjs.com/package/cairn-work)
- [Cairn website](https://letcairn.work/)
- [Cairn GitHub Discussions](https://github.com/letcairnwork/cairn-cli/discussions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on creating and maintaining markdown workspace files, projects, tasks, notes, and artifacts with the cairn CLI.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-02-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
