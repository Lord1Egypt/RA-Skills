## Description:

Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent propose and run common GitHub CLI workflows for repository setup, issues, pull requests, releases, and basic repository checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated GitHub CLI commands can create or change repositories, issues, pull requests, comments, merges, and releases in the wrong target if account or repository context is mistaken.

Mitigation: Confirm the GitHub account, owner, repository, branch, visibility, and command target before running mutating gh commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis2-gh)
- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands and target URLs for user review.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
