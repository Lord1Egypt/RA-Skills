## Description:

Analyzes code changes between two Git commits, including file modifications, additions, deletions, and commit context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afine907](https://clawhub.ai/user/afine907)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare two Git commits and produce commit metadata, change summaries, file breakdowns, and contextual diffs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted commit, branch, or ref names could influence Git command arguments.

Mitigation: Prefer full or normal commit hashes for untrusted input and validate or resolve refs before running Git commands.

Risk: The skill runs Git inspection commands in the user's repository.

Mitigation: Use it only in repositories where Git metadata and diffs are safe for the agent to inspect.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afine907/skills/commit-diff-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and diff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commit metadata, file-level change summaries, diff statistics, and detailed diffs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
