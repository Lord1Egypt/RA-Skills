## Description:

Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent propose or run GitHub CLI workflows for authenticated repository, issue, pull request, and release management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run authenticated GitHub CLI commands that create repositories, merge pull requests, publish releases, comment, fork, or push changes.

Mitigation: Confirm the repository owner/name and review each state-changing command before execution.

Risk: The skill links to a mutable external setup guide.

Mitigation: Review the external setup link before trusting or following it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvisdunlop-gh)
- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated GitHub CLI commands that change repository state.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
