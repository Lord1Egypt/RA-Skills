## Description:

Helps an agent inspect git state, commit relevant changes, push a branch, and create or update a pull request with a concise summary and test plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to take repository changes from the working tree through a safe commit, pushed branch, and ready pull request. It is intended for normal git delivery workflows where the agent should preserve guardrails around destructive commands, force pushes, secrets, and unrelated changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate repository and remote pull request state by staging, committing, pushing branches, and creating or updating pull requests.

Mitigation: Review the diff before invoking it, limit execution to intended repositories and branches, and confirm secrets or unrelated changes are not staged.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with git operation summaries, command results, and pull request title/body content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create commits, push branches, and create or update pull requests when invoked with repository access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
