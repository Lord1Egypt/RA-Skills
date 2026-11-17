## Description:

Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent to run or propose GitHub CLI commands for repository setup, repository inspection, issues, pull requests, releases, and basic repository management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide authenticated GitHub write actions such as repository creation, issue comments, pull request merges, and releases.

Mitigation: Confirm the exact owner, repository, branch, and operation before execution, and require explicit approval for destructive or publishing actions.

Risk: The external setup-guide link is unreviewed remote documentation.

Mitigation: Review the linked guide separately before relying on it, and use the bundled artifact and server evidence as the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-gh-cli)
- [Publisher profile](https://clawhub.ai/user/alvisdunlop)
- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated GitHub CLI commands; command effects depend on the user's gh login, repository permissions, and explicit execution approval.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
