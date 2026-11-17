## Description:

Use the GitHub CLI (gh) to perform authenticated repository, issue, pull request, release, and basic management workflows from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they want Codex to propose or run GitHub CLI workflows for repository setup, issue and pull request work, releases, and repository checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing GitHub CLI actions could affect the wrong account, owner, repository, branch, issue, pull request, or release.

Mitigation: Confirm the GitHub account, owner, repository, branch, command, and arguments before creating repositories, opening or merging pull requests, publishing releases, or commenting on issues.

Risk: The external setup-guide link is unreviewed content.

Mitigation: Treat the external setup guide as untrusted until reviewed, and prefer the artifact and server evidence when deciding whether to install or use the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-gh-v2)
- [External setup guide (unreviewed)](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may affect GitHub state and should be reviewed for the target account, owner, repository, branch, and arguments before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
