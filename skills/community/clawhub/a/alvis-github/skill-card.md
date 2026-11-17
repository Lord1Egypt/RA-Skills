## Description:

Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for authenticated repository, issue, pull request, and release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated GitHub CLI actions can mutate repositories, issues, pull requests, or releases.

Mitigation: Confirm the target owner, repository, branch, pull request, issue, or release before allowing create, comment, merge, publish, delete, or force-push operations.

Risk: The linked setup guide is third-party documentation that may change after release.

Mitigation: Review commands from the setup guide before running them and do not treat the linked page as authoritative security guidance.

Risk: Repository creation or destructive actions may expose private work or change shared project state.

Mitigation: Use private repository creation by default when intended and require explicit confirmation for destructive actions.

## Reference(s):

- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GitHub CLI command examples and operational guidance; commands may require authenticated gh access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
