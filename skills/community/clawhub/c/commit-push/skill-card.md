## Description:

commit and push all local changes to remote repo

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review local repository changes, write a Conventional Commit message, commit the intended files, push to the configured remote, and verify the branch is synchronized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pushing sends selected local code to the configured remote repository.

Mitigation: Verify the diff, staged files, remote URL, branch, and absence of secrets or private work-in-progress before allowing the push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/commit-push)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed Conventional Commit messages and git command sequences for staging, committing, pushing, and verification.]

## Skill Version(s):

1.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
