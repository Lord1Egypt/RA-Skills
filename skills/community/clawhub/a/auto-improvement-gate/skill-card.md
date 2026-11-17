## Description:

Improvement Gate helps agents validate completed skill changes through schema, compile, lint, regression, review, doubt, and human-review gates, rejecting or reverting required-layer failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide whether an executed improvement candidate should be kept, reverted, rejected, or sent for human promotion review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make or undo approval-related file changes with weak path and gate controls.

Mitigation: Use trusted signed artifacts, contain rollback and review paths, and require explicit review before running it against real repositories or shared approval state.

Risk: Approval or rejection actions may affect shared review state.

Mitigation: Make required gates non-bypassable and require explicit confirmation before approve or reject actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON receipts and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces gate decisions, review-queue actions, and rollback or promotion guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
