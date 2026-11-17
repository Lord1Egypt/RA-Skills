## Description:

Automatise la documentation des problemes resolus et leur sauvegarde immediate sur Git pour eviter les regressions lors de nouvelles installations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rez0](https://clawhub.ai/user/rez0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to document resolved issues, verify changed files, commit and push fixes, and report the resulting commit hash so fixes remain recoverable across reinstalls, migrations, or handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to stage all repository changes, commit, and push to GitHub without explicit user approval.

Mitigation: Require explicit confirmation, show the diff and remote target, and stage only approved files before committing or pushing.

Risk: The skill directs credential retrieval through 1Password after a push failure.

Mitigation: Stop on authentication failure and ask the user to handle or approve credential access before retrying.

Risk: The skill may automatically edit documentation as part of declaring a fix complete.

Mitigation: Review the generated documentation entry for accuracy before saving it to the repository.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs documentation updates, Git commit and push steps, and user-facing confirmation with a commit hash.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
