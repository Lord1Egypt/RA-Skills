## Description:

Records AI-generated code context and binds it to git commits so developers can audit why and how changes were produced.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill when committing AI-produced code changes and need a consistent, commit-linked checkpoint for audit, traceability, or later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint records may persist sensitive prompts, conversation details, private instructions, or detailed reasoning.

Mitigation: Use sanitized summaries by default, exclude secrets and private instructions, and review the exact checkpoint payload before it is written.

Risk: Commit messages, tags, repository files, or external tools can make checkpoint content visible beyond the intended audience.

Mitigation: Apply a local storage and sharing policy, confirm the destination before committing or uploading, and store only the minimum context needed for auditability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/checkpoints)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON, Files]

**Output Format:** [Markdown guidance with suggested JSON or Markdown checkpoint records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to create commit-linked checkpoint records; payload content and storage destination should be reviewed before persistence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
