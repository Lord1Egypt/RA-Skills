## Description:

Audits Reddit Devvit apps for environment, configuration, compliance, and documentation readiness before server upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asifdotpy](https://clawhub.ai/user/asifdotpy)

### License/Terms of Use:


## Use Case:

Reddit Devvit developers use this skill to check whether an app is ready for upload by reviewing environment status, dependency health, Devvit configuration, Web View game compliance, and required documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx and Devvit CLI commands can execute tooling that changes over time.

Mitigation: Prefer project-local, lockfile-pinned devvit and TypeScript binaries before running checks.

Risk: Publishing-related commands may update or upload the target app.

Mitigation: Review any devvit update app changes before committing and run the upload command only when publication is intended.

Risk: Project scans can inspect broad directories such as source and assets.

Mitigation: Ask for user approval before scanning project files and limit review to the relevant Devvit app paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asifdotpy/skills/devvit-publishing-auditor)
- [Publisher profile](https://clawhub.ai/user/asifdotpy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown Go / No-Go report with suggested shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are presented for user approval rather than run automatically.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
