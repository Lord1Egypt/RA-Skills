## Description:

Automatically scans GitHub repositories to label, comment on, assign, and optionally fix issues and pull requests for triage workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gruted](https://clawhub.ai/user/gruted)

### License/Terms of Use:

MIT

## Use Case:

Developers and maintainers use this skill to automate routine GitHub issue and pull request triage, including labeling, commenting, assigning, and producing maintainer follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a GitHub token to make remote repository changes.

Mitigation: Install only with a narrowly scoped, short-lived GitHub token and only for repositories you fully trust.

Risk: The optional auto-fix workflow can run repository code and push changes.

Mitigation: Avoid enabling auto-fix until it runs in a credential-free sandbox, removes token-bearing clone metadata, cleans up temporary workspaces, validates command inputs, and offers dry-run or explicit approval controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gruted/skills/gh-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [GitHub issue and pull request updates, console output, configuration guidance, and optional pull requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses repository configuration and a GitHub token supplied outside the repository.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
