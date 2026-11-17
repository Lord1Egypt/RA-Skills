## Description:

Modifies code based on GitHub PR review comments and creates a local commit using gh and git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danie1lin](https://clawhub.ai/user/danie1lin)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to apply GitHub PR review feedback, validate targeted changes, create local commits, and report the branch and commit status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use GitHub CLI authentication to read PR details, clone or open repositories, edit code, and create a local commit.

Mitigation: Install only when that access is acceptable, use an appropriately scoped GitHub session, and review the resulting diff before approving any push.

Risk: A PR review comment may be ambiguous or broader than intended, leading to unintended code changes.

Mitigation: Limit the requested scope when needed, require a focused clarification for ambiguous comments, and review the final changed files before sharing the commit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danie1lin/skills/gh-modify-pr)
- [ClawHub publisher profile](https://clawhub.ai/user/danie1lin)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown]

**Output Format:** [Markdown operational summary with shell commands and local code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local git commit; pushing remains subject to explicit user approval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
