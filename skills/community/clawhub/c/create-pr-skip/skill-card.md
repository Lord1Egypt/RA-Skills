## Description:

create a pull request with standardized description template

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to gather branch evidence, draft a conventional pull request title and body, create the pull request with GitHub CLI, and apply suitable labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-derived branch, commit, or diff text may be interpolated into generated shell commands.

Mitigation: Review the generated PR title, body, and exact GitHub CLI command before execution, especially for untrusted branches or external contributions.

Risk: Generated PR content may include incorrect summaries, unresolved placeholders, or unsuitable labels.

Mitigation: Use the skill's branch, evidence, template, and create gates; remove empty optional sections and confirm labels before applying them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown PR description with inline shell commands and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PR title, PR body, suggested labels, and GitHub CLI commands for review and execution.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
