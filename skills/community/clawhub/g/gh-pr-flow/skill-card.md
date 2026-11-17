## Description:

GitHub Pull Request lifecycle management: create, review, merge, changelog generation, CI checks, conflict resolution, and draft management via gh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage GitHub pull request workflows from an agent session, including PR creation, review status checks, CI inspection, merge handling, conflict-resolution guidance, and changelog generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide or invoke repository-changing pull request actions through an authenticated GitHub CLI, including merge, push, force-with-lease, label, review, and auto-merge workflows.

Mitigation: Require explicit confirmation before repository-changing actions and verify the repository, branch ownership, CI status, review state, and branch protection expectations.

Risk: Generated PR titles, bodies, and changelogs may omit important context or misclassify changes from commit messages, labels, or PR metadata.

Mitigation: Review generated PR and changelog text before publishing or merging, especially for release notes and externally visible summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericlooi504/skills/gh-pr-flow)
- [GitHub CLI](https://cli.github.com)
- [PR Templates](references/pr-templates.md)
- [Label Conventions](references/label-conventions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and code blocks, plus optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated GitHub CLI and a Git repository with a GitHub remote.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
