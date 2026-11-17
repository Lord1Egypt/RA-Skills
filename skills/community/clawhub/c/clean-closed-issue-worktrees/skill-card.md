## Description:

Safely audit and remove Git worktrees linked to closed GitHub or GitLab issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoranyu](https://clawhub.ai/user/haoranyu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scan local Git worktrees, verify linked GitHub or GitLab issue and change state, estimate reclaimable space, and remove completed worktrees only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remove local Git worktrees after approval.

Mitigation: Review the exact proposed paths, issue or change states, harness state, ignored-file risks, and branch behavior before approving cleanup.

Risk: Deleting branches or worktrees with uncertain retained commits can lose local work.

Mitigation: Keep branches by default, require explicit approval for branch deletion, and use backup branches for approved detached orphan commits.

Risk: Ignored local files such as credentials, databases, uploads, or unknown paths may be deleted with a worktree.

Mitigation: Do not approve cleanup for worktrees with sensitive or unknown ignored paths unless those paths have been reviewed and explicitly approved.

## Reference(s):

- [Selection evidence and execution plans](references/evidence-schema.md)
- [Agent harness detection](references/harness-detection.md)
- [Provider access and repository matching](references/provider-access.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON or Markdown audit artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+ and Git for the bundled worktree inventory and cleanup script.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
