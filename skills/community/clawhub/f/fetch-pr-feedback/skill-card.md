## Description:

Fetch unresolved review comments from a PR and evaluate with receive-feedback skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to gather unresolved pull request review feedback and pass the formatted review document into a downstream feedback-evaluation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PR reviewer comments from other users are fed into a downstream agent workflow.

Mitigation: Use on trusted repositories, inspect the formatted feedback before changes are made, and ensure downstream feedback handling verifies each item before running commands or editing files.

## Reference(s):

- [Fetch Pr Feedback ClawHub listing](https://clawhub.ai/anderskev/skills/fetch-pr-feedback)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash commands and formatted PR review feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return a no-comments message when no eligible review comments are found.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
