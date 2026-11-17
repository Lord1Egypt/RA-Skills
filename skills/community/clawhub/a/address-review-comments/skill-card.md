## Description:

Addresses the latest reviewer comments on a numbered GitHub PR by applying fixes, running a pre-commit self-audit, committing, pushing, and replying point-by-point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunjeetsingh](https://clawhub.ai/user/arunjeetsingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to address the latest review batch on a GitHub pull request, apply the requested fixes on the PR branch, self-audit the changes, and post a point-by-point reply. It is intended for trusted repositories where automated PR edits, commits, pushes, and comments are acceptable under the user's GitHub credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PR comments can drive automatic file edits, commits, pushes, and GitHub replies using the user's credentials.

Mitigation: Use the skill only on repositories where PR commenters are tightly trusted, and review the proposed diff and reply before treating a round as final.

Risk: A forged or reused review marker can shape which comment is treated as the latest reviewer batch.

Mitigation: Run the skill only where commenters are trusted not to forge batch markers, and verify the selected review batch before relying on the result.

Risk: Background watch behavior can continue GitHub reads and trigger another edit, commit, push, and comment round after the initial invocation ends.

Mitigation: Confirm how to list, pause, or stop the watch before enabling loop behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arunjeetsingh/skills/address-review-comments)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown narrative with shell command blocks and GitHub PR comment text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a numeric PR argument and access to gh, jq, and git; may produce file edits, one commit per review round, a push, and one PR reply comment.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
