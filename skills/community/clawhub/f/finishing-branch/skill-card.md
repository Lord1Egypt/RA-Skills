## Description:

Complete development work by presenting structured options for merge, PR, or cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill after implementation is complete and tests pass to decide whether to merge locally, create a pull request, keep the branch, or discard the work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run project test commands and Git or GitHub mutations during branch completion.

Mitigation: Review commands before execution and prefer dry-run or manual confirmation for repository-changing actions.

Risk: Branch cleanup can delete local or remote branches, including forced local deletion in the discard workflow.

Mitigation: Avoid cleanup or delete flags on shared repositories unless the target branch and commits have been reviewed and the destructive action is explicitly confirmed.

Risk: The server security verdict is suspicious because branch deletion safeguards are limited.

Mitigation: Install only from a pinned commit or verified source, and require human review before allowing branch deletion or remote deletion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/finishing-branch)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, code]

**Output Format:** [Markdown guidance with inline shell commands and generated PR or merge-summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run project test commands and Git or GitHub branch operations when the agent follows the workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
